"""
Long-Term Memory
================
Persistent vector memory powered by ChromaDB + Sentence Transformers.
Stores successful strategies, extracted facts, and error resolutions
so the agent can learn from past experiences across sessions.
"""

import logging
import os
from datetime import datetime
from typing import Optional

import chromadb

from config.settings import settings
from memory.embeddings import get_embedding_function

logger = logging.getLogger("browser_agent.memory.long_term")


class LongTermMemory:
    """
    ChromaDB-backed long-term memory for the browser agent.

    Memories are stored as documents with metadata (type, timestamp, source).
    Retrieval uses semantic similarity search via sentence-transformer embeddings.
    """

    def __init__(
        self,
        collection_name: str = "agent_memory",
        persist_dir: Optional[str] = None,
    ):
        """
        Initialise the long-term memory store.

        Args:
            collection_name: Name of the ChromaDB collection.
            persist_dir: Directory for persistent storage.
                         Defaults to settings.chromadb_persist_dir.
        """
        self.persist_dir = persist_dir or settings.chromadb_persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)

        logger.info("Initialising ChromaDB at: %s", self.persist_dir)

        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.embedding_fn = get_embedding_function()

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )

        logger.info(
            "✅ Long-term memory ready (collection: %s, documents: %d)",
            collection_name,
            self.collection.count(),
        )

    def store_memory(
        self,
        content: str,
        memory_type: str = "general",
        source: str = "",
        metadata: Optional[dict] = None,
    ) -> str:
        """
        Store a new memory in the vector database.

        Args:
            content:     The text content to remember.
            memory_type: Category — 'strategy', 'fact', 'error_resolution', 'general'.
            source:      Where this memory came from (URL, task name, etc.).
            metadata:    Additional metadata key-value pairs.

        Returns:
            The generated document ID.
        """
        doc_id = f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        doc_metadata = {
            "type": memory_type,
            "source": source,
            "timestamp": datetime.now().isoformat(),
        }
        if metadata:
            doc_metadata.update(metadata)

        self.collection.add(
            documents=[content],
            metadatas=[doc_metadata],
            ids=[doc_id],
        )

        logger.info(
            "💾 Stored memory [%s] type=%s: %s",
            doc_id,
            memory_type,
            content[:100],
        )
        return doc_id

    def retrieve_memories(
        self,
        query: str,
        n_results: int = 5,
        memory_type: Optional[str] = None,
    ) -> list[dict]:
        """
        Retrieve relevant memories using semantic similarity search.

        Args:
            query:       The search query (embedded and compared to stored memories).
            n_results:   Maximum number of results to return.
            memory_type: Optional filter — only return memories of this type.

        Returns:
            List of dicts with keys: 'content', 'metadata', 'distance'.
        """
        where_filter = None
        if memory_type:
            where_filter = {"type": memory_type}

        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, max(self.collection.count(), 1)),
            where=where_filter,
        )

        memories = []
        if results and results["documents"]:
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                memories.append({
                    "content": doc,
                    "metadata": meta,
                    "distance": dist,
                })

        logger.info(
            "🔍 Retrieved %d memories for query: '%s'",
            len(memories),
            query[:60],
        )
        return memories

    def get_memory_context(self, query: str, n_results: int = 3) -> list[str]:
        """
        Convenience method: retrieve memories and return as a list of strings
        suitable for injecting into the agent prompt.

        Args:
            query:     The search query.
            n_results: Maximum number of results.

        Returns:
            List of memory content strings.
        """
        memories = self.retrieve_memories(query, n_results=n_results)
        return [m["content"] for m in memories]

    def clear_memories(self) -> int:
        """
        Delete all memories from the collection.

        Returns:
            Number of documents deleted.
        """
        count = self.collection.count()
        if count > 0:
            all_ids = self.collection.get()["ids"]
            self.collection.delete(ids=all_ids)
            logger.info("🗑️ Cleared %d memories", count)
        return count

    @property
    def count(self) -> int:
        """Return the number of stored memories."""
        return self.collection.count()
