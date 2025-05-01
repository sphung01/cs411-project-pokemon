from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# from flask_cors import CORS

from config import ProductionConfig

from models.user_model import Users
from models.pokemon_model import Pokemons
from models.pokemon_battle_model import BattleModel
from db import db
from models.logger import configure_logger

import requests

load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    configure_logger(app.logger)
    app.config.from_object(config_class)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.filter_by(username=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        return make_response(jsonify({
            "status": "error",
            "message": "Authentication required"
        }), 401)

    pokemon_model = Pokemons()
    battle_model = BattleModel()

    ####################################################
    #
    # Healthchecks
    #
    ####################################################

    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        app.logger.info("Health check endpoint hit")
        return make_response(jsonify({
            'status': 'success',
            'message': 'Service is running'
        }), 200)

    ##########################################################
    #
    # User Management
    #
    #########################################################

    @app.route('/api/create-user', methods=['PUT'])
    def create_user() -> Response:
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Username and password are required"
                }), 400)

            Users.create_user(username, password)
            return make_response(jsonify({
                "status": "success",
                "message": f"User '{username}' created successfully"
            }), 201)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"User creation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while creating user",
                "details": str(e)
            }), 500)

    @app.route('/api/login', methods=['POST'])
    def login() -> Response:
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Username and password are required"
                }), 400)

            if Users.check_password(username, password):
                user = Users.query.filter_by(username=username).first()
                login_user(user)
                return make_response(jsonify({
                    "status": "success",
                    "message": f"User '{username}' logged in successfully"
                }), 200)
            else:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid username or password"
                }), 401)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 401)
        except Exception as e:
            app.logger.error(f"Login failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred during login",
                "details": str(e)
            }), 500)

    @app.route('/api/logout', methods=['POST'])
    @login_required
    def logout() -> Response:
        logout_user()
        return make_response(jsonify({
            "status": "success",
            "message": "User logged out successfully"
        }), 200)

    @app.route('/api/change-password', methods=['POST'])
    @login_required
    def change_password() -> Response:
        try:
            data = request.get_json()
            new_password = data.get("new_password")

            if not new_password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "New password is required"
                }), 400)

            username = current_user.username
            Users.update_password(username, new_password)
            return make_response(jsonify({
                "status": "success",
                "message": "Password changed successfully"
            }), 200)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Password change failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while changing password",
                "details": str(e)
            }), 500)

    @app.route('/api/reset-users', methods=['DELETE'])
    def reset_users() -> Response:
        try:
            app.logger.info("Received request to recreate Users table")
            with app.app_context():
                Users.__table__.drop(db.engine)
                Users.__table__.create(db.engine)
            app.logger.info("Users table recreated successfully")
            return make_response(jsonify({
                "status": "success",
                "message": f"Users table recreated successfully"
            }), 200)

        except Exception as e:
            app.logger.error(f"Users table recreation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while deleting users",
                "details": str(e)
            }), 500)

    ##########################################################
    #
    # Pokemons
    #
    ##########################################################

    @app.route('/api/fetch-pokemon/<string:name>', methods=['GET'])
    def fetch_pokemon(name):
        existing_pokemon = Pokemons.query.filter_by(name=name.lower()).first()
        if existing_pokemon:
            return jsonify({
                "status": "success",
                "pokemon": {
                    "name": existing_pokemon.name,
                    "attack": existing_pokemon.attack,
                    "defense": existing_pokemon.defense
                },
                "source": "local database"
            }), 200

        url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'
        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": f"Pokémon '{name}' not found in PokéAPI."
            }), 404

        data = response.json()
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        attack = stats.get('attack')
        defense = stats.get('defense')

        new_pokemon = Pokemons(name=name.lower(), attack=attack, defense=defense)
        db.session.add(new_pokemon)
        db.session.commit()

        return jsonify({
            "status": "success",
            "pokemon": {
                "name": name.lower(),
                "attack": attack,
                "defense": defense
            },
            "source": "external API and saved to DB"
        }), 201

    @app.route('/api/enter-ring', methods=['POST'])
    @login_required
    def enter_ring():
        data = request.get_json()
        name = data.get("name")

        if not name:
            return make_response(jsonify({
                "status": "error",
                "message": "Missing Pokémon name"
            }), 400)

        pokemon = Pokemons.query.filter_by(name=name.lower()).first()
        if not pokemon:
            return make_response(jsonify({
                "status": "error",
                "message": f"Pokémon '{name}' not found"
            }), 404)

        try:
            battle_model.enter_battlefield(pokemon.id)
        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)

        return jsonify({
            "status": "success",
            "message": f"Pokémon '{name}' entered the ring"
        }), 200

    @app.route('/api/battle', methods=['GET'])
    @login_required
    def battle():
        try:
            winner = battle_model.battle()
            return jsonify({
                "status": "success",
                "winner": winner
            }), 200
        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)

    return app

if __name__ == '__main__':
    app = create_app()
    app.logger.info("Starting Flask app...")
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        app.logger.error(f"Flask app encountered an error: {e}")
    finally:
        app.logger.info("Flask app has stopped.")
