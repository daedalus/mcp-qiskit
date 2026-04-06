#!/usr/bin/env python3
"""
Shor's Algorithm Example - Factoring N=15 using Qiskit MCP Server

This example demonstrates factoring N=15 using Shor's algorithm
via the MCP server tools. Run with: python shor_example.py
"""

import sys

sys.path.insert(0, "src")

from mcp_qiskit._circuit import create_quantum_circuit, add_gate, add_measurement
from mcp_qiskit._execution import run_circuit
from fractions import Fraction
from math import gcd, pi


def build_shor_circuit_mcp(N: int = 15, a: int = 2, n_count: int = 4):
    """Build Shor's factoring circuit for N=15 using MCP tools"""
    n = N.bit_length()
    total_qubits = n_count + n

    circuit = create_quantum_circuit(total_qubits, n_count)

    # Step 1: Superposition on first register (H gates)
    for i in range(n_count):
        circuit = add_gate(circuit, "h", [i])

    # Step 2: Initialize second register to |1>
    for i in range(n):
        circuit = add_gate(circuit, "x", [n_count + i])

    # Step 3: Controlled modular exponentiation using CP gates
    for i in range(n_count):
        power = pow(a, 2**i, N)
        for j in range(n):
            if (power >> j) & 1:
                angle = 2 * pi / (2 ** (j + 1))
                circuit = add_gate(circuit, "cp", [i, n_count + j], [angle])

    # Step 4: Inverse QFT using H and CP gates
    for i in range(n_count - 1, -1, -1):
        for j in range(i + 1, n_count):
            angle = -pi / (2 ** (j - i))
            circuit = add_gate(circuit, "cp", [j, i], [angle])
        circuit = add_gate(circuit, "h", [i])

    # Step 5: Measure first register
    circuit = add_measurement(circuit, list(range(n_count)))

    return circuit


def extract_factors(measurement: int, n_count: int, a: int, N: int):
    """Extract factors from measurement using continued fractions"""
    if measurement == 0:
        return None

    phase = measurement / (2**n_count)
    frac = Fraction(phase).limit_denominator(100)
    r = frac.denominator

    if r > 0 and r % 2 == 0:
        p = gcd(pow(a, r // 2, N) - 1, N)
        q = gcd(pow(a, r // 2, N) + 1, N)
        if p > 1 and p < N:
            return p, N // p
        if q > 1 and q < N:
            return q, N // q

    # Try direct approach
    for r in [measurement, 2**n_count - measurement]:
        if r > 0:
            p = gcd(pow(a, r, N) - 1, N)
            if p > 1 and p < N:
                return p, N // p

    return None


def main():
    N = 15
    a = 2
    n_count = 4

    print("=" * 60)
    print("Shor's Algorithm - Factoring N=15 (MCP Server)")
    print("=" * 60)

    # Build circuit using MCP tools
    circuit = build_shor_circuit_mcp(N, a, n_count)
    print(
        f"\nCircuit: {circuit['num_qubits']} qubits, {len(circuit['operations'])} operations"
    )

    # Execute using Aer simulator
    result = run_circuit(circuit, "aer_simulator", shots=4096, seed=42)

    print(f"\nStatus: {result['status']}")
    print(f"Backend: {result['backend']}")

    counts = result.get("counts", {})
    print(f"\nTop measurement results:")
    for state, count in sorted(counts.items(), key=lambda x: -x[1])[:8]:
        print(f"  |{state}⟩: {count} ({count / 4096 * 100:.1f}%)")

    # Extract factors
    print("\n" + "-" * 60)
    print("Factor Extraction:")

    for state, count in sorted(counts.items(), key=lambda x: -x[1]):
        measurement = int(state, 2)
        factors = extract_factors(measurement, n_count, a, N)
        if factors:
            p, q = factors
            print(f"✓ SUCCESS: {p} × {q} = {N}")
            print(f"  From measurement: {measurement} (r={measurement})")
            return

    print("No factors found - trying alternative extraction...")

    # Alternative: Look at the most frequent results
    for state, count in sorted(counts.items(), key=lambda x: -x[1])[:3]:
        measurement = int(state, 2)
        # Try different r values
        for r in [
            measurement,
            2**n_count - measurement,
            measurement * 2,
            measurement // 2,
        ]:
            if r > 0:
                p = gcd(pow(a, r, N) - 1, N)
                if p > 1 and p < N:
                    print(f"✓ SUCCESS: {p} × {N // p} = {N}")
                    print(f"  Using r={r}")
                    return

    print("No factors extracted in this run")


if __name__ == "__main__":
    main()
