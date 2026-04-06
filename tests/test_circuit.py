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

    def test_add_x_gate(self) -> None:
        """Test adding X gate to circuit."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "x", [0])
        assert len(result["operations"]) == 1

    def test_add_y_gate(self) -> None:
        """Test adding Y gate to circuit."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "y", [0])
        assert len(result["operations"]) == 1

    def test_add_z_gate(self) -> None:
        """Test adding Z gate to circuit."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "z", [0])
        assert len(result["operations"]) == 1

    def test_add_s_gate(self) -> None:
        """Test adding S gate to circuit."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "s", [0])
        assert len(result["operations"]) == 1

    def test_add_t_gate(self) -> None:
        """Test adding T gate to circuit."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "t", [0])
        assert len(result["operations"]) == 1

    def test_add_rx_gate(self) -> None:
        """Test adding RX (parameterized) gate to circuit."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "rx", [0], [0.5])
        assert len(result["operations"]) == 1

    def test_add_ry_gate(self) -> None:
        """Test adding RY (parameterized) gate to circuit."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "ry", [0], [0.5])
        assert len(result["operations"]) == 1

    def test_add_rz_gate(self) -> None:
        """Test adding RZ (parameterized) gate to circuit."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "rz", [0], [0.5])
        assert len(result["operations"]) == 1

    def test_add_u1_gate(self) -> None:
        """Test adding U1 (parameterized) gate to circuit."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "u1", [0], [0.5])
        assert len(result["operations"]) == 1

    def test_add_u3_gate(self) -> None:
        """Test adding U3 (parameterized) gate to circuit."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "u3", [0], [0.5, 0.3, 0.1])
        assert len(result["operations"]) == 1

    def test_add_barrier_gate(self) -> None:
        """Test adding barrier to circuit."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "barrier", [0, 1])
        assert len(result["operations"]) == 1

    def test_add_reset_gate(self) -> None:
        """Test adding reset to circuit."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "reset", [0])
        assert len(result["operations"]) == 1

    def test_add_i_gate(self) -> None:
        """Test adding Identity gate to circuit."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "i", [0])
        assert len(result["operations"]) == 1

    def test_add_gate_invalid_qubit(self) -> None:
        """Test adding gate with invalid qubit index."""
        circuit = create_quantum_circuit(2, 0)
        with pytest.raises(IndexError, match="out of range"):
            add_gate(circuit, "h", [5])

    def test_add_gate_empty_qubits(self) -> None:
        """Test adding gate with empty qubit list."""
        circuit = create_quantum_circuit(2, 0)
        with pytest.raises(ValueError, match="At least one qubit"):
            add_gate(circuit, "h", [])

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

    def test_add_measurement_explicit_clbits(self) -> None:
        """Test measurement with explicit classical bits."""
        circuit = create_quantum_circuit(2, 2)
        result = add_measurement(circuit, [0, 1], [1, 0])
        assert "operations" in result

    def test_add_measurement_invalid_qubit(self) -> None:
        """Test measurement with invalid qubit index."""
        circuit = create_quantum_circuit(2, 2)
        with pytest.raises(IndexError, match="out of range"):
            add_measurement(circuit, [5])

    def test_add_measurement_invalid_clbit(self) -> None:
        """Test measurement with invalid classical bit index."""
        circuit = create_quantum_circuit(2, 2)
        with pytest.raises(IndexError, match="out of range"):
            add_measurement(circuit, [0], [10])

    def test_add_measurement_empty_qubits(self) -> None:
        """Test measurement with empty qubit list."""
        circuit = create_quantum_circuit(2, 2)
        with pytest.raises(ValueError, match="At least one qubit"):
            add_measurement(circuit, [])


class TestGetCircuitDepth:
    """Tests for get_circuit_depth function."""

    def test_get_depth(self) -> None:
        """Test getting circuit depth."""
        circuit = create_quantum_circuit(2, 0)
        circuit = add_gate(circuit, "h", [0])
        circuit = add_gate(circuit, "cx", [0, 1])
        result = get_circuit_depth(circuit)
        assert result >= 2

    def test_get_depth_empty(self) -> None:
        """Test getting depth of empty circuit."""
        circuit = create_quantum_circuit(2, 0)
        result = get_circuit_depth(circuit)
        assert result == 0


class TestListAvailableGates:
    """Tests for list_available_gates function."""

    def test_list_gates(self) -> None:
        """Test listing available gates."""
        gates = list_available_gates()
        assert "h" in gates
        assert "x" in gates
        assert "cx" in gates

    def test_list_gates_contains_parametrized(self) -> None:
        """Test that parametrized gates are listed."""
        gates = list_available_gates()
        assert "rx" in gates
        assert "ry" in gates
        assert "rz" in gates


class TestGetGateDefinition:
    """Tests for get_gate_definition function."""

    def test_get_h_gate_definition(self) -> None:
        """Test getting H gate definition."""
        result = get_gate_definition("h")
        assert result["name"] == "h"
        assert result["num_qubits"] == 1

    def test_get_x_gate_definition(self) -> None:
        """Test getting X gate definition."""
        result = get_gate_definition("x")
        assert result["name"] == "x"
        assert result["num_qubits"] == 1

    def test_get_cx_gate_definition(self) -> None:
        """Test getting CX gate definition."""
        result = get_gate_definition("cx")
        assert result["num_qubits"] == 2

    def test_get_rx_gate_definition(self) -> None:
        """Test getting RX gate definition."""
        result = get_gate_definition("rx")
        assert result["num_qubits"] == 1
        assert result["num_parameters"] == 1

    def test_get_unknown_gate(self) -> None:
        """Test getting unknown gate definition."""
        with pytest.raises(ValueError, match="Unknown gate"):
            get_gate_definition("nonexistent")

    def test_get_gate_with_alias(self) -> None:
        """Test getting gate with alias (toffoli = ccx)."""
        result = get_gate_definition("ccx")
        assert result["num_qubits"] == 3


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

    def test_draw_text(self) -> None:
        """Test drawing circuit in text format."""
        circuit = create_quantum_circuit(2, 2)
        circuit = add_gate(circuit, "h", [0])
        result = draw_circuit(circuit, "text")
        assert isinstance(result, str)

    def test_draw_mpl(self) -> None:
        """Test drawing circuit in matplotlib format."""
        try:
            import pylatexenc  # noqa: F401
        except ImportError:
            pytest.skip("pylatexenc not installed")

        circuit = create_quantum_circuit(2, 0)
        circuit = add_gate(circuit, "h", [0])
        result = draw_circuit(circuit, "mpl")
        assert isinstance(result, str)
        assert result.startswith("iVBOR")

    def test_draw_latex(self) -> None:
        """Test drawing circuit in LaTeX format."""
        try:
            import pylatexenc  # noqa: F401
            import subprocess

            subprocess.run(["pdftocairo", "-v"], capture_output=True, check=True)
        except (ImportError, FileNotFoundError):
            pytest.skip("pylatexenc or pdftocairo not installed")

        circuit = create_quantum_circuit(2, 0)
        circuit = add_gate(circuit, "h", [0])
        result = draw_circuit(circuit, "latex")
        assert isinstance(result, str)

    def test_draw_invalid_format(self) -> None:
        """Test drawing with invalid format."""
        circuit = create_quantum_circuit(2, 2)
        with pytest.raises(ValueError, match="Unknown output format"):
            draw_circuit(circuit, "invalid")
