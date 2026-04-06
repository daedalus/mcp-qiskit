"""Test configuration for pytest."""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_qiskit() -> MagicMock:
    """Mock Qiskit modules for testing without dependencies."""
    with patch("mcp_qiskit._circuit.qiskit") as mock_qiskit:
        mock_circuit = MagicMock()
        mock_qiskit.QuantumCircuit.return_value = mock_circuit
        mock_qiskit.circuit.library.HGate.return_value = MagicMock(
            name="h", num_qubits=1
        )
        yield mock_qiskit


@pytest.fixture
def sample_circuit() -> dict[str, Any]:
    """Sample circuit dictionary for testing."""
    return {
        "num_qubits": 2,
        "num_clbits": 2,
        "operations": [],
        "name": "circuit",
    }
