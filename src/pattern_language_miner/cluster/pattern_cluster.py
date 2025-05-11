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
    def __init__(self, input_dir, field, model_name="all-MiniLM-L6-v2", batch_size=64):
        self.input_dir = Path(input_dir)
        self.field = field
        self.model_name = model_name
        self.patterns = []
        self.embeddings = None
        self.batch_size = batch_size
        self.model = SentenceTransformer(model_name)

    def load_patterns(self):
        logging.info(f"📁 Scanning for patterns in: {self.input_dir}")
        files = list(self.input_dir.glob("*.yaml"))
        total = len(files)
        logging.info(f"🔍 Found {total} YAML file(s) to process...")

        for i, file_path in enumerate(files, start=1):
            if i % 100 == 0 or logging.getLogger().level <= logging.DEBUG:
                logging.debug(f"📄 Processing file {i}/{total}: {file_path.name}")
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    pattern = yaml.safe_load(f)
                    if self.field in pattern:
                        self.patterns.append(pattern)
                except yaml.YAMLError as e:
                    logging.warning(f"⚠️ Skipping {file_path.name}: {e}")

        logging.info(f"✅ Loaded {len(self.patterns)} valid pattern(s).")

    def embed_patterns(self, batch_size=64):
        texts = [p[self.field] for p in self.patterns]
        total = len(texts)
        logging.info(f"🧠 Encoding {total} pattern(s) in batches of {batch_size}...")

        embeddings = []
        for start in range(0, total, self.batch_size):
            end = min(start + batch_size, total)
            batch = texts[start:end]
            logging.debug(f"🔄 Encoding batch {start // batch_size + 1}: items {start}-{end - 1}")
            batch_embeddings = self.model.encode(batch, show_progress_bar=False)
            embeddings.extend(batch_embeddings)

        self.embeddings = np.array(embeddings)
        logging.info("✅ All embeddings generated.")
        return self.embeddings

    def cluster_and_reduce(self, embeddings, n_clusters=5):
        n_samples = embeddings.shape[0]
        if n_clusters > n_samples:
            logging.warning(
                f"⚠️ Requested {n_clusters} clusters but only {n_samples} samples available. "
                f"Reducing to {n_samples} cluster(s)."
            )
            n_clusters = n_samples

        logging.info(f"📊 Clustering with KMeans (k={n_clusters})...")
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
        cluster_ids = kmeans.fit_predict(embeddings)
        logging.info("✅ KMeans clustering finished.")

        logging.info("📉 Reducing dimensions with UMAP for 2D projection...")
        reducer = umap.UMAP(n_neighbors=min(15, n_samples - 1), random_state=42)
        reduced = reducer.fit_transform(embeddings)
        logging.info("✅ Dimensionality reduction complete.")
        return reduced, cluster_ids

    def visualize_clusters(self, reduced, cluster_ids, output_path):
        logging.info(f"🖼️ Rendering cluster plot: {output_path}")
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
        logging.info("✅ Cluster plot saved as image.")

    def generate_cluster_report(self, cluster_ids, output_path):
        logging.info(f"📝 Generating cluster report to: {output_path}")
        report = []
        for i, (pattern, cluster_id) in enumerate(zip(self.patterns, cluster_ids), 1):
            entry = pattern.copy()
            entry["cluster"] = int(cluster_id)
            report.append(entry)
            if i % 100 == 0 or logging.getLogger().level <= logging.DEBUG:
                logging.debug(f"📦 Processed pattern {i} into cluster {cluster_id}")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        logging.info("✅ Cluster report written.")