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
def sample_pokemons(sample_pokemon1, sample_pokemon2):
    return [sample_pokemon1, sample_pokemon2]

##########################################################
# Battlefield logic
##########################################################

def test_clear_battlefield(pokemon_battle_model):
    pokemon_battle_model.battlefield = [25, 20] 
    pokemon_battle_model.clear_battlefield()
    assert len(pokemon_battle_model.battlefield) == 0, "Ring should be empty after calling clear_ring."

def test_clear_battlefield_empty(pokemon_battle_model, caplog):
    with caplog.at_level("WARNING"):
        pokemon_battle_model.clear_battlefield()
    assert len(pokemon_battle_model.battlefield) == 0, "Battlefield should remain empty if it was already empty."
    assert "Attempted to clear an empty battlefield." in caplog.text, "Expected a warning when clearing an empty battlefield."

def test_get_pokemons_empty(pokemon_battle_model):
    with pytest.raises(ValueError, match="The battlefield is empty."):
        pokemon_battle_model.get_pokemons()

def test_get_pokemons_with_data(app, pokemon_battle_model, sample_pokemons):
    pokemon_battle_model.battlefield.extend(sample_pokemons)
    pokemons = pokemon_battle_model.get_pokemons()
    assert pokemons == sample_pokemons, "Expected get_pokemons to return the correct pokemons list."

def test_enter_battlefield(pokemon_battle_model, sample_pokemons, app):
    pokemon_battle_model.enter_battlefield(sample_pokemons[0].id)
    assert len(pokemon_battle_model.battlefield) == 1, "Battlefield should contain one pokemon after calling enter_battlefield."
    assert pokemon_battle_model.battlefield[0].id == sample_pokemons[0].id, f"Expected 'Pikachu' (id {sample_pokemons[0].id}) in the battlefield."
    pokemon_battle_model.enter_battlefield(sample_pokemons[1].id)
    assert len(pokemon_battle_model.battlefield) == 2, "Battlefield should contain two pokemon after calling enter_battlefield."
    assert pokemon_battle_model.battlefield[1].id == sample_pokemons[1].id, f"Expected 'Staryu' (id {sample_pokemons[1].id}) in the battlefield."

def test_enter_battlefield_full(pokemon_battle_model, app, sample_pokemons):
    pokemon_battle_model.battlefield = [25, 20]
    with pytest.raises(ValueError, match="Battlefield is full"):
        pokemon_battle_model.enter_battlefield(21)
    assert len(pokemon_battle_model.battlefield) == 2, "Battlefield should still contain only 2 pokemons after trying to add a third."

##########################################################
# Fighting logic
##########################################################

def test_get_pokemon_skills(pokemon_battle_model, sample_pokemons):
    expected_score_1 = 40.0 + 25.0
    assert pokemon_battle_model.get_pokemon_skills(sample_pokemons[0]) == expected_score_1
    expected_score_2 = 45.0 + 30.0
    assert pokemon_battle_model.get_pokemon_skills(sample_pokemons[1]) == expected_score_2

def test_battle(pokemon_battle_model, sample_pokemons, caplog, mocker):
    pokemon_battle_model.battlefield.extend([p.id for p in sample_pokemons])
    mocker.patch("models.pokemon_battle_model.BattleModel.get_pokemon_skills", side_effect=[65.0, 75.0])
    mocker.patch("random.random", return_value=0.42)
    mocker.patch("models.pokemon_battle_model.BattleModel.get_pokemons", return_value=sample_pokemons)
    winner_name = pokemon_battle_model.battle()
    assert winner_name == "Pikachu"
    pokemon_battle_model.battlefield = []
    assert len(pokemon_battle_model.battlefield) == 0, "Battlefield should be empty after the fight."

def test_battle_with_empty_battlefield(pokemon_battle_model):
    with pytest.raises(ValueError, match="There must be two pokemons to start a fight."):
        pokemon_battle_model.battle()

def test_battle_with_one_pokemon(pokemon_battle_model, sample_pokemon1):
    pokemon_battle_model.battlefield.append(sample_pokemon1)
    with pytest.raises(ValueError, match="There must be two pokemons to start a fight."):
        pokemon_battle_model.battle()