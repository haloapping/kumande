"""
init
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE locations (
            id VARCHAR(26) UNIQUE NOT NULL PRIMARY KEY,
            district VARCHAR(255) DEFAULT NULL,
            city VARCHAR(255) DEFAULT NULL,
            province VARCHAR(255) DEFAULT NULL,
            postal_code VARCHAR(255) DEFAULT NULL,
            details VARCHAR(255) DEFAULT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NULL
        );
        """
    ),
    step(
        """
        CREATE TABLE users (
            id VARCHAR(26) UNIQUE NOT NULL PRIMARY KEY,
            profile_picture VARCHAR(255) DEFAULT NULL,
            username VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NULL
        );
        """
    ),
    step(
        """
        CREATE TABLE owners (
            id VARCHAR(26) UNIQUE NOT NULL PRIMARY KEY,
            image VARCHAR(255) DEFAULT NULL,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NULL
        );
        """
    ),
    step(
        """
        CREATE TABLE owner_images (
            id VARCHAR(26) UNIQUE NOT NULL PRIMARY KEY,
            owner_id VARCHAR(26) NOT NULL REFERENCES owners(id),
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NULL
        );
        """
    ),
    step(
        """
        CREATE TABLE foods (
            id VARCHAR(26) UNIQUE NOT NULL PRIMARY KEY,
            user_id VARCHAR(26) NOT NULL REFERENCES users(id),
            owner_id VARCHAR(26) NOT NULL REFERENCES owners(id),
            location_id VARCHAR(26) NOT NULL REFERENCES locations(id),
            image VARCHAR(255) DEFAULT NULL,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            price VARCHAR(255) NOT NULL,
            review VARCHAR(255) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NULL
        );
        """
    ),
    step(
        """
        CREATE TABLE food_images (
            id VARCHAR(26) UNIQUE NOT NULL PRIMARY KEY,
            food_id VARCHAR(26) NOT NULL REFERENCES foods(id),
            images VARCHAR(26) DEFAULT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NULL
        );
        """
    ),
]
