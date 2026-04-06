# mcp-qiskit

MCP server exposing Qiskit 2.3.1 quantum computing functionality through the Model Context Protocol. Enables LLMs to create, manipulate, and execute quantum circuits via standardized MCP tools and resources.

[![PyPI](https://img.shields.io/pypi/v/mcp-qiskit.svg)](https://pypi.org/project/mcp-qiskit/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-qiskit.svg)](https://pypi.org/project/mcp-qiskit/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Tests](https://github.com/daedalus/mcp-qiskit/actions/workflows/ci.yml/badge.svg)](https://github.com/daedalus/mcp-qiskit/actions)

mcp-name: io.github.daedalus/mcp-qiskit

## Overview

This project provides a Model Context Protocol (MCP) server that exposes [Qiskit](https://qiskit.com/) quantum computing functionality to Large Language Models (LLMs). It allows AI assistants to:

- Create and manipulate quantum circuits
- Execute circuits on quantum simulators or real backends
- Analyze circuit properties (depth, gates, operations)
- Visualize circuits in various formats
- Manage quantum backends

### Why Use This?

- **LLM Integration**: Enables AI assistants to perform quantum computing tasks without external tooling
- **Standardized Interface**: MCP provides a consistent tool-based interface for quantum operations
- **Qiskit 2.3.1 Compatible**: Specifically designed for Qiskit 2.3.1 with all its features
- **Extensible**: Easy to add new tools or backends

## Installation

### Prerequisites

- Python 3.11 or higher
- Qiskit 2.3.1
- A running MCP client (Claude Desktop, Cursor, etc.)

### Install from PyPI

```bash
pip install mcp-qiskit[qiskit]
```

The `[qiskit]` extra installs the required Qiskit dependencies. Other extras available:

```bash
# Install with development dependencies
pip install mcp-qiskit[dev,test]

# Install with MCP server dependencies
pip install mcp-qiskit[mcp]
```

### Install from Source

```bash
git clone https://github.com/daedalus/mcp-qiskit.git
cd mcp-qiskit
pip install -e ".[all]"
```

## Quick Start

### As a Python Library

```python
from mcp_qiskit import create_quantum_circuit, add_gate, add_measurement, run_circuit

# Create a 2-qubit circuit with 2 classical bits
circuit = create_quantum_circuit(2, 2)

# Apply a Hadamard gate on qubit 0
circuit = add_gate(circuit, "h", [0])

# Apply CNOT gate (control: qubit 0, target: qubit 1)
circuit = add_gate(circuit, "cx", [0, 1])

# Measure all qubits
circuit = add_measurement(circuit, [0, 1])

# Execute on Aer simulator
result = run_circuit(circuit, "aer_simulator", shots=1024)
print(f"Measurement results: {result['counts']}")
```

### As an MCP Server

#### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-qiskit": {
      "command": "mcp-qiskit",
      "env": {}
    }
  }
}
```

#### Cursor

Add to your Cursor settings under MCP Servers:

```json
{
  "mcpServers": {
    "mcp-qiskit": {
      "command": "mcp-qiskit",
      "args": []
    }
  }
}
```

#### Other MCP Clients

```bash
# Run as stdio server
mcp-qiskit

