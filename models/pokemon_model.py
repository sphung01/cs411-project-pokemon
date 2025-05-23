import logging
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db import db
from models.logger import configure_logger
from models.api_utils import get_attack_and_defense

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

    def __init__(self, name: str = None, attack: float = None, defense: float = None):
        """Initialize a new Pokemon instance with validation (manual instantiation only)."""

        # Skip validation when SQLAlchemy instantiates via ORM
        if name is None and attack is None and defense is None:
            return  

        if not name or not isinstance(name, str):
            raise ValueError("Pokemon must be a non-empty string.")
        
        if attack is None or defense is None:
            stats = get_attack_and_defense(name.lower())
            attack = stats[0]
            defense = stats[1]
        
        if not isinstance(attack, (int, float)) or attack <= 0:
            raise ValueError("Attack must be a float and greater than 0.")
        if not isinstance(defense, (int, float)) or defense <= 0:
            raise ValueError("Defense must be a float and greater than 0.")

        self.name = name
        self.attack = attack
        self.defense = defense

    @classmethod
    def get_attack(cls, attack: float) -> str:
        """Get the attack stat.

        Args:
            attack: The attack stat of the pokemon.

        Returns:
            float: The pokemon's attack stat.
        """
        return attack
    
    @classmethod
    def get_defense(cls, defense: float) -> str:
        """Get the defense stat.
        Args:
            defense: The defense stat of the pokemon.

        Returns:
            float: The pokemon's defense stat.
        """
        return defense

    @classmethod
    def create_pokemon(cls, name: str, attack: float = None, defense: float = None) -> None:
        """Create and persist a new Pokemon instance.

        Args:
            name: The name of the pokemon.
            attack: Optional attack stat. If None, fetched from PokéAPI.
            defense: Optional defense stat. If None, fetched from PokéAPI.

        Raises:
            IntegrityError: If a pokemon with the same name already exists.
            ValueError: If the attack is less than 0 or if any of the input parameters are invalid.
            SQLAlchemyError: If there is a database error during creation.
        """
        logger.info(f"Creating pokemon: {name}, {attack=} {defense=}")

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
            ValueError: If the pokemon with the given ID does not exist.

        """

        logger.info(f"Attmepting to retrieve pokemon with ID {pokemon_id}")

        try:
            pokemon = db.session.get(cls, pokemon_id)

            if not pokemon:
                logger.info(f"Pokemon with ID {pokemon_id} not found")
                raise ValueError(f"Pokemon with ID {pokemon_id} not found")
            
            logger.info(f"Successfully retrieved pokemon")
            return pokemon
        
        except SQLAlchemyError as e:
            logger.error(f"Database error while retriving pokemon by ID {pokemon_id}")
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

    def update_stats(self, stat, change):
        """Update a pokemon's attack or defense

        Args:
            stat (str): the stat you want to update
            change (float): how you want the stat to change. Can be positive or negative

        Raises:
            ValueError: If invalid stat selection, change isn't a float, or if the change would bring a stat below 0 
        """
        if stat not in {"attack", "defense"}:
            raise ValueError("stat must be 'attack' or 'defense'.")
        
        if not isinstance(change, float):
            raise ValueError("change must be a float")
        
        if self.attack + change < 0:
            raise ValueError("attack can't be < 0")
        if self.defense + change < 0:
            raise ValueError("defense can't be < 0")
        
        if stat == "attack":
            self.attack += change
            
        if stat == "defense":
            self.defense += change
            
        db.session.commit()
        logger.info(f"Updated stats for pokemon {self.name}: {self.defense} defense, {self.attack} attack.")
        
        
            
        