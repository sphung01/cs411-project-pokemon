import requests

# ------------------------------
# Configuration
# ------------------------------

BASE_URL = "http://localhost:5000/api"
USERNAME = "smokeuser"
PASSWORD = "smokepassword"
NEW_PASSWORD = "smokenewpass"
POKEMON_1 = "pikachu"
POKEMON_2 = "bulbasaur"

session = requests.Session()

# ------------------------------
# Health Check
# ------------------------------

def check_health():
    print("[1] Checking /health...")
    res = session.get(f"{BASE_URL}/health")
    assert res.status_code == 200 and "Service is running" in res.text
    print("Healthcheck passed")

# ------------------------------
# User Management
# ------------------------------

def reset_users():
    print("[2] Resetting user table...")
    res = session.delete(f"{BASE_URL}/reset-users")
    assert res.status_code == 200
    print("Users table reset")

def create_user():
    print("[3] Creating user...")
    res = session.put(f"{BASE_URL}/create-user", json={"username": USERNAME, "password": PASSWORD})
    assert res.status_code == 201
    print("User created")

def login(password):
    print(f"[4] Logging in with password: {password}...")
    res = session.post(f"{BASE_URL}/login", json={"username": USERNAME, "password": password})
    assert res.status_code == 200
    print("Login succeeded")

def change_password():
    print("[5] Changing password...")
    res = session.post(f"{BASE_URL}/change-password", json={"new_password": NEW_PASSWORD})
    assert res.status_code == 200
    print("Password changed")

def logout():
    print("[6] Logging out...")
    res = session.post(f"{BASE_URL}/logout")
    assert res.status_code == 200
    print("Logout succeeded")

# ------------------------------
# Pokémon API
# ------------------------------

def fetch_pokemon(name):
    print(f"Fetching Pokémon: {name}...")
    res = session.get(f"{BASE_URL}/fetch-pokemon/{name}")
    assert res.status_code in (200, 201) and name.lower() in res.text.lower()
    print(f"Pokémon {name} fetched")

def get_pokemon_by_name(name):
    res = session.get(f"{BASE_URL}/fetch-pokemon/{name}")
    if res.status_code not in (200, 201):
        print(f"Failed to fetch Pokémon {name}, status code {res.status_code}")
        return None
    return res.json().get("pokemon")

# ------------------------------
# Battle Simulation
# ------------------------------

def simulate_battle():
    print("[8] Simulating Pokémon battle...")

    poke1 = get_pokemon_by_name(POKEMON_1)
    poke2 = get_pokemon_by_name(POKEMON_2)

    if poke1 is None or poke2 is None:
        raise ValueError("Failed to retrieve one or both Pokémon from the API")

    print(f"Got {POKEMON_1} from DB: {poke1}")
    print(f"Got {POKEMON_2} from DB: {poke2}")

    for name in [POKEMON_1, POKEMON_2]:
        print(f"Adding Pokémon '{name}' to battlefield...")
        response = session.post(f"{BASE_URL}/enter-ring", json={"name": name})
        if response.status_code != 200:
            print(f"Failed to enter Pokémon {name} into battlefield: {response.status_code} {response.text}")
            raise Exception("Battlefield entry failed")

    res = session.get(f"{BASE_URL}/battle")
    assert res.status_code == 200 and "winner" in res.text
    winner = res.json().get("winner")
    print(f"Battle simulation complete. Winner: {winner}")

# ------------------------------
# Run All Smoketests
# ------------------------------

def run_smoketests():
    print("=== SMOKETEST START ===")
    check_health()
    reset_users()
    create_user()
    login(PASSWORD)
    change_password()
    logout()
    login(NEW_PASSWORD)
    fetch_pokemon(POKEMON_1)
    fetch_pokemon(POKEMON_2)
    simulate_battle()
    print("=== SMOKETEST COMPLETE ===")

if __name__ == "__main__":
    run_smoketests()
