import pytest

from models.pokemon_model import Pokemons
from models.pokemon_battle_model import BattleModel

@pytest.fixture
def pokemon_battle_model():
    """Fixture to provide a new instance of RingModel for each test."""
    return BattleModel()

