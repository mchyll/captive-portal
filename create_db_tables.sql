DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS banned_users;

CREATE TABLE clients (
  ip TEXT PRIMARY KEY,
  username TEXT NOT NULL,
  drifter INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE banned_users (
  username TEXT NOT NULL
);
