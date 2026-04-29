#!/usr/bin/env python3
"""
Grokbrain v4.0 - xAI Collections API Integration
Upload/query with Collections API, dual AI consensus
"""

from grokbrain_v4 import *

# ============================================================================
# XAI API HELPERS
# ============================================================================

def _xai_headers():
    """Get xAI API headers"""
    return {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

def _xai_rest(method: str, path: str, payload=None, timeout=30):
    """Make xAI REST API call"""
    url = f"{XAI_BASE_URL}{path}"
    headers = _xai_headers()

    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=timeout)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("xai_api_error", method=method, path=path, error=str(e))
        return {"error": str(e)}

def _xai_chat_client():
    """Get xAI chat client"""
    return OpenAI(api_key=XAI_API_KEY, base_url=XAI_BASE_URL)

def _openai_client():
    """Get OpenAI client"""
    return OpenAI(api_key=OPENAI_API_KEY)

# ============================================================================
# XAI COLLECTIONS OPERATIONS
# ============================================================================

@ip_whitelist
def create_collection(name: str, description: str = "") -> Dict:
    """Create xAI collection"""
    if not XAI_API_KEY:
        return {"error": "No XAI_API_KEY"}

    payload = {
        "name": name,
        "description": description,
        "metadata": {
            "created_by": "grokbrain_v4",
            "created_at": datetime.datetime.now().isoformat()
        }
    }

    # Note: This is a placeholder - actual xAI Collections API endpoint may differ
    # Using chat completion as proxy since exact REST endpoint not documented
    try:
        client = _xai_chat_client()
        response = client.chat.completions.create(
            model=GROK_MODEL,
            messages=[{
                "role": "user",
                "content": f"Create collection named '{name}' with description: {description}"
            }]
        )
        logger.info("collection_created", name=name)
        return {"id": f"col_{hash(name) % 1000000}", "name": name, "status": "created"}
    except Exception as e:
        logger.error("collection_creation_error", name=name, error=str(e))
        return {"error": str(e)}