# Or use the Python module directly
python -m mcp_qiskit
```

## MCP Tools Reference

### Circuit Creation Tools

#### create_quantum_circuit_tool

Creates an empty quantum circuit with specified number of qubits and classical bits.

**Parameters:**
- `num_qubits` (int): Number of quantum bits
- `num_classical_bits` (int): Number of classical bits for measurements

**Returns:** Dictionary representing the circuit

**Example:**
```python
circuit = create_quantum_circuit_tool(num_qubits=3, num_classical_bits=3)
# Returns: {"num_qubits": 3, "num_clbits": 3, "operations": [], "name": "circuit"}
```

#### add_gate_tool

Adds a quantum gate to a circuit. **This tool maintains circuit state between calls.**

**Parameters:**
- `circuit` (dict, optional): The circuit to modify. If None, creates a new 8-qubit circuit with 8 classical bits automatically.
- `gate_name` (str): Name of the gate (e.g., "h", "x", "cx", "rx")
- `qubits` (list[int]): List of qubit indices to apply the gate to. Can be a single qubit (e.g., `[0]`) or multiple qubits (e.g., `[0, 1, 2, 3]`). When multiple qubits are specified for a single-qubit gate, the gate is applied to each qubit.
- `params` (list[float], optional): Parameters for parameterized gates

**Supported Gates:**
- Single-qubit: `h`, `x`, `y`, `z`, `s`, `t`, `sdg`, `tdg`, `i`, `id`
- Parameterized: `rx`, `ry`, `rz`, `u1`, `u2`, `u3`, `p`
- Multi-qubit: `cx`, `cy`, `cz`, `swap`
- Multi-controlled: `mcx`, `mct`, `mcp`, `ccx`, `toffoli`, `c3x`, `c3sx`, `c4x`
- Specialized: `rxx`, `ryy`, `rzz`, `ch`, `cswap`, `cu`, `crx`, `cry`, `crz`

**State Maintenance Pattern:**
Always pass the circuit returned by the previous call to maintain state:

```python
# Option 1: Pass circuit explicitly
circuit = add_gate_tool(circuit=None, gate_name="h", qubits=[0])  # Creates new circuit
circuit = add_gate_tool(circuit=circuit, gate_name="x", qubits=[1])  # Appends

# Option 2: Use returned circuit
circuit = add_gate_tool(None, "h", [0])
circuit = add_gate_tool(circuit, "cx", [0, 1])
circuit = add_gate_tool(circuit, "rx", [0], [0.5])
```

**Apply Single-Quantum Gate to Multiple Qubits:**
When applying single-qubit gates (like `h`, `x`, `y`, `z`, etc.) to multiple qubits at once, use a list of qubit indices:

```python
# Apply H gate to qubits 0, 1, 2, 3 simultaneously
circuit = add_gate_tool(circuit, "h", [0, 1, 2, 3])

# Apply X gate to qubits 4, 5, 6, 7 simultaneously  
circuit = add_gate_tool(circuit, "x", [4, 5, 6, 7])
```

#### add_measurement_tool

Adds measurement operations to qubits. **This tool maintains circuit state between calls.**

**Parameters:**
- `circuit` (dict, optional): The circuit to modify. If None, creates a new 8-qubit circuit with 8 classical bits automatically.
- `qubits` (list[int]): Qubit indices to measure
- `clbits` (list[int], optional): Classical bit indices to store results

**Example:**
```python
# Maintain state between calls
circuit = add_measurement_tool(circuit=None, qubits=[0, 1])           # Creates new circuit
circuit = add_measurement_tool(circuit=circuit, qubits=[2])          # Appends measurement

# Or use returned circuit
circuit = add_measurement_tool(None, [0, 1])           # Measure q0->c0, q1->c1
circuit = add_measurement_tool(circuit, [0, 1], [1, 0]) # Measure q0->c1, q1->c0
```

### Analysis Tools

#### get_circuit_depth_tool

Returns the depth (number of layers) of the circuit.

**Parameters:**
- `circuit` (dict): The circuit to analyze

**Returns:** Integer representing circuit depth

#### list_available_gates_tool

Lists all available quantum gates in Qiskit.

**Returns:** List of gate name strings

#### get_gate_definition_tool

Gets detailed information about a quantum gate.

**Parameters:**
- `gate_name` (str): Name of the gate

**Returns:** Dictionary with gate properties:
- `name`: Gate name
- `num_qubits`: Number of qubits the gate operates on
- `num_parameters`: Number of parameters (0 for fixed gates)
- `params`: List of parameter values

### Visualization Tools

#### draw_circuit_tool

Renders a circuit in various formats.

**Parameters:**
- `circuit` (dict): The circuit to draw
- `output_format` (str): Output format - "ascii", "text", "mpl", "latex"

**Returns:** String representation of the circuit

**Example Output (ASCII):**
```
     ┌───┐
q_0: ┤ H ├──■──
     └───┘┌─┴─┐
q_1: ────┤ X ├
         └───┘
c: 2/═══════╪═══
         0   1
