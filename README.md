# FNP Premium Ad Automation Pipeline — Event Intelligence Layer

> **Generate campaign-ready, luxury-occasion premium ad assets** for Ferns N Petals by detecting upcoming gifting events and crafting event-aware creatives with AI.

## 🏗️ Architecture

```
📅 Context Agent ──────────┐
   (Event Intelligence)    │
                           ├──→ 🎨 Creative Orchestrator ──→ 🖼️ Generation Agent ──→ 📦 Campaign Asset
👁️ Vision Agent ───────────┘       (Director Agent)           (Image + Overlay)       (PNG + JSON)
   (Product Analyzer)
```

| Agent | Purpose | Model |
|-------|---------|-------|
| Context Agent | Detects next gifting event within 30 days | gemini-2.5-flash |
| Vision Agent | Analyzes product image (flowers, colors, mood) | gemini-2.5-flash |
| Creative Orchestrator | Merges event + product into luxury creative brief | gemini-2.5-flash |
| Generation Agent | Generates ad image + premium text overlay | gemini-2.0-flash-exp + Pillow |

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Your API Key
Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```
Get one from: https://aistudio.google.com/

### 3. Add Your Input Image
Place a bouquet/product image in the `input/` directory:
```
input/
  └── pink_carnations.jpg..
```

### 4. Add FNP Logo (Optional)
Place the FNP logo (transparent PNG) at:
```
assets/logo/fnp_logo.png
```

### 5. Run the Pipeline
```bash
python pipeline.py
```

Or specify a custom image:
```bash
python pipeline.py --image path/to/bouquet.jpg
```

## 📁 Project Structure
```
FNP/
├── pipeline.py              # Main orchestrator
├── config.py                # Configuration & settings
├── luxury_archetypes.py     # Event → creative direction mapping
├── utils.py                 # Shared utilities
├── agents/
│   ├── context_agent.py     # Event Intelligence
│   ├── vision_agent.py      # Product Analysis
│   ├── creative_agent.py    # Creative Director
│   └── generation_agent.py  # Image Generation + Overlay
├── assets/
│   ├── fonts/               # Premium fonts (.ttf)
│   └── logo/                # FNP logo (fnp_logo.png)
├── input/                   # Place product images here
├── output/                  # Generated campaign assets
├── .env                     # API key
└── requirements.txt
```

## 🎭 Luxury Archetypes
The pipeline shifts creative direction based on the detected event:

| Event | Mood | Example Tagline |
|-------|------|----------------|
| Mother's Day | Warm, ethereal, maternal elegance | "For the one who bloomed first" |
| Valentine's Day | Deep reds, candlelit, romantic velvet | "Some fires bloom" |
| Diwali | Opulent, radiant, festival of lights | "Light a thousand blooms" |
| Raksha Bandhan | Sibling warmth, festive joy | "Tied with petals, sealed with love" |
| Anniversary | Timeless elegance, classic luxury | "Still blooming, still us" |
| Default | Fresh, joyful, premium everyday | "Bloom, delivered" | "new version" |

## 📋 Output
The pipeline generates:
- **`campaign_asset.png`** — Final campaign-ready ad with overlay
- **`campaign_metadata.json`** — Full metadata (event, product, brief, settings)
