CREATE DATABASE IF NOT EXISTS finance_tracker;

USE finance_tracker;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    note TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS budgets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount FLOAT NOT NULL,
    month INT NOT NULL,
    year INT NOT NULL,
    UNIQUE KEY (user_id, category, month, year),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
