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

    def test_run_circuit_no_measurement_returns_statevector(self) -> None:
        """Test that circuit without measurement returns statevector."""
        circuit = create_quantum_circuit(2, 2)
        circuit = add_gate(circuit, "h", [0])
        # No measurement added

        result = run_circuit(circuit, shots=100)
        assert result["status"] == "COMPLETED"
        assert "statevector" in result

    def test_run_circuit_with_mcx(self) -> None:
        """Test running circuit with MCX gate."""
        circuit = create_quantum_circuit(3, 2)
        circuit = add_gate(circuit, "h", [0])
        circuit = add_gate(circuit, "mcx", [0, 1, 2])
        circuit = add_measurement(circuit, [0, 1])

        result = run_circuit(circuit, "aer_simulator", shots=100)
        assert result["status"] == "COMPLETED"
        assert "counts" in result

    def test_run_circuit_qasm_simulator(self) -> None:
        """Test running circuit on QASM simulator."""
        circuit = create_quantum_circuit(2, 2)
        circuit = add_gate(circuit, "h", [0])
        circuit = add_measurement(circuit, [0, 1])

        result = run_circuit(circuit, "qasm_simulator", shots=100)
        assert result["status"] == "COMPLETED"
        assert "counts" in result

    def test_run_circuit_with_seed(self) -> None:
        """Test running circuit with seed."""
        circuit = create_quantum_circuit(2, 2)
        circuit = add_gate(circuit, "h", [0])
        circuit = add_measurement(circuit, [0, 1])

        result = run_circuit(circuit, shots=100, seed=42)
        assert result["status"] == "COMPLETED"
        assert result["seed"] == 42

    def test_run_circuit_default_backend(self) -> None:
        """Test running circuit with default backend."""
        circuit = create_quantum_circuit(2, 2)
        circuit = add_gate(circuit, "h", [0])
        circuit = add_measurement(circuit, [0, 1])

        result = run_circuit(circuit, shots=100)
        assert result["status"] == "COMPLETED"

    def test_run_circuit_returns_time(self) -> None:
        """Test that execution returns time taken."""
        circuit = create_quantum_circuit(2, 2)
        circuit = add_gate(circuit, "h", [0])
        circuit = add_measurement(circuit, [0, 1])

        result = run_circuit(circuit, shots=100)
        assert "time_taken" in result
        assert result["time_taken"] > 0

    def test_run_circuit_bell_state(self) -> None:
        """Test running Bell state circuit."""
        circuit = create_quantum_circuit(2, 2)
        circuit = add_gate(circuit, "h", [0])
        circuit = add_gate(circuit, "cx", [0, 1])
        circuit = add_measurement(circuit, [0, 1])

        result = run_circuit(circuit, shots=100)
        assert result["status"] == "COMPLETED"
        counts = result["counts"]
        # Bell state should have roughly equal |00> and |11>
        assert "00" in counts or "11" in counts


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

    def test_run_circuits_statevector(self) -> None:
        """Test running multiple circuits with statevector."""
        circuits = []
        for _ in range(2):
            c = create_quantum_circuit(2, 0)
            c = add_gate(c, "h", [0])
            circuits.append(c)

        results = run_circuits(circuits, shots=None)
        assert len(results) == 2
        for r in results:
            assert "statevector" in r

    def test_run_circuits_returns_metadata(self) -> None:
        """Test that batch execution returns metadata."""
        circuits = []
        for _ in range(2):
            c = create_quantum_circuit(2, 2)
            c = add_gate(c, "h", [0])
            c = add_measurement(c, [0, 1])
            circuits.append(c)

        results = run_circuits(circuits, shots=100)
        for r in results:
            assert "backend" in r
            assert "shots" in r


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

    def test_transpile_circuit_level_0(self) -> None:
        """Test transpiling with optimization level 0."""
        circuit = create_quantum_circuit(2, 0)
        circuit = add_gate(circuit, "h", [0])

        result = transpile_circuit(circuit, optimization_level=0)
        assert "operations" in result

    def test_transpile_circuit_level_3(self) -> None:
        """Test transpiling with optimization level 3."""
        circuit = create_quantum_circuit(2, 0)
        circuit = add_gate(circuit, "h", [0])

        result = transpile_circuit(circuit, optimization_level=3)
        assert "operations" in result

    def test_transpile_circuit_with_basis_gates(self) -> None:
        """Test transpiling with custom basis gates."""
        circuit = create_quantum_circuit(2, 0)
        circuit = add_gate(circuit, "h", [0])
        circuit = add_gate(circuit, "cx", [0, 1])

        result = transpile_circuit(circuit, basis_gates=["h", "cx", "x", "y", "z"])
        assert "operations" in result
