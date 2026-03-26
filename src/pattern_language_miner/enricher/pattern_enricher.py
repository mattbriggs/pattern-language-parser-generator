"""Pattern enrichment module.

Adds or refreshes high-level metadata fields to the raw pattern YAML files
produced by the ``analyze`` pipeline step:

- **title** — single-line human label (defaults to capitalised solution).
- **summary** — one-sentence description if missing.
- **problem** — naively inferred from the solution text.
- **keywords** — lower-cased tokens, de-duplicated, preserving order.

The module exposes two entry-points:

- :func:`enrich_pattern` — enrich a single pattern dict (non-mutating).
- :class:`PatternEnricher` — batch-process a directory of YAML files.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Dict, List

import yaml

logger = logging.getLogger(__name__)

#: Regex matching valid keyword tokens (alphanumeric plus interior hyphens).
_TOKEN_RE = re.compile(r"[A-Za-z0-9-]+")


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------


def extract_keywords(text: str) -> List[str]:
    """Return a deduplicated, order-preserving list of lower-case tokens.

    Interior hyphens are preserved (e.g. ``apt-get`` stays as one token).
    Surrounding punctuation is stripped.

    Args:
        text: Input string from which keywords are extracted.

    Returns:
        A list of unique, lower-cased keyword tokens.

    Example:
        >>> extract_keywords("Install the apt-get package")
        ['install', 'the', 'apt-get', 'package']
    """
    if not text:
        return []
    seen: set[str] = set()
    keywords: List[str] = []
    for token in _TOKEN_RE.findall(text.lower()):
        if token not in seen:
            seen.add(token)
            keywords.append(token)
    return keywords


def infer_problem_from_solution(solution: str) -> str:
    """Map common solution verbs to a plausible problem statement.

    This is a lightweight heuristic intended as a starting point.
    Replace with an NLU model for production quality.

    Args:
        solution: The solution text from a pattern.

    Returns:
        A short problem statement inferred from the solution.

    Example:
        >>> infer_problem_from_solution("install the package")
        'Software is not installed.'
    """
    sol = solution.lower()
    if "install" in sol:
        return "Software is not installed."
    if "restart" in sol:
        return "Service is not running properly."
    if "remove" in sol or "delete" in sol:
        return "Resource needs to be deleted."
    return "Unknown problem."


# ---------------------------------------------------------------------------
# Core enrichment logic
# ---------------------------------------------------------------------------


def enrich_pattern(pattern: Dict[str, Any]) -> Dict[str, Any]:
    """Return a new dict with all inferred metadata fields populated.

    The *pattern* argument is **not** mutated; a shallow copy is enriched
    and returned.

    Fields populated (when absent):

    - ``title`` — capitalised solution or ``"Untitled"``.
    - ``summary`` — a generated one-sentence description.
    - ``problem`` — inferred from the solution via :func:`infer_problem_from_solution`.
    - ``keywords`` — always replaced with tokens from the solution.

    Args:
        pattern: Source pattern dictionary, typically loaded from YAML.

    Returns:
        A new dictionary with enriched fields.

    Example:
        >>> result = enrich_pattern({"solution": "install the package"})
        >>> result["title"]
        'Install the package'
    """
    enriched: Dict[str, Any] = dict(pattern)
    solution: str = enriched.get("solution", "").strip()

    if not enriched.get("title"):
        enriched["title"] = solution.capitalize() if solution else "Untitled"

    if not enriched.get("summary"):
        enriched["summary"] = (
            f"This pattern proposes the solution '{solution}'."
            if solution
            else "No solution provided."
        )

    if not enriched.get("problem"):
        enriched["problem"] = infer_problem_from_solution(solution)

    enriched["keywords"] = extract_keywords(solution)
    return enriched


# ---------------------------------------------------------------------------
# Batch enricher class
# ---------------------------------------------------------------------------


class PatternEnricher:
    """Batch-enrich every YAML file in *input_dir* and write to *output_dir*.

    This class implements the *Strategy* pattern: the enrichment logic is
    encapsulated in the :func:`enrich_pattern` function so it can be swapped
    without changing this class.

    Args:
        input_dir: Directory containing raw ``*.yaml`` / ``*.yml`` pattern files.
        output_dir: Directory where enriched files are written (same filenames).

    Example:
        >>> enricher = PatternEnricher("./raw_patterns", "./enriched_patterns")
        >>> enricher.run()
    """

    def __init__(self, input_dir: Path | str, output_dir: Path | str) -> None:
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Walk *input_dir*, enrich each pattern file, and write to *output_dir*.

        Files that cannot be parsed are skipped with a WARNING log entry.
        """
        self._prepare_output_dir()
        files = sorted(
            list(self.input_dir.glob("*.yml")) + list(self.input_dir.glob("*.yaml"))
        )
        logger.info("Enriching %d pattern file(s) in %s", len(files), self.input_dir)

        for path in files:
            try:
                pattern = self._load_yaml(path)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Failed to read %s: %s", path.name, exc)
                continue

            enriched = enrich_pattern(pattern)
            self._write_yaml(enriched, self.output_dir / path.name)

        logger.info("Enrichment complete. Saved to %s", self.output_dir)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

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
        except OSError as exc:  # noqa: BLE001
            logger.warning("Failed to write %s: %s", path.name, exc)
