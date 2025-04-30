import logging
import os
import requests

from models.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

def fetch_pokemon_data(pokemon_name):
    """Use the API to fetch a pokemon's data

    Args:
        pokemon_name (str): Pokemon's name

    Returns:
        json: The pokemon's data
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
    try:
        logger.info(f"Fetching stats for {pokemon_name} from {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Couldn't fetch stats for {pokemon_name}")
        return None

def get_attack_and_defense(pokemon_name):
    """Extract a pokemon's attack and defense stats

    Args:
        pokemon_name (str): Pokemon's name

    Raises:
        ValueError: If stats can't be found

    Returns:
        List[int]: List of pokemon stats
    """
    data = fetch_pokemon_data(pokemon_name)
    if data is None:
        return

    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}

    attack = stats.get("attack", "Not found")
    defense = stats.get("defense", "Not found")
    
    if attack == "Not found" or defense == "Not found":
        logger.error(f"Attack and defense stats not found for {pokemon_name}")
        raise ValueError("Stats not found")
    
    logger.info(f"Succesfully retreved attack and defense stats for {pokemon_name}")

    return [attack, defense]


