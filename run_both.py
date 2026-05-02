"""
Run the pipeline for both bouquet images sequentially.
Saves each output with a unique name.
"""
import sys
import shutil
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent))

import config
from pipeline import run_pipeline

# The two bouquet images
images = [
    "input/written-in-roses_1.jpg",
    "input/written-in-roses_2.jpg",
]

for i, img_path in enumerate(images, 1):
    print(f"\n{'='*60}")
    print(f"  RUNNING PIPELINE FOR BOUQUET {i}: {img_path}")
    print(f"{'='*60}\n")

    try:
        result = run_pipeline(img_path)

        # Rename output to unique name
        if result:
            result_path = Path(result)
            unique_name = config.OUTPUT_DIR / f"campaign_bouquet_{i}.png"
            shutil.copy2(result_path, unique_name)
            print(f"\n  [SAVED] Saved as: {unique_name}")

            # Also rename metadata
            meta_src = config.OUTPUT_DIR / "campaign_metadata.json"
            meta_dst = config.OUTPUT_DIR / f"campaign_metadata_bouquet_{i}.json"
            if meta_src.exists():
                shutil.copy2(meta_src, meta_dst)

    except Exception as e:
        print(f"\n  [ERROR] Error processing bouquet {i}: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*60}")
print("  [DONE] ALL DONE! Check the output/ directory.")
print(f"{'='*60}")
