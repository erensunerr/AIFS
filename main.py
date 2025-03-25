import argparse
import subprocess
import sys

from pathlib import Path
import random
import shutil

# --- CONFIG --- #
SRC_ROOT = Path("kaggle-dataset/h-and-m-personalized-fashion-recommendations/images")
DEST_ROOT = Path("data/images")
SAMPLE_LIMIT = 500  # Optional: max to avoid massive resampling

# --- COMMANDS --- #

def serve():
    print("🚀 Starting Streamlit app...")
    subprocess.run(["streamlit", "run", "ui.py"])

def process_images():
    print("🧠 Processing images...")
    subprocess.run([sys.executable, "process_images.py"])

def sample_images(n: int):
    print(f"🎲 Sampling {n} images...")
    all_images = list(SRC_ROOT.rglob("*.jpg"))
    existing = set(p.name for p in DEST_ROOT.glob("*.jpg"))

    # Filter out already-sampled images
    unsampled = [img for img in all_images if img.name not in existing]
    if len(unsampled) == 0:
        print("⚠️ No more unsampled images available.")
        return

    to_sample = min(n, len(unsampled), SAMPLE_LIMIT)
    sampled = random.sample(unsampled, to_sample)

    for src_path in sampled:
        dest_path = DEST_ROOT / src_path.name
        shutil.copy(src_path, dest_path)

    print(f"✅ Sampled and copied {to_sample} new images.")


# --- CLI Setup --- #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AIFS CLI")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("serve", help="Launch Streamlit UI")
    subparsers.add_parser("process_images", help="Run image embedder")

    sample_parser = subparsers.add_parser("sample", help="Sample N random images from full dataset")
    sample_parser.add_argument("n", type=int, help="Number of images to sample")

    args = parser.parse_args()

    if args.command == "serve":
        serve()
    elif args.command == "process_images":
        process_images()
    elif args.command == "sample":
        sample_images(args.n)
    else:
        parser.print_help()
