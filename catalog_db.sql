CREATE TABLE directors IF NOT EXISTS
(
	director_id serial PRIMARY KEY,
	director_name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE studios IF NOT EXISTS
(
	studio_id serial PRIMARY KEY,
	studio_name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE genres IF NOT EXISTS
(
	genre_id serial PRIMARY KEY,
	genre_name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE actors IF NOT EXISTS
(
	actor_id serial PRIMARY KEY,
	actor_name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE countries IF NOT EXISTS
(
	country_id serial PRIMARY KEY,
	country_name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE platforms IF NOT EXISTS
(
	platform_id serial PRIMARY KEY,
	platform_name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE projects IF NOT EXISTS
(
	project_id serial PRIMARY KEY,
	title varchar(256) UNIQUE NOT NULL,
	type varchar(256) CHECK (type IN('serial','movie')) NOT NULL,
	date_of_release date NOT NULL,
	rating decimal (3,1) CHECK (0, 10),
	description text,
	director_id int,
	studio_id int,
	country_id int,

	FOREIGN KEY (director_id) REFERENCES directors(director_id),
	FOREIGN KEY (studio_id) REFERENCES studios(studio_id),
	FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

CREATE TABLE project_genre IF NOT EXISTS
(
	project_id int,
	genre_id int,
	
	PRIMARY KEY(project_id,genre_id),

	FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE project_cast IF NOT EXISTS
(
	project_id int,
	actor_id int,
	role varchar(256) NOT NULL,

	PRIMARY KEY(project_id, actor_id),

	FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
);

CREATE TABLE project_on_platform IF NOT EXISTS
(
	project_id int,
	platform_id int,

	PRIMARY KEY(project_id, platform_id),

	FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (platform_id) REFERENCES platforms(platform_id)
)
