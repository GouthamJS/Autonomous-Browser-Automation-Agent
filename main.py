"""
Autonomous Browser Automation Agent
====================================
Main entry point for running the agent from the command line.

Usage:
    python main.py "Search for AI news on TechCrunch and extract top 5 headlines"
    python main.py --help
    python main.py --interactive
"""

import argparse
import asyncio
import sys
import os
import time

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
from config.logging_config import setup_logging


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="🤖 Autonomous Browser Automation Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "Navigate to example.com and extract the page title"
  python main.py "Search for Python tutorials on Google and list the top 5 results"
  python main.py --interactive
  python main.py --api
        """,
    )

    parser.add_argument(
        "goal",
        nargs="?",
        default=None,
        help="The task/goal for the agent to accomplish (in natural language).",
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode (enter goals one at a time).",
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Start the FastAPI server instead of running a single task.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=None,
        help="Run browser in headless mode (no visible window).",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Run browser with visible window (for debugging).",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help=f"Maximum ReAct loop iterations (default: {settings.max_iterations}).",
    )
    parser.add_argument(
        "--no-memory",
        action="store_true",
        help="Disable long-term memory for this run.",
    )

    return parser.parse_args()


async def run_agent(goal: str, use_memory: bool = True) -> str:
    """
    Execute the browser automation agent with the given goal.

    Args:
        goal:       Natural-language task description.
        use_memory: Whether to use long-term memory.

    Returns:
        The agent's final output string.
    """
    from config.browser import get_browser
    from tools import get_all_tools, get_tool_map
    from agent.graph import create_agent_graph
    from agent.state import create_initial_state

    logger = setup_logging()

    logger.info("=" * 60)
    logger.info("🤖 AUTONOMOUS BROWSER AUTOMATION AGENT")
    logger.info("=" * 60)
    logger.info("🎯 Goal: %s", goal)
    logger.info("=" * 60)

    # ── Retrieve long-term memories ────────────────────────────────────
    memory_context = []
    if use_memory:
        try:
            from memory.long_term import LongTermMemory
            ltm = LongTermMemory()
            memory_context = ltm.get_memory_context(goal, n_results=3)
            if memory_context:
                logger.info("💾 Retrieved %d relevant memories", len(memory_context))
        except Exception as e:
            logger.warning("⚠️ Long-term memory unavailable: %s", e)

    # ── Set up tools and graph ─────────────────────────────────────────
    tools = get_all_tools()
    tool_map = get_tool_map()

    start_time = time.time()

    async with get_browser() as (browser, context, page):
        logger.info("🌐 Browser launched successfully")

        graph = create_agent_graph(tools=tools, tool_map=tool_map, page=page)

        # Create initial state
        initial_state = create_initial_state(goal)
        initial_state["memory_context"] = memory_context

        config = {
            "configurable": {"thread_id": "cli-run"},
            "recursion_limit": settings.max_iterations * 3,  # Allow room for reflection
        }

        # ── Execute the graph ──────────────────────────────────────────
        logger.info("🚀 Starting agent execution …")

        final_output = ""

        async for event in graph.astream(initial_state, config=config):
            for node_name, node_output in event.items():
                if isinstance(node_output, dict):
                    # Log node execution
                    status = node_output.get("status", "")
                    logger.info("📍 Node [%s] completed (status: %s)", node_name, status)

                    # Capture final output
                    if node_output.get("final_output"):
                        final_output = node_output["final_output"]

        elapsed = time.time() - start_time

        # ── Store result in long-term memory ───────────────────────────
        if use_memory and final_output:
            try:
                ltm = LongTermMemory()
                ltm.store_memory(
                    content=f"Goal: {goal}\nResult: {final_output[:500]}",
                    memory_type="strategy",
                    source="cli-run",
                )
                logger.info("💾 Strategy saved to long-term memory")
            except Exception as e:
                logger.warning("⚠️ Failed to store memory: %s", e)

        logger.info("=" * 60)
        logger.info("✅ AGENT EXECUTION COMPLETE")
        logger.info("⏱️  Duration: %.1f seconds", elapsed)
        logger.info("=" * 60)

        if final_output:
            print("\n" + "=" * 60)
            print("📤 FINAL OUTPUT:")
            print("=" * 60)
            print(final_output)
            print("=" * 60)
        else:
            print("\n⚠️ Agent did not produce a final output.")

        return final_output


async def interactive_mode(use_memory: bool = True):
    """Run the agent in interactive mode — accept goals one at a time."""
    logger = setup_logging()

    print("\n" + "=" * 60)
    print("🤖 AUTONOMOUS BROWSER AUTOMATION AGENT — Interactive Mode")
    print("=" * 60)
    print("Enter a goal (or 'quit' to exit):\n")

    while True:
        try:
            goal = input("🎯 Goal: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break

        if not goal:
            continue
        if goal.lower() in ("quit", "exit", "q"):
            print("👋 Goodbye!")
            break

        await run_agent(goal, use_memory=use_memory)
        print()  # Blank line between runs


def start_api_server():
    """Start the FastAPI server."""
    import uvicorn
    print("\n🚀 Starting API server …")
    uvicorn.run(
        "api.routes:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info",
    )


def main():
    """Main entry point."""
    args = parse_args()

    # Apply CLI overrides to settings
    if args.headless is not None:
        settings.browser_headless = True
    if args.no_headless:
        settings.browser_headless = False
    if args.max_iterations is not None:
        settings.max_iterations = args.max_iterations

    use_memory = not args.no_memory

    # ── Mode selection ─────────────────────────────────────────────────
    if args.api:
        start_api_server()
    elif args.interactive:
        asyncio.run(interactive_mode(use_memory=use_memory))
    elif args.goal:
        asyncio.run(run_agent(args.goal, use_memory=use_memory))
    else:
        print("🤖 Autonomous Browser Automation Agent")
        print()
        print("Usage:")
        print('  python main.py "Your goal here"')
        print("  python main.py --interactive")
        print("  python main.py --api")
        print()
        print("Run 'python main.py --help' for all options.")


if __name__ == "__main__":
    main()
