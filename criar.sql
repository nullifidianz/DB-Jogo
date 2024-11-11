-- Criação das tabelas principais
CREATE TABLE game (
    game_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    release_date DATE,
    rating FLOAT,
    description TEXT,
    background_image VARCHAR(255),
    website VARCHAR(255)
);

CREATE TABLE genre (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE platform (
    platform_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE developer (
    developer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE publisher (
    publisher_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE
);

-- Criação das tabelas de relacionamento
CREATE TABLE game_genre (
    game_id INTEGER REFERENCES game(game_id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genre(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (game_id, genre_id)
);

CREATE TABLE game_platform (
    game_id INTEGER REFERENCES game(game_id) ON DELETE CASCADE,
    platform_id INTEGER REFERENCES platform(platform_id) ON DELETE CASCADE,
    PRIMARY KEY (game_id, platform_id)
);

CREATE TABLE game_developer (
    game_id INTEGER REFERENCES game(game_id) ON DELETE CASCADE,
    developer_id INTEGER REFERENCES developer(developer_id) ON DELETE CASCADE,
    PRIMARY KEY (game_id, developer_id)
);

CREATE TABLE game_publisher (
    game_id INTEGER REFERENCES game(game_id) ON DELETE CASCADE,
    publisher_id INTEGER REFERENCES publisher(publisher_id) ON DELETE CASCADE,
    PRIMARY KEY (game_id, publisher_id)
);