CREATE DATABASE task_manager;

USE task_manager;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT  CURRENT_TIMESTAMP
);

SELECT * FROM tasks;