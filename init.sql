-- first switch to the database - esb, then run the following commands

-- user table
create table IF NOT EXISTS users(
	username text primary key,
	password text not null,
	role text not null,
	priority integer not null
)

-- waiting users
create table IF NOT EXISTS waiting_users(
	username text primary key,
	password text not null,
	role text not null
)


-- logs
create table IF NOT EXISTS logs(
	RequestID varchar(10) not null,
	UserID varchar(10) not null,
	TypeofRequest varchar(10) not null,
	InitialTimestamp timestamp not null,
	FinalTimestamp timestamp not null,
	ServiceResponseStatus int not null,
	ReturnResponseStatus smallint not null
)