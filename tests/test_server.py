import pytest
from flask import url_for
from server import create_app


@pytest.fixture
def client():
    app = create_app({'TESTING': True, 'SECRET_KEY': 'something_special'})
    with app.test_client() as client:
        yield client


def test_show_summary_valid_email(client):
    valid_email = 'john@simplylift.co'
    response = client.post('/showSummary', data={'email': valid_email})
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_show_summary_invalid_email(client):
    invalid_email = 'invalid@email.com'
    response = client.post('/showSummary', data={'email': invalid_email}, follow_redirects=False)
    assert response.status_code == 302, "Should redirect when email is not found"
    assert response.location.endswith(url_for('index')), "Should redirect to the index page"