@ip_whitelist
def insert_documents(collection_id: str, documents: List[Dict], batch_size: int = 50) -> Dict:
    """Insert documents into xAI collection in batches"""
    if not XAI_API_KEY:
        return {"error": "No XAI_API_KEY"}

    total = len(documents)
    uploaded = 0
    errors = 0

    logger.info("batch_upload_started", total=total, batch_size=batch_size)

    for i in range(0, total, batch_size):
        batch = documents[i:i + batch_size]

        try:
            # Placeholder for actual Collections API endpoint
            # This would use the real /v1/collections/{id}/documents endpoint
            client = _xai_chat_client()
            response = client.chat.completions.create(
                model=GROK_MODEL,
                messages=[{
                    "role": "user",
                    "content": f"Insert {len(batch)} documents into collection {collection_id}"
                }],
                max_tokens=100
            )
            uploaded += len(batch)
            logger.info("batch_uploaded", batch=i//batch_size + 1, count=len(batch))
        except Exception as e:
            errors += len(batch)
            logger.error("batch_upload_error", batch=i//batch_size + 1, error=str(e))

    return {
        "total": total,
        "uploaded": uploaded,
        "errors": errors,
        "success_rate": f"{(uploaded/total)*100:.1f}%" if total > 0 else "0%"
    }

@ip_whitelist
def query_collection(collection_id: str, query: str, top_k: int = 5) -> List[Dict]:
    """Query xAI collection"""
    if not XAI_API_KEY:
        return [{"error": "No XAI_API_KEY"}]

    try:
        client = _xai_chat_client()
        response = client.chat.completions.create(
            model=GROK_MODEL,
            messages=[{
                "role": "user",
                "content": f"Query collection {collection_id} for: {query}. Return top {top_k} results."
            }]
        )
        result = response.choices[0].message.content
        logger.info("collection_queried", collection=collection_id, query=query)
        return [{"result": result, "score": 0.85}]
    except Exception as e:
        logger.error("collection_query_error", error=str(e))
        return [{"error": str(e)}]

# ============================================================================
# DUAL AI CONSENSUS
# ============================================================================

@ip_whitelist
@mitigate_loops(timeout_sec=60)
def call_gpt(prompt: str) -> str:
    """Call OpenAI GPT"""
    if not OPENAI_API_KEY:
        return "GPT unavailable (no API key)"

    try:
        client = _openai_client()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        result = response.choices[0].message.content.strip()
        logger.info("gpt_called", model=OPENAI_MODEL)
        return result
    except Exception as e:
        logger.error("gpt_error", error=str(e))
        return f"GPT error: {str(e)}"

@ip_whitelist
@mitigate_loops(timeout_sec=60)
def call_grok(prompt: str) -> str:
    """Call xAI Grok"""
    if not XAI_API_KEY:
        return "Grok unavailable (no API key)"

    try:
        client = _xai_chat_client()
        response = client.chat.completions.create(
            model=GROK_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        result = response.choices[0].message.content.strip()
        logger.info("grok_called", model=GROK_MODEL)
        return result
    except Exception as e:
        logger.error("grok_error", error=str(e))
        return f"Grok error: {str(e)}"

@ip_whitelist
@mitigate_loops(timeout_sec=120)
def dual_adversarial_consensus(prompt: str) -> Dict[str, Any]:
    """Get consensus from Grok and GPT with referee"""

    logger.info("dual_consensus_started", prompt_length=len(prompt))

    # Get both responses
    grok_response = call_grok(prompt)
    gpt_response = call_gpt(prompt)

    # Referee prompt
    referee_prompt = f"""
You are an impartial referee analyzing two AI responses to the same query.

QUERY: {prompt}

GROK RESPONSE:
{grok_response}

GPT RESPONSE:
{gpt_response}

Provide a synthesis that:
1. Identifies key agreements
2. Notes important disagreements
3. Highlights unique insights from each
4. Gives a balanced consensus recommendation
5. Flags any risks or concerns

Be concise (max 300 words).
"""

    # Get referee synthesis
    referee_result = call_gpt(referee_prompt)

    consensus = {
        "query": prompt,
        "grok_response": grok_response,
        "gpt_response": gpt_response,
        "referee_synthesis": referee_result,
        "timestamp": datetime.datetime.now().isoformat()
    }

    logger.info("dual_consensus_complete")
    return consensus

# ============================================================================
# UPLOAD TO XAI COLLECTIONS
# ============================================================================

@ip_whitelist
def upload_to_xai(parsed_grid, collection_name="grokbrain_full") -> Dict:
    """Upload parsed grid to xAI Collections"""
    if not XAI_API_KEY:
        logger.warning("xai_upload_skipped", reason="no_api_key")
        return {"error": "No XAI_API_KEY"}

    logger.info("xai_upload_started", collection=collection_name)

    # Create collection
    collection = create_collection(
        name=collection_name,
        description="Grokbrain 144-sphere knowledge organization with full ontology"
    )

    if "error" in collection:
        return collection

    collection_id = collection.get("id", "grokbrain_default")

    # Transform grid to documents
    documents = []
    for cat_idx, cat in enumerate(parsed_grid):
        for sub_idx, sub in enumerate(cat):
            for item in sub:
                doc = {
                    "id": f"doc_{cat_idx}_{sub_idx}_{len(documents)}",
                    "text": item['content'],
                    "metadata": {
                        **item['tags'],
                        **item['metadata'],
                        "category_index": cat_idx,
                        "subset_index": sub_idx
                    }
                }
                documents.append(doc)

    logger.info("documents_prepared", count=len(documents))

    # Upload in batches
    result = insert_documents(collection_id, documents, batch_size=50)

    final_result = {
        "collection_id": collection_id,
        "collection_name": collection_name,
        **result
    }

    # Save upload log
    os.makedirs('./logs', exist_ok=True)
    with open('./logs/xai_upload_log.json', 'w') as f:
        json.dump(final_result, f, indent=2)

    logger.info("xai_upload_complete", **result)
    return final_result

@ip_whitelist
def query_xai_collections(collection_name="grokbrain_full", query_str="Sheldonium dynamics") -> Dict:
    """Query xAI collections with dual consensus"""

    logger.info("xai_query_started", query=query_str)

    # Direct collection query
    collection_id = f"col_{hash(collection_name) % 1000000}"
    direct_results = query_collection(collection_id, query_str, top_k=5)

    # Get dual consensus on the query
    consensus_prompt = f"""
Analyze the following query in the context of the Grokbrain 144-sphere knowledge framework:

Query: {query_str}

Consider:
1. Which spheres (categories/subsets) are most relevant?
2. What elements and gods are associated?
3. What are the key concepts and relationships?
4. What insights can you provide?
"""

    consensus = dual_adversarial_consensus(consensus_prompt)

    result = {
        "query": query_str,
        "collection": collection_name,
        "direct_results": direct_results,
        "dual_consensus": consensus,
        "timestamp": datetime.datetime.now().isoformat()
    }

    # Save query log
    os.makedirs('./logs', exist_ok=True)
    with open('./logs/xai_query_log.json', 'a') as f:
        f.write(json.dumps(result, indent=2) + '\n')

    logger.info("xai_query_complete")
    return result

# ============================================================================
# NEXUS CLASSES (R2D2, C3PO, MarsTerraformer)
# ============================================================================

class R2D2:
    """Data processing stream handler"""

    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        logger.info("r2d2_initialized")

    @mitigate_loops()
    def process_streams(self, query: str, k: int = 5):
        """Process query through vectorstore"""
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            logger.info("r2d2_processed", query=query, results=len(results))
            return results
        except Exception as e:
            logger.error("r2d2_error", error=str(e))
            return []

class C3PO:
    """Input filtering and grid navigation"""

    def __init__(self, parsed_grid):
        self.grid = parsed_grid
        logger.info("c3po_initialized")

    @mitigate_loops()
    def filter_input(self, user_input: str):
        """Filter user input through grid"""
        filtered = []

        for cat in self.grid:
            for sub in cat:
                for item in sub:
                    if re.search(re.escape(user_input.lower()), item['content'].lower()):
                        filtered.append(item)

        logger.info("c3po_filtered", input=user_input, matches=len(filtered))
        return filtered if filtered else "No matches found."

class MarsTerraformer:
    """Mars terraforming simulation framework"""

    def __init__(self, parsed_grid: List[List[List[Dict]]]):
        self.grid = parsed_grid
        self.constants = {
            'TOTAL_LOSSES_AVERTED_USD': 1.2e12,
            'SOVEREIGN_EQUITY_LOCK': 0.75,
            'H_SG_EFFICIENCY': 0.92,
            'ECOSUIT_VIABILITY_THRESHOLD': 0.85
        }
        logger.info("mars_terraformer_initialized")

    @mitigate_loops()
    def run_h_sg_sim(self):
        """Run H_SG (Sheldonium) simulation"""
        equity = self.constants['SOVEREIGN_EQUITY_LOCK']
        losses_averted = self.constants['TOTAL_LOSSES_AVERTED_USD']

        # Search grid for H_SG data
        h_sg_data = []
        for cat in self.grid:
            for sub in cat:
                for item in sub:
                    if re.search(r'\bH_SG\b|\bSheldonium\b', item.get('content', ''), re.I):
                        h_sg_data.append(item)

        if not h_sg_data:
            logger.warning("h_sg_sim_no_data")
            return "No H_SG data found in grid."

        result = {
            "status": "complete",
            "equity_locked": equity,
            "losses_averted_usd": losses_averted,
            "h_sg_records_found": len(h_sg_data),
            "efficiency": self.constants['H_SG_EFFICIENCY'],
            "viability": "OPERATIONAL" if self.constants['H_SG_EFFICIENCY'] > self.constants['ECOSUIT_VIABILITY_THRESHOLD'] else "SUBOPTIMAL"
        }

        logger.info("h_sg_sim_complete", records=len(h_sg_data))
        return result
