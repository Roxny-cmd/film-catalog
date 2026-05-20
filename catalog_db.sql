CREATE TABLE IF NOT EXISTS directors
(
	id serial PRIMARY KEY,
	name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS studios
(
	id serial PRIMARY KEY,
	name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS genres
(
	id serial PRIMARY KEY,
	name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS actors
(
	id serial PRIMARY KEY,
	name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS countries
(
	id serial PRIMARY KEY,
	name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS platforms
(
	id serial PRIMARY KEY,
	name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS users
(
    id SERIAL PRIMARY KEY,
    email VARCHAR(256) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects
(
	id serial PRIMARY KEY,
	title varchar(256) UNIQUE NOT NULL,
	project_type varchar(256) CHECK (project_type IN('serial','movie')) NOT NULL,
	date_of_release date NOT NULL,
	rating decimal (3,1) CHECK (rating >= 0 and rating <= 10),
	description text,
	director_id int,
	studio_id int,
	country_id int,
	owner_id int,

	FOREIGN KEY (director_id) REFERENCES directors(id),
	FOREIGN KEY (studio_id) REFERENCES studios(id),
	FOREIGN KEY (country_id) REFERENCES countries(id),
	FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS project_genre
(
	project_id int,
	genre_id int,

	PRIMARY KEY(project_id,genre_id),

	FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id)
);

CREATE TABLE IF NOT EXISTS project_cast
(
	project_id int,
	actor_id int,
	role varchar(256) NOT NULL,

	PRIMARY KEY(project_id, actor_id),

	FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES actors(id)
);

CREATE TABLE IF NOT EXISTS project_on_platform
(
	project_id int,
	platform_id int,

	PRIMARY KEY(project_id, platform_id),

	FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (platform_id) REFERENCES platforms(id)
)