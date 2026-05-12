"""Configuration management for TradingAgents.

This module handles loading and validating configuration from environment
variables and config files, providing a central place for all settings.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


@dataclass
class LLMConfig:
    """Configuration for LLM providers."""

    openai_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY")
    )
    anthropic_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY")
    )
    google_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("GOOGLE_API_KEY")
    )
    default_model: str = field(
        default_factory=lambda: os.getenv("DEFAULT_LLM_MODEL", "gpt-4o-mini")
    )
    temperature: float = field(
        default_factory=lambda: float(os.getenv("LLM_TEMPERATURE", "0.1"))
    )
    max_tokens: int = field(
        default_factory=lambda: int(os.getenv("LLM_MAX_TOKENS", "4096"))
    )


@dataclass
class DataConfig:
    """Configuration for market data sources."""

    finnhub_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("FINNHUB_API_KEY")
    )
    alpha_vantage_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("ALPHA_VANTAGE_API_KEY")
    )
    polygon_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("POLYGON_API_KEY")
    )
    # Default lookback period in days for historical data
    default_lookback_days: int = field(
        default_factory=lambda: int(os.getenv("DEFAULT_LOOKBACK_DAYS", "90"))
    )


@dataclass
class AgentConfig:
    """Configuration for trading agents behavior."""

    max_debate_rounds: int = field(
        default_factory=lambda: int(os.getenv("MAX_DEBATE_ROUNDS", "3"))
    )
    max_risk_discuss_rounds: int = field(
        default_factory=lambda: int(os.getenv("MAX_RISK_DISCUSS_ROUNDS", "3"))
    )
    # Whether to use online tools (live data) or cached/offline data
    use_online_tools: bool = field(
        default_factory=lambda: os.getenv("USE_ONLINE_TOOLS", "true").lower() == "true"
    )
    # Directory to cache tool results
    cache_dir: str = field(
        default_factory=lambda: os.getenv("CACHE_DIR", ".cache/tradingagents")
    )


@dataclass
class TradingAgentsConfig:
    """Top-level configuration for the TradingAgents system."""

    llm: LLMConfig = field(default_factory=LLMConfig)
    data: DataConfig = field(default_factory=DataConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)

    # Results output directory
    results_dir: str = field(
        default_factory=lambda: os.getenv("RESULTS_DIR", "results")
    )
    # Logging level
    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO")
    )

    def validate(self) -> list[str]:
        """Validate config and return list of warnings for missing optional keys."""
        warnings: list[str] = []

        if not self.llm.openai_api_key and not self.llm.anthropic_api_key:
            warnings.append(
                "No LLM API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY."
            )
        if not self.data.finnhub_api_key:
            warnings.append(
                "FINNHUB_API_KEY not set. Some market data features will be unavailable."
            )

        return warnings


# Module-level default config instance
default_config = TradingAgentsConfig()
