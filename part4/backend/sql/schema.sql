-- Create Users table
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Places table
CREATE TABLE places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Create Reviews table
CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    UNIQUE (user_id, place_id)
);

-- Create Amenities table
CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Place_Amenity table
CREATE TABLE place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

-- Insert initial admin user
INSERT INTO users (
    id,
    username,
    first_name,
    last_name,
    email,
    password,
    is_admin
) VALUES (
    '6725b2d6-6d2a-4919-98a8-c6ad69e2bb53',
    'admin',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    -- Password hash for 'admin1234'
    '$2b$12$UemmAxgZOGF1Me/bPNgBGesol5.i9PIM9wa0NRlmIkKbPgIe5A/xW',
    TRUE
);

-- Insert initial amenities
INSERT INTO amenities (id, name) VALUES
    ('79618355-1c74-41f6-af13-1de3b09b3a6d', 'WiFi'),
    ('0b96c362-c7ea-417f-a645-fd80c9c4ac34', 'Swimming Pool'),
    ('845e6a73-16ee-4728-9b44-01b3bf97e33f', 'Air Conditioning');
