"""
═══════════════════════════════════════════════════════════════
  FNP Premium Ad Pipeline — Luxury Archetypes Database
  Maps gifting events to premium creative direction.
  Each archetype drives the entire visual & tonal identity
  of the generated ad campaign.
═══════════════════════════════════════════════════════════════
"""

LUXURY_ARCHETYPES = {
    "Mother's Day": {
        "mood": "Warm, ethereal, maternal elegance, soft sunlight",
        "color_palette": ["soft pink", "ivory", "gold", "blush rose"],
        "lighting": "Golden hour, warm diffused light through sheer curtains",
        "setting": "Sunlit garden room, linen tablecloth, morning dew on petals",
        "tagline_style": "Tender, emotional, celebrating the origin of love",
        "sample_taglines": [
            "For the one who bloomed first",
            "Where every petal learned to love",
            "The first garden was her arms",
        ],
        "typography": {
            "style": "Elegant serif, soft gold on translucent overlay",
            "tagline_color": (255, 248, 230),       # Warm cream
            "subheadline_color": (255, 228, 196),    # Bisque
            "overlay_gradient": [(0, 0, 0, 0), (45, 25, 15, 200)],  # Warm dark gradient
        },
    },
    "Valentine's Day": {
        "mood": "Deep reds, candlelit, romantic velvet",
        "color_palette": ["deep crimson", "burgundy", "midnight black", "gold"],
        "lighting": "Candlelit, warm amber glow, intimate shadows",
        "setting": "Velvet draped table, crystal vase, scattered rose petals, champagne",
        "tagline_style": "Passionate, poetic, whispered luxury",
        "sample_taglines": [
            "Some fires bloom",
            "Written in petals, sealed in velvet",
            "Love, arranged",
        ],
        "typography": {
            "style": "Script font, cream on dark overlay",
            "tagline_color": (255, 235, 215),       # Antique white
            "subheadline_color": (220, 190, 170),
            "overlay_gradient": [(0, 0, 0, 0), (60, 10, 20, 210)],  # Deep crimson gradient
        },
    },
    "Diwali": {
        "mood": "Opulent, radiant, festival of lights grandeur",
        "color_palette": ["marigold gold", "deep purple", "royal red", "bronze"],
        "lighting": "Warm diyas, fairy lights bokeh, golden hour",
        "setting": "Ornate brass vase, silk fabric, marigold garlands, lit diyas",
        "tagline_style": "Celebratory, auspicious, luminous",
        "sample_taglines": [
            "Light a thousand blooms",
            "Prosperity, in every petal",
            "Where light meets fragrance",
        ],
        "typography": {
            "style": "Decorative serif, gold foil on dark gradient",
            "tagline_color": (255, 215, 0),          # Gold
            "subheadline_color": (255, 223, 130),
            "overlay_gradient": [(0, 0, 0, 0), (40, 10, 40, 210)],  # Deep purple gradient
        },
    },
    "Raksha Bandhan": {
        "mood": "Sibling warmth, festive joy, tradition meets modern elegance",
        "color_palette": ["saffron", "turquoise", "magenta", "pearl white"],
        "lighting": "Bright, festive, cheerful morning light",
        "setting": "Decorated thali, colorful ribbons, mixed bouquet, rakhi threads",
        "tagline_style": "Warm, playful, bond-celebrating",
        "sample_taglines": [
            "Tied with petals, sealed with love",
            "A bloom for every bond",
            "Flowers speak what threads promise",
        ],
        "typography": {
            "style": "Modern sans-serif, vibrant on light overlay",
            "tagline_color": (255, 255, 255),
            "subheadline_color": (240, 240, 255),
            "overlay_gradient": [(0, 0, 0, 0), (80, 20, 60, 190)],  # Warm magenta gradient
        },
    },
    "Christmas": {
        "mood": "Festive warmth, cozy elegance, winter wonder",
        "color_palette": ["forest green", "crimson red", "gold", "snow white"],
        "lighting": "Warm fairy lights, fireplace glow, soft winter light",
        "setting": "Decorated mantle, pine branches, wrapped gifts, crystal vase",
        "tagline_style": "Joyful, warm, classic holiday elegance",
        "sample_taglines": [
            "Blooms under the mistletoe",
            "Wrapped in petals, tied with joy",
            "The season's finest arrangement",
        ],
        "typography": {
            "style": "Classic serif, gold on forest green overlay",
            "tagline_color": (255, 248, 220),
            "subheadline_color": (220, 230, 210),
            "overlay_gradient": [(0, 0, 0, 0), (15, 40, 20, 200)],  # Forest green gradient
        },
    },
    "New Year": {
        "mood": "Celebratory glamour, midnight sparkle, fresh beginnings",
        "color_palette": ["midnight blue", "champagne gold", "silver", "white"],
        "lighting": "Sparklers, champagne bubbles, midnight blue glow",
        "setting": "Elegant party table, champagne flutes, confetti, sleek vase",
        "tagline_style": "Optimistic, glamorous, forward-looking",
        "sample_taglines": [
            "New year, first bloom",
            "Begin with beauty",
            "Cheers to fresh petals",
        ],
        "typography": {
            "style": "Modern elegant, silver on midnight overlay",
            "tagline_color": (230, 240, 255),
            "subheadline_color": (200, 210, 230),
            "overlay_gradient": [(0, 0, 0, 0), (10, 15, 45, 210)],  # Midnight blue gradient
        },
    },
    "Women's Day": {
        "mood": "Empowering, vibrant, modern femininity",
        "color_palette": ["purple", "lavender", "white", "gold"],
        "lighting": "Clean, bright studio light with soft purple accents",
        "setting": "Modern minimalist, geometric vase, empowering backdrop",
        "tagline_style": "Bold, celebratory, honoring strength and grace",
        "sample_taglines": [
            "Bloom without permission",
            "Fierce. Fragrant. Unapologetic.",
            "Strength looks like petals",
        ],
        "typography": {
            "style": "Bold modern serif, white on purple overlay",
            "tagline_color": (255, 255, 255),
            "subheadline_color": (230, 220, 255),
            "overlay_gradient": [(0, 0, 0, 0), (50, 20, 70, 200)],  # Purple gradient
        },
    },
    "Anniversary": {
        "mood": "Timeless elegance, enduring romance, classic luxury",
        "color_palette": ["champagne", "ivory", "dusty rose", "sage green"],
        "lighting": "Soft studio light, elegant and timeless",
        "setting": "Marble surface, crystal vase, silk ribbon, soft bokeh",
        "tagline_style": "Sophisticated, timeless, celebrating endurance",
        "sample_taglines": [
            "Still blooming, still us",
            "Years fade. Flowers remember",
            "Every year, a new petal",
        ],
        "typography": {
            "style": "Classic serif, embossed style, muted gold",
            "tagline_color": (235, 220, 195),
            "subheadline_color": (210, 200, 180),
            "overlay_gradient": [(0, 0, 0, 0), (35, 30, 25, 190)],  # Warm neutral gradient
        },
    },
    "Father's Day": {
        "mood": "Distinguished, warm strength, refined masculinity",
        "color_palette": ["navy blue", "forest green", "amber", "white"],
        "lighting": "Rich, warm study light, leather and wood tones",
        "setting": "Wooden desk, leather-bound books, sturdy vase, whiskey glass",
        "tagline_style": "Strong yet tender, honoring quiet devotion",
        "sample_taglines": [
            "For the roots that held us steady",
            "Strength in every stem",
            "The man behind every garden",
        ],
        "typography": {
            "style": "Strong serif, cream on dark navy overlay",
            "tagline_color": (245, 240, 225),
            "subheadline_color": (210, 205, 190),
            "overlay_gradient": [(0, 0, 0, 0), (15, 25, 50, 200)],  # Navy gradient
        },
    },
    "Default / General Gifting": {
        "mood": "Fresh, joyful, premium everyday luxury",
        "color_palette": ["soft lavender", "mint green", "warm white", "peach"],
        "lighting": "Clean, bright, airy daylight",
        "setting": "Modern minimalist, white marble, fresh greenery, clean lines",
        "tagline_style": "Uplifting, graceful, universally appealing",
        "sample_taglines": [
            "Because some moments deserve petals",
            "Arranged with intention",
            "Bloom, delivered",
        ],
        "typography": {
            "style": "Clean sans-serif, dark on frosted glass overlay",
            "tagline_color": (255, 255, 255),
            "subheadline_color": (230, 230, 240),
            "overlay_gradient": [(0, 0, 0, 0), (30, 30, 40, 180)],  # Neutral dark gradient
        },
    },
}


def get_archetype(event_name: str) -> dict:
    """
    Retrieve the luxury archetype for a given event.
    Falls back to 'Default / General Gifting' if event not found.
    """
    # Try exact match first
    if event_name in LUXURY_ARCHETYPES:
        return LUXURY_ARCHETYPES[event_name]

    # Try partial match (case-insensitive)
    event_lower = event_name.lower()
    for key, archetype in LUXURY_ARCHETYPES.items():
        if event_lower in key.lower() or key.lower() in event_lower:
            return archetype

    # Fallback
    return LUXURY_ARCHETYPES["Default / General Gifting"]
