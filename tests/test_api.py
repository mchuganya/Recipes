import json
import pytest
from app import app, db
import load_data


@pytest.fixture(scope='module')
def client():
    # prepare app and load sample data
    with app.app_context():
        db.drop_all()
        db.create_all()
        load_data.load('recipes.json')
        with app.test_client() as client:
            yield client


def test_get_recipes(client):
    resp = client.get('/api/recipes?page=1&limit=10')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, dict)
    assert data.get('total') == 5
    assert len(data.get('data', [])) == 5
    # highest rating should be first (4.9)
    assert data['data'][0]['rating'] == 4.9


def test_search_pie(client):
    resp = client.get('/api/recipes/search?calories=%3C%3D400&title=pie&rating=%3E%3D4.5')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'data' in data
    assert len(data['data']) == 1
    assert 'Sweet Potato Pie' in data['data'][0]['title']


def test_nan_handling(client):
    resp = client.get('/api/recipes')
    assert resp.status_code == 200
    data = resp.get_json()
    # find Margherita pizza and ensure NaN fields are null
    pizza = next((r for r in data['data'] if 'Margherita' in r['title']), None)
    assert pizza is not None
    assert pizza['rating'] is None
    assert pizza['prep_time'] is None
