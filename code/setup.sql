drop table adults if exists cascade;
drop table unmarried if exists cascade;
drop table married if exists cascade;
-- creating the tables
create table adults (age int NULL, workclass varchar(30) NULL, fnlwgt int NULL, 
	education varchar(30) NULL, education_num int NULL, marital_status varchar(30) NULL, 
	occupation varchar(30) NULL, relationship varchar(30) NULL, race varchar(30) NULL, 
	sex varchar(30) NULL, capital_gain int NULL, capital_loss int NULL, 
	hours_per_week int NULL, native_country varchar(30) NULL, income varchar(10) NULL);

-- inserting data
\copy adults from '/Users/sazzle/Desktop/645/645-AIDE/data/processed.csv' delimiter ',' csv

-- tables for brute force (probably not necessary)
create table unmarried as
	select * from adults where marital_status = 'Unmarried';
alter table unmarried drop marital_status;
create table married as
	select * from adults where marital_status = 'Married';
alter table married drop marital_status;