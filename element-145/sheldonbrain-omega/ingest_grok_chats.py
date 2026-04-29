#!/usr/bin/env python3
import json, sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant as LangchainQdrant
from langchain_core.documents import Document

chat_file = 'exports/grok_chats/ttl/30d/export_data/591ad8c2-a366-440e-9f69-f30db7a4ca1f/prod-grok-backend.json'
print(f"Loading {chat_file}...")
data = json.load(open(chat_file))
conversations = data.get('conversations', [])
print(f"Found {len(conversations)} conversations with {sum(len(c.get('responses',[])) for c in conversations):,} messages\n")

print("Creating documents...")
docs = []
for i, conv in enumerate(conversations):
    text = f"Conversation: {conv['conversation'].get('title','Untitled')}\n\n"
    for r in conv.get('responses', []):
        resp = r['response']
        if msg := resp.get('message'):
            text += f"{resp.get('sender','').upper()}: {msg}\n\n"
    docs.append(Document(page_content=text, metadata={
        "source": "grok", "title": conv['conversation'].get('title','Untitled'),
        "conversation_id": conv['conversation']['id'], 
        "message_count": len(conv.get('responses',[])),
        "sphere": "Computer Science", "house": "Formal Sciences"
    }))
    if (i+1) % 25 == 0: print(f"  {i+1}/{len(conversations)}")

print(f"\nEmbedding {len(docs)} conversations...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device':'cpu'})
vectorstore = LangchainQdrant.from_documents(docs, embeddings, path="./qdrant_db", collection_name="grokbrain_grid")
print("✅ Done! Database ready.")
