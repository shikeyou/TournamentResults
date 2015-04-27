## Introduction

This is project 2 for Udacity's Full Stack Web Developer Nanodegree.

Main objectives of this project:

* Create a PostgreSQL database for storing results of a Swiss tournament using SQL statements
* Manipulating that database using Python

## Requirements

You will need these installed in your computer:

* [PostgreSQL](http://www.postgresql.org/download/)
* [Python 2.x](https://www.python.org/downloads/)

## Files

These are the files that come with this project:

* **tournament.sql:** This contains SQL statements that create the `players` and `matches` tables. An additional `score` view is created which tallies up the total number of wins and loses for each player, for convenience.

* **tournament.py:** This contains Python codes which connect to the `tournament` database, manipulate it and query results from it 

* **tournament_test.py:** This is the unit test file provided

## Running The Project

You need to first create a `tournament` database in PostgreSQL. In a shell:

	> psql
	=> create database tournament;
    => \c test;
     
Then in a new command shell, run the unit tests:

    > python tournament_test.py
	
The tables defined in *tournament.sql* will be added to the `tournament` database and the functions in *tournament.py* will be tested.	Results of the unit tests will be displayed in the shell.