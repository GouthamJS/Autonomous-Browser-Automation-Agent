"""
Embedding Configuration
=======================
Initialises the sentence-transformer embedding model used by ChromaDB
for semantic memory retrieval.  Uses a lightweight model (all-MiniLM-L6-v2)
that runs entirely on CPU.
"""

import logging
from functools import lru_cache

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from config.settings import settings

logger = logging.getLogger("browser_agent.memory.embeddings")


@lru_cache(maxsize=1)
def get_embedding_function() -> SentenceTransformerEmbeddingFunction:
    """
    Return a cached embedding function instance.

    Uses the model specified in settings.embedding_model
    (default: all-MiniLM-L6-v2, ~80 MB, 384-dim vectors).

    Returns:
        SentenceTransformerEmbeddingFunction ready for ChromaDB.
    """
    logger.info(
        "Loading embedding model: %s (this may take a moment on first run)",
        settings.embedding_model,
    )
    ef = SentenceTransformerEmbeddingFunction(
        model_name=settings.embedding_model,
    )
    logger.info("✅ Embedding model loaded")
    return ef