```

### Backend Tools

#### list_backends_tool

Lists available quantum backends.

**Parameters:**
- `filters` (dict, optional): Filter criteria (e.g., `{"status": "ONLINE"}`)

**Returns:** List of backend information dictionaries

#### get_backend_status_tool

Gets status information for a backend.

**Parameters:**
- `backend_name` (str): Name of the backend

**Returns:** Dictionary with:
- `name`: Backend name
- `status`: Status (ONLINE/OFFLINE)
- `num_qubits`: Number of qubits

#### get_backend_configuration_tool

Gets detailed configuration for a backend.

**Parameters:**
- `backend_name` (str): Name of the backend

**Returns:** Dictionary with:
- `name`: Backend name
- `num_qubits`: Number of qubits
- `coupling_map`: Qubit connectivity (if applicable)
- `basis_gates`: List of available basis gates
- `max_shots`: Maximum allowed shots

### Execution Tools

#### run_circuit_tool

Executes a single quantum circuit.

**Parameters:**
- `circuit` (dict): Circuit to execute
- `backend_name` (str, optional): Backend name (default: "aer_simulator")
- `shots` (int, optional): Number of measurement shots (default: 1024)
- `seed` (int, optional): Random seed for reproducibility

**Returns:** Dictionary with:
- `status`: "COMPLETED" or error message
- `backend`: Backend used
- `shots`: Number of shots
- `counts`: Measurement outcome counts (if shots > 0)
- `statevector`: Statevector (if shots=None)
- `time_taken`: Execution time in seconds

**Example:**
```python
result = run_circuit_tool(circuit, "aer_simulator", shots=1000, seed=42)
# Returns: {"status": "COMPLETED", "counts": {"00": 512, "11": 488}, ...}
```

#### run_circuits_tool

Executes multiple circuits in a batch.

**Parameters:**
- `circuits` (list[dict]): List of circuits to execute
- `backend_name` (str, optional): Backend name
- `shots` (int, optional): Number of shots
- `seed` (int, optional): Random seed

**Returns:** List of result dictionaries

**Example:**
```python
circuits = [circuit1, circuit2, circuit3]
results = run_circuits_tool(circuits, shots=100)
# Returns list of 3 result dictionaries
```

#### transpile_circuit_tool

Transpiles a circuit for optimization or specific backend.

**Parameters:**
- `circuit` (dict): Circuit to transpile
- `optimization_level` (int, optional): 0-3 (default: 1)
- `basis_gates` (list[str], optional): Target basis gates

**Returns:** Transpiled circuit dictionary

**Example:**
```python
transpiled = transpile_circuit_tool(circuit, optimization_level=2)
```

## MCP Resources

### resource://backends

Provides a list of available quantum backends. Updated dynamically based on available providers.

### resource://gates

Provides a list of all available quantum gates in Qiskit.

## Usage Examples

### Create a Bell State

```python
# Create 2-qubit circuit
circuit = create_quantum_circuit(2, 2)

# Create Bell state: |Φ+⟩ = (|00⟩ + |11⟩) / √2
circuit = add_gate(circuit, "h", [0])
circuit = add_gate(circuit, "cx", [0, 1])
circuit = add_measurement(circuit, [0, 1])

# Execute
result = run_circuit(circuit, "aer_simulator", shots=1000)
print(result["counts"])  # Approximately {"00": 500, "11": 500}
```

### Run Grover's Algorithm

```python
def create_grover_circuit(num_qubits, iterations):
    circuit = create_quantum_circuit(num_qubits, num_qubits)
    
    # Initial superposition
    for i in range(num_qubits):
        circuit = add_gate(circuit, "h", [i])
    
    # Grover iterations
    for _ in range(iterations):
        # Oracle (marked state |11...1⟩)
        for i in range(num_qubits):
            circuit = add_gate(circuit, "x", [i])
        circuit = add_gate(circuit, "cx", list(range(num_qubits - 1)), [num_qubits - 1])
        for i in range(num_qubits):
            circuit = add_gate(circuit, "x", [i])
        
        # Diffusion operator
        for i in range(num_qubits):
            circuit = add_gate(circuit, "h", [i])
        for i in range(num_qubits):
            circuit = add_gate(circuit, "x", [i])
        circuit = add_gate(circuit, "cx", list(range(num_qubits - 1)), [num_qubits - 1])
        for i in range(num_qubits):
            circuit = add_gate(circuit, "x", [i])
        for i in range(num_qubits):
            circuit = add_gate(circuit, "h", [i])
    
    # Measurement
    circuit = add_measurement(circuit, list(range(num_qubits)))
    return circuit

