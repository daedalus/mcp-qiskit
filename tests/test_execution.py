"""Tests for execution module."""

import pytest

from mcp_qiskit._circuit import add_gate, add_measurement, create_quantum_circuit
from mcp_qiskit._execution import run_circuit, run_circuits, transpile_circuit


class TestRunCircuit:
    """Tests for run_circuit function."""

    def test_run_circuit_aer(self) -> None:
        """Test running circuit on Aer simulator."""
        circuit = create_quantum_circuit(2, 2)
        circuit = add_gate(circuit, "h", [0])
        circuit = add_gate(circuit, "cx", [0, 1])
        circuit = add_measurement(circuit, [0, 1])

        result = run_circuit(circuit, "aer_simulator", shots=1024)
        assert result["status"] == "COMPLETED"
        assert result["shots"] == 1024
        assert "counts" in result

    def test_run_circuit_statevector(self) -> None:
        """Test running circuit without shots (statevector)."""
        circuit = create_quantum_circuit(2, 0)
        circuit = add_gate(circuit, "h", [0])

        result = run_circuit(circuit, shots=None)
        assert result["status"] == "COMPLETED"
        assert "statevector" in result


class TestRunCircuits:
    """Tests for run_circuits function."""

    def test_run_circuits_empty(self) -> None:
        """Test running empty circuit list."""
        with pytest.raises(ValueError, match="At least one circuit"):
            run_circuits([], "aer_simulator")

    def test_run_circuits_too_many(self) -> None:
        """Test running too many circuits."""
        circuits = [{"num_qubits": 2, "num_clbits": 2, "operations": []}] * 101
        with pytest.raises(ValueError, match="Maximum 100 circuits"):
            run_circuits(circuits, "aer_simulator")

    def test_run_multiple_circuits(self) -> None:
        """Test running multiple circuits."""
        circuits = []
        for _ in range(3):
            c = create_quantum_circuit(2, 2)
            c = add_gate(c, "h", [0])
            c = add_measurement(c, [0, 1])
            circuits.append(c)

        results = run_circuits(circuits, "aer_simulator", shots=100)
        assert len(results) == 3
        for r in results:
            assert r["status"] == "COMPLETED"
            assert "counts" in r


class TestTranspileCircuit:
    """Tests for transpile_circuit function."""

    def test_transpile_circuit(self) -> None:
        """Test transpiling a circuit."""
        circuit = create_quantum_circuit(2, 0)
        circuit = add_gate(circuit, "h", [0])

        result = transpile_circuit(circuit)
        assert "num_qubits" in result
        assert "operations" in result

    def test_transpile_circuit_optimization(self) -> None:
        """Test transpiling with different optimization levels."""
        circuit = create_quantum_circuit(2, 0)
        circuit = add_gate(circuit, "h", [0])
        circuit = add_gate(circuit, "h", [1])

        result = transpile_circuit(circuit, optimization_level=2)
        assert "operations" in result
