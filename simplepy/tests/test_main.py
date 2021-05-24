import pytest
import main


@pytest.fixture
def client():
    main.app.config['TESTING'] = True

    with main.app.test_client() as client:
        with main.app.app_context():
            pass
        yield client


def test_index(client):
    rv = client.get('/')
    assert b'OK' in rv.data
