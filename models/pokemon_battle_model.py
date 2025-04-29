import logging
import math
import os
import time
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

        random_number = get_random()

        logger.debug(f"Random number from random.org: {random_number:.3f}")

        if random_number < normalized_delta:
            winner = pokemon_1
        else:
            winner = pokemon_2

        logger.info(f"The winner is: {winner.name}")

        self.clear_battlefield()

        return winner.name

    def clear_battlefield(self):
        pass

    def enter_battlefield(self):
        pass

    def get_pokemons(self) -> List[Pokemons]:
        pass

    def get_pokemon_skills(self, pokemon: Pokemons) -> float:
        pass