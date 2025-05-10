from typing import List
from sentence_transformers import SentenceTransformer, util


class SemanticCluster:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", similarity_threshold: float = 0.75):
        """
        Initialize the semantic cluster engine.

        Args:
            model_name (str): Name of the SentenceTransformer model to use.
            similarity_threshold (float): Cosine similarity threshold for clustering.
        """
        self.model = SentenceTransformer(model_name)
        self.similarity_threshold = similarity_threshold

    def cluster_sentences(self, sentences: List[str]) -> List[List[str]]:
        """
        Group semantically similar sentences into clusters.

        Args:
            sentences (List[str]): A list of sentences.

        Returns:
            List[List[str]]: A list of clusters, each containing similar sentences.
        """
        embeddings = self.model.encode(sentences, convert_to_tensor=True)
        clusters = []
        used = set()

        for i, emb in enumerate(embeddings):
            if i in used:
                continue

            cluster = [sentences[i]]
            used.add(i)

            for j in range(i + 1, len(sentences)):
                if j in used:
                    continue

                sim = util.pytorch_cos_sim(emb, embeddings[j]).item()
                if sim >= self.similarity_threshold:
                    cluster.append(sentences[j])
                    used.add(j)

            clusters.append(cluster)

        return clusters