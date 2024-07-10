from typing import Dict, List

from app.models.ai.model_config import ModelConfig


class ModelConfigs:
    """
    Data model for a list of model configurations.

    Attributes:
        configs (List[ModelConfig]): List of model configurations.
    """

    def __init__(self, configs: List[Dict[str, str]]):
        self.configs = [ModelConfig(**config) for config in configs]

    def get_model_config(self, identifier: str) -> ModelConfig:
        """
        Retrieves a specific model configuration by model name or key, case-insensitively.

        Args:
            identifier (str): The model name or key of the model to retrieve.

        Returns:
            ModelConfig: The model configuration matching the identifier.
        """
        identifier_lower = identifier.lower()
        for config in self.configs:
            if config.model.lower() == identifier_lower or (
                config.key and config.key.lower() == identifier_lower
            ):
                return config
        raise ValueError(
            f"Model or key '{identifier}' not found in the configurations."
        )

    @classmethod
    def from_dict_list(cls, configs: List[Dict[str, str]]) -> "ModelConfigs":
        """Creates a ModelConfigs instance from a list of dictionaries."""
        return cls(configs=configs)


# Example usage
# if __name__ == "__main__":
#     import json

#     # Sample data structure read from a file
#     with open('config/model_configs.json', 'r') as f:
#         MODEL_CONFIGS = json.load(f)

#     # Validate and parse the data structure
#     model_configs = ModelConfigs.from_dict_list(MODEL_CONFIGS)
#     for config in model_configs.configs:
#         print(f"Description: {config.description}, Base URL: {config.base_url}, API Key: {config.api_key}, Model: {config.model}, Key: {config.key}")
