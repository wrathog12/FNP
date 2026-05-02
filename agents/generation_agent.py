"""
═══════════════════════════════════════════════════════════════
  Agent 4: Generation & Overlay Agent — Asset Producer
  
  Two-stage process:
  Stage 1: Generate the ad image using Gemini's native image gen
  Stage 2: Apply premium text overlay + logo using Pillow
  
  Produces a campaign-ready PNG with tagline, sub-headline,
  and FNP logo composited onto a luxury visual.
═══════════════════════════════════════════════════════════════
"""

import os
from pathlib import Path

from google import genai
from google.genai import types

from PIL import Image, ImageDraw, ImageFont, ImageFilter

import config
from utils import (
    log_agent_start, log_agent_complete, log_step, log_result,
    Timer, get_timestamp_filename,
)
from agents.creative_agent import CreativeBrief
from luxury_archetypes import get_archetype


def generate_campaign_asset(brief: CreativeBrief) -> str:
    """
    Generate a campaign-ready premium ad asset.
    
    Stage 1: Generate base image with Gemini
    Stage 2: Apply premium overlay (gradient + tagline + logo)
    
    Args:
        brief: CreativeBrief from the Creative Director Agent
        
    Returns:
        Path to the final campaign-ready PNG file.
    """
    log_agent_start("Generation & Overlay Agent - Asset Producer", "[GEN]")

    # ── Stage 1: Image Generation ──
    raw_image_path = _generate_image(brief)

    # ── Stage 2: Premium Overlay ──
    final_path = _apply_premium_overlay(raw_image_path, brief)

    log_result("Final Asset", str(final_path))
    log_agent_complete("Generation & Overlay Agent")
    return str(final_path)


