"""
═══════════════════════════════════════════════════════════════
  FNP Premium Ad Pipeline — Configuration
  Central config for API keys, model IDs, paths, and defaults.
═══════════════════════════════════════════════════════════════
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Load Environment Variables ──
load_dotenv()

# ── API Configuration ──
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ── Model IDs ──
TEXT_MODEL = "gemini-2.5-flash"                    # For text reasoning & vision analysis
IMAGE_GEN_MODEL = "gemini-2.5-flash-image"     # For native image generation

# ── Project Paths ──
PROJECT_ROOT = Path(__file__).parent
ASSETS_DIR = PROJECT_ROOT / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
LOGO_DIR = ASSETS_DIR / "logo"
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"

# ── Logo Configuration ──
LOGO_PATH = LOGO_DIR / "fnp_logo.webp"
LOGO_SCALE = 0.15          # Logo width as % of ad width
LOGO_POSITION = "top-right" # Options: top-right, top-left, bottom-right, bottom-left
LOGO_MARGIN_RATIO = 0.03   # Margin as % of ad width

# ── Output Configuration ──
DEFAULT_RESOLUTION = (1080, 1080)   # Instagram Post (square)
RESOLUTIONS = {
    "instagram_post": (1080, 1080),
    "instagram_story": (1080, 1920),
    "facebook_ad": (1200, 628),
    "landscape": (1920, 1080),
}

# ── Font Configuration ──
# Uses Windows system fonts as fallback. Place premium .ttf files in assets/fonts/
FONT_PATHS = {
    "tagline": str(FONTS_DIR / "PlayfairDisplay-Bold.ttf"),
    "subheadline": str(FONTS_DIR / "PlayfairDisplay-Regular.ttf"),
    "brand": str(FONTS_DIR / "PlayfairDisplay-Bold.ttf"),
}

# System font fallbacks (Windows)
SYSTEM_FONT_FALLBACKS = [
    "C:/Windows/Fonts/georgia.ttf",
    "C:/Windows/Fonts/times.ttf",
    "C:/Windows/Fonts/arial.ttf",
]

# Font sizes (relative to image height)
FONT_SIZES = {
    "tagline": 0.045,       # ~4.5% of image height
    "subheadline": 0.025,   # ~2.5% of image height
    "brand": 0.02,          # ~2% of image height
}

# ── Event Detection ──
EVENT_LOOKAHEAD_DAYS = 30   # How far ahead to look for events

# ── Overlay Styling ──
OVERLAY_HEIGHT_RATIO = 0.30     # Bottom overlay covers 30% of image
OVERLAY_OPACITY = 180            # 0-255, higher = more opaque
TAGLINE_COLOR = (255, 255, 255)  # White
SUBHEADLINE_COLOR = (255, 255, 255, 200)  # Slightly transparent white

# ── Ensure directories exist ──
for directory in [ASSETS_DIR, FONTS_DIR, LOGO_DIR, INPUT_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
