# please set root password when setup ran, after that you can login with that password
mysql -u root -p

# show databases
show databases;

# create a database
CREATE DATABASE test;

# give all database privileges to root
GRANT ALL PRIVILEGES ON DATABASE test TO root;

# choose databases
\c test

# create table
CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);

# give all table privileges to root
GRANT ALL PRIVILEGES ON TABLE COMPANY TO root;

# show all the tables
\d

# show spectific table
\d COMPANY

#insert someting into table
INSERT INTO COMPANY (ID, NAME, AGE,ADDRESS) VALUES (1001, 'Mike', 35,'China');

# select someting from that table
SELECT * FROM COMPANY;