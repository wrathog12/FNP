"""
═══════════════════════════════════════════════════════════════
  Agent 3: Creative Orchestrator — Creative Director Agent
  
  Merges Event Intelligence + Product Analysis + Luxury Archetype
  into a campaign-ready creative brief with image prompt, tagline,
  and art direction.
  
  This is the BRAIN of the pipeline — it shifts the entire creative
  direction based on the detected event's "Luxury Archetype."
═══════════════════════════════════════════════════════════════
"""

import json
from dataclasses import dataclass, asdict

from google import genai
from google.genai import types

import config
from utils import log_agent_start, log_agent_complete, log_step, log_result, Timer
from luxury_archetypes import get_archetype
from agents.context_agent import EventContext
from agents.vision_agent import ProductAnalysis


@dataclass
class CreativeBrief:
    """Structured output from the Creative Director Agent."""
    image_prompt: str           # Full detailed prompt for image generation
    tagline: str                # "For the one who bloomed first"
    sub_headline: str           # "Pink Carnations, hand-arranged for Mother's Day"
    brand_name: str             # "FNP"
    color_direction: str        # "Soft pinks, ivory, warm gold accents"
    typography_direction: str   # "Elegant serif, soft gold on translucent overlay"
    event_name: str             # "Mother's Day"
    product_name: str           # "Pink Carnations Bouquet"
    luxury_mood: str            # The archetype mood applied

    def to_dict(self) -> dict:
        return asdict(self)


def create_brief(event: EventContext, product: ProductAnalysis) -> CreativeBrief:
    """
    Create a campaign-ready creative brief by merging event + product + archetype.
    
    The creative direction SHIFTS based on the event's Luxury Archetype:
    - Mother's Day → "Warm, ethereal, maternal elegance, soft sunlight"
    - Valentine's → "Deep reds, candlelit, romantic velvet"
    - Diwali → "Opulent, radiant, festival of lights grandeur"
    
    Args:
        event: EventContext from the Context Agent
        product: ProductAnalysis from the Vision Agent
        
    Returns:
        CreativeBrief with image prompt, tagline, and art direction.
    """
    log_agent_start("Creative Orchestrator - Director Agent", "[ART]")

    # Step 1: Retrieve the Luxury Archetype
    archetype = get_archetype(event.event_name)
    log_step(f"[ARCH] Luxury Archetype: {event.event_name}")
    log_step(f"[MOOD] Mood: {archetype['mood']}")

    # Step 2: Build the creative direction prompt
    log_step("[CRAFT] Crafting creative brief with Gemini...")

    client = genai.Client(api_key=config.GEMINI_API_KEY)

    prompt = f"""You are a world-class creative director at FNP (Ferns N Petals), crafting a LUXURY OCCASION AD — not just a product ad.

═══ EVENT CONTEXT ═══
Event: {event.event_name}
Date: {event.event_date} ({event.days_until} days away)
Urgency: {event.gifting_urgency}
Target Emotion: {event.target_emotion}
Cultural Significance: {event.cultural_significance}

═══ PRODUCT ANALYSIS ═══
Flowers: {', '.join(product.flower_types)}
Colors: {', '.join(product.color_names)} ({', '.join(product.dominant_colors)})
Style: {product.arrangement_style}
Tier: {product.price_tier}
Mood: {product.mood}
Summary: {product.product_summary}

═══ LUXURY ARCHETYPE DIRECTION ═══
Mood: {archetype['mood']}
Color Palette: {', '.join(archetype['color_palette'])}
Lighting: {archetype['lighting']}
Setting: {archetype['setting']}
Tagline Style: {archetype['tagline_style']}
Sample Taglines for Inspiration: {', '.join(archetype['sample_taglines'])}

═══ YOUR TASK ═══
Create a campaign-ready creative brief that makes this a LUXURY OCCASION AD.

The visual should feel like it belongs in Vogue or a Hermès campaign — not a product catalog.

Respond ONLY with valid JSON in this exact format (no markdown, no code blocks):
{{
    "image_prompt": "A highly detailed, photorealistic premium advertisement photograph of [describe the scene merging the product with the occasion setting]. The lighting is [archetype lighting]. The mood is [archetype mood]. Style: luxury editorial photography, 8K, shallow depth of field, rich textures, premium brand aesthetic. NO text, NO logos, NO watermarks in the image.",
    "tagline": "A short, powerful, emotional tagline (max 8 words)",
    "sub_headline": "A slightly longer supporting line that mentions both the product and occasion (max 15 words)",
    "color_direction": "Describe the color palette direction for the ad",
    "typography_direction": "Describe the typography style that matches the mood",
    "product_name": "The product name in elegant form"
}}

RULES:
1. The image_prompt MUST be highly detailed (50-100 words minimum)
2. The image_prompt must merge the actual product (flowers) with the event setting naturally
3. The tagline must be emotionally resonant and luxury-tier — NOT generic
4. Do NOT use clichés like "Say it with flowers" or "The perfect gift"
5. The image_prompt must explicitly say "NO text, NO logos, NO watermarks"
6. Focus on creating a FEELING, not describing a product
"""

    with Timer("Creative direction"):
        response = client.models.generate_content(
            model=config.TEXT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,  # Higher creativity for art direction
                response_mime_type="application/json",
            ),
        )

    # Step 3: Parse the response
    try:
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]
            raw_text = raw_text.rsplit("```", 1)[0]

        brief_data = json.loads(raw_text)

        brief = CreativeBrief(
            image_prompt=brief_data["image_prompt"],
            tagline=brief_data["tagline"],
            sub_headline=brief_data["sub_headline"],
            brand_name="FNP",
            color_direction=brief_data["color_direction"],
            typography_direction=brief_data["typography_direction"],
            event_name=event.event_name,
            product_name=brief_data.get("product_name", ", ".join(product.flower_types)),
            luxury_mood=archetype["mood"],
        )
    except (json.JSONDecodeError, TypeError, KeyError) as e:
        log_step(f"[WARN] Parse error: {e}. Using fallback brief.")
        brief = _get_fallback_brief(event, product, archetype)

    # Step 4: Log results
    log_result("Tagline", f'"{brief.tagline}"')
    log_result("Sub-headline", f'"{brief.sub_headline}"')
    log_result("Product", brief.product_name)
    log_result("Mood", brief.luxury_mood)
    log_step(f"[PROMPT] Image Prompt: {brief.image_prompt[:100]}...")

    log_agent_complete("Creative Orchestrator")
    return brief


def _get_fallback_brief(event: EventContext, product: ProductAnalysis, archetype: dict) -> CreativeBrief:
    """Fallback creative brief when Gemini fails."""
    flowers = ", ".join(product.flower_types)
    tagline = archetype["sample_taglines"][0] if archetype["sample_taglines"] else "Bloom, delivered"

    return CreativeBrief(
        image_prompt=(
            f"A photorealistic premium advertisement photograph of a luxurious {flowers} bouquet "
            f"arranged in an elegant setting. {archetype['lighting']}. {archetype['setting']}. "
            f"The mood is {archetype['mood']}. Style: luxury editorial photography, 8K, "
            f"shallow depth of field, rich textures. NO text, NO logos, NO watermarks."
        ),
        tagline=tagline,
        sub_headline=f"{flowers} — crafted for {event.event_name}",
        brand_name="FNP",
        color_direction=", ".join(archetype["color_palette"]),
        typography_direction=archetype["typography"]["style"],
        event_name=event.event_name,
        product_name=f"{flowers} Bouquet",
        luxury_mood=archetype["mood"],
    )
