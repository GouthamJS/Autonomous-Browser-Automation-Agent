"""
API Routes
==========
FastAPI application with endpoints for running the browser automation agent,
checking run status, and health checks.
"""

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Dict

from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import (
    AgentRunRequest,
    AgentRunResponse,
    AgentRunResult,
    AgentStatus,
    HealthResponse,
)
from api.middleware import verify_api_key, CORS_ORIGINS
from config.settings import settings
from config.logging_config import setup_logging

logger = setup_logging()

# ── FastAPI App ────────────────────────────────────────────────────────
app = FastAPI(
    title="Autonomous Browser Automation Agent",
    description=(
        "An AI-powered agent that autonomously navigates websites, "
        "interacts with web elements, and extracts information using "
        "LLM reasoning and planning."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for run results (swap for Redis/DB in production)
_runs: Dict[str, AgentRunResult] = {}


# ═══════════════════════════════════════════════════════════════════════
# Background task: execute the agent
# ═══════════════════════════════════════════════════════════════════════

async def _execute_agent_run(run_id: str, request: AgentRunRequest):
    """Background task that executes the agent and stores results."""
    from config.browser import get_browser
    from tools import get_all_tools, get_tool_map
    from agent.graph import create_agent_graph
    from agent.state import create_initial_state
    from memory.long_term import LongTermMemory

    start_time = datetime.now()
    _runs[run_id].status = AgentStatus.RUNNING

    try:
        # Initialize memory
        memory_context = []
        if request.use_memory:
            try:
                ltm = LongTermMemory()
                memory_context = ltm.get_memory_context(request.goal, n_results=3)
            except Exception as e:
                logger.warning("Memory retrieval failed: %s", e)

        # Build tools and graph
        tools = get_all_tools()
        tool_map = get_tool_map()

        async with get_browser() as (browser, context, page):
            graph = create_agent_graph(tools=tools, tool_map=tool_map, page=page)

            # Create initial state
            initial_state = create_initial_state(request.goal)
            initial_state["memory_context"] = memory_context

            # Override settings if provided
            config = {
                "configurable": {"thread_id": run_id},
                "recursion_limit": request.max_iterations or settings.max_iterations,
            }

            # Run the graph
            final_state = None
            async for event in graph.astream(initial_state, config=config):
                # Track the latest state
                for node_name, node_output in event.items():
                    if isinstance(node_output, dict):
                        if node_output.get("final_output"):
                            final_state = node_output

            # Store results
            end_time = datetime.now()
            _runs[run_id].status = AgentStatus.SUCCESS
            _runs[run_id].final_output = (
                final_state.get("final_output", "Task completed.") if final_state
                else "Task completed."
            )
            _runs[run_id].completed_at = end_time
            _runs[run_id].duration_seconds = (end_time - start_time).total_seconds()

            # Store successful strategy in memory
            if request.use_memory:
                try:
                    ltm = LongTermMemory()
                    ltm.store_memory(
                        content=f"Goal: {request.goal}\nResult: {_runs[run_id].final_output[:500]}",
                        memory_type="strategy",
                        source=run_id,
                    )
                except Exception as e:
                    logger.warning("Memory storage failed: %s", e)

    except Exception as e:
        logger.error("❌ Agent run %s failed: %s", run_id, str(e))
        _runs[run_id].status = AgentStatus.FAILED
        _runs[run_id].errors = [str(e)]
        _runs[run_id].completed_at = datetime.now()
        _runs[run_id].duration_seconds = (datetime.now() - start_time).total_seconds()


# ═══════════════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════════════

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check if the API is running and healthy."""
    return HealthResponse()


@app.post(
    "/agent/run",
    response_model=AgentRunResponse,
    tags=["Agent"],
    dependencies=[Depends(verify_api_key)],
)
async def start_agent_run(
    request: AgentRunRequest,
    background_tasks: BackgroundTasks,
):
    """
    Start a new agent run with the given goal.

    The agent will execute in the background. Use the run_id
    to check the status via GET /agent/status/{run_id}.
    """
    run_id = str(uuid.uuid4())

    # Create the run record
    _runs[run_id] = AgentRunResult(
        run_id=run_id,
        status=AgentStatus.QUEUED,
        goal=request.goal,
    )

    # Launch the agent in the background
    background_tasks.add_task(_execute_agent_run, run_id, request)

    logger.info("🚀 Agent run queued: %s — goal: %s", run_id, request.goal[:80])

    return AgentRunResponse(
        run_id=run_id,
        status=AgentStatus.QUEUED,
        goal=request.goal,
        message="Agent run queued. Check status at /agent/status/{run_id}.",
    )


@app.get(
    "/agent/status/{run_id}",
    response_model=AgentRunResult,
    tags=["Agent"],
    dependencies=[Depends(verify_api_key)],
)
async def get_agent_status(run_id: str):
    """Get the status and result of an agent run."""
    if run_id not in _runs:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found.")
    return _runs[run_id]


@app.get("/agent/runs", tags=["Agent"], dependencies=[Depends(verify_api_key)])
async def list_runs():
    """List all agent runs (most recent first)."""
    runs = sorted(
        _runs.values(),
        key=lambda r: r.created_at,
        reverse=True,
    )
    return {"runs": [r.model_dump() for r in runs[:50]]}
