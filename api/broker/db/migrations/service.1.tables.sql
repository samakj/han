CREATE TABLE IF NOT EXISTS users
(
    user_id     SERIAL PRIMARY KEY,
    username    TEXT NOT NULL UNIQUE,
    password    TEXT NOT NULL,
    mac_address TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS superusers
(
    superuser_id SERIAL PRIMARY KEY,
    user_id      INTEGER NOT NULL UNIQUE REFERENCES users (user_id)
);

CREATE TABLE IF NOT EXISTS access_controls
(
    access_control_id SERIAL PRIMARY KEY,
    user_id           INTEGER NOT NULL REFERENCES users (user_id),
    topic             TEXT    NOT NULL,
    action            INTEGER NOT NULL,

    UNIQUE  (user_id, topic, action)
);
