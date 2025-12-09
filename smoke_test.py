import json
from app import app, db


def pretty_print(title, obj):
    print('\n' + '='*40)
    print(title)
    print('='*40)
    print(json.dumps(obj, indent=2, ensure_ascii=False))


with app.app_context():
    # ensure DB/tables exist
    db.create_all()
    client = app.test_client()

    # GET /api/recipes
    resp = client.get('/api/recipes?page=1&limit=10')
    try:
        data = resp.get_json()
    except Exception:
        data = {'status_code': resp.status_code, 'data': resp.data.decode()}
    pretty_print('GET /api/recipes?page=1&limit=10', data)

    # Search example
    resp2 = client.get('/api/recipes/search?calories=%3C%3D400&title=pie&rating=%3E%3D4.5')
    try:
        data2 = resp2.get_json()
    except Exception:
        data2 = {'status_code': resp2.status_code, 'data': resp2.data.decode()}
    pretty_print('GET /api/recipes/search?calories=<=400&title=pie&rating=>=4.5', data2)

    print('\nSmoke tests completed.')
