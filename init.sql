-- first switch to the database - esb, then run the following commands
create table IF NOT EXISTS users(username text primary key, password text not null, role text not null, priority integer not null)
create table IF NOT EXISTS waiting_users(username text primary key, password text not null, role text not null)