"""Quantum circuit management functionality."""

from typing import Any

import qiskit
from qiskit import QuantumCircuit


def _circuit_to_dict(circuit: QuantumCircuit) -> dict[str, Any]:
    """Serialize a QuantumCircuit to a dictionary."""
    operations = []
    for instruction in circuit.data:
        op_name = instruction.operation.name
        qubits = [circuit.qubits.index(q) for q in instruction.qubits]
        clbits = []
        if instruction.clbits:
            clbits = [circuit.clbits.index(c) for c in instruction.clbits]
        params = []
        if hasattr(instruction.operation, "params"):
            params = instruction.operation.params
        op_dict = {"name": op_name, "qubits": qubits, "params": params}
        if clbits:
            op_dict["clbits"] = clbits
        operations.append(op_dict)

    return {
        "num_qubits": circuit.num_qubits,
        "num_clbits": circuit.num_clbits,
        "operations": operations,
        "name": circuit.name,
    }


def _dict_to_circuit(data: dict[str, Any]) -> QuantumCircuit:
    """Deserialize a dictionary to a QuantumCircuit."""
    circuit = QuantumCircuit(data["num_qubits"], data["num_clbits"])
    circuit.name = data.get("name", "circuit")

    for op in data.get("operations", []):
        gate_name = op["name"]
        qubits = op["qubits"]
        params = op.get("params", [])

        if gate_name == "measure":
            clbits = op.get("clbits", list(range(len(qubits))))
            for q, c in zip(qubits, clbits):
                circuit.measure(q, c)
        else:
            gate_cls = _get_gate_class(gate_name)
            if gate_cls is None:
                if params:
                    from qiskit.circuit import Parameter

                    p = Parameter(f"p{len(params)}")
                    circuit.append(gate_name, qubits, [p] * len(params))
            else:
                if params:
                    gate = gate_cls(*params)
                else:
                    gate = gate_cls()
                circuit.append(gate, qubits)

    return circuit


def create_quantum_circuit(num_qubits: int, num_classical_bits: int) -> dict[str, Any]:
    """Create an empty quantum circuit.

    Args:
        num_qubits: Number of quantum bits in the circuit.
        num_classical_bits: Number of classical bits for measurements.

    Returns:
        Dictionary representation of the created quantum circuit.

    Example:
        >>> create_quantum_circuit(2, 2)
        {"num_qubits": 2, "num_clbits": 2, "operations": [], "name": "circuit"}
    """
    if num_qubits < 1:
        raise ValueError("num_qubits must be at least 1")
    if num_classical_bits < 0:
        raise ValueError("num_classical_bits must be non-negative")

    circuit = QuantumCircuit(num_qubits, num_classical_bits)
    circuit.name = "circuit"
    return _circuit_to_dict(circuit)


