#!/usr/bin/env python3
"""
Grokbrain v4.0 - Streamlit GUI Dashboard
Interactive visualization and exploration
"""

import streamlit as st
import json
import os
from pathlib import Path
import pandas as pd

# Page config
st.set_page_config(
    page_title="Grokbrain v4.0",
    page_icon="🧠",
    layout="wide"
)

# Load data
@st.cache_data
def load_parsed_grid():
    try:
        with open('./parsed/parsed_grids.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@st.cache_data
def load_artifacts():
    try:
        with open('./artifacts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@st.cache_data
def load_stats():
    try:
        with open('./logs/pipeline_stats.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Main app
def main():
    st.title("🧠 Grokbrain v4.0")
    st.markdown("### 144-Sphere Knowledge Organization System")

    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", [
        "📊 Dashboard",
        "🌐 Sphere Explorer",
        "📁 Projects",
        "🔍 Search",
        "🤖 AI Consensus",
        "⚙️ Settings"
    ])

    # Load data
    parsed_grid = load_parsed_grid()
    artifacts = load_artifacts()
    stats = load_stats()

    if page == "📊 Dashboard":
        show_dashboard(parsed_grid, artifacts, stats)
    elif page == "🌐 Sphere Explorer":
        show_sphere_explorer(parsed_grid)
    elif page == "📁 Projects":
        show_projects()
    elif page == "🔍 Search":
        show_search(parsed_grid)
    elif page == "🤖 AI Consensus":
        show_ai_consensus()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard(parsed_grid, artifacts, stats):
    """Dashboard overview"""
    st.header("📊 Dashboard")

    if not stats:
        st.warning("⚠️ No pipeline data found. Run `python main.py --sample` first.")
        return

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Artifacts", stats.get('total_artifacts', 0))

    with col2:
        st.metric("Items Categorized", stats.get('total_items_categorized', 0))

    with col3:
        st.metric("Projects Detected", stats.get('projects_detected', 0))

    with col4:
        spheres_populated = stats.get('spheres_populated', 0)
        st.metric("Spheres Populated", f"{spheres_populated}/144")

    # Recent activity
    st.subheader("Recent Activity")
    if artifacts:
        df = pd.DataFrame(artifacts[:10])
        st.dataframe(df[['source_file', 'timestamp']], use_container_width=True)

    # Sphere distribution
    st.subheader("Sphere Distribution")
    if parsed_grid:
        from grokbrain_v4 import CATEGORY_NAMES
        counts = []
        for cat_idx, cat in enumerate(parsed_grid):
            total = sum(len(sub) for sub in cat)
            counts.append({
                "Category": CATEGORY_NAMES[cat_idx],
                "Items": total
            })

        df_dist = pd.DataFrame(counts)
        st.bar_chart(df_dist.set_index("Category"))

def show_sphere_explorer(parsed_grid):
    """Explore 144 spheres"""
    st.header("🌐 Sphere Explorer")

    if not parsed_grid:
        st.warning("⚠️ No parsed grid found.")
        return

    from grokbrain_v4 import CATEGORY_NAMES, SPHERES, ELEMENTS, GODS

    # Category selector
    category = st.selectbox("Select Category", CATEGORY_NAMES)
    cat_idx = CATEGORY_NAMES.index(category)

    # Show subsets in this category
    st.subheader(f"{category} Subsets")

    for sub_idx in range(12):
        flat_idx = cat_idx * 12 + sub_idx
        sphere = SPHERES[flat_idx]
        element = ELEMENTS[flat_idx]
        god = GODS[flat_idx]

        items = parsed_grid[cat_idx][sub_idx]

        with st.expander(f"**{sphere}** ({element}) - {god}"):
            st.write(f"**Items:** {len(items)}")

            if items:
                for idx, item in enumerate(items[:3], 1):
                    st.markdown(f"**{idx}.** {item['content'][:200]}...")
                    st.json(item['tags'])

                if len(items) > 3:
                    st.info(f"+ {len(items) - 3} more items")

def show_projects():
    """Show project aggregates"""
    st.header("📁 Projects")

    parsed_dir = Path('./parsed')
    if not parsed_dir.exists():
        st.warning("⚠️ No parsed data found.")
        return

    # Find project files
    project_files = [f for f in parsed_dir.glob("*.json") if f.name != "parsed_grids.json"]

    if not project_files:
        st.info("No projects detected yet.")
        return

    for proj_file in project_files:
        with open(proj_file, 'r') as f:
            data = json.load(f)

        proj_name = proj_file.stem.replace('_', ' ').title()

        with st.expander(f"📦 {proj_name}"):
            st.write(f"**Entries:** {data.get('entry_count', 'N/A')}")
            st.write(f"**Report:** {data.get('report', 'N/A')}")

            if 'aggregate' in data and 'timeline' in data['aggregate']:
                timeline = data['aggregate']['timeline']
                st.write(f"**Timeline:** {len(timeline)} entries")

                for entry in timeline[:5]:
                    st.markdown(f"- {entry['content'][:150]}...")

def show_search(parsed_grid):
    """Search functionality"""
    st.header("🔍 Search")

    query = st.text_input("Enter search query")

    if query and parsed_grid:
        st.subheader("Search Results")

        results = []
        from grokbrain_v4 import SPHERES

        for cat_idx, cat in enumerate(parsed_grid):
            for sub_idx, sub in enumerate(cat):
                for item in sub:
                    if query.lower() in item['content'].lower():
                        flat_idx = cat_idx * 12 + sub_idx
                        results.append({
                            **item,
                            'sphere': SPHERES[flat_idx]
                        })

        if results:
            st.write(f"Found **{len(results)}** matches")

            for idx, res in enumerate(results[:10], 1):
                st.markdown(f"**{idx}. [{res['sphere']}]**")
                st.write(res['content'][:300] + "...")
                st.json(res['tags'])
        else:
            st.info("No results found.")

def show_ai_consensus():
    """AI consensus queries"""
    st.header("🤖 AI Consensus")

    query = st.text_area("Enter query for dual AI consensus")

    if st.button("Get Consensus"):
        if not query:
            st.warning("Please enter a query.")
            return

        with st.spinner("Querying Grok and GPT..."):
            from xai_integration import dual_adversarial_consensus

            try:
                result = dual_adversarial_consensus(query)

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("🤖 Grok Response")
                    st.write(result['grok_response'])

                with col2:
                    st.subheader("🤖 GPT Response")
                    st.write(result['gpt_response'])

                st.subheader("⚖️ Referee Synthesis")
                st.success(result['referee_synthesis'])

            except Exception as e:
                st.error(f"Error: {str(e)}")

def show_settings():
    """Settings page"""
    st.header("⚙️ Settings")

    st.subheader("Environment")
    st.code(f"""
XAI_API_KEY: {'✅ Set' if os.getenv('XAI_API_KEY') else '❌ Not set'}
OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not set'}
ALLOWED_IP: {os.getenv('ALLOWED_IP', 'Not set')}
DEV_BYPASS: {os.getenv('DEV_BYPASS', '0')}
    """)

    st.subheader("File Structure")
    paths = [
        './exports',
        './clean_exports',
        './quarantine',
        './parsed',
        './qdrant_db',
        './logs'
    ]

    for path in paths:
        exists = "✅" if Path(path).exists() else "❌"
        st.write(f"{exists} `{path}`")

if __name__ == "__main__":
    main()
