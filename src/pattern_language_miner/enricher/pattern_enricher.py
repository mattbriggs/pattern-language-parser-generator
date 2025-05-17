"""
Pattern Enricher
================

Adds (or refreshes) high‑level metadata to the pattern‑YAML files produced by the
`analyze` step:

* **title**      – single‑line human label (defaults to capitalised solution).
* **summary**    – one‑sentence description if missing.
* **problem**    – naïvely inferred from the solution text.
* **keywords**   – lower‑cased tokens stripped of punctuation and de‑duplicated.

The module can be used one‑off via :class:`PatternEnricher` (CLI sub‑command
``enrich``) or programmatically via :func:`enrich_pattern`.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

import yaml

# ---------------------------- simple inference helpers ---------------------------- #

TOKEN_RE = re.compile(r"[A-Za-z0-9-]+")


def extract_keywords(text: str) -> list[str]:
    """
    Return a list of lower‑case tokens without surrounding punctuation.

    Hyphens inside words (``apt-get``) are preserved. Order is preserved while
    silently de‑duplicating.
    """
    if not text:
        return []

    seen: set[str] = set()
    keywords: list[str] = []
    for token in TOKEN_RE.findall(text.lower()):
        if token not in seen:
            seen.add(token)
            keywords.append(token)
    return keywords


def infer_problem_from_solution(solution: str) -> str:
    """
    Very naïve heuristics mapping solution verbs to a problem statement.

    Replace with something smarter (NLU model) when available.
    """
    sol = solution.lower()
    if "install" in sol:
        return "Software is not installed."
    if "restart" in sol:
        return "Service is not running properly."
    if "remove" in sol or "delete" in sol:
        return "Resource needs to be deleted."
    return "Unknown problem."


# ---------------------------- core enrichment logic ---------------------------- #


def enrich_pattern(pattern: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a *new* dict with all inferred fields populated / normalised.

    The original dict passed in is **not** mutated.
    """
    enriched: Dict[str, Any] = dict(pattern)  # shallow copy is enough

    solution: str = enriched.get("solution", "").strip()

    # ---- title --------------------------------------------------------------- #
    if not enriched.get("title"):
        enriched["title"] = solution.capitalize() if solution else "Untitled"

    # ---- summary ------------------------------------------------------------- #
    if not enriched.get("summary"):
        enriched["summary"] = (
            f"This pattern proposes the solution “{solution}”."
            if solution
            else "No solution provided."
        )

    # ---- problem ------------------------------------------------------------- #
    if not enriched.get("problem"):
        enriched["problem"] = infer_problem_from_solution(solution)

    # ---- keywords ------------------------------------------------------------ #
    enriched["keywords"] = extract_keywords(solution)

    return enriched


class PatternEnricher:
    """
    Batch‑enrich every ``*.yaml``/``*.yml`` file in *input_dir* and write the
    result to *output_dir* using the same filename.
    """

    def __init__(self, input_dir: Path | str, output_dir: Path | str) -> None:
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

    # --------------------------------------------------------------------- public

    def run(self) -> None:
        """Walk input‑directory, enrich each YAML, write to *output_dir*."""
        self._prepare_output_dir()
        files = list(self.input_dir.glob("*.yml")) + list(
            self.input_dir.glob("*.yaml")
        )
        logging.info("🔍 Enriching %d pattern files…", len(files))

        for path in files:
            try:
                pattern = self._load_yaml(path)
            except Exception as exc:  # pragma: no cover – logged, skip file
                logging.warning("⚠️  Failed to read %s: %s", path.name, exc)
                continue

            enriched = enrich_pattern(pattern)
            self._write_yaml(enriched, self.output_dir / path.name)

        logging.info("✅ Enrichment complete. Saved to %s", self.output_dir)

    # ------------------------------------------------------------------ internals

    def _prepare_output_dir(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _load_yaml(path: Path) -> Dict[str, Any]:
        with path.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}

    @staticmethod
    def _write_yaml(data: Dict[str, Any], path: Path) -> None:
        try:
            with path.open("w", encoding="utf-8") as fh:
                yaml.dump(data, fh, allow_unicode=True, sort_keys=False)
        except Exception as exc:  # pragma: no cover
            logging.warning("⚠️  Failed to write %s: %s", path.name, exc)