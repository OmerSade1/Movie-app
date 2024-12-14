CREATE DATABASE IF NOT EXISTS todo_db;
USE todo_db;

CREATE TABLE IF NOT EXISTS todo (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    text VARCHAR(255) NOT NULL
);