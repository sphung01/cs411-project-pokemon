import logging
import math
import os
import time
from typing import List

logger = logging.getLogger(__name__)
configure_logger(logger)

class BattleModel:
    """
        A class that manages the battlefield where pokemons fight.
    """