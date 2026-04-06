"""MCP server implementation for Qiskit."""

from typing import Any

from fastmcp import FastMCP

from ._backend import (
    get_backend_configuration,
    get_backend_status,
    list_backends,
)
from ._circuit import (
    add_gate,
    add_measurement,
    create_quantum_circuit,
    draw_circuit,
    get_circuit_depth,
    get_gate_definition,
    list_available_gates,
)
from ._execution import (
    run_circuit,
    run_circuits,
    transpile_circuit,
)

mcp = FastMCP("mcp-qiskit")


@mcp.tool()
def create_quantum_circuit_tool(
    num_qubits: int,
    num_classical_bits: int,
) -> dict[str, Any]:
    """Create an empty quantum circuit.

    Args:
        num_qubits: Number of quantum bits in the circuit.
        num_classical_bits: Number of classical bits for measurements.

    Returns:
        Dictionary representation of the created quantum circuit.

    Example:
        >>> create_quantum_circuit_tool(2, 2)
        {"num_qubits": 2, "num_clbits": 2, "operations": [], "name": "circuit"}
    """
    return create_quantum_circuit(num_qubits, num_classical_bits)


@mcp.tool()
def add_gate_tool(
    circuit: dict[str, Any],
    gate_name: str,
    qubits: list[int],
    params: list[float] | None = None,
) -> dict[str, Any]:
    """Add a quantum gate to a circuit.

    Args:
        circuit: Dictionary representation of the quantum circuit.
        gate_name: Name of the gate to add (e.g., 'h', 'x', 'cx', 'rz', 'u').
        qubits: List of qubit indices to apply the gate to.
        params: Optional list of parameters for parameterized gates.

    Returns:
        Updated dictionary representation of the quantum circuit.

    Example:
        >>> circuit = create_quantum_circuit_tool(2, 0)
        >>> circuit = add_gate_tool(circuit, 'h', [0])
        >>> circuit = add_gate_tool(circuit, 'cx', [0, 1])
    """
    return add_gate(circuit, gate_name, qubits, params)


@mcp.tool()
def add_measurement_tool(
    circuit: dict[str, Any],
    qubits: list[int],
    clbits: list[int] | None = None,
) -> dict[str, Any]:
    """Add measurement operations to a circuit.

    Args:
        circuit: Dictionary representation of the quantum circuit.
        qubits: List of qubit indices to measure.
        clbits: List of classical bit indices to store results.

    Returns:
        Updated dictionary representation of the quantum circuit.

    Example:
        >>> circuit = create_quantum_circuit_tool(2, 2)
        >>> circuit = add_gate_tool(circuit, 'h', [0])
        >>> circuit = add_measurement_tool(circuit, [0, 1])
    """
    return add_measurement(circuit, qubits, clbits)


@mcp.tool()
def get_circuit_depth_tool(circuit: dict[str, Any]) -> int:
    """Get the depth of a quantum circuit.

    Args:
        circuit: Dictionary representation of the quantum circuit.

    Returns:
        Depth of the circuit (number of layers in the longest path).

    Example:
        >>> circuit = create_quantum_circuit_tool(2, 0)
        >>> circuit = add_gate_tool(circuit, 'h', [0])
        >>> circuit = add_gate_tool(circuit, 'cx', [0, 1])
        >>> get_circuit_depth_tool(circuit)
        2
    """
    return get_circuit_depth(circuit)


@mcp.tool()
def list_available_gates_tool() -> list[str]:
    """List all available quantum gates in Qiskit.

    Returns:
        List of gate names available in Qiskit.

    Example:
        >>> gates = list_available_gates_tool()
        >>> 'h' in gates
        True
    """
    return list_available_gates()


@mcp.tool()
def get_gate_definition_tool(gate_name: str) -> dict[str, Any]:
    """Get the definition of a quantum gate.

    Args:
        gate_name: Name of the quantum gate.

    Returns:
        Dictionary containing gate definition and parameters.

    Example:
        >>> gate_def = get_gate_definition_tool('h')
        >>> 'name' in gate_def
        True
    """
    return get_gate_definition(gate_name)


