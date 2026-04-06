"""Quantum backend management functionality."""

from typing import Any

from qiskit.providers import Backend


def list_backends(filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """List available quantum backends.

    Args:
        filters: Optional dictionary of filters to apply (e.g., {'status': 'ONLINE'}).

    Returns:
        List of backend information dictionaries.

    Example:
        >>> backends = list_backends()
        >>> len(backends) > 0
        True
    """
    backends = []

    try:
        from qiskit_ibm_provider import IBMProvider

        try:
            provider = IBMProvider()
            available_backends = provider.backends()
            for backend in available_backends:
                try:
                    status = backend.status()
                    backends.append(
                        {
                            "name": backend.name,
                            "status": status.status_msg,
                            "num_qubits": backend.configuration().num_qubits,
                            "is_virtual": getattr(backend, "is_virtual", False),
                        }
                    )
                except Exception:
                    pass
        except Exception:
            pass
    except ImportError:
        pass

    try:
        from qiskit_aer import AerSimulator

        backends.append(
            {
                "name": "aer_simulator",
                "status": "ONLINE",
                "num_qubits": 128,
                "is_virtual": True,
            }
        )

        for method in ["density_matrix", "unitary", "matrix_product_state"]:
            backends.append(
                {
                    "name": f"aer_simulator_{method}",
                    "status": "ONLINE",
                    "num_qubits": 128,
                    "is_virtual": True,
                }
            )
    except ImportError:
        pass

    try:
        from qiskit_aer import QasmSimulator

        backends.append(
            {
                "name": "qasm_simulator",
                "status": "ONLINE",
                "num_qubits": 128,
                "is_virtual": True,
            }
        )
    except ImportError:
        pass

    try:
        from qiskit_qcd import QiskitChiralDynamicsBackend

        backends.append(
            {
                "name": "qcd_simulator",
                "status": "ONLINE",
                "num_qubits": 50,
                "is_virtual": True,
            }
        )
    except ImportError:
        pass

    if filters:
        filtered = []
        for backend in backends:
            match = True
            for key, value in filters.items():
                if backend.get(key) != value:
                    match = False
                    break
            if match:
                filtered.append(backend)
        return filtered

    return backends


def get_backend_status(backend_name: str) -> dict[str, Any]:
    """Get the status of a specific quantum backend.

    Args:
        backend_name: Name of the backend.

    Returns:
        Dictionary containing backend status information.

    Example:
        >>> status = get_backend_status('aer_simulator')
        >>> 'status' in status
        True
    """
    backends = list_backends()

    for backend in backends:
        if backend["name"] == backend_name:
            return {
                "name": backend["name"],
                "status": backend["status"],
                "num_qubits": backend["num_qubits"],
            }

    available = [b["name"] for b in backends]
    raise KeyError(
        f"Backend '{backend_name}' not found. Available backends: {available}"
    )


def get_backend_configuration(backend_name: str) -> dict[str, Any]:
    """Get detailed configuration of a quantum backend.

    Args:
        backend_name: Name of the backend.

    Returns:
        Dictionary containing detailed backend configuration.

    Example:
        >>> config = get_backend_configuration('aer_simulator')
        >>> 'num_qubits' in config
        True
    """
    try:
        from qiskit_ibm_provider import IBMProvider

        provider = IBMProvider()
        backend = provider.get_backend(backend_name)
        config = backend.configuration()

        return {
            "name": config.backend_name,
            "num_qubits": config.num_qubits,
            "coupling_map": config.coupling_map,
            "basis_gates": config.basis_gates,
            "quantum_volume": getattr(config, "quantum_volume", None),
            "max_experiments": getattr(config, "max_experiments", None),
            "max_shots": getattr(config, "max_shots", None),
        }
    except Exception:
        pass

    try:
        if backend_name == "aer_simulator":

            return {
                "name": "aer_simulator",
                "num_qubits": 128,
                "coupling_map": None,
                "basis_gates": [
                    "i",
                    "x",
                    "y",
                    "z",
                    "h",
                    "s",
                    "sdg",
                    "t",
                    "tdg",
                    "rx",
                    "ry",
                    "rz",
                    "cx",
                    "cz",
                    "swap",
                    "cu1",
                    "cu3",
                ],
                "max_shots": 100000,
            }
        elif backend_name == "qasm_simulator":

            return {
                "name": "qasm_simulator",
                "num_qubits": 128,
                "coupling_map": None,
                "basis_gates": [
                    "i",
                    "x",
                    "y",
                    "z",
                    "h",
                    "s",
                    "sdg",
                    "t",
                    "tdg",
                    "rx",
                    "ry",
                    "rz",
                    "cx",
                    "cz",
                    "swap",
                ],
                "max_shots": 100000,
            }
    except Exception:
        pass

    available = [b["name"] for b in list_backends()]
    raise KeyError(
        f"Backend '{backend_name}' not found. Available backends: {available}"
    )


def get_backend(backend_name: str) -> Backend:
    """Get a backend instance by name.

    Args:
        backend_name: Name of the backend.

    Returns:
        Qiskit Backend instance.

    Example:
        >>> backend = get_backend('aer_simulator')
        >>> backend.name
        'aer_simulator'
    """
    try:
        from qiskit_ibm_provider import IBMProvider

        provider = IBMProvider()
        return provider.get_backend(backend_name)
    except Exception:
        pass

    try:
        if backend_name == "aer_simulator":
            from qiskit_aer import AerSimulator

            return AerSimulator()
        elif backend_name == "qasm_simulator":
            from qiskit_aer import QasmSimulator

            return QasmSimulator()
    except Exception:
        pass

    available = [b["name"] for b in list_backends()]
    raise KeyError(
        f"Backend '{backend_name}' not found. Available backends: {available}"
    )
