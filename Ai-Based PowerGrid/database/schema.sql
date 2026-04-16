CREATE DATABASE IF NOT EXISTS power_grid_db;
USE power_grid_db;

CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    load_percentage FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    weather_condition VARCHAR(50) NOT NULL,
    equipment_health VARCHAR(50) NOT NULL,
    maintenance_delay BOOLEAN NOT NULL,
    zone_name VARCHAR(100) NOT NULL,
    failure_probability FLOAT NOT NULL,
    expected_delay_hours FLOAT NOT NULL,
    risk_level VARCHAR(20) NOT NULL
);
