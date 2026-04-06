"""Tests for backend module."""

import pytest

from mcp_qiskit._backend import (
    get_backend,
    get_backend_configuration,
    get_backend_status,
    list_backends,
)


class TestListBackends:
    """Tests for list_backends function."""

    def test_list_backends_aer(self) -> None:
        """Test listing backends with Aer."""
        backends = list_backends()
        assert isinstance(backends, list)
        assert len(backends) > 0
        assert any(b["name"] == "aer_simulator" for b in backends)

    def test_list_backends_with_filters(self) -> None:
        """Test listing backends with filters."""
        backends = list_backends(filters={"status": "ONLINE"})
        assert isinstance(backends, list)

    def test_list_backends_filter_by_name(self) -> None:
        """Test filtering backends by name."""
        backends = list_backends(filters={"name": "aer_simulator"})
        assert len(backends) >= 1

    def test_list_backends_qasm_simulator(self) -> None:
        """Test that qasm_simulator is listed."""
        backends = list_backends()
        names = [b["name"] for b in backends]
        assert "qasm_simulator" in names


class TestGetBackendStatus:
    """Tests for get_backend_status function."""

    def test_get_status_aer(self) -> None:
        """Test getting Aer backend status."""
        result = get_backend_status("aer_simulator")
        assert "name" in result
        assert "status" in result
        assert result["name"] == "aer_simulator"
        assert result["status"] == "ONLINE"

    def test_get_status_qasm(self) -> None:
        """Test getting QASM backend status."""
        result = get_backend_status("qasm_simulator")
        assert result["status"] == "ONLINE"

    def test_get_status_not_found(self) -> None:
        """Test getting status of non-existent backend."""
        with pytest.raises(KeyError, match="not found"):
            get_backend_status("nonexistent_backend_xyz")


class TestGetBackendConfiguration:
    """Tests for get_backend_configuration function."""

    def test_get_config_aer(self) -> None:
        """Test getting Aer backend configuration."""
        result = get_backend_configuration("aer_simulator")
        assert "name" in result
        assert "num_qubits" in result
        assert result["name"] == "aer_simulator"

    def test_get_config_qasm(self) -> None:
        """Test getting QASM backend configuration."""
        result = get_backend_configuration("qasm_simulator")
        assert result["name"] == "qasm_simulator"
        assert "basis_gates" in result

    def test_get_config_not_found(self) -> None:
        """Test getting config of non-existent backend."""
        with pytest.raises(KeyError, match="not found"):
            get_backend_configuration("nonexistent_backend_xyz")


class TestGetBackend:
    """Tests for get_backend function."""

    def test_get_backend_aer(self) -> None:
        """Test getting Aer backend instance."""
        backend = get_backend("aer_simulator")
        assert backend is not None
        assert backend.name == "aer_simulator"

    def test_get_backend_qasm(self) -> None:
        """Test getting QASM backend instance."""
        backend = get_backend("qasm_simulator")
        assert backend is not None

    def test_get_backend_not_found(self) -> None:
        """Test getting non-existent backend."""
        with pytest.raises(KeyError, match="not found"):
            get_backend("nonexistent_backend_xyz")
