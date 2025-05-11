# src/pattern_language_miner/enricher/pattern_enricher.py

import logging
from pathlib import Path
import yaml
from typing import List, Dict, Any


def infer_problem_from_solution(solution: str) -> str:
    if "install" in solution.lower():
        return "Software is not installed."
    if "restart" in solution.lower():
        return "Service is not running properly."
    if "remove" in solution.lower():
        return "Resource needs to be deleted."
    return "Unknown problem."


def enrich_pattern(pattern: Dict[str, Any]) -> Dict[str, Any]:
    enriched = dict(pattern)

    solution = enriched.get("solution", "").strip()

    # Inferred title
    if "title" not in enriched or not enriched["title"]:
        enriched["title"] = solution.capitalize() if solution else "Untitled"

    # Inferred summary
    if "summary" not in enriched or not enriched["summary"]:
        if solution:
            enriched["summary"] = f"This pattern proposes the solution '{solution}'."
        else:
            enriched["summary"] = "No solution provided."

    # Inferred problem
    if "problem" not in enriched or not enriched["problem"]:
        enriched["problem"] = infer_problem_from_solution(solution)

    # Inferred keywords
    if "keywords" not in enriched or not enriched["keywords"]:
        enriched["keywords"] = solution.lower().split() if solution else []

    return enriched


class PatternEnricher:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

    def run(self) -> None:
        """Enrich pattern files in the input directory and save them to the output directory."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        files = list(self.input_dir.glob("*.yaml"))
        logging.info(f"🔍 Enriching {len(files)} pattern files...")

        for path in files:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    pattern = yaml.safe_load(f)
            except Exception as e:
                logging.warning(f"⚠️ Failed to read {path.name}: {e}")
                continue

            enriched = enrich_pattern(pattern)

            output_path = self.output_dir / path.name
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    yaml.dump(enriched, f, allow_unicode=True, sort_keys=False)
            except Exception as e:
                logging.warning(f"⚠️ Failed to write {output_path.name}: {e}")

        logging.info(f"✅ Enrichment complete. Saved to {self.output_dir}")