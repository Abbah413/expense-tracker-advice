DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS categories;


CREATE TABLE user (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bank TEXT NOT NULL,
  transacted DATE NOT NULL,
  uploaded DATETIME NOT NULL,
  amount DECIMAL(6, 2) NOT NULL,
  [description] TEXT NOT NULL,
  category TEXT,
  user_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE categories (
  category_id INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT,
  budget DECIMAL(6, 2),
  user_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES user(user_id)
);




