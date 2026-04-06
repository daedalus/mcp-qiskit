"""Tests for MCP server tools."""

import pytest

from mcp_qiskit._mcp import (
    add_gate_tool,
    add_gates_tool,
    add_measurement_tool,
    create_quantum_circuit_tool,
    draw_circuit_tool,
    get_circuit_depth_tool,
    get_gate_definition_tool,
    list_available_gates_tool,
)


class TestCreateQuantumCircuitTool:
    """Tests for create_quantum_circuit_tool."""

    def test_create_quantum_circuit_tool(self) -> None:
        """Test creating circuit via MCP tool."""
        result = create_quantum_circuit_tool(2, 2)
        assert result["num_qubits"] == 2
        assert result["num_clbits"] == 2
        assert result["operations"] == []


class TestAddGateTool:
    """Tests for add_gate_tool MCP wrapper."""

    def test_add_gate_tool_with_existing_circuit(self) -> None:
        """Test adding gate with existing circuit."""
        circuit = create_quantum_circuit_tool(2, 0)
        result = add_gate_tool(circuit, "h", [0])
        assert "operations" in result

    def test_add_gate_tool_with_none_circuit(self) -> None:
        """Test adding gate with None circuit (auto-creates)."""
        result = add_gate_tool(None, "h", [0])
        assert result["num_qubits"] == 8
        assert len(result["operations"]) == 1

    def test_add_gate_tool_maintains_state(self) -> None:
        """Test that state is maintained between calls."""
        circuit = add_gate_tool(None, "h", [0])
        circuit = add_gate_tool(circuit, "x", [1])
        assert len(circuit["operations"]) == 2

    def test_add_gate_tool_requires_gate_name(self) -> None:
        """Test that gate_name is required."""
        with pytest.raises(ValueError, match="gate_name is required"):
            add_gate_tool(None, None, [0])

    def test_add_gate_tool_requires_qubits(self) -> None:
        """Test that qubits is required."""
        with pytest.raises(ValueError, match="qubits is required"):
            add_gate_tool(None, "h", None)


class TestAddMeasurementTool:
    """Tests for add_measurement_tool MCP wrapper."""

    def test_add_measurement_tool_with_existing_circuit(self) -> None:
        """Test adding measurement with existing circuit."""
        circuit = create_quantum_circuit_tool(2, 2)
        result = add_measurement_tool(circuit, [0, 1])
        assert "operations" in result

    def test_add_measurement_tool_with_none_circuit(self) -> None:
        """Test adding measurement with None circuit (auto-creates)."""
        result = add_measurement_tool(None, [0])
        assert result["num_qubits"] == 8
        assert len(result["operations"]) == 1

    def test_add_measurement_tool_maintains_state(self) -> None:
        """Test that state is maintained between calls."""
        circuit = add_gate_tool(None, "h", [0])
        circuit = add_measurement_tool(circuit, [0])
        assert len(circuit["operations"]) == 2

    def test_add_measurement_tool_requires_qubits(self) -> None:
        """Test that qubits is required."""
        with pytest.raises(ValueError, match="qubits is required"):
            add_measurement_tool(None, None)


class TestGetCircuitDepthTool:
    """Tests for get_circuit_depth_tool."""

    def test_get_circuit_depth_tool(self) -> None:
        """Test getting circuit depth via MCP tool."""
        circuit = create_quantum_circuit_tool(2, 0)
        circuit = add_gate_tool(circuit, "h", [0])
        result = get_circuit_depth_tool(circuit)
        assert result >= 0


class TestListAvailableGatesTool:
    """Tests for list_available_gates_tool."""

    def test_list_available_gates_tool(self) -> None:
        """Test listing gates via MCP tool."""
        result = list_available_gates_tool()
        assert isinstance(result, list)
        assert "h" in result
        assert "x" in result
        assert "cx" in result


class TestGetGateDefinitionTool:
    """Tests for get_gate_definition_tool."""

    def test_get_gate_definition_tool(self) -> None:
        """Test getting gate definition via MCP tool."""
        result = get_gate_definition_tool("h")
        assert result["name"] == "h"
        assert result["num_qubits"] == 1

    def test_get_gate_definition_tool_rx(self) -> None:
        """Test getting parameterized gate definition."""
        result = get_gate_definition_tool("rx")
        assert result["num_parameters"] == 1


class TestDrawCircuitTool:
    """Tests for draw_circuit_tool."""

    def test_draw_circuit_tool_ascii(self) -> None:
        """Test drawing circuit via MCP tool."""
        circuit = create_quantum_circuit_tool(2, 2)
        circuit = add_gate_tool(circuit, "h", [0])
        circuit = add_measurement_tool(circuit, [0, 1])
        result = draw_circuit_tool(circuit, "ascii")
        assert isinstance(result, str)

    def test_draw_circuit_tool_text(self) -> None:
        """Test drawing circuit in text format."""
        circuit = create_quantum_circuit_tool(2, 0)
        circuit = add_gate_tool(circuit, "h", [0])
        result = draw_circuit_tool(circuit, "text")
        assert isinstance(result, str)


class TestAddGatesTool:
    """Tests for add_gates_tool MCP wrapper."""

    def test_add_gates_tool_with_existing_circuit(self) -> None:
        """Test adding multiple gates with existing circuit."""
        circuit = create_quantum_circuit_tool(2, 0)
        gates = [
            {"gate": "h", "qubits": [0]},
            {"gate": "cx", "qubits": [0, 1]},
        ]
        result = add_gates_tool(circuit, gates)
        assert len(result["operations"]) == 2

    def test_add_gates_tool_with_none_circuit(self) -> None:
        """Test adding gates with None circuit (auto-creates)."""
        gates = [
            {"gate": "h", "qubits": [0]},
            {"gate": "x", "qubits": [1]},
        ]
        result = add_gates_tool(None, gates)
        assert result["num_qubits"] == 8
        assert len(result["operations"]) == 2

    def test_add_gates_tool_maintains_state(self) -> None:
        """Test that state is maintained when chaining."""
        circuit = add_gates_tool(None, [{"gate": "h", "qubits": [0]}])
        circuit = add_gates_tool(circuit, [{"gate": "x", "qubits": [1]}])
        assert len(circuit["operations"]) == 2

    def test_add_gates_tool_requires_gates(self) -> None:
        """Test that gates list is required."""
        with pytest.raises(ValueError, match="gates is required"):
            add_gates_tool(None, None)

    def test_add_gates_tool_with_params(self) -> None:
        """Test adding parameterized gates."""
        gates = [
            {"gate": "rx", "qubits": [0], "params": [0.5]},
            {"gate": "rz", "qubits": [1], "params": [1.2]},
        ]
        result = add_gates_tool(None, gates)
        assert len(result["operations"]) == 2
