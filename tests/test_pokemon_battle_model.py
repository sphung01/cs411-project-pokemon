import time

import pytest

from models.pokemon_battle_model import BattleModel
# from models.pokemon_team_model

@pytest.fixture
def pokemon_battle_model():
    """
        Fixture to provide a new instance of BattleModel for each test.
    """
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
def sample_pokemons(sample_pokemon1, sample_pokemon2):
    return [sample_pokemon1, sample_pokemon2]