def _generate_image(brief: CreativeBrief) -> str:
    """Generate the base ad image using Gemini's native image generation."""
    log_step("[ART] Stage 1: Generating base image with Gemini...")

    client = genai.Client(api_key=config.GEMINI_API_KEY)

    with Timer("Image generation"):
        response = client.models.generate_content(
            model=config.IMAGE_GEN_MODEL,
            contents=brief.image_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

    # Extract and save the generated image
    raw_path = config.OUTPUT_DIR / "raw_generated.png"

    image_saved = False
    if response.candidates:
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                with open(raw_path, "wb") as f:
                    f.write(part.inline_data.data)
                image_saved = True
                log_step(f"[OK] Raw image saved: {raw_path.name}")
                break

    if not image_saved:
        raise RuntimeError(
            "Gemini did not return an image. Check your API key and model availability. "
            f"Response text: {response.text if response.text else 'No text returned'}"
        )

    return str(raw_path)


def _apply_premium_overlay(image_path: str, brief: CreativeBrief) -> str:
    """
    Apply premium text overlay + logo to the generated image.
    
    Creates a luxury ad feel with:
    - Gradient overlay bar at the bottom
    - Tagline in premium font (large, elegant)
    - Sub-headline below (smaller, lighter)
    - FNP logo composited at top-right corner
    """
    log_step("[OVERLAY] Stage 2: Applying premium overlay...")

    # Load the base image
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    log_step(f"[SIZE] Image size: {width}x{height}")

    # Get archetype typography settings
    archetype = get_archetype(brief.event_name)
    typo = archetype.get("typography", {})
    tagline_color = typo.get("tagline_color", config.TAGLINE_COLOR)
    subheadline_color = typo.get("subheadline_color", config.SUBHEADLINE_COLOR)
    gradient_colors = typo.get("overlay_gradient", [(0, 0, 0, 0), (0, 0, 0, 180)])

    # ── Logo Compositing ──
    img = _composite_logo(img)

    # ── Gradient Overlay Bar ──
    img = _apply_gradient_overlay(img, gradient_colors)

    # ── Text Rendering ──
    img = _render_text(img, brief, tagline_color, subheadline_color)

    # ── Save Final Asset ──
    filename = get_timestamp_filename("FNP_campaign", "png")
    final_path = config.OUTPUT_DIR / filename
    img.convert("RGB").save(final_path, quality=95)
    log_step(f"[SAVE] Final asset saved: {filename}")

    # Also save a copy with a fixed name for easy access
    fixed_path = config.OUTPUT_DIR / "campaign_asset.png"
    img.convert("RGB").save(fixed_path, quality=95)

    return str(final_path)


def _composite_logo(img: Image.Image) -> Image.Image:
    """Composite the FNP logo onto the image."""
    logo_path = config.LOGO_PATH

    if not logo_path.exists():
        log_step("[WARN] Logo not found - skipping logo overlay")
        log_step(f"   Place your logo at: {logo_path}")
        return img

    log_step("[LOGO] Compositing FNP logo...")

    logo = Image.open(logo_path).convert("RGBA")

    # Auto-scale logo to configured percentage of ad width
    logo_width = int(img.width * config.LOGO_SCALE)
    logo_ratio = logo_width / logo.width
    logo_height = int(logo.height * logo_ratio)
    logo = logo.resize((logo_width, logo_height), Image.LANCZOS)

    # Calculate position based on config
    margin = int(img.width * config.LOGO_MARGIN_RATIO)
    position = _get_logo_position(img.size, (logo_width, logo_height), margin)

    # Paste with alpha mask
    img.paste(logo, position, logo)
    log_step(f"[OK] Logo placed at {config.LOGO_POSITION} ({logo_width}x{logo_height}px)")

    return img


def _get_logo_position(img_size: tuple, logo_size: tuple, margin: int) -> tuple:
    """Calculate logo position based on config setting."""
    w, h = img_size
    lw, lh = logo_size

    positions = {
        "top-right": (w - lw - margin, margin),
        "top-left": (margin, margin),
        "bottom-right": (w - lw - margin, h - lh - margin),
        "bottom-left": (margin, h - lh - margin),
    }

    return positions.get(config.LOGO_POSITION, positions["top-right"])


def _apply_gradient_overlay(img: Image.Image, gradient_colors: list) -> Image.Image:
    """Apply a semi-transparent gradient overlay at the bottom of the image."""
    log_step("[GRAD] Applying gradient overlay...")

    width, height = img.size
    overlay_height = int(height * config.OVERLAY_HEIGHT_RATIO)

    # Create gradient overlay
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Get gradient end color (the solid color at bottom)
    if len(gradient_colors) >= 2:
        end_color = tuple(gradient_colors[1])
    else:
        end_color = (0, 0, 0, config.OVERLAY_OPACITY)

    # Draw gradient from transparent to end_color
    start_y = height - overlay_height
    for y in range(overlay_height):
        progress = y / overlay_height
        # Ease-in curve for smoother transition
        progress = progress * progress
        alpha = int(end_color[3] * progress)
        color = (end_color[0], end_color[1], end_color[2], alpha)
        draw.line([(0, start_y + y), (width, start_y + y)], fill=color)

    img = Image.alpha_composite(img, overlay)
    return img


def _render_text(
    img: Image.Image,
    brief: CreativeBrief,
    tagline_color: tuple,
    subheadline_color: tuple,
) -> Image.Image:
    """Render tagline and sub-headline text on the image."""
    log_step("[TEXT] Rendering text overlay...")

    width, height = img.size

    # Create a text layer for proper alpha compositing
    txt_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Load fonts
    tagline_font = _load_font("tagline", height)
    sub_font = _load_font("subheadline", height)

    # ── Tagline ──
    tagline_text = brief.tagline.upper() if len(brief.tagline) < 30 else brief.tagline
    tagline_bbox = draw.textbbox((0, 0), tagline_text, font=tagline_font)
    tagline_w = tagline_bbox[2] - tagline_bbox[0]
    tagline_h = tagline_bbox[3] - tagline_bbox[1]

    # Position: centered, in the lower portion of the image
    tagline_x = (width - tagline_w) // 2
    tagline_y = height - int(height * 0.18) - tagline_h

    # Draw text shadow for depth
    shadow_offset = max(2, int(height * 0.003))
    shadow_color = (0, 0, 0, 120)
    draw.text(
        (tagline_x + shadow_offset, tagline_y + shadow_offset),
        tagline_text, font=tagline_font, fill=shadow_color,
    )

    # Draw main tagline
    # Ensure tagline_color has alpha
    if len(tagline_color) == 3:
        tagline_color = (*tagline_color, 255)
    draw.text((tagline_x, tagline_y), tagline_text, font=tagline_font, fill=tagline_color)

    # ── Sub-headline ──
    sub_text = brief.sub_headline
    sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
    sub_w = sub_bbox[2] - sub_bbox[0]

    sub_x = (width - sub_w) // 2
    sub_y = tagline_y + tagline_h + int(height * 0.02)

    # Sub-headline shadow
    draw.text(
        (sub_x + shadow_offset, sub_y + shadow_offset),
        sub_text, font=sub_font, fill=shadow_color,
    )

    # Draw sub-headline
    if len(subheadline_color) == 3:
        subheadline_color = (*subheadline_color, 230)
    draw.text((sub_x, sub_y), sub_text, font=sub_font, fill=subheadline_color)

    # ── Brand Name ──
    brand_font = _load_font("brand", height)
    brand_text = f"- {brief.brand_name} -"
    brand_bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
    brand_w = brand_bbox[2] - brand_bbox[0]
    brand_x = (width - brand_w) // 2
    brand_y = sub_y + (sub_bbox[3] - sub_bbox[1]) + int(height * 0.015)

    brand_color = (*tagline_color[:3], 180)
    draw.text((brand_x, brand_y), brand_text, font=brand_font, fill=brand_color)

    # Composite text layer onto image
    img = Image.alpha_composite(img, txt_layer)
    return img


def _load_font(font_type: str, image_height: int) -> ImageFont.FreeTypeFont:
    """
    Load a font for the given type (tagline/subheadline/brand).
    Tries custom fonts first, then falls back to system fonts.
    """
    size = int(image_height * config.FONT_SIZES.get(font_type, 0.03))

    # Try custom font path
    custom_path = config.FONT_PATHS.get(font_type, "")
    if custom_path and os.path.exists(custom_path):
        try:
            return ImageFont.truetype(custom_path, size)
        except (IOError, OSError):
            pass

    # Try system font fallbacks
    for fallback_path in config.SYSTEM_FONT_FALLBACKS:
        if os.path.exists(fallback_path):
            try:
                return ImageFont.truetype(fallback_path, size)
            except (IOError, OSError):
                continue

    # Last resort: default font (will look basic)
    log_step(f"[WARN] No premium font found for '{font_type}', using default")
    return ImageFont.load_default()
