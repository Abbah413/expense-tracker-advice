DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS transactions;


CREATE TABLE user (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  transacted DATE NOT NULL,
  uploaded DATETIME NOT NULL,
  amount DECIMAL NOT NULL,
  [description] TEXT NOT NULL,
  category TEXT,
  user_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES user(user_id)
);




