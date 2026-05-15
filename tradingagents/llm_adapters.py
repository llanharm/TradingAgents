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
    # Note: Google's API does not accept a max_tokens kwarg the same way;
    # use max_output_tokens instead if cfg.max_tokens is set.
    if cfg.max_tokens:
        kwargs["max_output_tokens"] = cfg.max_tokens

    logger.debug("Building ChatGoogleGenerativeAI with model=%s", cfg.model_name)
    return ChatGoogleGenerativeAI(**kwargs)


def _build_ollama_chat(cfg: "LLMConfig") -> Any:
    """Construct a LangChain ChatOllama instance for local models."""
    try:
        from langchain_ollama import ChatOllama
    except ImportError as exc:
        raise ImportError(
            "langchain-ollama is required for Ollama models. "
            "
