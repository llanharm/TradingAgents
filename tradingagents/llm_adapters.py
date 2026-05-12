"""LLM adapter layer for TradingAgents.

Provides a unified interface for interacting with different LLM providers
(OpenAI, Anthropic, Google, local models via Ollama) based on the LLMConfig.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from tradingagents.config import LLMConfig

logger = logging.getLogger(__name__)


def _build_openai_chat(cfg: "LLMConfig") -> Any:
    """Construct a LangChain ChatOpenAI instance from config."""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise ImportError(
            "langchain-openai is required for OpenAI models. "
            "Install it with: pip install langchain-openai"
        ) from exc

    kwargs: dict[str, Any] = {
        "model": cfg.model_name,
        "temperature": cfg.temperature,
        "max_tokens": cfg.max_tokens,
        "streaming": cfg.streaming,
    }
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url

    logger.debug("Building ChatOpenAI with model=%s", cfg.model_name)
    return ChatOpenAI(**kwargs)


def _build_anthropic_chat(cfg: "LLMConfig") -> Any:
    """Construct a LangChain ChatAnthropic instance from config."""
    try:
        from langchain_anthropic import ChatAnthropic
    except ImportError as exc:
        raise ImportError(
            "langchain-anthropic is required for Anthropic models. "
            "Install it with: pip install langchain-anthropic"
        ) from exc

    kwargs: dict[str, Any] = {
        "model": cfg.model_name,
        "temperature": cfg.temperature,
        "max_tokens": cfg.max_tokens,
        "streaming": cfg.streaming,
    }
    if cfg.api_key:
        kwargs["anthropic_api_key"] = cfg.api_key

    logger.debug("Building ChatAnthropic with model=%s", cfg.model_name)
    return ChatAnthropic(**kwargs)


def _build_google_chat(cfg: "LLMConfig") -> Any:
    """Construct a LangChain ChatGoogleGenerativeAI instance from config."""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError as exc:
        raise ImportError(
            "langchain-google-genai is required for Google models. "
            "Install it with: pip install langchain-google-genai"
        ) from exc

    kwargs: dict[str, Any] = {
        "model": cfg.model_name,
        "temperature": cfg.temperature,
        "streaming": cfg.streaming,
    }
    if cfg.api_key:
        kwargs["google_api_key"] = cfg.api_key

    logger.debug("Building ChatGoogleGenerativeAI with model=%s", cfg.model_name)
    return ChatGoogleGenerativeAI(**kwargs)


def _build_ollama_chat(cfg: "LLMConfig") -> Any:
    """Construct a LangChain ChatOllama instance for local models."""
    try:
        from langchain_ollama import ChatOllama
    except ImportError as exc:
        raise ImportError(
            "langchain-ollama is required for Ollama models. "
            "Install it with: pip install langchain-ollama"
        ) from exc

    base_url = cfg.base_url or "http://localhost:11434"
    kwargs: dict[str, Any] = {
        "model": cfg.model_name,
        "temperature": cfg.temperature,
        "base_url": base_url,
    }

    logger.debug("Building ChatOllama with model=%s base_url=%s", cfg.model_name, base_url)
    return ChatOllama(**kwargs)


_PROVIDER_BUILDERS = {
    "openai": _build_openai_chat,
    "anthropic": _build_anthropic_chat,
    "google": _build_google_chat,
    "ollama": _build_ollama_chat,
}


def create_llm(cfg: "LLMConfig") -> Any:
    """Factory function that returns an appropriate LangChain chat model.

    Args:
        cfg: An :class:`~tradingagents.config.LLMConfig` instance.

    Returns:
        A LangChain ``BaseChatModel`` compatible object.

    Raises:
        ValueError: If the provider specified in *cfg* is not supported.
        ImportError: If the required provider package is not installed.
    """
    provider = cfg.provider.lower()
    builder = _PROVIDER_BUILDERS.get(provider)
    if builder is None:
        supported = ", ".join(_PROVIDER_BUILDERS)
        raise ValueError(
            f"Unsupported LLM provider '{cfg.provider}'. "
            f"Supported providers: {supported}"
        )
    return builder(cfg)
