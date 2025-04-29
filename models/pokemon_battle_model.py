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
        pass

    def clear_battlefield(self):
        pass

    def enter_battlefield(self):
        pass

    def get_pokemons(self) -> List[Pokemons]:
        pass

    def get_pokemon_skills(self, pokemon: Pokemons) -> float:
        pass