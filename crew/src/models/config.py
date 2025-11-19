"""Model configuration loader and manager.

Handles loading model configurations from YAML and environment variables,
making it easy to switch between different LLM providers.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


class ModelConfig(BaseModel):
    """Configuration for a single model."""

    provider: str = Field(..., description="Provider name (google, anthropic, openai)")
    model_name: str = Field(..., description="Model identifier")
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, gt=0)
    api_key_env: str = Field(..., description="Environment variable name for API key")

    def get_api_key(self) -> Optional[str]:
        """Retrieve API key from environment."""
        return os.getenv(self.api_key_env)

    def to_llm_config(self) -> Dict[str, Any]:
        """Convert to LLM configuration dict for CrewAI/LiteLLM."""
        config = {
            "model": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        api_key = self.get_api_key()
        if api_key:
            config["api_key"] = api_key

        return config


class ModelConfigManager:
    """Manager for model configurations."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the model config manager.

        Args:
            config_path: Path to models.yaml. If None, uses default location.
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "models.yaml"

        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._models: Dict[str, ModelConfig] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Model config not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            self._config = yaml.safe_load(f)

        # Parse model configurations
        for model_id, model_data in self._config.get("models", {}).items():
            self._models[model_id] = ModelConfig(**model_data)

    def get_model(self, model_id: Optional[str] = None) -> ModelConfig:
        """Get model configuration by ID.

        Args:
            model_id: Model identifier. If None, uses default from env or config.

        Returns:
            ModelConfig instance

        Raises:
            ValueError: If model_id not found
        """
        if model_id is None:
            # Check environment variable first
            model_id = os.getenv("DEFAULT_MODEL")

        if model_id is None:
            # Use default from config
            model_id = self._config.get("default", "gemini-pro")

        if model_id not in self._models:
            raise ValueError(
                f"Model '{model_id}' not found. Available models: {list(self._models.keys())}"
            )

        return self._models[model_id]

    def get_agent_model(self, agent_name: str) -> ModelConfig:
        """Get model configuration for a specific agent.

        Args:
            agent_name: Name of the agent

        Returns:
            ModelConfig instance (uses agent-specific or default model)
        """
        agent_models = self._config.get("agent_models", {})
        model_id = agent_models.get(agent_name)
        return self.get_model(model_id)

    def list_models(self) -> list[str]:
        """List all available model IDs."""
        return list(self._models.keys())

    def get_llm_config(self, model_id: Optional[str] = None) -> Dict[str, Any]:
        """Get LLM configuration dict suitable for CrewAI.

        Args:
            model_id: Model identifier

        Returns:
            Dict with LLM configuration
        """
        model = self.get_model(model_id)
        return model.to_llm_config()


# Global instance (can be imported and used throughout the app)
_config_manager: Optional[ModelConfigManager] = None


def get_model_config_manager() -> ModelConfigManager:
    """Get or create the global ModelConfigManager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ModelConfigManager()
    return _config_manager


def get_model(model_id: Optional[str] = None) -> ModelConfig:
    """Convenience function to get a model config."""
    return get_model_config_manager().get_model(model_id)


def get_llm_config(model_id: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to get LLM config dict."""
    return get_model_config_manager().get_llm_config(model_id)
