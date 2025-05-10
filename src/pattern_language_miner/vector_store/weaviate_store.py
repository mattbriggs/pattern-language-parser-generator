import weaviate
from typing import List, Dict, Optional


class WeaviateStore:
    def __init__(self, url: str = "http://localhost:8080", class_name: str = "Pattern"):
        """
        Initializes the connection to the Weaviate instance.

        Args:
            url (str): URL of the Weaviate instance.
            class_name (str): The class name used to store patterns.
        """
        self.client = weaviate.Client(url)
        self.class_name = class_name

    def upsert_pattern(self, pattern: Dict):
        """
        Inserts or updates a pattern object into the Weaviate index.

        Args:
            pattern (Dict): The pattern to insert.
        """
        uuid = pattern["id"]
        self.client.data_object.create(
            data_object=pattern,
            class_name=self.class_name,
            uuid=uuid
        )

    def query_similar_patterns(self, text: str, top_k: int = 5) -> List[Dict]:
        """
        Queries the Weaviate index for patterns similar to the input text.

        Args:
            text (str): Query string to search against.
            top_k (int): Number of similar patterns to return.

        Returns:
            List[Dict]: A list of similar patterns with their metadata.
        """
        results = self.client.query.get(
            class_name=self.class_name,
            properties=["id", "name", "context", "solution"]
        ).with_near_text({
            "concepts": [text]
        }).with_limit(top_k).do()

        return results["data"]["Get"].get(self.class_name, [])

    def delete_pattern(self, uuid: str) -> Optional[Dict]:
        """
        Deletes a pattern object from the Weaviate index by UUID.

        Args:
            uuid (str): The UUID of the pattern to delete.

        Returns:
            Optional[Dict]: The response from the deletion operation, if applicable.
        """
        return self.client.data_object.delete(uuid=uuid, class_name=self.class_name)