import os
import json
import logging
import numpy as np
import yaml
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import umap
from pathlib import Path


class PatternClusterer:
    def __init__(self, input_dir, field, model_name="all-MiniLM-L6-v2"):
        self.input_dir = Path(input_dir)
        self.field = field
        self.model_name = model_name
        self.patterns = []
        self.embeddings = None
        self.model = SentenceTransformer(model_name)

    def load_patterns(self):
        logging.info(f"📁 Loading patterns from: {self.input_dir}")
        for file_path in self.input_dir.glob("*.yaml"):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    pattern = yaml.safe_load(f)
                    if self.field in pattern:
                        self.patterns.append(pattern)
                except yaml.YAMLError as e:
                    logging.warning(f"⚠️ Skipping {file_path.name}: {e}")
        logging.info(f"✅ Loaded {len(self.patterns)} patterns.")

    def embed_patterns(self):
        texts = [p[self.field] for p in self.patterns]
        logging.info(f"🧠 Generating embeddings for {len(texts)} patterns...")
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        logging.info("✅ Embeddings generated.")
        return self.embeddings

    def cluster_and_reduce(self, embeddings, n_clusters=5):
        n_samples = embeddings.shape[0]
        if n_clusters > n_samples:
            logging.warning(
                f"⚠️ Requested {n_clusters} clusters but only {n_samples} samples found. "
                f"Reducing to {n_samples} clusters."
            )
            n_clusters = n_samples

        logging.info(f"📊 Running KMeans with {n_clusters} clusters...")
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
        cluster_ids = kmeans.fit_predict(embeddings)
        logging.info("✅ Clustering completed.")

        logging.info("📉 Reducing dimensions with UMAP for visualization...")
        reducer = umap.UMAP(n_neighbors=min(15, n_samples - 1), random_state=42)
        reduced = reducer.fit_transform(embeddings)
        logging.info("✅ Dimensionality reduction complete.")
        return reduced, cluster_ids

    def visualize_clusters(self, reduced, cluster_ids, output_path):
        logging.info(f"🖼️ Generating cluster plot: {output_path}")
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(
            reduced[:, 0], reduced[:, 1], c=cluster_ids, cmap="tab10", s=50
        )
        plt.colorbar(scatter, label="Cluster ID")
        plt.title("Pattern Clusters (UMAP Reduced)")
        plt.xlabel("UMAP-1")
        plt.ylabel("UMAP-2")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        logging.info("✅ Cluster visualization saved.")

    def generate_cluster_report(self, cluster_ids, output_path):
        logging.info(f"📝 Writing clustered pattern report to {output_path}")
        report = []
        for pattern, cluster_id in zip(self.patterns, cluster_ids):
            entry = pattern.copy()
            entry["cluster"] = int(cluster_id)
            report.append(entry)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        logging.info("✅ Cluster report saved.")
