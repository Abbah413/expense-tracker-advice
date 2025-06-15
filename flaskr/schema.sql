DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS transactions;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    budget REAL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE advice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

