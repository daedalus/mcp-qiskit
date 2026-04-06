# SPEC.md — mcp-qiskit

## Purpose

MCP server exposing Qiskit 2.3.1 quantum computing functionality through the Model Context Protocol. Enables LLMs to create, manipulate, and execute quantum circuits via standardized MCP tools and resources.

## Scope

### In Scope
- Quantum circuit creation (gates, registers, circuits)
- Quantum circuit transpilation and optimization
- Quantum backend management (available backends, status)
- Quantum job execution (run circuits, retrieve results)
- Quantum circuit visualization (ASCII, matplotlib)
- Quantum information utilities (operators, states, metrics)
- Circuit analysis (depth, operations, fidelity)
- Standard gates and composite operations

### Not Scope
- Qiskit Runtime specific features
- Qiskit Aer simulator specifics beyond basic execution
- Visualization beyond ASCII/matplotlib export
- Circuit optimization passes customization
- Statevector simulation details

## Public API

### Tools

#### Circuit Creation Tools
- `create_quantum_circuit(num_qubits: int, num_classical_bits: int) -> dict` - Create empty quantum circuit
- `add_gate(circuit: dict, gate_name: str, qubits: list[int], params: list[float] | None) -> dict` - Add gate to circuit
- `add_measurement(circuit: dict, qubits: list[int], clbits: list[int]) -> dict` - Add measurement to circuit
- `get_circuit_depth(circuit: dict) -> int` - Get circuit depth

#### Gate Tools
- `list_available_gates() -> list[str]` - List all available quantum gates
- `get_gate_definition(gate_name: str) -> dict` - Get gate definition and matrix

#### Backend Tools
- `list_backends(filters: dict | None) -> list[dict]` - List available backends
- `get_backend_status(backend_name: str) -> dict` - Get backend status and configuration
- `get_backend_configuration(backend_name: str) -> dict` - Get backend detailed configuration

#### Execution Tools
- `run_circuit(circuit: dict, backend_name: str, shots: int | None, seed: int | None) -> dict` - Execute quantum circuit
- `run_circuits(circuits: list[dict], backend_name: str, shots: int | None, seed: int | None) -> list[dict]` - Execute multiple circuits

#### Visualization Tools
- `draw_circuit(circuit: dict, output_format: str) -> str` - Draw circuit in various formats

### Resources

- `resource://quantum-circuits/` - List of active quantum circuits
- `resource://backends/` - List of available backends

## Data Formats

### Circuit Serialization
```json
{
  "num_qubits": 2,
  "num_clbits": 2,
  "operations": [
    {"name": "h", "qubits": [0], "params": []},
    {"name": "cx", "qubits": [0, 1], "params": []},
    {"name": "measure", "qubits": [0], "clbits": [0]}
  ]
}
```

### Backend Info
```json
{
  "name": "ibmq_qasm_simulator",
  "status": "ONLINE",
  "num_qubits": 127,
  "version": "2.3.1"
}
```

### Execution Result
```json
{
  "status": "COMPLETED",
  "shots": 1000,
  "counts": {"00": 500, "11": 500},
  "time_taken": 0.123
}
```

## Edge Cases

1. Empty circuit execution (no operations) - Return empty result
2. Invalid gate name - Raise ValueError with available alternatives
3. Backend offline - Raise RuntimeError with status info
4. Circuit with no measurements - Run but return statevector or job ID
5. Invalid qubit index - Raise IndexError
6. Backend not found - Raise KeyError with available backends
7. Job timeout - Return job ID for later retrieval
8. Large circuit (>100 qubits) - Warn about execution time

## Performance Constraints

- Circuit drawing limited to 50 qubits for ASCII
- Maximum 100 circuits per batch execution
- Default shots: 1024
- Timeout: 300 seconds for synchronous execution