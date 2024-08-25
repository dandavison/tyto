from io import BytesIO

import duckdb
import pytest

from tyto import create_schema, tyto


@pytest.fixture
def db_connection():
    conn = duckdb.connect(":memory:")
    create_schema(conn)
    yield conn
    conn.close()


def test_parse_junit_xml_passing(db_connection: duckdb.DuckDBPyConnection):
    xml_content = """
    <testsuite name="TestSuite1">
        <testcase name="test_passing" />
    </testsuite>
    """
    tyto(iter([BytesIO(xml_content.encode())]), db_connection)
    result = db_connection.execute("SELECT * FROM test_results").fetchall()
    assert len(result) == 1
    assert result[0] == ("TestSuite1", "test_passing", "Passed")


def test_parse_junit_xml_failing(db_connection: duckdb.DuckDBPyConnection):
    xml_content = """
    <testsuite name="TestSuite1">
        <testcase name="test_failing">
            <failure message="Test failed" />
        </testcase>
    </testsuite>
    """
    tyto(iter([BytesIO(xml_content.encode())]), db_connection)
    result = db_connection.execute("SELECT * FROM test_results").fetchall()
    assert len(result) == 1
    assert result[0] == ("TestSuite1", "test_failing", "Failed")
