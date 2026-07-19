import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from dataclasses import dataclass, field
from typing import Any, Dict

# Import the core architectural elements we want to test
from app_pipeline import NextGenComputeCore

# Tell pytest-asyncio to allow module-scoped event loops
pytestmark = pytest.mark.asyncio

# =====================================================================
# A. FIXTURES (Reusable test setups)
# =====================================================================
@pytest.fixture
def target_node():
    """Initializes a clean, memory-dense production node for each test."""
    return NextGenComputeCore(node_id="Test-Core-01", hardware_cost=5000.00, region="us-east-1")

# =====================================================================
# B. TEST CASES
# =====================================================================
async def test_successful_packet_ingestion(target_node):
    """Asserts that a valid packet triggers telemetry and registers a log."""
    # Setup: Create an explicit non-blocking task call
    result = await target_node.ingest_packet_async("ValidSuperLongPacketData")
    
    # Assertions
    assert result["status"] == "SUCCESS"
    assert result["region"] == "us-east-1"
    assert "PROCESSED: ValidSuperLongPacketData" in target_node.packet_logs


async def test_checksum_failure_handling(target_node):
    """Verifies that short packets fail validation and update the rejected logs."""
    result = await target_node.ingest_packet_async("Bad")  # Length <= 5
    
    assert result["status"] == "MALFORMED_PACKET"
    assert "REJECTED: Bad" in target_node.packet_logs


async def test_asynchronous_mixin_mocking(target_node):
    """
    Demonstrates how to safely mock an inherited async mixin method.
    We must use an explicit AsyncMock to isolate network I/O during tests.
    """
    # Override the mixed-in method with an async mock recorder
    mock_streamer = AsyncMock()
    target_node.stream_telemetry_async = mock_streamer

    # Trigger action
    await target_node.ingest_packet_async("TriggerTelemetryPacket")

    # Assert that the mixed-in dependency was executed exactly once with expected 
    # values
    mock_streamer.assert_awaited_once_with(
        node_id="Test-Core-01", 
        metric="PACKET_INGEST_SUCCESS"
    )


def test_slotted_memory_protection_remains_active(target_node):
    """Guarantees that mixing in parent classes didn't corrupt the slotted memory 
    boundaries."""
    # 1. Assert __dict__ does not exist anywhere on the object graph
    with pytest.raises(AttributeError):
        _ = target_node.__dict__

    # 2. Assert that arbitrary attribute injections are strictly blocked at 
    #    runtime
    with pytest.raises(AttributeError, match="has no attribute"):
        target_node.illegal_runtime_hack = True
