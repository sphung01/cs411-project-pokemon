import logging
from typing import List

from sqlalchemy.exc import IntegrityError, SQLAlchemyError


from db import db
from models.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


class Pokemons(db.Model):
    """Represents a competitive pokemon in the system.

    This model maps to the 'pokemons' table in the database and stores information
    related to a pokemons name, id, and battle stats. Used in a Flask-SQLAlchemy application to
    manage pokemons data, and run fights.

    """

    __tablename__ = 'pokemons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    attack = db.Column(db.Float, nullable=False)
    defense = db.Column(db.Float, nullable=False)

    def __init__(self, name: str, attack: float, defense: float):
        """Initialize a new pokemon instance with basic attributes.

        Args:
            name (str): The pokemon's name. Must be unique.
            attack (float): The pokemon's attack stat. Must be greater than 0
            defense (float): The pokemons's defense stat. Must be greater than 0.

        Raises:
            ValueError: If any required fields are invalid

        """

        existing = Pokemons.query.filter_by(name=name).first()
        if existing:
            raise ValueError(f"pokemon with name '{name}' already exists.")

        if not name or not isinstance(name, str):
            raise ValueError("Pokemon must be a non-empty string.")
        if not isinstance(attack, float) or attack <= 0:
            raise ValueError("attack must be a float and at least 0")
        if not isinstance(defense, float) or defense <= 0:
            raise ValueError("defense must be a float and greater than 0.")
        
        self.name = name 
        self.defense = float(defense)
        self.attack = float(attack)

    @classmethod
    def get_attack(cls, attack: float) -> str:
        """Get the attack stat.

        This method is defined as a class method rather than a static method,
        even though it does not currently require access to the class object.
        Both @staticmethod and @classmethod would be valid choices in this context;
        however, using @classmethod makes it easier to support subclass-specific
        behavior or logic overrides in the future.

        Args:
            attack: The attack stat of the pokemon.

        Returns:
            float: The pokemon's attack stat.
        """
        return attack
    
    @classmethod
    def get_defense(cls, defense: float) -> str:
        """Get the defense stat.

        This method is defined as a class method rather than a static method,
        even though it does not currently require access to the class object.
        Both @staticmethod and @classmethod would be valid choices in this context;
        however, using @classmethod makes it easier to support subclass-specific
        behavior or logic overrides in the future.

        Args:
            defense: The defense stat of the pokemon.

        Returns:
            float: The pokemon's defense stat.
        """
        return defense

    @classmethod
    def create_pokemon(cls, name: str, attack: float, defense: float) -> None:
        """Create and persist a new Pokemon instance.

        Args:
            name: The name of the pokemon.
            attack: The attack stat of the boxer.
            defense: The defense stat of the boxer.

        Raises:
            IntegrityError: If a pokemon with the same name already exists.
            ValueError: If the attack is less than 0 or if any of the input parameters are invalid.
            SQLAlchemyError: If there is a database error during creation.
        """
        logger.info(f"Creating boxer: {name}, {attack=} {defense=}")

        if attack <= 0:
            raise ValueError("pokemon's attack must be larger than 0")
        if defense <= 0:
            raise ValueError("pokemon's defense must be larger than 0")

        try:
            pokemon = Pokemons(
                name=name.strip(),
                attack=attack,
                defense=defense, 
            )
            
            db.session.add(pokemon)
            db.session.commit()
            logger.info(f"pokemon created successfully: {name}")

        except IntegrityError:
            logger.error(f"pokemon with name '{name}' already exists.")
            db.session.rollback()
            raise ValueError(f"The name '{name}' already exist in the data")
        except SQLAlchemyError as e:
            logger.error(f"Database error during creation: {e}")
            db.session.rollback()
            raise

    @classmethod
    def get_pokemon_by_id(cls, pokemon_id: int) -> "Pokemons":
        """Retrieve a pokemon by ID.

        Args:
            pokemon_id: The ID of the pokemon.

        Returns:
            Boxer: The boxer instance.

        Raises:
            ValueError: If the boxer with the given ID does not exist.

        """

        logger.info(f"Attmepting to retrieve pokemon with ID {pokemon_id}")

        try:
            pokemon = db.session.get(cls, pokemon_id)

            if not pokemon:
                logger.info(f"Boxer with ID {pokemon_id} not found")
                raise ValueError(f"Boxer with ID {pokemon_id} not found")
            
            logger.info(f"Successfully retrieved boxer")
            return pokemon
        
        except SQLAlchemyError as e:
            logger.error(f"Database error while retriving boxer by ID {pokemon_id}")
            raise

    @classmethod
    def get_pokemon_by_name(cls, name: str) -> "Pokemons":
        """Retrieve a pokemon by name.

        Args:
            name: The name of the pokemon.

        Returns:
            Pokemons: The pokemon instance.

        Raises:
            ValueError: If the pokemon with the given name does not exist.

        """
        pokemon = cls.query.filter_by(name=name).first()
        if not pokemon:
            logger.info(f"Pokemon '{name}' not found.")
            raise ValueError(f"Pokemon with name '{name}' does not exist.")
        
        return pokemon

    @classmethod
    def delete(cls, pokemon_id: int) -> None:
        """Delete a pokemon by ID.

        Args:
            pokemon_id: The ID of the pokemon to delete.

        Raises:
            ValueError: If the pokemon with the given ID does not exist.

        """
        pokemon = cls.query.get(pokemon_id)
        if pokemon is None:
            logger.info(f"pokemon with ID {pokemon_id} not found.")
            raise ValueError(f"pokemon with ID {pokemon_id} not found.")
        db.session.delete(pokemon)
        db.session.commit()
        logger.info(f"pokemon with ID {pokemon_id} permanently deleted.")

