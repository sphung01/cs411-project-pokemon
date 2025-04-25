DROP TABLE IF EXISTS boxers;
CREATE TABLE boxers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    weight FLOAT NOT NULL,
    height FLOAT NOT NULL,
    reach FLOAT NOT NULL,
    age INTEGER NOT NULL,
    fights INTEGER NOT NULL DEFAULT 0,
    wins INTEGER NOT NULL DEFAULT 0,
    weight_class TEXT,
    UNIQUE(name)
);

CREATE INDEX idx_boxers_name ON boxers(name);