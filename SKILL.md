# MCP Qiskit

MCP server exposing Qiskit quantum computing functionality.

## When to use this skill

Use this skill when you need to:
- Create and manipulate quantum circuits
- Execute on quantum simulators
- Analyze circuit properties
- Visualize circuits

## Tools

**Circuit Creation:**
- `create_quantum_circuit` - Create circuit with qubits/classical bits
- `add_gate` - Add quantum gates
- `add_gates` - Add multiple gates
- `add_measurement` - Add measurements

**Analysis:**
- `get_circuit_depth` - Get circuit depth
- `list_available_gates` - List all gates
- `get_gate_definition` - Get gate details

**Visualization:**
- `draw_circuit` - Render circuit (ASCII, text, mpl, latex)

**Backend:**
- `list_backends` - List available backends
- `get_backend_status` - Get backend status
- `get_backend_configuration` - Get backend config

**Execution:**
- `run_circuit` - Execute single circuit
- `run_circuits` - Execute multiple circuits
- `transpile_circuit` - Transpile for backend

## Install

```bash
pip install mcp-qiskit[qiskit]
```