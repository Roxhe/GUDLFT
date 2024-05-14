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


def test_purchase_valid_request(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '10'
    }, follow_redirects=True)
    assert b"Great-booking complete!" in response.data
    assert b"3" in response.data


def test_purchase_exceeds_points(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '14'  # More than available points
    }, follow_redirects=True)
    assert b"You cannot book more places than your available points" in response.data
    assert b"13" in response.data
