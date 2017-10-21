## Golf Command Line Stat Tool

This is a command line interface tool written in Python.  The goal of the tool is to track statistics for
golfers.  Data is stored in a SQLite DB, with object mapping using the Peewee ORM tools.  The data models included are for Golfers, Courses, and Rounds.  Statistics are calculated internally by querying the database for a golfer's completed
rounds.

Run the code by navigating to the source directory and typing:

	python golf_stats.py
	
at the command prompt.  Follow the instructions on the screen to begin tracking Golfers, Courses and Rounds.


Developed by:  Jon Lunsford
Date:  October 20, 2017
Copyright:  Springwood Software
