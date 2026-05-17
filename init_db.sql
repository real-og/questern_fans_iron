CREATE TABLE IF NOT EXISTS users (
    user_id INT NOT NULL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(30),
    telegram_id BIGINT,
    max_id VARCHAR(100),
    fan_number VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uniq_telegram_id (telegram_id),
    UNIQUE KEY uniq_fan_number (fan_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS bot_sections (
    section_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    button_name VARCHAR(255) NOT NULL,
    content_text TEXT,
    file_name VARCHAR(500),
    is_shown TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS user_actions (
    action_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    section_id INT NOT NULL,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_user_id (user_id),
    INDEX idx_section_id (section_id),
    INDEX idx_executed_at (executed_at),

    CONSTRAINT fk_user_actions_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_user_actions_section
        FOREIGN KEY (section_id) REFERENCES bot_sections(section_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;