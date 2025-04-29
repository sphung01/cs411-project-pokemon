import logging
from typing import List

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db import db
from logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

class Pokemons(db.Model):
    """
        Represents a pokemon in the system

    This model maps the 'pokemons' table in the database and stores
    the attributes such as id, name, attack, and defense. Used in a
    Flask-SQLAlchemy application to manage pokemon data, run simulations,
    and track fight outcomes.

    """

    __tablename__ = 'pokemons'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    attack = db.Column(db.float, nullable=False)
    defense = db.Column(db.float, nullable=False)