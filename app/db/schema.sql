CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE puzzle (
    id INTEGER PRIMARY KEY,
    solution TEXT NOT NULL,
    print_date TEXT UNIQUE NOT NULL,
    days_since_launch INTEGER NOT NULL,
    editor TEXT
);

CREATE TABLE solve (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  puzzle_id INTEGER NOT NULL,
  solved INTEGER NOT NULL,
  num_attempts INTEGER NOT NULL,
  attempt1 TEXT NOT NULL,
  attempt2 TEXT,
  attempt3 TEXT,
  attempt4 TEXT,
  attempt5 TEXT,
  attempt6 TEXT,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (puzzle_id) REFERENCES puzzle (id)
);

CREATE TABLE acceptable (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  word TEXT NOT NULL
)
