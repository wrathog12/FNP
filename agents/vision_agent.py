"""
═══════════════════════════════════════════════════════════════
  Agent 2: Vision Analysis Agent — Product Analyzer
  
  Analyzes the input product image (bouquet/gift) using Gemini's
  multimodal capabilities to extract flower types, colors, mood,
  and artistic direction.
═══════════════════════════════════════════════════════════════
"""

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

from google import genai
from google.genai import types

import config
from utils import log_agent_start, log_agent_complete, log_step, log_result, Timer


@dataclass
class ProductAnalysis:
    """Structured output from the Vision Analysis Agent."""
    flower_types: list = field(default_factory=list)        # ["Pink Carnations", "Baby's Breath"]
    dominant_colors: list = field(default_factory=list)      # ["#FFB6C1", "#FFFFFF"]
    color_names: list = field(default_factory=list)          # ["Soft Pink", "White"]
    arrangement_style: str = ""                              # "Rounded hand-tied bouquet"
    price_tier: str = ""                                     # "Premium"
    mood: str = ""                                           # "Gentle, nurturing, soft elegance"
    suggested_occasions: list = field(default_factory=list)  # ["Mother's Day", "Birthday"]
    product_summary: str = ""                                # One-line luxury description

    def to_dict(self) -> dict:
        return asdict(self)


def analyze_product(image_path: str) -> ProductAnalysis:
    """
    Analyze a product image using Gemini's vision capabilities.
    
    Extracts detailed information about flowers, colors, mood,
    and artistic qualities from the input image.
    
    Args:
        image_path: Path to the product image file.
        
    Returns:
        ProductAnalysis with detailed product information.
    """
    log_agent_start("Vision Analysis Agent - Product Analyzer", "[VIS]")

    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Product image not found: {image_path}")

    log_step(f"[IMG] Loading image: {image_path.name}")

    # Step 1: Load and prepare the image
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Determine MIME type
    suffix = image_path.suffix.lower()
    mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
    mime_type = mime_map.get(suffix, "image/jpeg")

    # Step 2: Send to Gemini for analysis
    log_step("[ANALYZE] Analyzing product with Gemini Vision...")

    client = genai.Client(api_key=config.GEMINI_API_KEY)

    prompt = """You are a luxury floral art director at FNP (Ferns N Petals), India's premium gifting brand.

Analyze this bouquet/flower product image in detail.

Respond ONLY with valid JSON in this exact format (no markdown, no code blocks):
{
    "flower_types": ["Pink Carnations", "Baby's Breath"],
    "dominant_colors": ["#FFB6C1", "#FFFFFF", "#90EE90"],
    "color_names": ["Soft Pink", "Pure White", "Light Green"],
    "arrangement_style": "Rounded hand-tied bouquet with mixed textures",
    "price_tier": "Premium",
    "mood": "Gentle, nurturing, soft elegance with a touch of innocence",
    "suggested_occasions": ["Mother's Day", "Birthday", "Get Well"],
    "product_summary": "An elegant hand-tied bouquet of soft pink carnations accented with baby's breath"
}

RULES:
1. Identify ALL flower types visible in the image
2. Extract 3-5 dominant colors as hex codes
3. price_tier must be one of: "Budget", "Standard", "Premium", "Luxury"
4. mood should describe the emotional feeling in 8-15 words
5. product_summary should be a single elegant sentence (luxury copywriting tone)
"""

    with Timer("Vision analysis"):
        response = client.models.generate_content(
            model=config.TEXT_MODEL,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                prompt,
            ],
            config=types.GenerateContentConfig(
                temperature=0.3,
                response_mime_type="application/json",
            ),
        )

    # Step 3: Parse the response
    try:
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]
            raw_text = raw_text.rsplit("```", 1)[0]

        analysis_data = json.loads(raw_text)
        analysis = ProductAnalysis(**analysis_data)
    except (json.JSONDecodeError, TypeError, KeyError) as e:
        log_step(f"[WARN] Parse error: {e}. Using fallback analysis.")
        analysis = _get_fallback_analysis()

    # Step 4: Log results
    log_result("Flowers", ", ".join(analysis.flower_types))
    log_result("Colors", ", ".join(analysis.color_names))
    log_result("Style", analysis.arrangement_style)
    log_result("Tier", analysis.price_tier)
    log_result("Mood", analysis.mood)
    log_result("Summary", analysis.product_summary)

    log_agent_complete("Vision Analysis Agent")
    return analysis


def _get_fallback_analysis() -> ProductAnalysis:
    """Fallback product analysis when Gemini fails."""
    return ProductAnalysis(
        flower_types=["Mixed Flowers"],
        dominant_colors=["#FFB6C1", "#FFFFFF"],
        color_names=["Soft Pink", "White"],
        arrangement_style="Hand-tied bouquet",
        price_tier="Premium",
        mood="Elegant, fresh, thoughtfully arranged",
        suggested_occasions=["Any Occasion"],
        product_summary="A premium hand-arranged bouquet of fresh flowers",
    )
