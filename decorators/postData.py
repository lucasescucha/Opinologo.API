from functools import wraps

from flask import jsonify, request


def data_required(fields):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            json = request.get_json(force=True)

            for field in fields:
                if json.get(field) is None:
                    return jsonify({'message': 'Parámetro' + field + 'no encontrado'}), 400

            return f(*args, **kwargs)
        return decorator
    return wrapper