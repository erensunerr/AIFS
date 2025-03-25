import os, sys
from pathlib import Path
from tqdm import tqdm
import pandas as pd

from tools.describe_image import describe_image
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()

IMAGE_DIR = Path("data/images")
VECTOR_DIR = "data/clothing_vectors"
CSV_FILE_PATH = "data/articles.csv"

try:
    articles_df = pd.read_csv(CSV_FILE_PATH)
except Exception as e:
    print(f"[!] Error reading CSV file: {e}")
    sys.exit(1)

# Init vector store
embedding = OpenAIEmbeddings()
vector_store = Chroma(
    persist_directory=VECTOR_DIR,
    embedding_function=embedding
)

# Optional: Load existing metadata to avoid re-indexing
existing_ids = set()
try:
    # Grabs all docs to cache processed IDs
    all_docs = vector_store.get(include=["metadatas"])
    for meta in all_docs["metadatas"]:
        if "clothing_id" in meta:
            existing_ids.add(meta["clothing_id"])
except Exception as e:
    print(f"[!] Warning: Could not fetch existing docs: {e}")

# Process images
new_items = 0
for img_path in tqdm(sorted(IMAGE_DIR.glob("*.jpg"))):
    clothing_id = img_path.stem

    if clothing_id in existing_ids:
        continue  # already processed

    try:
        # Get additional context from the articles dataframe
        context_rows = articles_df[articles_df['article_id'] == int(clothing_id)]

        context_dump = "Extra information about the clothing item:\n"

        if not context_rows.empty:
            row = context_rows.iloc[0]
            for column in row.index:
                if isinstance(row[column], str):
                    context_dump += f"{column}: {row[column]}\n"
        description = describe_image(str(img_path), context_dump=context_dump)

    except Exception as e:
        print(f"[!] Failed to process {clothing_id}: {e}")
        continue

    # Add to vector store
    vector_store.add_texts(
        texts=[description],
        metadatas=[{
            "clothing_id": clothing_id,
            "img_path": str(img_path)
        }]
    )

    new_items += 1

print(f"✅ Done. Processed {new_items} new items.")
