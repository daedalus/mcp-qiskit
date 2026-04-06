"""Tests for circuit module."""

import pytest

from mcp_qiskit._circuit import (
    add_gate,
    add_measurement,
    create_quantum_circuit,
    draw_circuit,
    get_circuit_depth,
    get_gate_definition,
    list_available_gates,
)


class TestCreateQuantumCircuit:
    """Tests for create_quantum_circuit function."""

    def test_create_circuit_basic(self) -> None:
        """Test creating a basic quantum circuit."""
        result = create_quantum_circuit(2, 2)
        assert result["num_qubits"] == 2
        assert result["num_clbits"] == 2
        assert result["operations"] == []
        assert result["name"] == "circuit"

    def test_create_circuit_no_classical(self) -> None:
        """Test creating circuit with no classical bits."""
        result = create_quantum_circuit(3, 0)
        assert result["num_qubits"] == 3
        assert result["num_clbits"] == 0

    def test_create_circuit_invalid_qubits(self) -> None:
        """Test creating circuit with invalid qubit count."""
        with pytest.raises(ValueError, match="num_qubits must be at least 1"):
            create_quantum_circuit(0, 2)

    def test_create_circuit_negative_classical(self) -> None:
        """Test creating circuit with negative classical bits."""
        with pytest.raises(ValueError, match="num_classical_bits must be non-negative"):
            create_quantum_circuit(2, -1)


class TestAddGate:
    """Tests for add_gate function."""

    def test_add_h_gate(self) -> None:
        """Test adding H gate to circuit."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "h", [0])
        assert "operations" in result

    def test_add_cx_gate(self) -> None:
        """Test adding CX (CNOT) gate to circuit."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "cx", [0, 1])
        assert "operations" in result

    def test_add_gate_invalid_qubit(self) -> None:
        """Test adding gate with invalid qubit index."""
        circuit = create_quantum_circuit(2, 0)
        with pytest.raises(IndexError, match="out of range"):
            add_gate(circuit, "h", [5])

    def test_add_gate_unknown(self) -> None:
        """Test adding unknown gate."""
        circuit = create_quantum_circuit(2, 0)
        with pytest.raises(ValueError, match="Unknown gate"):
            add_gate(circuit, "nonexistent_gate", [0])

    def test_add_measurement_gate(self) -> None:
        """Test adding measurement via add_gate."""
        circuit = create_quantum_circuit(2, 2)
        result = add_gate(circuit, "measure", [0], [0])
        assert "operations" in result


class TestAddMeasurement:
    """Tests for add_measurement function."""

    def test_add_measurement_default_clbits(self) -> None:
        """Test measurement with default classical bits."""
        circuit = create_quantum_circuit(2, 2)
        result = add_measurement(circuit, [0, 1])
        assert "operations" in result


class TestGetCircuitDepth:
    """Tests for get_circuit_depth function."""

    def test_get_depth(self) -> None:
        """Test getting circuit depth."""
        circuit = create_quantum_circuit(2, 0)
        circuit = add_gate(circuit, "h", [0])
        circuit = add_gate(circuit, "cx", [0, 1])
        result = get_circuit_depth(circuit)
        assert result >= 2


class TestListAvailableGates:
    """Tests for list_available_gates function."""

    def test_list_gates(self) -> None:
        """Test listing available gates."""
        gates = list_available_gates()
        assert "h" in gates
        assert "x" in gates
        assert "cx" in gates


class TestGetGateDefinition:
    """Tests for get_gate_definition function."""

    def test_get_h_gate_definition(self) -> None:
        """Test getting H gate definition."""
        result = get_gate_definition("h")
        assert result["name"] == "h"
        assert result["num_qubits"] == 1

    def test_get_unknown_gate(self) -> None:
        """Test getting unknown gate definition."""
        with pytest.raises(ValueError, match="Unknown gate"):
            get_gate_definition("nonexistent")


class TestDrawCircuit:
    """Tests for draw_circuit function."""

    def test_draw_ascii(self) -> None:
        """Test drawing circuit in ASCII format."""
        circuit = create_quantum_circuit(2, 2)
        circuit = add_gate(circuit, "h", [0])
        circuit = add_gate(circuit, "cx", [0, 1])
        circuit = add_measurement(circuit, [0, 1])
        result = draw_circuit(circuit, "ascii")
        assert isinstance(result, str)
        assert "─" in result or "|" in result

    def test_draw_invalid_format(self) -> None:
        """Test drawing with invalid format."""
        circuit = create_quantum_circuit(2, 2)
        with pytest.raises(ValueError, match="Unknown output format"):
            draw_circuit(circuit, "invalid")
