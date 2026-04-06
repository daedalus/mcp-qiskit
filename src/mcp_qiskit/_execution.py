"""Quantum circuit execution functionality."""

import time
from typing import Any

import qiskit

from ._backend import get_backend, list_backends
from ._circuit import _circuit_to_dict, _dict_to_circuit


def run_circuit(
    circuit: dict[str, Any],
    backend_name: str = "aer_simulator",
    shots: int | None = 1024,
    seed: int | None = None,
) -> dict[str, Any]:
    """Execute a quantum circuit on a backend.

    Args:
        circuit: Dictionary representation of the quantum circuit.
        backend_name: Name of the backend to execute on.
        shots: Number of measurement shots (None for statevector simulation).
        seed: Optional seed for reproducibility.

    Returns:
        Dictionary containing execution results.

    Example:
        >>> circuit = create_quantum_circuit(2, 2)
        >>> add_gate(circuit, 'h', [0])
        >>> add_gate(circuit, 'cx', [0, 1])
        >>> add_measurement(circuit, [0, 1])
        >>> result = run_circuit(circuit)
        >>> 'counts' in result
        True
    """
    qc = _dict_to_circuit(circuit)

    if not backend_name:
        available = [b["name"] for b in list_backends()]
        if not available:
            backend_name = "aer_simulator"
        else:
            backend_name = available[0]

    try:
        backend = get_backend(backend_name)
    except KeyError:
        from qiskit_aer import AerSimulator

        backend = AerSimulator()

    start_time = time.time()

    try:
        if shots is None:
            from qiskit.quantum_info import Statevector

            state = Statevector(qc)
            result_data = {"statevector": state.data.tolist()}
        else:
            job = backend.run(qc, shots=shots, seed=seed if seed else 42)
            result = job.result()

            # Check if circuit has measurements
            has_measurements = any(inst.operation.name == "measure" for inst in qc.data)

            if has_measurements:
                counts = result.get_counts(qc)
                result_data = {"counts": counts}
            else:
                # Return statevector for circuits without measurements
                from qiskit.quantum_info import Statevector

                state = Statevector(qc)
                result_data = {"statevector": state.data.tolist()}

            if hasattr(result, "time_taken"):
                result_data["time_taken"] = result.time_taken
    except Exception as e:
        raise RuntimeError(f"Execution failed: {str(e)}") from e

    end_time = time.time()

    return {
        "status": "COMPLETED",
        "backend": backend_name,
        "shots": shots,
        "seed": seed,
        "time_taken": end_time - start_time,
        **result_data,
    }


def run_circuits(
    circuits: list[dict[str, Any]],
    backend_name: str = "aer_simulator",
    shots: int | None = 1024,
    seed: int | None = None,
) -> list[dict[str, Any]]:
    """Execute multiple quantum circuits on a backend.

    Args:
        circuits: List of dictionary representations of quantum circuits.
        backend_name: Name of the backend to execute on.
        shots: Number of measurement shots (None for statevector simulation).
        seed: Optional seed for reproducibility.

    Returns:
        List of result dictionaries.

    Example:
        >>> circuits = [create_quantum_circuit(2, 2) for _ in range(3)]
        >>> results = run_circuits(circuits)
        >>> len(results)
        3
    """
    if not circuits:
        raise ValueError("At least one circuit must be provided")

    if len(circuits) > 100:
        raise ValueError("Maximum 100 circuits per batch execution")

    qiskit_circuits = [_dict_to_circuit(c) for c in circuits]

    available = [b["name"] for b in list_backends()]
    if backend_name not in available:
        backend_name = "aer_simulator"

    try:
        backend = get_backend(backend_name)
    except KeyError:
        from qiskit_aer import AerSimulator

        backend = AerSimulator()

    start_time = time.time()

    try:
        if shots is None:
            from qiskit.quantum_info import Statevector

            results = []
            for qc in qiskit_circuits:
                state = Statevector(qc)
                results.append(
                    {
                        "status": "COMPLETED",
                        "statevector": state.data.tolist(),
                    }
                )
        else:
            job = backend.run(qiskit_circuits, shots=shots, seed=seed if seed else 42)
            job_result = job.result()

            results = []
            if hasattr(job_result, "results"):
                for result in job_result.results:
                    if hasattr(result.data, "counts"):
                        counts = dict(result.data.counts)
                    else:
                        counts = {}
                    results.append(
                        {
                            "status": "COMPLETED",
                            "counts": counts,
                        }
                    )
            else:
                counts = job_result.get_counts()
                results.append(
                    {
                        "status": "COMPLETED",
                        "counts": counts,
                    }
                )
    except Exception as e:
        raise RuntimeError(f"Batch execution failed: {str(e)}") from e

    end_time = time.time()
    total_time = end_time - start_time

    for r in results:
        r["backend"] = backend_name
        r["shots"] = shots
        r["seed"] = seed
        r["time_taken"] = total_time / len(results)

    return results


def transpile_circuit(
    circuit: dict[str, Any],
    optimization_level: int = 1,
    basis_gates: list[str] | None = None,
) -> dict[str, Any]:
    """Transpile a quantum circuit for a specific backend.

    Args:
        circuit: Dictionary representation of the quantum circuit.
        optimization_level: Optimization level (0-3).
        basis_gates: Optional list of basis gates to target.

    Returns:
        Transpiled circuit dictionary.

    Example:
        >>> circuit = create_quantum_circuit(2, 0)
        >>> add_gate(circuit, 'h', [0])
        >>> transpiled = transpile_circuit(circuit)
        >>> transpiled['num_qubits']
        2
    """
    qc = _dict_to_circuit(circuit)

    transpiled_qc = qiskit.transpile(
        qc,
        optimization_level=optimization_level,
        basis_gates=basis_gates,
    )

    return _circuit_to_dict(transpiled_qc)
