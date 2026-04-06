"""Tests for backend module."""

import pytest

from mcp_qiskit._backend import (
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

    def test_list_backends_with_filters(self) -> None:
        """Test listing backends with filters."""
        backends = list_backends(filters={"status": "ONLINE"})
        assert isinstance(backends, list)


class TestGetBackendStatus:
    """Tests for get_backend_status function."""

    def test_get_status_aer(self) -> None:
        """Test getting Aer backend status."""
        backends = list_backends()
        if backends:
            result = get_backend_status(backends[0]["name"])
            assert "name" in result
            assert "status" in result

    def test_get_status_not_found(self) -> None:
        """Test getting status of non-existent backend."""
        with pytest.raises(KeyError, match="not found"):
            get_backend_status("nonexistent_backend_xyz")


class TestGetBackendConfiguration:
    """Tests for get_backend_configuration function."""

    def test_get_config_aer(self) -> None:
        """Test getting Aer backend configuration."""
        backends = list_backends()
        if backends:
            result = get_backend_configuration(backends[0]["name"])
            assert "name" in result
            assert "num_qubits" in result

    def test_get_config_not_found(self) -> None:
        """Test getting config of non-existent backend."""
        with pytest.raises(KeyError, match="not found"):
            get_backend_configuration("nonexistent_backend_xyz")
