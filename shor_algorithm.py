from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from fractions import Fraction
import math
import numpy as np

# Build Shor's algorithm circuit for N=15
qc = QuantumCircuit(8, 4)

# Step 2: Apply H gates to qubits 0-3 (superposition)
for i in range(4):
    qc.h(i)

# Step 3: Apply X gates to qubits 4-7 (initialize to |1⟩)
for i in range(4, 8):
    qc.x(i)

# Step 4: Add modular exponentiation using CP gates
# CP(π/2) on [0,4]
qc.cp(math.pi / 2, 0, 4)
# CP(π/4) on [1,6]
qc.cp(math.pi / 4, 1, 6)
# CP(π) on [2,4]
qc.cp(math.pi, 2, 4)
# CP(π) on [3,4]
qc.cp(math.pi, 3, 4)

# Step 5: Apply inverse QFT using H and CP gates (reverse order)
# IQFT on qubits 0-3
# Start from qubit 3 down to 0
# Qubit 3
qc.h(3)
qc.cp(-math.pi / 2, 2, 3)
qc.cp(-math.pi / 4, 1, 3)
qc.cp(-math.pi / 8, 0, 3)

# Qubit 2
qc.h(2)
qc.cp(-math.pi / 2, 1, 2)
qc.cp(-math.pi / 4, 0, 2)

# Qubit 1
qc.h(1)
qc.cp(-math.pi / 2, 0, 1)

# Qubit 0
qc.h(0)

# Step 6: Measure qubits 0-3
qc.measure([0, 1, 2, 3], [0, 1, 2, 3])

# Draw the circuit
print("=" * 60)
print("SHOR'S ALGORITHM CIRCUIT FOR N=15")
print("=" * 60)
print("\nCircuit diagram:")
print(qc.draw())

# Step 7: Run on aer_simulator
simulator = AerSimulator()
job = simulator.run(qc, shots=1000)
result = job.result()
counts = result.get_counts()

print("\n" + "=" * 60)
print("MEASUREMENT RESULTS")
print("=" * 60)
print(f"Counts: {counts}")

# Extract factors from measurement result
N = 15

print("\n" + "=" * 60)
print("FACTOR EXTRACTION")
print("=" * 60)

for measured_value, count in counts.items():
    print(f"\nMeasured value: {measured_value} (count: {count})")

    # Convert to integer
    x = int(measured_value, 2)
    print(f"  Binary {measured_value} = decimal {x}")

    # Compute the phase: x / 2^n where n=4 (number of measure qubits)
    n = 4
    phase = x / (2**n)
    print(f"  Phase = {x}/16 = {phase}")

    # Get fraction representation
    frac = Fraction(phase).limit_denominator(15)
    print(f"  Continued fraction: {frac}")

    # The denominator is the guess for r
    r = frac.denominator
    print(f"  Guess for r = {r}")

    if r % 2 == 1:
        print(f"  r is odd, skipping...")
        continue

    print(f"  r is even, trying to extract factors...")

    # Try a^r ± 1
    for a in [2, 3, 4, 5, 6, 7, 8]:
        try:
            # Compute a^r mod N
            power_result = pow(a, r, N)
            print(f"    a={a}: {a}^{r} mod {N} = {power_result}")

            if power_result != 1:
                # Try gcd(a^r - 1, N)
                g1 = math.gcd(power_result - 1, N)
                g2 = math.gcd(power_result + 1, N)

                if g1 != 1 and g1 != N:
                    print(f"    gcd({power_result}-1, {N}) = {g1}")
                    if g1 * (N // g1) == N:
                        print(f"    *** FACTOR FOUND: {g1} × {N // g1} = {N} ***")

                if g2 != 1 and g2 != N:
                    print(f"    gcd({power_result}+1, {N}) = {g2}")
                    if g2 * (N // g2) == N:
                        print(f"    *** FACTOR FOUND: {g2} × {N // g2} = {N} ***")
        except Exception as e:
            print(f"    a={a}: error {e}")

print("\n" + "=" * 60)
print("EXPECTED FACTORIZATION: 15 = 3 × 5")
print("=" * 60)
