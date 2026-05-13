"""
Memory System Tests
===================
Tests for the long-term (ChromaDB) and short-term (MemorySaver) memory systems.
"""

import os
import shutil
import pytest

# Use a temporary directory for test ChromaDB data
TEST_PERSIST_DIR = "./data/test_chromadb"


# ═══════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════

@pytest.fixture(autouse=True)
def cleanup_test_db():
    """Clean up the test database before and after each test."""
    if os.path.exists(TEST_PERSIST_DIR):
        shutil.rmtree(TEST_PERSIST_DIR)
    yield
    if os.path.exists(TEST_PERSIST_DIR):
        shutil.rmtree(TEST_PERSIST_DIR)


@pytest.fixture
def ltm():
    """Create a LongTermMemory instance with test directory."""
    from memory.long_term import LongTermMemory
    return LongTermMemory(
        collection_name="test_memory",
        persist_dir=TEST_PERSIST_DIR,
    )


# ═══════════════════════════════════════════════════════════════════════
# Long-Term Memory Tests
# ═══════════════════════════════════════════════════════════════════════

class TestLongTermMemory:
    """Tests for ChromaDB-backed long-term memory."""

    def test_initialization(self, ltm):
        """Test that memory initialises correctly."""
        assert ltm.count == 0

    def test_store_memory(self, ltm):
        """Test storing a memory."""
        doc_id = ltm.store_memory(
            content="Navigate to Google by going to google.com",
            memory_type="strategy",
            source="test",
        )
        assert doc_id.startswith("mem_")
        assert ltm.count == 1

    def test_store_multiple_memories(self, ltm):
        """Test storing multiple memories."""
        ltm.store_memory("First memory", memory_type="fact")
        ltm.store_memory("Second memory", memory_type="strategy")
        ltm.store_memory("Third memory", memory_type="error_resolution")
        assert ltm.count == 3

    def test_retrieve_memories(self, ltm):
        """Test retrieving memories by similarity."""
        ltm.store_memory(
            "To search on Google, navigate to google.com and type in the search box",
            memory_type="strategy",
        )
        ltm.store_memory(
            "Amazon product pages have prices in the #priceblock element",
            memory_type="fact",
        )

        results = ltm.retrieve_memories("How to search Google", n_results=2)
        assert len(results) > 0
        assert "content" in results[0]
        assert "metadata" in results[0]
        assert "distance" in results[0]

    def test_get_memory_context(self, ltm):
        """Test the convenience method for prompt injection."""
        ltm.store_memory("Test memory content", memory_type="general")

        context = ltm.get_memory_context("test", n_results=3)
        assert isinstance(context, list)
        assert len(context) >= 1
        assert isinstance(context[0], str)

    def test_clear_memories(self, ltm):
        """Test clearing all memories."""
        ltm.store_memory("Memory 1")
        ltm.store_memory("Memory 2")
        assert ltm.count == 2

        deleted = ltm.clear_memories()
        assert deleted == 2
        assert ltm.count == 0

    def test_clear_empty_collection(self, ltm):
        """Test clearing an already empty collection."""
        deleted = ltm.clear_memories()
        assert deleted == 0

    def test_store_with_metadata(self, ltm):
        """Test storing memory with custom metadata."""
        doc_id = ltm.store_memory(
            content="Custom metadata test",
            memory_type="strategy",
            source="unit_test",
            metadata={"task_id": "test_123", "confidence": "high"},
        )
        assert doc_id.startswith("mem_")
        assert ltm.count == 1

    def test_retrieve_empty_collection(self, ltm):
        """Test retrieving from an empty collection."""
        results = ltm.retrieve_memories("anything")
        assert isinstance(results, list)
        assert len(results) == 0


# ═══════════════════════════════════════════════════════════════════════
# Short-Term Memory Tests
# ═══════════════════════════════════════════════════════════════════════

class TestShortTermMemory:
    """Tests for the LangGraph MemorySaver checkpointer."""

    def test_get_checkpointer(self):
        """Test that the checkpointer is created."""
        from memory.short_term import get_checkpointer
        checkpointer = get_checkpointer()
        assert checkpointer is not None

    def test_checkpointer_singleton(self):
        """Test that get_checkpointer returns the same instance."""
        from memory.short_term import get_checkpointer
        cp1 = get_checkpointer()
        cp2 = get_checkpointer()
        assert cp1 is cp2


# ═══════════════════════════════════════════════════════════════════════
# Agent State Tests
# ═══════════════════════════════════════════════════════════════════════

class TestAgentState:
    """Tests for the agent state schema."""

    def test_create_initial_state(self):
        """Test creating an initial state."""
        from agent.state import create_initial_state
        state = create_initial_state("Test goal")

        assert state["goal"] == "Test goal"
        assert state["status"] == "running"
        assert state["iteration_count"] == 0
        assert state["retry_count"] == 0
        assert state["messages"] == []
        assert state["plan"] == []
        assert state["screenshots"] == []
        assert state["error_log"] == []
        assert state["final_output"] == ""

    def test_create_initial_state_different_goals(self):
        """Test that different goals produce different states."""
        from agent.state import create_initial_state
        state1 = create_initial_state("Goal A")
        state2 = create_initial_state("Goal B")

        assert state1["goal"] != state2["goal"]
