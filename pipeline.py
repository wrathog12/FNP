"""
═══════════════════════════════════════════════════════════════
  FNP PREMIUM AD AUTOMATION PIPELINE
  Event Intelligence Layer
  
  Generates campaign-ready, luxury-occasion premium ad assets
  for Ferns N Petals (FNP) by detecting upcoming gifting events,
  analyzing product images, and crafting event-aware creatives.
  
  Usage:
      python pipeline.py                          # Uses default input image
      python pipeline.py --image path/to/photo.jpg  # Custom input image
═══════════════════════════════════════════════════════════════
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from utils import log_header, log_divider, log_success, log_error, log_step, save_json, Timer

from agents.context_agent import get_current_event
from agents.vision_agent import analyze_product
from agents.creative_agent import create_brief
from agents.generation_agent import generate_campaign_asset


def run_pipeline(input_image_path: str = None):
    """
    Execute the full 4-agent premium ad pipeline.
    
    Flow:
    1. Context Agent → Detect upcoming gifting event
    2. Vision Agent → Analyze input product image
    3. Creative Orchestrator → Generate creative brief
    4. Generation Agent → Produce campaign-ready asset
    
    Args:
        input_image_path: Path to the input product image.
                         If None, uses the first image found in input/ directory.
    """
    log_header("CAMPAIGN GENERATION")

    # ── Resolve input image ──
    if input_image_path:
        image_path = Path(input_image_path)
    else:
        image_path = _find_input_image()

    if not image_path or not image_path.exists():
        log_error(f"No input image found! Please place a product image in: {config.INPUT_DIR}")
        log_step("Supported formats: .jpg, .jpeg, .png, .webp")
        sys.exit(1)

    log_step(f"[IMG] Input image: {image_path.name}")
    log_step(f"[DATE] Current date: {datetime.now().strftime('%B %d, %Y')}")
    log_divider()

    # ═══════════════════════════════════════
    #  AGENT 1: Event Intelligence
    # ═══════════════════════════════════════
    with Timer("Full pipeline"):
        event = get_current_event()

        # ═══════════════════════════════════════
        #  AGENT 2: Vision Analysis
        # ═══════════════════════════════════════
        product = analyze_product(str(image_path))

        # ═══════════════════════════════════════
        #  AGENT 3: Creative Orchestration
        # ═══════════════════════════════════════
        brief = create_brief(event, product)

        # ═══════════════════════════════════════
        #  AGENT 4: Generation & Overlay
        # ═══════════════════════════════════════
        final_asset_path = generate_campaign_asset(brief)

    # ── Save Campaign Metadata ──
    log_divider()
    metadata = _build_metadata(event, product, brief, final_asset_path)
    metadata_path = config.OUTPUT_DIR / "campaign_metadata.json"
    save_json(metadata, metadata_path)
    log_step(f"[META] Metadata saved: {metadata_path.name}")

    # ── Final Summary ──
    log_divider()
    log_success("CAMPAIGN ASSET GENERATED SUCCESSFULLY!")
    print(f"  [DIR]     Output directory: {config.OUTPUT_DIR}")
    print(f"  [ASSET]   Final asset:     {final_asset_path}")
    print(f"  [META]    Metadata:        {metadata_path}")
    print()
    print(f"  [EVENT]   Event:    {event.event_name} ({event.days_until} days away)")
    print(f"  [PRODUCT] Product:  {brief.product_name}")
    print(f"  [TAG]     Tagline:  \"{brief.tagline}\"")
    print(f"  [HEAD]    Headline: \"{brief.sub_headline}\"")
    print()

    return final_asset_path


def _find_input_image() -> Path | None:
    """Find the first image file in the input directory."""
    valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}

    if not config.INPUT_DIR.exists():
        return None

    for file in sorted(config.INPUT_DIR.iterdir()):
        if file.suffix.lower() in valid_extensions:
            return file

    return None


def _build_metadata(event, product, brief, asset_path: str) -> dict:
    """Build the campaign metadata JSON."""
    return {
        "campaign": {
            "generated_at": datetime.now().isoformat(),
            "pipeline_version": "1.0.0",
            "brand": "FNP (Ferns N Petals)",
        },
        "event_intelligence": event.to_dict(),
        "product_analysis": product.to_dict(),
        "creative_brief": brief.to_dict(),
        "output": {
            "asset_path": asset_path,
            "format": "PNG",
            "type": "Campaign-Ready Premium Asset",
        },
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FNP Premium Ad Automation Pipeline - Event Intelligence Layer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pipeline.py
  python pipeline.py --image input/pink_carnations.jpg
  python pipeline.py --image "C:/Users/photos/bouquet.jpg"
        """,
    )
    parser.add_argument(
        "--image", "-i",
        type=str,
        default=None,
        help="Path to the input product image (default: first image in input/ directory)",
    )

    args = parser.parse_args()
    run_pipeline(args.image)


if __name__ == "__main__":
    main()
