import logging
import math
from typing import List

from logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

class BattleModel:
    """
        A class that manages the battlefield where pokemons fight.
    """

    def __init__(self):
        """
            Initializes the BattleManager with an empty list of combatants.

            Attributes:
                battlefield (List[int]): The list of ids of the pokemons in the battlefield
        """

        self.battlefield: List[int] = []

    def battle(self) -> str:
        """
            Simulates a fight between two pokemons.

            Returns:
                str: The name of the winning pokemon.

            Raises:
                ValueError: If there is not enough pokemons in the ring
        """

        if len(self.battlefield) < 2:
            logger.error("There must be two pokemons to start a fight.")
            raise ValueError("There must be two boxers to start a fight.")
        
        pokemon_1, pokemon_2 = self.get_pokemons()

        logger.info(f"Fight started between {pokemon_1.name} and {pokemon_2.name}")

        skill_1 = self.get_pokemon_skills(pokemon_1)
        skill_2 = self.get_pokemon_skills(pokemon_2)

        logger.debug(f"Fighting skill for {pokemon_1.name}: {skill_1:.3f}")
        logger.debug(f"Fighting skill for {pokemon_2.name}: {skill_2:.3f}")

        delta = abs(skill_1 - skill_2)
        normalized_delta = 1 / (1 + math.e ** (-delta))

        logger.debug(f"Raw delta between skills: {delta:.3f}")
        logger.debug(f"Normalized delta: {normalized_delta:.3f}")

        random = random.randint(1, 100)

        logger.debug(f"Random number from random.org: {random :.3f}")

        if random < normalized_delta:
            winner = pokemon_1
        else:
            winner = pokemon_2

        logger.info(f"The winner is: {winner.name}")

        self.clear_battlefield()

        return winner.name

    def clear_battlefield(self):
        """
            Clears the list of pokemons on the battlefield.
        """

        if not self.battlefield:
            logger.warning("Attempted to clear an empty battlefield.")
            return
        logger.info("Clearing pokemons from the battlefield.")
        self.battlefield.clear()

    def enter_battlefield(self, pokemon_id: int):
        """
            Prepares a pokemon by adding them to the battlefield.

            Args:
                pokemon_id (int): The ID of the pokemon to enter the ring.

            Raises:
                ValueError: If the battlefield already has two pokemons.
                ValueError: If the pokemon ID is invalid or the pokemon does not exist.
        """

        if len(self.battlefield) >= 2:
            logger.error(f"Battlefield is full")
            raise ValueError("Battlefield is full")
        try:
            pokemon = Pokemons.get_pokemon_by_id(pokemon_id)
        except ValueError as e:
            logger.error(str(e))
            raise
        
        self.battlefield.append(pokemon.id)
        logger.info(f"Adding pokemon '{pokemon.name}' (ID {pokemon_id}) to the battlefield")

        logger.info(f"Current pokemons in the battlefield: {[Pokemons.get_pokemon_by_id(p).name for p in self.battlefield]}")

    def get_pokemons(self) -> List[Pokemons]:
        """
            Retrieves the current list of pokemons on the battlefield.

        Returns:
            List[Pokemons]: A list of Pokemons dataclass instances representing the pokemons in the battlefield.
        """

        if not self.battlefield:
            raise ValueError("The battlefield is empty.")
        else:
            pass

        logger.info(f"Battlefield has pokemons!")
        return self.battlefield

    def get_pokemon_skills(self, pokemon: Pokemons) -> float:
        """
            Calculates the skill for a pokemon

            Args:
                pokemon (Pokemons): A Pokemons dataclass representing the combatant.
            
            Returns:
                float: The calculated skill
        """

        logger.info(f"Calculating fighting skill for {pokemon.name}: attack={pokemon.attack}, defense={pokemon.defense}")

        skill = (pokemon.attack + pokemon.defense)

        logger.info(f"Fighting skill for {pokemon.name}: {skill:.3f}")
        return skill