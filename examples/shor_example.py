#!/usr/bin/env python3
"""
Shor's Algorithm Example - Factoring N=15 using Qiskit MCP Server

This example demonstrates factoring N=15 using Shor's algorithm.
Run: python shor_example.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from math import gcd
from fractions import Fraction


def build_shor_circuit(N: int = 15, a: int = 2, n_count: int = 8) -> QuantumCircuit:
    """Build Shor's factoring circuit for N=15"""
    n = N.bit_length()
    qc = QuantumCircuit(n_count + n, n_count)

    # Step 1: Superposition on first register
    for i in range(n_count):
        qc.h(i)

    # Step 2: Initialize second register to |1>
    qc.x(n_count)

    # Step 3: Controlled modular exponentiation using MCX
    for i in range(n_count):
        power = pow(a, 2**i, N)
        for j in range(n):
            if (power >> j) & 1:
                qc.mcx([i], n_count + j)

    # Step 4: Inverse QFT using H and CP gates
    for i in range(n_count - 1, -1, -1):
        for j in range(i + 1, n_count):
            qc.cp(-3.14159 / (2 ** (j - i)), i, j)
        qc.h(i)

    # Step 5: Measure first register
    qc.measure(range(n_count), range(n_count))

    return qc


def extract_factors(
    measurement: int, n_count: int, a: int, N: int
) -> tuple[int, int] | None:
    """Extract factors from measurement using continued fractions"""
    if measurement == 0:
        return None

    phase = measurement / (2**n_count)
    frac = Fraction(phase).limit_denominator(100)
    r = frac.denominator

    if r > 0 and r % 2 == 0:
        p = gcd(pow(a, r // 2, N) - 1, N)
        q = N // p
        if p > 1 and q > 1:
            return p, q

        # Try alternative
        p2 = gcd(pow(a, r // 2, N) + 1, N)
        q2 = N // p2
        if p2 > 1 and q2 > 1:
            return p2, q2

    return None


if __name__ == "__main__":
    N = 15
    a = 2

    print("=" * 60)
    print("Shor's Algorithm - Factoring N=15")
    print("=" * 60)

    # Build circuit
    qc = build_shor_circuit(N, a)
    print(f"\nCircuit: {qc.num_qubits} qubits, depth {qc.depth()}")

    # Execute
    simulator = AerSimulator()
    result = simulator.run(qc, shots=4096).result()
    counts = result.get_counts()

    print(f"\nTop results:")
    for state, count in sorted(counts.items(), key=lambda x: -x[1])[:5]:
        print(f"  |{state}⟩: {count}")

    # Extract factors
    print("\n" + "-" * 60)
    n_count = 8
    for state, count in sorted(counts.items(), key=lambda x: -x[1]):
        x = int(state, 2)
        factors = extract_factors(x, n_count, a, N)
        if factors:
            p, q = factors
            print(f"✓ SUCCESS: {p} × {q} = {N}")
            break
    else:
        print("No factors found in this run")