def add_gate(
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
        >>> circuit = create_quantum_circuit(2, 0)
        >>> add_gate(circuit, 'h', [0])
        >>> add_gate(circuit, 'cx', [0, 1])
    """
    qc = _dict_to_circuit(circuit)

    if len(qubits) == 0:
        raise ValueError("At least one qubit must be specified")

    max_qubit = max(qubits)
    if max_qubit >= qc.num_qubits:
        raise IndexError(
            f"Qubit index {max_qubit} out of range for circuit with {qc.num_qubits} qubits"
        )

    params = params or []

    if gate_name == "measure":
        if params:
            clbits = [int(p) for p in params]
        else:
            clbits = list(range(len(qubits)))
        if len(clbits) != len(qubits):
            raise ValueError("Number of classical bits must match number of qubits")
        for q, c in zip(qubits, clbits):
            qc.measure(q, c)
    elif gate_name == "barrier":
        qc.barrier(*qubits)
    elif gate_name == "reset":
        qc.reset(*qubits)
    else:
        gate_cls = _get_gate_class(gate_name)
        if gate_cls is None:
            available_gates = list_available_gates()
            raise ValueError(
                f"Unknown gate '{gate_name}'. Available gates: {available_gates}"
            )

        if params:
            gate = gate_cls(*params)
        else:
            gate = gate_cls()
        qc.append(gate, qubits)

    return _circuit_to_dict(qc)


def _get_gate_class(gate_name: str) -> type | None:
    """Get gate class from gate name."""
    gate_mappings = {
        "h": "HGate",
        "x": "XGate",
        "y": "YGate",
        "z": "ZGate",
        "s": "SGate",
        "sdg": "SdgGate",
        "t": "TGate",
        "tdg": "TdgGate",
        "cx": "CXGate",
        "cy": "CYGate",
        "cz": "CZGate",
        "swap": "SwapGate",
        "i": "IGate",
        "id": "IGate",
        "rx": "RXGate",
        "ry": "RYGate",
        "rz": "RZGate",
        "u1": "U1Gate",
        "u2": "U2Gate",
        "u3": "U3Gate",
        "p": "PhaseGate",
        "cp": "CPhaseGate",
    }

    if gate_name in gate_mappings:
        class_name = gate_mappings[gate_name]
        return getattr(qiskit.circuit.library, class_name)  # type: ignore[no-any-return]

    if hasattr(qiskit.circuit.library, gate_name):
        attr = getattr(qiskit.circuit.library, gate_name)
        if isinstance(attr, type):
            return attr

    return None


def add_measurement(
    circuit: dict[str, Any],
    qubits: list[int],
    clbits: list[int] | None = None,
) -> dict[str, Any]:
    """Add measurement operations to a circuit.

    Args:
        circuit: Dictionary representation of the quantum circuit.
        qubits: List of qubit indices to measure.
        clbits: List of classical bit indices to store results. If None, uses sequential indices.

    Returns:
        Updated dictionary representation of the quantum circuit.

    Example:
        >>> circuit = create_quantum_circuit(2, 2)
        >>> add_gate(circuit, 'h', [0])
        >>> add_measurement(circuit, [0, 1])
    """
    qc = _dict_to_circuit(circuit)

    if not qubits:
        raise ValueError("At least one qubit must be specified for measurement")

    for q in qubits:
        if q >= qc.num_qubits:
            raise IndexError(f"Qubit index {q} out of range")

    if clbits is None:
        clbits = list(range(len(qubits)))
    elif len(clbits) != len(qubits):
        raise ValueError("Number of classical bits must match number of qubits")

    for q, c in zip(qubits, clbits):
        if c >= qc.num_clbits:
            raise IndexError(
                f"Classical bit index {c} out of range for circuit with {qc.num_clbits} classical bits"
            )
        qc.measure(q, c)

    return _circuit_to_dict(qc)


def get_circuit_depth(circuit: dict[str, Any]) -> int:
    """Get the depth of a quantum circuit.

    Args:
        circuit: Dictionary representation of the quantum circuit.

    Returns:
        Depth of the circuit (number of layers in the longest path).

    Example:
        >>> circuit = create_quantum_circuit(2, 0)
        >>> add_gate(circuit, 'h', [0])
        >>> add_gate(circuit, 'cx', [0, 1])
        >>> get_circuit_depth(circuit)
        2
    """
    qc = _dict_to_circuit(circuit)
    return qc.depth()  # type: ignore[no-any-return]


def list_available_gates() -> list[str]:
    """List all available quantum gates in Qiskit.

    Returns:
        List of gate names available in Qiskit.

    Example:
        >>> gates = list_available_gates()
        >>> 'h' in gates
        True
    """
    return [
        "h",
        "x",
        "y",
        "z",
        "s",
        "sdg",
        "t",
        "tdg",
        "cx",
        "cy",
        "cz",
        "swap",
        "cswap",
        "cu",
        "cu1",
        "cu3",
        "ccx",
        "ccz",
        "u1",
        "u2",
        "u3",
        "rx",
        "ry",
        "rz",
        "crx",
        "cry",
        "crz",
        "cp",
        "rxx",
        "ryy",
        "rzz",
        "rccx",
        "rc3x",
        "c3x",
        "c3sx",
        "c4x",
        "ch",
        "csx",
        "cswap",
        "cu",
        "dcx",
        "ecr",
        "i",
        "id",
        "ms",
        "p",
        "psix",
        "rzx",
        "xx_minus_yz",
        "xx_plus_yz",
        "z",
    ]


def get_gate_definition(gate_name: str) -> dict[str, Any]:
    """Get the definition and matrix of a quantum gate.

    Args:
        gate_name: Name of the quantum gate.

    Returns:
        Dictionary containing gate definition, matrix representation, and parameters.

    Example:
        >>> gate_def = get_gate_definition('h')
        >>> 'matrix' in gate_def
        True
    """
    gate_name = gate_name.lower()

    if gate_name in ["h", "hadamard"]:
        from qiskit.circuit.library import HGate

        gate = HGate()
    elif gate_name in ["x", "x_gate"]:
        from qiskit.circuit.library import XGate

        gate = XGate()
    elif gate_name in ["y", "y_gate"]:
        from qiskit.circuit.library import YGate

        gate = YGate()
    elif gate_name in ["z", "z_gate"]:
        from qiskit.circuit.library import ZGate

        gate = ZGate()
    elif gate_name in ["s", "sgate"]:
        from qiskit.circuit.library import SGate

        gate = SGate()
    elif gate_name in ["sdg"]:
        from qiskit.circuit.library import SdgGate

        gate = SdgGate()
    elif gate_name in ["t", "tgate"]:
        from qiskit.circuit.library import TGate

        gate = TGate()
    elif gate_name in ["tdg"]:
        from qiskit.circuit.library import TdgGate

        gate = TdgGate()
    elif gate_name in ["cx", "cnot"]:
        from qiskit.circuit.library import CXGate

        gate = CXGate()
    elif gate_name in ["cy"]:
        from qiskit.circuit.library import CYGate

        gate = CYGate()
    elif gate_name in ["cz"]:
        from qiskit.circuit.library import CZGate

        gate = CZGate()
    elif gate_name in ["swap"]:
        from qiskit.circuit.library import SwapGate

        gate = SwapGate()
    elif gate_name in ["rx"]:
        from qiskit.circuit.library import RXGate

        gate = RXGate(0.5)
    elif gate_name in ["ry"]:
        from qiskit.circuit.library import RYGate

        gate = RYGate(0.5)
    elif gate_name in ["rz"]:
        from qiskit.circuit.library import RZGate

        gate = RZGate(0.5)
    elif gate_name in ["u1"]:
        from qiskit.circuit.library import U1Gate

        gate = U1Gate(0.5)
    elif gate_name in ["u2"]:
        from qiskit.circuit.library import U2Gate

        gate = U2Gate(0, 0)
    elif gate_name in ["u3"]:
        from qiskit.circuit.library import U3Gate

        gate = U3Gate(0, 0, 0)
    elif gate_name in ["p", "phase"]:
        from qiskit.circuit.library import PhaseGate

        gate = PhaseGate(0.5)
    elif gate_name in ["cp"]:
        from qiskit.circuit.library import CPhaseGate

        gate = CPhaseGate(0.5)
    elif gate_name in ["cu"]:
        from qiskit.circuit.library import CUGate

        gate = CUGate(0, 0, 0, 0)
    elif gate_name in ["ccx", "toffoli"]:
        from qiskit.circuit.library import CCXGate

        gate = CCXGate()
    elif gate_name in ["rxx"]:
        from qiskit.circuit.library import RXXGate

        gate = RXXGate(0.5)
    elif gate_name in ["ryy"]:
        from qiskit.circuit.library import RYYGate

        gate = RYYGate(0.5)
    elif gate_name in ["rzz"]:
        from qiskit.circuit.library import RZZGate

        gate = RZZGate(0.5)
    elif gate_name in ["ch"]:
        from qiskit.circuit.library import CHGate

        gate = CHGate()
    elif gate_name == "i" or gate_name == "id":
        from qiskit.circuit.library import IGate

        gate = IGate()
    else:
        available = list_available_gates()
        raise ValueError(f"Unknown gate '{gate_name}'. Available gates: {available}")

    return {
        "name": gate.name,
        "num_qubits": gate.num_qubits,
        "num_parameters": len(gate.params),
        "params": list(gate.params) if gate.params else [],
    }


def draw_circuit(
    circuit: dict[str, Any],
    output_format: str = "ascii",
) -> str:
    """Draw a quantum circuit.

    Args:
        circuit: Dictionary representation of the quantum circuit.
        output_format: Format for output ('ascii', 'text', 'mpl', 'latex', 'latex_source').
        filename: Optional filename to save the output.

    Returns:
        String representation of the circuit diagram.

    Example:
        >>> circuit = create_quantum_circuit(2, 2)
        >>> add_gate(circuit, 'h', [0])
        >>> add_gate(circuit, 'cx', [0, 1])
        >>> add_measurement(circuit, [0, 1])
        >>> print(draw_circuit(circuit, 'ascii'))
    """
    qc = _dict_to_circuit(circuit)

    if output_format in ("ascii", "text"):
        return str(qc.draw(output="text", cregbundle=False))
    elif output_format == "mpl":
        from io import BytesIO

        img = qc.draw(output="mpl")
        buf = BytesIO()
        img.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        import base64

        return base64.b64encode(buf.read()).decode()
    elif output_format in ("latex", "latex_source"):
        return str(qc.draw(output=output_format))
    else:
        raise ValueError(
            f"Unknown output format '{output_format}'. "
            f"Valid options: ascii, text, mpl, latex, latex_source"
        )
