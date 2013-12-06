create database artgames;

create table artwork
(
id serial,
this_api int,
title character varying,
url character varying,
image_url character varying,
external_id int,
external_id2 int,
primary key (id)
);

create table artvote
(
 won int,
 lost int,
 FOREIGN KEY (won) REFERENCES artwork (id) ON UPDATE NO ACTION ON DELETE NO ACTION,
 FOREIGN KEY (lost) REFERENCES artwork (id) ON UPDATE NO ACTION ON DELETE NO ACTION
);
