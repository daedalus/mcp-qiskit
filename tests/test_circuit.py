"""Tests for circuit module."""

import pytest

from mcp_qiskit._circuit import (
    add_gate,
    add_gates,
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

    def test_add_gate_none_circuit_creates_new(self) -> None:
        """Test that passing None creates a new circuit."""
        result = add_gate(None, "h", [0])
        assert result["num_qubits"] == 8
        assert result["num_clbits"] == 8
        assert len(result["operations"]) == 1
        assert result["operations"][0]["name"] == "h"

    def test_add_gate_none_then_append(self) -> None:
        """Test state maintenance when passing None then circuit."""
        circuit = add_gate(None, "h", [0])
        assert len(circuit["operations"]) == 1
        circuit = add_gate(circuit, "x", [1])
        assert len(circuit["operations"]) == 2
        assert circuit["operations"][0]["name"] == "h"
        assert circuit["operations"][1]["name"] == "x"

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


class TestAddMCXGate:
    """Tests for MCX (multi-controlled X) gate."""

    def test_add_mcx_2_controls(self) -> None:
        """Test adding MCX with 2 control qubits."""
        circuit = create_quantum_circuit(3, 0)
        result = add_gate(circuit, "mcx", [0, 1, 2])
        assert len(result["operations"]) == 1

    def test_add_mcx_3_controls(self) -> None:
        """Test adding MCX with 3 control qubits."""
        circuit = create_quantum_circuit(5, 0)
        result = add_gate(circuit, "mcx", [0, 1, 2, 3, 4])
        assert len(result["operations"]) == 1

    def test_add_mct_alias(self) -> None:
        """Test MCT alias for MCX."""
        circuit = create_quantum_circuit(3, 0)
        result = add_gate(circuit, "mct", [0, 1, 2])
        assert len(result["operations"]) == 1

    def test_add_mcx_single_qubit_fails(self) -> None:
        """Test MCX fails with only 1 qubit."""
        circuit = create_quantum_circuit(2, 0)
        with pytest.raises(ValueError, match="MCX requires at least 2"):
            add_gate(circuit, "mcx", [0])


class TestAddToffoliGates:
    """Tests for Toffoli and related gates."""

    def test_add_ccx(self) -> None:
        """Test adding CCX (Toffoli) gate."""
        circuit = create_quantum_circuit(3, 0)
        result = add_gate(circuit, "ccx", [0, 1, 2])
        assert len(result["operations"]) == 1

    def test_add_toffoli(self) -> None:
        """Test adding toffoli gate (alias for ccx)."""
        circuit = create_quantum_circuit(3, 0)
        result = add_gate(circuit, "toffoli", [0, 1, 2])
        assert len(result["operations"]) == 1

    def test_add_c3x(self) -> None:
        """Test adding C3X gate."""
        circuit = create_quantum_circuit(4, 0)
        result = add_gate(circuit, "c3x", [0, 1, 2, 3])
        assert len(result["operations"]) == 1


class TestAddSpecializedGates:
    """Tests for specialized gates (rxx, ch, cu, etc.)."""

    def test_add_rxx(self) -> None:
        """Test adding RXX gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "rxx", [0, 1], [0.5])
        assert len(result["operations"]) == 1

    def test_add_ryy(self) -> None:
        """Test adding RYY gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "ryy", [0, 1], [0.5])
        assert len(result["operations"]) == 1

    def test_add_rzz(self) -> None:
        """Test adding RZZ gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "rzz", [0, 1], [0.5])
        assert len(result["operations"]) == 1

    def test_add_ch(self) -> None:
        """Test adding CH (controlled-Hadamard) gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "ch", [0, 1])
        assert len(result["operations"]) == 1

    def test_add_cswap(self) -> None:
        """Test adding CSWAP gate."""
        circuit = create_quantum_circuit(3, 0)
        result = add_gate(circuit, "cswap", [0, 1, 2])
        assert len(result["operations"]) == 1

    def test_add_swap(self) -> None:
        """Test adding SWAP gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "swap", [0, 1])
        assert len(result["operations"]) == 1

    def test_add_sdg(self) -> None:
        """Test adding SDG gate."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "sdg", [0])
        assert len(result["operations"]) == 1

    def test_add_tdg(self) -> None:
        """Test adding TDG gate."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "tdg", [0])
        assert len(result["operations"]) == 1

    def test_add_cy(self) -> None:
        """Test adding CY gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "cy", [0, 1])
        assert len(result["operations"]) == 1

    def test_add_cz(self) -> None:
        """Test adding CZ gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "cz", [0, 1])
        assert len(result["operations"]) == 1

    def test_add_cu(self) -> None:
        """Test adding CU gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "cu", [0, 1], [0.1, 0.2, 0.3, 0.4])
        assert len(result["operations"]) == 1

    def test_add_cu1(self) -> None:
        """Test adding CU1 gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "cu1", [0, 1], [0.5])
        assert len(result["operations"]) == 1

    def test_add_cu3(self) -> None:
        """Test adding CU3 gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "cu3", [0, 1], [0.1, 0.2, 0.3])
        assert len(result["operations"]) == 1

    def test_add_c3sx(self) -> None:
        """Test adding C3SX gate."""
        circuit = create_quantum_circuit(4, 0)
        result = add_gate(circuit, "c3sx", [0, 1, 2, 3])
        assert len(result["operations"]) == 1

    def test_add_rzx(self) -> None:
        """Test adding RZX gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "rzx", [0, 1], [0.5])
        assert len(result["operations"]) == 1

    def test_add_dcx(self) -> None:
        """Test adding DCX gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "dcx", [0, 1])
        assert len(result["operations"]) == 1

    def test_add_ecr(self) -> None:
        """Test adding ECR gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "ecr", [0, 1])
        assert len(result["operations"]) == 1

    def test_add_id(self) -> None:
        """Test adding ID gate."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "id", [0])
        assert len(result["operations"]) == 1

    def test_add_u2(self) -> None:
        """Test adding U2 gate."""
        circuit = create_quantum_circuit(1, 0)
        result = add_gate(circuit, "u2", [0], [0.1, 0.2])
        assert len(result["operations"]) == 1

    def test_add_crz(self) -> None:
        """Test adding CRZ gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "crz", [0, 1], [0.5])
        assert len(result["operations"]) == 1

    def test_add_cry(self) -> None:
        """Test adding CRY gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "cry", [0, 1], [0.5])
        assert len(result["operations"]) == 1

    def test_add_crx(self) -> None:
        """Test adding CRX gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "crx", [0, 1], [0.5])
        assert len(result["operations"]) == 1

    def test_add_csx(self) -> None:
        """Test adding CSX gate."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gate(circuit, "csx", [0, 1])
        assert len(result["operations"]) == 1

    def test_add_c4x(self) -> None:
        """Test adding C4X gate."""
        circuit = create_quantum_circuit(5, 0)
        result = add_gate(circuit, "c4x", [0, 1, 2, 3, 4])
        assert len(result["operations"]) == 1

    def test_add_rccx(self) -> None:
        """Test adding RCCX (relative Clifford) gate."""
        circuit = create_quantum_circuit(3, 0)
        result = add_gate(circuit, "rccx", [0, 1, 2])
        assert len(result["operations"]) == 1


