import os
import yaml
from typing import Dict


class YAMLWriter:
    def __init__(self, output_dir: str):
        """
        Initializes the YAML writer with the target output directory.

        Args:
            output_dir (str): The path where YAML files will be written.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def write_pattern(self, pattern: Dict, filename: str):
        """
        Write a single pattern to a YAML file.

        Args:
            pattern (Dict): The pattern dictionary to serialize.
            filename (str): The filename to write the YAML to.
        """
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(
                pattern,
                f,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False
            )

    def write_patterns(self, patterns: Dict[str, Dict]):
        """
        Write multiple patterns to individual YAML files.

        Args:
            patterns (Dict[str, Dict]): A dictionary mapping filenames to pattern dicts.
        """
        for filename, pattern in patterns.items():
            self.write_pattern(pattern, filename)