circuit = create_grover_circuit(3, 1)
result = run_circuit(circuit, "aer_simulator", shots=1000)
```

### Draw and Analyze Circuit

```python
circuit = create_quantum_circuit(2, 2)
circuit = add_gate(circuit, "h", [0])
circuit = add_gate(circuit, "cx", [0, 1])
circuit = add_measurement(circuit, [0, 1])

# Get depth
depth = get_circuit_depth(circuit)
print(f"Circuit depth: {depth}")

# List gates
gates = list_available_gates()
print(f"Available gates: {len(gates)}")

# Draw circuit
ascii_output = draw_circuit(circuit, "ascii")
print(ascii_output)
```

### Run Shor's Algorithm

```python
from mcp_qiskit import (
    create_quantum_circuit,
    add_gate,
    add_measurement,
    run_circuit,
)

def build_shor_circuit(N=15, a=2, n_count=8):
    """Build Shor's factoring circuit for N=15 using MCX gates."""
    n = N.bit_length()
    circuit = create_quantum_circuit(n_count + n, n_count)
    
    # Superposition on first register
    for i in range(n_count):
        circuit = add_gate(circuit, "h", [i])
    
    # Initialize second register to |1>
    circuit = add_gate(circuit, "x", [n_count])
    
    # Controlled modular exponentiation using MCX
    for i in range(n_count):
        power = pow(a, 2**i, N)
        for j in range(n):
            if (power >> j) & 1:
                circuit = add_gate(circuit, "mcx", [[i], [n_count + j]])
    
    # Inverse QFT (simplified)
    for i in range(n_count - 1, -1, -1):
        for j in range(i + 1, n_count):
            circuit = add_gate(circuit, "cp", [i, j], [3.14159 / (2 ** (j - i))])
        circuit = add_gate(circuit, "h", [i])
    
    # Measure first register
    circuit = add_measurement(circuit, list(range(n_count)))
    return circuit

# Run Shor's algorithm to factor 15
circuit = build_shor_circuit(N=15, a=2, n_count=8)
result = run_circuit(circuit, "aer_simulator", shots=1000)
print(f"Results: {result['counts']}")
```

See `examples/shor_example.py` for a complete implementation with factor extraction.

### Shor's Algorithm with MCP Qiskit Tools

Build Shor's algorithm circuit to factor N=15 using the MCP Qiskit server tools:

```python
# Step 1: Create an 8-qubit circuit with 4 classical bits
circuit = create_quantum_circuit_tool(num_qubits=8, num_classical_bits=4)

# Step 2: Apply H gates to qubits 0-3 (superposition)
circuit = add_gate_tool(circuit=circuit, gate_name="h", qubits=[0, 1, 2, 3])

# Step 3: Apply X gates to qubits 4-7 (initialize to |1⟩)
circuit = add_gate_tool(circuit=circuit, gate_name="x", qubits=[4, 5, 6, 7])

# Step 4: Add modular exponentiation using CP gates
circuit = add_gate_tool(circuit=circuit, gate_name="cp", qubits=[0, 4], params=[3.14159/2])  # CP(π/2)
circuit = add_gate_tool(circuit=circuit, gate_name="cp", qubits=[1, 6], params=[3.14159/4])  # CP(π/4)
circuit = add_gate_tool(circuit=circuit, gate_name="cp", qubits=[2, 4], params=[3.14159])    # CP(π)
circuit = add_gate_tool(circuit=circuit, gate_name="cp", qubits=[3, 4], params=[3.14159])    # CP(π)

# Step 5: Apply inverse QFT using H and CP gates (reverse order)
# CP(π/4) on [2,3], CP(π/2) on [1,2], CP(π) on [0,1]
circuit = add_gate_tool(circuit=circuit, gate_name="cp", qubits=[2, 3], params=[3.14159/4])
circuit = add_gate_tool(circuit=circuit, gate_name="cp", qubits=[1, 2], params=[3.14159/2])
circuit = add_gate_tool(circuit=circuit, gate_name="cp", qubits=[0, 1], params=[3.14159])
# H gates in reverse order
circuit = add_gate_tool(circuit=circuit, gate_name="h", qubits=[3, 2, 1, 0])