class TestListAvailableGatesNew:
    """Tests for new gates in list_available_gates."""

    def test_list_mcx_gates(self) -> None:
        """Test MCX gates are listed."""
        gates = list_available_gates()
        assert "mcx" in gates
        assert "mct" in gates
        assert "mcp" in gates

    def test_list_toffoli_gates(self) -> None:
        """Test Toffoli gates are listed."""
        gates = list_available_gates()
        assert "ccx" in gates
        assert "toffoli" in gates

    def test_list_c3x_gates(self) -> None:
        """Test C3X gates are listed."""
        gates = list_available_gates()
        assert "c3x" in gates
        assert "c3sx" in gates
        assert "c4x" in gates


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

    def test_add_measurement_none_circuit_creates_new(self) -> None:
        """Test that passing None creates a new circuit."""
        result = add_measurement(None, [0])
        assert result["num_qubits"] == 8
        assert result["num_clbits"] == 8
        assert len(result["operations"]) == 1

    def test_add_measurement_none_then_append(self) -> None:
        """Test state maintenance with measurement after gate."""
        circuit = add_gate(None, "h", [0])
        assert len(circuit["operations"]) == 1
        circuit = add_measurement(circuit, [0])
        assert len(circuit["operations"]) == 2

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
            import subprocess

            import pylatexenc  # noqa: F401

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


class TestAddGates:
    """Tests for add_gates function."""

    def test_add_gates_basic(self) -> None:
        """Test adding multiple gates at once."""
        circuit = create_quantum_circuit(2, 0)
        gates = [
            {"gate": "h", "qubits": [0]},
            {"gate": "cx", "qubits": [0, 1]},
        ]
        result = add_gates(circuit, gates)
        assert len(result["operations"]) == 2

    def test_add_gates_with_none_circuit(self) -> None:
        """Test add_gates with None circuit."""
        gates = [
            {"gate": "h", "qubits": [0]},
            {"gate": "x", "qubits": [1]},
        ]
        result = add_gates(None, gates)
        assert result["num_qubits"] == 8
        assert len(result["operations"]) == 2

    def test_add_gates_empty_list(self) -> None:
        """Test add_gates with empty list."""
        circuit = create_quantum_circuit(2, 0)
        result = add_gates(circuit, [])
        assert result == circuit

    def test_add_gates_maintains_state(self) -> None:
        """Test add_gates maintains state between calls."""
        circuit = add_gates(None, [{"gate": "h", "qubits": [0]}])
        circuit = add_gates(circuit, [{"gate": "x", "qubits": [1]}])
        assert len(circuit["operations"]) == 2

    def test_add_gates_with_params(self) -> None:
        """Test add_gates with parameterized gates."""
        circuit = create_quantum_circuit(2, 0)
        gates = [
            {"gate": "rx", "qubits": [0], "params": [0.5]},
            {"gate": "rz", "qubits": [1], "params": [1.2]},
        ]
        result = add_gates(circuit, gates)
        assert len(result["operations"]) == 2

    def test_add_gates_multi_qubit_single_gate(self) -> None:
        """Test adding single-qubit gate to multiple qubits."""
        circuit = create_quantum_circuit(4, 0)
        gates = [
            {"gate": "h", "qubits": [0, 1, 2, 3]},
        ]
        result = add_gates(circuit, gates)
        assert len(result["operations"]) == 4

    def test_add_gates_requires_gates(self) -> None:
        """Test that gates parameter is required."""
        with pytest.raises(TypeError):
            add_gates(None, None)

    def test_add_gates_invalid_gate_name(self) -> None:
        """Test add_gates with invalid gate name."""
        gates = [{"gate": "invalid_gate", "qubits": [0]}]
        with pytest.raises(ValueError, match="Unknown gate"):
            add_gates(None, gates)
