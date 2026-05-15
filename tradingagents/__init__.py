"""\nTradingAgents - A multi-agent framework for AI-driven trading analysis.\n\nThis package provides a collection of specialized AI agents that collaborate\nto analyze financial markets, process news sentiment, and generate trading\nrecommendations.\n\nBased on TauricResearch/TradingAgents with additional enterprise features.\n\nPersonal fork notes:\n- Using this for learning multi-agent LLM patterns and backtesting strategies\n- See README for setup instructions with local Ollama models\n- Added __author__ to __all__ for easier introspection when debugging\n"""

__version__ = "0.1.0"
__author__ = "TradingAgents Contributors"
__license__ = "Apache-2.0"

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

__all__ = [
    "TradingAgentsGraph",
    "DEFAULT_CONFIG",
    "__version__",
    "__author__",
]
