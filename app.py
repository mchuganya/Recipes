import os
import re
import json
from flask import Flask, request, jsonify, send_from_directory
from models import db, Recipe
from sqlalchemy import desc
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv('DATABASE_URL', 'sqlite:///recipes.db')

app = Flask(__name__, static_folder='frontend', static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# helpers
OP_RE = re.compile(r"^(<=|>=|=|<|>)(\d+)$")

def parse_op_value(s):
    # s like ">=4.5" or "<=400" or "400"
    if not s:
        return None
    m = OP_RE.match(s)
    if m:
        op, val = m.groups()
        return op, int(val)
    # try numeric
    try:
        return '=', int(s)
    except Exception:
        return None

@app.route('/api/recipes')
def get_recipes():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({"error": "page and limit must be integers"}), 400
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10

    query = Recipe.query.order_by(desc(Recipe.rating))
    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()
    data = [r.to_dict() for r in items]
    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "data": data
    })

@app.route('/api/recipes/search')
def search_recipes():
    args = request.args
    query = Recipe.query

    # title partial match
    title = args.get('title')
    if title:
        query = query.filter(Recipe.title.ilike(f"%{title}%"))

    # cuisine exact
    cuisine = args.get('cuisine')
    if cuisine:
        query = query.filter(Recipe.cuisine == cuisine)

    # total_time filter
    total_time = args.get('total_time')
    if total_time:
        parsed = parse_op_value(total_time)
        if parsed:
            op, val = parsed
            if op == '=':
                query = query.filter(Recipe.total_time == val)
            elif op == '<=':
                query = query.filter(Recipe.total_time <= val)
            elif op == '>=':
                query = query.filter(Recipe.total_time >= val)
            elif op == '<':
                query = query.filter(Recipe.total_time < val)
            elif op == '>':
                query = query.filter(Recipe.total_time > val)

    # rating filter
    rating = args.get('rating')
    if rating:
        # rating might be float
        m = re.match(r'^(<=|>=|=|<|>){0,1}([0-9]+\.?[0-9]*)$', rating)
        if m:
            op = m.group(1) or '='
            val = float(m.group(2))
            if op == '=':
                query = query.filter(Recipe.rating == val)
            elif op == '<=':
                query = query.filter(Recipe.rating <= val)
            elif op == '>=':
                query = query.filter(Recipe.rating >= val)
            elif op == '<':
                query = query.filter(Recipe.rating < val)
            elif op == '>':
                query = query.filter(Recipe.rating > val)

    # calories filter (use numeric calories column)
    calories = args.get('calories')
    if calories:
        parsed = parse_op_value(calories)
        if parsed:
            op, val = parsed
            if op == '=':
                query = query.filter(Recipe.calories == val)
            elif op == '<=':
                query = query.filter(Recipe.calories <= val)
            elif op == '>=':
                query = query.filter(Recipe.calories >= val)
            elif op == '<':
                query = query.filter(Recipe.calories < val)
            elif op == '>':
                query = query.filter(Recipe.calories > val)

    results = query.all()
    data = [r.to_dict() for r in results]
    return jsonify({"data": data})

# serve frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Run without debugger and without the reloader to avoid intermittent
    # connection refusals caused by the debug reloader restarting the process.
    # Bind to localhost for local development tests.
    app.run(debug=False, use_reloader=False, host='127.0.0.1', port=5000)
