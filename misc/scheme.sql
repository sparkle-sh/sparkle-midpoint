CREATE DATABASE syncerdb;
CREATE USER syncer WITH ENCRYPTED PASSWORD 'foobar';
GRANT ALL PRIVILEGES ON DATABASE syncerdb TO syncer;