# Step 6: Measure qubits 0-3
circuit = add_measurement_tool(circuit=circuit, qubits=[0, 1, 2, 3])

# Step 7: Run on aer_simulator
result = run_circuit_tool(circuit=circuit, backend_name="aer_simulator", shots=1024, seed=42)
print(f"Measurement results: {result['counts']}")

# Extract factors from the measurement result:
# 1. Compute the phase from measurement outcome
# 2. Find order r via continued fractions
# 3. Calculate gcd(a^(r/2) ± 1, N)
# Expected: Factorization of 15 = 3 × 5
```

## Architecture

```
mcp-qiskit/
├── src/mcp_qiskit/
│   ├── __init__.py          # Package exports
│   ├── __main__.py          # CLI entry point
│   ├── _circuit.py           # Circuit operations
│   ├── _backend.py           # Backend management
│   ├── _execution.py         # Circuit execution
│   └── _mcp.py               # MCP server definition
├── tests/                    # Test suite
├── SPEC.md                   # Project specification
└── README.md                 # This file
```

### Module Responsibilities

- **_circuit.py**: Quantum circuit creation, gates, measurements, visualization
- **_backend.py**: Backend discovery, status, configuration
- **_execution.py**: Circuit execution, transpilation
- **_mcp.py**: FastMCP server definition, tool registration

## Requirements

- Python 3.11+
- qiskit >= 2.3.1
- qiskit-aer >= 0.14.0
- fastmcp >= 2.0

## Development

### Setup

```bash
git clone https://github.com/daedalus/mcp-qiskit.git
cd mcp-qiskit
pip install -e ".[all]"
```

### Running Tests

```bash
pytest -v
```

### Code Quality

```bash
# Format code
ruff format src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

### Pre-commit Hooks

```bash
pre-commit install
```

## Troubleshooting

### API Keys and Credentials

This package supports two types of backends:

1. **Aer Simulator** (default) - Runs locally, no API key required
2. **IBM Quantum** - Requires an IBM Quantum API token

#### Using IBM Quantum Backends

To use IBM Quantum backends, you need to provide your API token:

**Option 1: Environment Variable**

```bash
export IBM_QUANTUM_TOKEN="your_api_token_here"
```

Or in your Python code:

```python
import os
os.environ["IBM_QUANTUM_TOKEN"] = "your_api_token_here"
```

**Option 2: Save Credentials via Qiskit**

```python
from qiskit_ibm_provider import IBMProvider

# Save your account (only needs to be done once)
IBMProvider.save_account(token="your_api_token_here", overwrite=True)

# Now you can use IBM backends
from mcp_qiskit._backend import list_backends, get_backend

backends = list_backends()  # Will include IBM backends
backend = get_backend("ibm_qasm_simulator")  # Or specific IBM backend
```

**Getting an IBM Quantum Token:**

1. Create an account at [IBM Quantum](https://quantum.ibm.com/)
2. Go to Account > My Tokens
3. Copy your API token

**Environment Variable for MCP Server:**

When running as an MCP server, set the environment variable before starting:

```bash
export IBM_QUANTUM_TOKEN="your_token"
mcp-qiskit
```

Or in your MCP client configuration:

```json
{
  "mcpServers": {
    "mcp-qiskit": {
      "command": "mcp-qiskit",
      "env": {
        "IBM_QUANTUM_TOKEN": "your_token_here"
      }
    }
  }
}
```

### Backend Not Found

If you get "Backend not found", ensure the backend name is correct:

```python
# List available backends
backends = list_backends()
print([b["name"] for b in backends])
```

### Import Errors

Make sure Qiskit is properly installed:

```bash
pip install qiskit==2.3.1 qiskit-aer
```

### MCP Connection Issues

Verify the server is running:

```bash
mcp-qiskit --help
```

## License

MIT License - see [LICENSE](LICENSE) file.

## Contributing

Contributions are welcome! Please open an issue or submit a PR on GitHub.

## Related Projects

- [Qiskit](https://qiskit.com/) - Quantum computing SDK
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP framework
- [Model Context Protocol](https://modelcontextprotocol.io/) - Protocol specification