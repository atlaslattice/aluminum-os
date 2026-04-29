# Google Drive Integration - Quick Start

## Overview

Grokbrain v4.0 now supports **automatic ingestion from Google Drive folders** containing your Grok chat exports. This eliminates manual file copying and enables seamless cloud→local→xAI Collections workflow.

## Workflow (Option A)

```
Google Drive Folder → Download to ./exports/ → Parse Grok JSON → Classify 144 Spheres → Upload to xAI Collections
```

**Total time: 5 minutes setup + automatic processing**

---

## Setup (One-Time, 10 minutes)

### Step 1: Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project:
   - Click "Select a project" → "New Project"
   - Name: `Grokbrain`
   - Click "Create"

### Step 2: Enable Google Drive API

1. In your project, go to **"APIs & Services" → "Library"**
2. Search for `Google Drive API`
3. Click **"Enable"**

### Step 3: Create OAuth2 Credentials

1. Go to **"APIs & Services" → "Credentials"**
2. Click **"Create Credentials" → "OAuth client ID"**
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: `Grokbrain`
   - User support email: Your email
   - Developer contact: Your email
   - Click **Save and Continue** (skip scopes, test users)
4. Return to Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: `Grokbrain Desktop`
   - Click **"Create"**

### Step 4: Download Credentials

1. Click the **download icon** (⬇️) next to your OAuth 2.0 Client ID
2. Save file as: `credentials.json`
3. **Move `credentials.json` to your Grokbrain project root** (same folder as `main.py`)

### Step 5: Prepare Your Google Drive Folder

1. In Google Drive, create a folder for your Grok chat exports (or use existing)
2. Upload all your `.json` chat export files
3. Right-click folder → **"Share"**
4. Change access to: **"Anyone with the link can view"** (or keep restricted to your account)
5. Copy the folder URL (looks like: `https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9`)

---

## Usage

### First Run (Authentication)

```bash
python main.py --gdrive "https://drive.google.com/drive/folders/YOUR_FOLDER_ID"
```

**What happens:**
1. Browser opens asking you to sign in to Google
2. Grant permission to read Google Drive files
3. Authentication token saved as `token.pickle` (reused for future runs)
4. Files download to `./exports/`
5. Full pipeline runs automatically

### Subsequent Runs (No Authentication)

```bash
python main.py --gdrive "https://drive.google.com/drive/folders/YOUR_FOLDER_ID"
```

Token is reused; no browser prompt needed.

---

## Supported File Formats

Grokbrain auto-detects and parses:

| Format | Source | Detection | Parser |
|--------|--------|-----------|--------|
| **Grok nested JSON** | xAI Grok exports | `"conversations"` key | `grok_parser.py` |
| **Simple chat JSON** | OpenAI, Gemini, DeepSeek | `"messages"` key | Built-in |
| **Text transcripts** | `.txt` files | `Human:` / `Assistant:` | Built-in regex |

**Dave's Grok exports** use the nested format and are fully supported.

---

## Complete Example

### 1. Export Your Grok Chats

In Grok interface:
- Open conversation
- Click **"⋮" menu → "Export"**
- Download JSON file
- Upload to Google Drive folder

### 2. Run Pipeline

```bash
# First time - authenticate
python main.py --gdrive "https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9"

# Output:
# 📥 Downloading from Google Drive folder: 1a2b3c4d5e6f7g8h9
# [info] file_downloaded file=grokbrain_chat_001.json
# [info] file_downloaded file=grokbrain_chat_002.json
# ✅ Downloaded 2 files to ./exports/
# 🚀 Running full pipeline...
# [info] grok_format_parsed file=grokbrain_chat_001.json count=47
# [info] artifacts_created count=94
# ✅ GROKBRAIN V4.0 PIPELINE COMPLETE
# 📊 Total artifacts: 94
# 🌐 Items categorized: 94
# 📁 Projects detected: 8
# 🔮 Spheres populated: 42/144
```

### 3. Upload to xAI Collections

```bash
python main.py --upload-xai
```

### 4. Query Your Knowledge Base

```bash
python main.py --query "quantum entanglement Mars terraforming"
```

---

## Folder Structure After Run

```
grokbrain_v4/
├── credentials.json          # OAuth2 credentials (DO NOT COMMIT)
├── token.pickle              # Auth token (DO NOT COMMIT)
├── exports/                  # Downloaded from Google Drive
│   ├── grokbrain_chat_001.json
│   └── grokbrain_chat_002.json
├── clean_exports/            # After quarantine filtering
├── parsed/                   # 144-sphere classified results
│   ├── parsed_grids.json
│   ├── project_timelines.json
│   └── by_god/               # Organized by mythological deity
├── qdrant_db/                # Vector embeddings (persistent)
└── logs/                     # Pipeline logs
```

---

## Troubleshooting

### Error: "credentials.json not found"

**Solution:** Download OAuth credentials from Google Cloud Console (Step 4 above)

### Error: "No files downloaded"

**Possible causes:**
1. Folder ID incorrect → Check URL
2. Folder not shared → Make "Anyone with link can view"
3. No `.json` files in folder → Add your Grok exports

### Error: "Browser doesn't open for authentication"

**Solution:** Copy the URL from terminal and paste into browser manually

### Files Downloaded But Pipeline Fails

**Check format:**
```bash
python3 -c "
from grok_parser import detect_export_format
print(detect_export_format('exports/YOUR_FILE.json'))
"
```

If output is `unknown`, file may be corrupted or wrong format.

---

## Security Notes

1. **`credentials.json`** and **`token.pickle`** contain sensitive OAuth data
2. Already added to `.gitignore` - **DO NOT commit to Git**
3. Token expires after inactivity; re-authentication required
4. Google Drive API is read-only; Grokbrain cannot modify your Drive files

---

## Alternative: Manual Upload

If you prefer not to use Google Drive integration:

```bash
# 1. Manually download your Grok exports from Google Drive
# 2. Copy .json files to ./exports/
cp ~/Downloads/grokbrain_*.json ./exports/

# 3. Run pipeline
python main.py --full
```

---

## Next Steps

After successful ingestion:

1. **Explore Results:**
   ```bash
   python main.py --demo
   ```

2. **Launch GUI:**
   ```bash
   streamlit run app.py
   ```

3. **Query xAI Collections:**
   ```bash
   python main.py --query "your search query"
   ```

---

## Help

**Setup Instructions:**
```bash
python main.py --gdrive-setup
```

**Full Documentation:**
- [USER_GUIDE.md](USER_GUIDE.md) - Complete usage guide
- [QUICKSTART.md](QUICKSTART.md) - Standard quickstart
- [DOCUMENTATION.md](DOCUMENTATION.md) - Documentation index
