DROP TABLE IF EXISTS pokemons;
CREATE TABLE pokemons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    attack FLOAT NOT NULL,
    defense FLOAT NOT NULL,
    UNIQUE(name)
);

CREATE INDEX idx_pokemons_name ON pokemons(name);