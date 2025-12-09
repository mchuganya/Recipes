import json
import sys
import re
from models import db, Recipe
from app import app

NUM_RE = re.compile(r"[-+]?[0-9]*\.?[0-9]+")


def parse_int(val):
    if val is None:
        return None
    try:
        # handle strings like "NaN"
        if isinstance(val, str):
            if val.strip().lower() == 'nan':
                return None
            m = NUM_RE.search(val)
            if m:
                return int(float(m.group(0)))
            return None
        if isinstance(val, (int, float)):
            if isinstance(val, float) and (val != val):  # NaN check
                return None
            return int(val)
    except Exception:
        return None


def parse_float(val):
    if val is None:
        return None
    try:
        if isinstance(val, str):
            if val.strip().lower() == 'nan':
                return None
            m = NUM_RE.search(val)
            if m:
                return float(m.group(0))
            return None
        if isinstance(val, (int, float)):
            if isinstance(val, float) and (val != val):
                return None
            return float(val)
    except Exception:
        return None


def extract_calories(nutrients):
    if not nutrients:
        return None
    try:
        c = nutrients.get('calories')
        if not c:
            return None
        m = NUM_RE.search(str(c))
        if m:
            return int(float(m.group(0)))
    except Exception:
        return None


def load(json_path):
    with app.app_context():
        db.create_all()
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # data might be a list or dict with key
        if isinstance(data, dict):
            # try to find list inside
            # common key names: recipes, data
            for k in ('recipes', 'data', 'items'):
                if k in data and isinstance(data[k], list):
                    data = data[k]
                    break
            else:
                # if dict is single recipe
                data = [data]

        count = 0
        for item in data:
            cuisine = item.get('cuisine')
            title = item.get('title') or item.get('name')
            rating = parse_float(item.get('rating'))
            prep_time = parse_int(item.get('prep_time'))
            cook_time = parse_int(item.get('cook_time'))
            total_time = parse_int(item.get('total_time'))
            description = item.get('description')
            nutrients = item.get('nutrients')
            serves = item.get('serves')

            calories = extract_calories(nutrients) if isinstance(nutrients, dict) else None

            # store nutrients as JSON string
            nutrients_text = None
            try:
                if nutrients is not None:
                    nutrients_text = json.dumps(nutrients)
            except Exception:
                nutrients_text = None

            recipe = Recipe(
                cuisine=cuisine,
                title=title,
                rating=rating,
                prep_time=prep_time,
                cook_time=cook_time,
                total_time=total_time,
                description=description,
                nutrients=nutrients_text,
                serves=serves,
                calories=calories
            )
            db.session.add(recipe)
            count += 1
        db.session.commit()
        print(f"Loaded {count} recipes into the database")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python load_data.py <recipes.json>')
        sys.exit(1)
    load(sys.argv[1])
