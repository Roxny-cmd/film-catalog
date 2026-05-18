CREATE TABLE directors
(
	id serial PRIMARY KEY,
	name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE studios
(
	id serial PRIMARY KEY,
	name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE genres
(
	id serial PRIMARY KEY,
	name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE actors
(
	id serial PRIMARY KEY,
	name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE countries
(
	id serial PRIMARY KEY,
	name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE platforms
(
	id serial PRIMARY KEY,
	name varchar(256) UNIQUE NOT NULL
);

CREATE TABLE projects
(
	id serial PRIMARY KEY,
	title varchar(256) UNIQUE NOT NULL,
	type varchar(256) CHECK (type IN('serial','movie')) NOT NULL,
	date_of_release date NOT NULL,
	rating decimal (3,1),
	description text,
	director_id int,
	studio_id int,
	country_id int,

	FOREIGN KEY (director_id) REFERENCES directors(did),
	FOREIGN KEY (studio_id) REFERENCES studios(id),
	FOREIGN KEY (country_id) REFERENCES countries(id)
);

CREATE TABLE project_genre
(
	project_id int,
	genre_id int,
	
	PRIMARY KEY(project_id,genre_id),

	FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id)
);

CREATE TABLE project_cast
(
	project_id int,
	actor_id int,
	role varchar(256) NOT NULL,

	PRIMARY KEY(project_id, actor_id),

	FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES actors(id)
);

CREATE TABLE project_on_platform
(
	project_id int,
	platform_id int,

	PRIMARY KEY(project_id, platform_id),

	FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (platform_id) REFERENCES platforms(id)
)
