# mcp-qiskit

MCP server exposing Qiskit 2.3.1 quantum computing functionality through the Model Context Protocol. Enables LLMs to create, manipulate, and execute quantum circuits via standardized MCP tools and resources.

[![PyPI](https://img.shields.io/pypi/v/mcp-qiskit.svg)](https://pypi.org/project/mcp-qiskit/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-qiskit.svg)](https://pypi.org/project/mcp-qiskit/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

mcp-name: io.github.daedalus/mcp-qiskit

## Install

```bash
pip install mcp-qiskit[qiskit]
```

## Usage

```python
from mcp_qiskit import create_quantum_circuit, add_gate, run_circuit

# Create a quantum circuit
circuit = create_quantum_circuit(2, 2)

# Add gates
circuit = add_gate(circuit, "h", [0])
circuit = add_gate(circuit, "cx", [0, 1])

# Add measurements
from mcp_qiskit import add_measurement
circuit = add_measurement(circuit, [0, 1])

# Run the circuit
result = run_circuit(circuit, "aer_simulator", shots=1024)
print(result["counts"])
```

## MCP Server

This package provides an MCP server that exposes Qiskit functionality through MCP tools and resources.

### Tools

- `create_quantum_circuit_tool` - Create an empty quantum circuit
- `add_gate_tool` - Add a quantum gate to a circuit
- `add_measurement_tool` - Add measurement operations
- `get_circuit_depth_tool` - Get circuit depth
- `list_available_gates_tool` - List all available quantum gates
- `get_gate_definition_tool` - Get gate definition and parameters
- `draw_circuit_tool` - Draw circuit in various formats
- `list_backends_tool` - List available quantum backends
- `get_backend_status_tool` - Get backend status
- `get_backend_configuration_tool` - Get backend configuration
- `run_circuit_tool` - Execute a quantum circuit
- `run_circuits_tool` - Execute multiple circuits
- `transpile_circuit_tool` - Transpile a circuit

### Resources

- `resource://backends` - List of available backends
- `resource://gates` - List of available gates

## CLI

```bash
mcp-qiskit --help
```

## Development

```bash
git clone https://github.com/daedalus/mcp-qiskit.git
cd mcp-qiskit
pip install -e ".[test]"

# Run tests
pytest

# Format
ruff format src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

## Supported Qiskit Version

This package supports Qiskit 2.3.1 specifically. The MCP server provides access to:

- Quantum circuit creation and manipulation
- Standard quantum gates (H, X, Y, Z, CX, etc.)
- Quantum backend management (Aer, IBM Quantum)
- Circuit execution and results
- Circuit visualization (ASCII, matplotlib, LaTeX)
- Circuit transpilation and optimization