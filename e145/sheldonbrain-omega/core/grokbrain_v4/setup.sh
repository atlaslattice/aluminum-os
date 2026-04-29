#!/bin/bash
# Grokbrain v4.0 - Setup Script

echo "🧠 Grokbrain v4.0 Setup"
echo "========================"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "✓ Python version: $python_version"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "⚙️  Creating .env file..."
    cp .env.template .env
    echo "✓ Created .env - Please edit with your API keys and IP"
    echo ""
    echo "  Get your public IP: curl https://api.ipify.org"
    echo "  Get xAI API key: https://x.ai/api"
    echo "  Get OpenAI API key (optional): https://platform.openai.com/api-keys"
    echo ""
else
    echo ""
    echo "✓ .env file already exists"
fi

# Create directory structure
echo ""
echo "📁 Creating directory structure..."
mkdir -p exports clean_exports quarantine parsed/{by_god,code_spheres,white_papers,gamma_apps} logs qdrant_db

echo "✓ Directories created"

# Download embedding model (optional, will auto-download on first use)
echo ""
echo "🤖 Downloading embedding model (this may take a few minutes)..."
python3 << EOF
from sentence_transformers import SentenceTransformer
print("Loading sentence-transformers/all-MiniLM-L6-v2...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("✓ Embedding model ready")
EOF

echo ""
echo "========================"
echo "✅ Setup Complete!"
echo "========================"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys and IP address"
echo "  2. Place your chat exports in ./exports/"
echo "  3. Run: python main.py --sample (test mode)"
echo "  4. Run: python main.py --full (process your data)"
echo "  5. Run: streamlit run app.py (launch GUI)"
echo ""
echo "For help: python main.py --help"
echo ""
