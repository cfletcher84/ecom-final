from flask import request, jsonify
from schemas.customerSchema import customer_schema, customers_schema
from services import customerService
from marshmallow import ValidationError
from caching import cache




def save():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    customer_save = customerService.save(customer_data)
    return customer_schema.jsonify(customer_save), 201

@cache.cached(timeout=60)
def find_all():
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    customers = customerService.find_all(page, per_page)
    return customers_schema.jsonify(customers), 200

def get_customer(customer_id):
    customer = customerService.get_customer(customer_id)
    if customer:
        pass