import pytest

from models.pokemon_model import Pokemons
from models.pokemon_battle_model import BattleModel

@pytest.fixture
def pokemon_battle_model():
    """Fixture to provide a new instance of RingModel for each test."""
    return BattleModel()

@pytest.fixture
def sample_pokemon1(session):
    pokemon = Pokemons(
        name="Pikachu",
        attack=40.0,
        defense=25.0
    )
    session.add(pokemon)
    session.commit()
    return pokemon

@pytest.fixture
def sample_pokemon2(session):
    pokemon = Pokemons(
        name="Staryu",
        attack=45.0,
        defense=30.0
    )
    session.add(pokemon)
    session.commit()
    return pokemon

@pytest.fixture
def sample_boxers(sample_pokemon1, sample_pokemon2):
    return [sample_pokemon1, sample_pokemon2]