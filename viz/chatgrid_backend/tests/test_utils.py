import pytest
from unittest.mock import patch, MagicMock
from agent.utils import _get_db_connection

# To run test run: 
# uv run python -m pytest tests/test_utils.py -v

class TestGetDbConnection:
    """Unit tests for _get_db_connection function."""

    @patch("agent.utils.psycopg.connect")
    def test_connection_with_explicit_params(self, mock_connect):
        """Test connection with all parameters provided explicitly."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn, db_name = _get_db_connection(
            database_name="test_db",
            host="localhost",
            port="5432",
            user="test_user",
            password="test_pass"
        )

        mock_connect.assert_called_once_with(
            host="localhost",
            port="5432",
            dbname="test_db",
            user="test_user",
            password="test_pass"
        )
        assert conn == mock_conn
        assert db_name == "test_db"

    @patch.dict("os.environ", {
        "POSTGRES_HOST": "env_host",
        "POSTGRES_PORT": "5433",
        "POSTGRES_DB": "env_db",
        "POSTGRES_USER": "env_user",
        "POSTGRES_PASSWORD": "env_pass"
    })
    @patch("agent.utils.psycopg.connect")
    def test_connection_with_env_vars(self, mock_connect):
        """Test connection using environment variables."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn, db_name = _get_db_connection()

        mock_connect.assert_called_once_with(
            host="env_host",
            port="5433",
            dbname="env_db",
            user="env_user",
            password="env_pass"
        )
        assert conn == mock_conn
        assert db_name == "env_db"

    @patch.dict("os.environ", {}, clear=True)
    def test_missing_required_params_raises_error(self):
        """Test that missing required parameters raise ValueError."""
        with pytest.raises(ValueError, match="Database connection parameters not configured"):
            _get_db_connection()

    @patch.dict("os.environ", {
        "POSTGRES_HOST": "localhost",
        "POSTGRES_PORT": "5432",
        "POSTGRES_DB": "test_db",
        "POSTGRES_USER": "test_user"
    })
    @patch("agent.utils.psycopg.connect")
    def test_connection_failure_raises_exception(self, mock_connect):
        """Test that connection failure propagates the exception."""
        mock_connect.side_effect = Exception("Connection refused")

        with pytest.raises(Exception, match="Connection refused"):
            _get_db_connection()

    @patch.dict("os.environ", {
        "POSTGRES_HOST": "default_host",
        "POSTGRES_PORT": "5432",
        "POSTGRES_DB": "default_db",
        "POSTGRES_USER": "default_user",
        "POSTGRES_PASSWORD": "default_pass"
    })
    @patch("agent.utils.psycopg.connect")
    def test_explicit_params_override_env_vars(self, mock_connect):
        """Test that explicit parameters override environment variables."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn, db_name = _get_db_connection(
            database_name="override_db",
            host="override_host"
        )

        mock_connect.assert_called_once_with(
            host="override_host",
            port="5432",
            dbname="override_db",
            user="default_user",
            password="default_pass"
        )
        assert db_name == "override_db"