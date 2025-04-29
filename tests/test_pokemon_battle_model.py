import time

import pytest

from models.pokemon_battle_model import BattleModel
from models.pokemon_team_model import Pokemons

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

##########################################################
# Pokemon Prep
##########################################################

def test_clear_battlefield(pokemon_battle_model):
    """
        Test that clear_battlefield empties the battlefield.
    """
    pokemon_battle_model.battlefield = [25, 20] 

    pokemon_battle_model.clear_battlefield()

    assert len(pokemon_battle_model.battlefield) == 0, "Ring should be empty after calling clear_ring."

def test_clear_battlefield_empty(pokemon_battle_model, caplog):
    """
        Test that calling clear_battlefield on an empty battlefield logs a warning and keeps the battlefield empty.
    """
    with caplog.at_level("WARNING"):
        pokemon_battle_model.clear_battlefield()

    assert len(pokemon_battle_model.battlefield) == 0, "Battlefield should remain empty if it was already empty."

    assert "Attempted to clear an empty battlefield." in caplog.text, "Expected a warning when clearing an empty battlefield."

def test_get_pokemons_empty(pokemon_battle_model, caplog):
    """
        Test that get_pokemons returns an empty list when there is no pokemon and logs a warning.
    """
    with caplog.at_level("WARNING"):
        pokemons = pokemon_battle_model.get_pokemons()

    assert pokemons == [], "Expected get_pokemons to return an empty list when there is no pokemon."

    assert "Retrieving pokemon from an empty battlefield." in caplog.text, "Expected a warning when getting pokemon from an empty battlefield."

def test_get_pokemons_with_data(app, pokemon_battle_model, sample_pokemons):
    """
        Test that get_pokemons returns the correct list when there are pokemon.
        # Note that app is a fixture defined in the conftest.py file
    """
    pokemon_battle_model.battlefield.extend([pokemon.id for pokemon in sample_pokemons])

    pokemons = pokemon_battle_model.get_pokemons()
    assert pokemons == sample_pokemons, "Expected get_pokemons to return the correct pokemons list."

def test_enter_ring(pokemon_battle_model, sample_pokemons, app):
    """
        Test that a pokemon is correctly added to the battlefield.
    """
    pokemon_battle_model.enter_battlefield(sample_pokemons[0].id)

    assert len(pokemon_battle_model.battlefield) == 25, "Battlefield should contain one pokemon after calling enter_battlefield."
    assert pokemon_battle_model.battlefield[0] == 25, "Expected 'Pikachu' (id 25) in the battlefield."

    pokemon_battle_model.enter_battlefield(sample_pokemons[1].id)

    assert len(pokemon_battle_model.battlefield) == 20, "Battlefield should contain one pokemon after calling enter_battlefield."
    assert pokemon_battle_model.battlefield[1] == 20, "Expected 'Staryu' (id 20) in the battlefield."

def test_enter_ring_full(pokemon_battle_model, app, sample_pokemons):
    """Test that enter_ring raises an error when the ring is full.

    """
    pokemon_battle_model.battlefield = [25, 20]

    with pytest.raises(ValueError, match="Battlefield is full"):
        pokemon_battle_model.enter_battlefield(sample_pokemons[1].id)

    assert len(pokemon_battle_model.battlefield) == 2, "Battlefield should still contain only 2 pokemons after trying to add a third."
