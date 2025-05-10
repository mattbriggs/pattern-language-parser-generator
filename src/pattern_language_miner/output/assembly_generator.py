from typing import List, Dict


class AssemblyGenerator:
    def __init__(self):
        """
        Initializes the generator responsible for creating assembly instructions
        from a pattern hierarchy.
        """
        self.instructions = []

    def generate(self, document_patterns: List[Dict]) -> Dict[str, List[str]]:
        """
        Generate a set of instructions from document-level patterns.

        Args:
            document_patterns (List[Dict]): List of document patterns, each containing a
                                            structure (list of subpattern IDs).

        Returns:
            Dict[str, List[str]]: A mapping from document pattern name to ordered subpatterns.
        """
        assembly_map = {}

        for pattern in document_patterns:
            name = pattern.get("name", "unnamed_pattern")
            structure = pattern.get("structure", [])
            notes = pattern.get("notes", "")
            entry = {
                "structure": structure,
                "notes": notes
            }
            assembly_map[name] = entry

        return assembly_map

    def to_yaml(self, assembly_map: Dict[str, Dict[str, List[str]]]) -> str:
        """
        Convert the instruction set to a YAML-formatted string.

        Args:
            assembly_map (Dict): Assembly instructions.

        Returns:
            str: YAML string representation.
        """
        import yaml
        return yaml.dump({"document_patterns": assembly_map}, sort_keys=False, default_flow_style=False)