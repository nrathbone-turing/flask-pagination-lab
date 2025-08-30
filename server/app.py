#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

class Books(Resource):
    def get(self):
        # Get query params, default page=1, per_page=5
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        # Sanitize inputs
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 5
        if per_page > 100:  # safety limit
            per_page = 100

        # Paginate query
        pagination = Book.query.paginate(page=page, per_page=per_page, error_out=False)

        items = [BookSchema().dump(book) for book in pagination.items]

        return {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": items,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }, 200

api.add_resource(Books, '/books', endpoint='books')


if __name__ == '__main__':
    app.run(port=5555, debug=True)