-- first switch to the database - esb, then run the following commands
create database ESB;
use ESB;

-- user table
create table IF NOT EXISTS Users(
	Username varchar(100) primary key,
	UserPassword varchar(100) not null,
	UserRole varchar(100) not null,
	UserPriority int not null,
	Email varchar(500) not null
);

 -- users waiting for confirmation after signup from the admin
create table IF NOT EXISTS SignupConfirmation(
	Username varchar(100) primary key,
	UserPassword varchar(100) not null,
	UserRole varchar(100) not null,
	Email varchar(500) not null
);

 -- logs for each request
create table IF NOT EXISTS AckLogs(
	RequestID varchar(24) not null,
	-- to be generated by the HTTP server
	Username varchar(100) not null,
	-- username of the user
	TypeofRequest varchar(100) not null,
	-- API Call / Client to client communication
	Receiver varchar(100) not null,
	-- API name / Receiver client
	RequestPayload text not null,
	-- if text then include, for file transfer use the file name
	Response text not NULL,
	-- Response of API 
	InitialTimestamp timestamp not null,
	-- time when request arrives at the HTTP server from a user client
	FinalTimestamp timestamp not null,
	-- time when the request response arrives at HTTP server to be sent back to the user client
	ServiceResponseStatus int not null,
	-- API call status, etc.
	ReturnResponseStatus int not null -- Successfully sent back to the user client or not
);

create table if not EXISTS Pending(
	RequestID varchar(24) not null,
	-- to be generated by the HTTP server
	Username varchar(100) not null,
	-- username of the user
	Receiver varchar(100) not null,
	-- API name / Receiver client
	RequestPayload text not null,
	-- if text then include, for file transfer use the file name
	InitialTimestamp timestamp not null
	-- time when request arrives at the HTTP server from a user client
);
