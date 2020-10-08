import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
    @app_route('/drinks', methods=['GET'])
    def get_drink():
        drinks = Drink.query.order.all()
        format_drinks = [drink.short() for drink in drinks]
        if len(drinks) == 0 :
            abort(404)

        return jsonify({
            'success': True,
            'drinks': drinks 
        }), 200
        


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
    @app_route('/drinks-detail', methodS=['GET'])
    @requires_auth('get:drinks-detail')
    def drinks_detail(payload):
        drinks = Drink.query.order.all()
        format_drinks = [drink.long() for drink in drinks] 
        if len(drinks) == 0:
            abort(422)
        
        token = get_token_auth_header()
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
    @app_route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def greate_drinks(payload):
        body = request.get_json()
        new_title = body.get('title', None)
        new_recipe = body.get('recpie', None)

        try:
            drinks = Drink(title=new_title, recpie=new_recipe)
            drinks.insert()
            format_drinks = [drink.long() for drink in drinks]

            return jsonify({
                'success'= True,
                'drinks'= drinks
            }), 200
        except:
            abort(422)





'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
    @app_route('/drinks/<int:drink_id>', methods=['PATCH'])
    @requires_auth('patch:drinks')
    def update_drinks(payload, drink_id):
        body = request.get_json()
        new_title = body.get('title', None)
        new_recipe = body.get('recpie', None)
        format_drinks = [drink.long() for drink in drinks]
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        try:
            if title:
                drink.new_title = title
            if recipe:
                drink.new_recipe = recpie
            drink.update()
            return jsonify({
                'success': True,
                'drinks': drink
            }), 200
        except:
            abort(404)




'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
    @app_route('/drinks/<int:drink_id>', merthods=['DELETE'])
    @requires_auth('delete:drinks')
    def delete_drinks(payload, drink_id):
        try:
            drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

            if drink is None:
                abort(404)

            drink.delete()

            return jsonify({
                'success': True,
                'delete': drink_id
            }), 200
        except:
            abort(404)


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
app.register_error_handler(404, not_found)

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(401)
def Auth_error(error):
    return jsonify({
                "success": False, 
                "error": 401,
                "message": "resource not found"
                }), 401

return app