@mcp.tool()
def draw_circuit_tool(
    circuit: dict[str, Any],
    output_format: str = "ascii",
) -> str:
    """Draw a quantum circuit.

    Args:
        circuit: Dictionary representation of the quantum circuit.
        output_format: Format for output ('ascii', 'text', 'mpl', 'latex').

    Returns:
        String representation of the circuit diagram.

    Example:
        >>> circuit = create_quantum_circuit_tool(2, 2)
        >>> circuit = add_gate_tool(circuit, 'h', [0])
        >>> circuit = add_gate_tool(circuit, 'cx', [0, 1])
        >>> circuit = add_measurement_tool(circuit, [0, 1])
        >>> draw = draw_circuit_tool(circuit, 'ascii')
    """
    return draw_circuit(circuit, output_format)


@mcp.tool()
def list_backends_tool(filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """List available quantum backends.

    Args:
        filters: Optional dictionary of filters (e.g., {'status': 'ONLINE'}).

    Returns:
        List of backend information dictionaries.

    Example:
        >>> backends = list_backends_tool()
    """
    return list_backends(filters)


@mcp.tool()
def get_backend_status_tool(backend_name: str) -> dict[str, Any]:
    """Get the status of a specific quantum backend.

    Args:
        backend_name: Name of the backend.

    Returns:
        Dictionary containing backend status information.

    Example:
        >>> status = get_backend_status_tool('aer_simulator')
    """
    return get_backend_status(backend_name)


@mcp.tool()
def get_backend_configuration_tool(backend_name: str) -> dict[str, Any]:
    """Get detailed configuration of a quantum backend.

    Args:
        backend_name: Name of the backend.

    Returns:
        Dictionary containing detailed backend configuration.

    Example:
        >>> config = get_backend_configuration_tool('aer_simulator')
    """
    return get_backend_configuration(backend_name)


@mcp.tool()
def run_circuit_tool(
    circuit: dict[str, Any],
    backend_name: str = "aer_simulator",
    shots: int | None = 1024,
    seed: int | None = None,
) -> dict[str, Any]:
    """Execute a quantum circuit on a backend.

    Args:
        circuit: Dictionary representation of the quantum circuit.
        backend_name: Name of the backend to execute on.
        shots: Number of measurement shots.
        seed: Optional seed for reproducibility.

    Returns:
        Dictionary containing execution results.

    Example:
        >>> circuit = create_quantum_circuit_tool(2, 2)
        >>> circuit = add_gate_tool(circuit, 'h', [0])
        >>> circuit = add_gate_tool(circuit, 'cx', [0, 1])
        >>> circuit = add_measurement_tool(circuit, [0, 1])
        >>> result = run_circuit_tool(circuit)
    """
    return run_circuit(circuit, backend_name, shots, seed)


@mcp.tool()
def run_circuits_tool(
    circuits: list[dict[str, Any]],
    backend_name: str = "aer_simulator",
    shots: int | None = 1024,
    seed: int | None = None,
) -> list[dict[str, Any]]:
    """Execute multiple quantum circuits on a backend.

    Args:
        circuits: List of dictionary representations of quantum circuits.
        backend_name: Name of the backend to execute on.
        shots: Number of measurement shots.
        seed: Optional seed for reproducibility.

    Returns:
        List of result dictionaries.

    Example:
        >>> circuits = [create_quantum_circuit_tool(2, 2) for _ in range(3)]
        >>> results = run_circuits_tool(circuits)
    """
    return run_circuits(circuits, backend_name, shots, seed)


@mcp.tool()
def transpile_circuit_tool(
    circuit: dict[str, Any],
    optimization_level: int = 1,
    basis_gates: list[str] | None = None,
) -> dict[str, Any]:
    """Transpile a quantum circuit.

    Args:
        circuit: Dictionary representation of the quantum circuit.
        optimization_level: Optimization level (0-3).
        basis_gates: Optional list of basis gates to target.

    Returns:
        Transpiled circuit dictionary.

    Example:
        >>> circuit = create_quantum_circuit_tool(2, 0)
        >>> circuit = add_gate_tool(circuit, 'h', [0])
        >>> transpiled = transpile_circuit_tool(circuit)
    """
    return transpile_circuit(circuit, optimization_level, basis_gates)


@mcp.resource("resource://backends")
def get_backends_resource() -> list[dict[str, Any]]:
    """Get list of available backends as an MCP resource.

    Returns:
        List of backend information dictionaries.
    """
    return list_backends()


@mcp.resource("resource://gates")
def get_gates_resource() -> list[str]:
    """Get list of available gates as an MCP resource.

    Returns:
        List of gate names.
    """
    return list_available_gates()
