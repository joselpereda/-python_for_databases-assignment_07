### --------------------------------------------------------------------------------------
### C:\Users\jopered\AppData\Local\Programs\Python\Python39\python.exe
### Assignment 7 - Data Analysis and Databases
### Author: Jose Pereda
### SDCE Student ID: 5696529
### Submission date: June 02, 2021
### --------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os
import logging

def debug_config():
    logging.basicConfig(level=logging.INFO, format = "\n%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s")

def db_checkfile(dbfile):
    if os.path.exists(dbfile) and os.path.getsize(dbfile) > 0:
        logging.debug("{a} found and not zero sieze".format(a=dbfile))
    else:
        logging.error("{a} not found or zero size".format(a=dbfile))

def db_connect(dbfile):
    con = sqlite3.connect(dbfile)
    logging.debug("DB connected".format())
    return con

def db_cursor(con):    
    cur = con.cursor()    
    logging.debug("Cursor set".format())    
    return cur

def db_runquery(cur,query):
    cur.execute(query)
    result = cur.fetchall()
    logging.debug("DB Query executed and returned".format())
    return result

def print_full(x):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')

def main():
     # Declare database file name 
    dbfile = 'beers.db'
    # Declare program name
    programname = "Data Analysis and Databases"
    debug_config()

    print(programname)
    db_checkfile(dbfile)
    try:
        # Setup connection to db
        con = db_connect(dbfile)
        cur = con.cursor()

        # Read the SQLite query results into a pandas data frame 
        df = pd.read_sql_query("SELECT * from reviews", con)

        # Question 1: How many rows are in the table?
        print("1. How many rows are in the table?")
        print("[A] " + str(len(df))+ "\n")

        # Question 2: Describe the table
        print("2. Describe the table:")
        print(df.describe())

        # Question 3: How many entries are there for each brewery
        print("\n3: How many entries are there for each brewery?")
        print(df.groupby(['brewery_name']).size())

        # Question 4: Find all entries are low alcohol.  Alcohol by volume (ABV) less than 1%
        print("\n4: Find all entries are low alcohol. Alcohol by volume (ABV) less than 1%")
        low_abv = df[df.beer_abv < 1]
        print_full(low_abv)

        # Question 5:How many reviews are there for low ABV beers?
        print("\n5. How many reviews are there for low ABV beers?")
        print("[A] " + str(len(low_abv)))

        # Question 6:Group  the AVB beers by beer and count
        print("\n6. Group the AVB beers by beer and count:")
        grouping = low_abv.groupby('beer_name')
        print(grouping.size())

        # Question 7:How consistent are the O'Douls overall scores?
        print("\n7. How consistent are the O'Douls overall scores?")
        odouls = low_abv[low_abv.beer_name == "O'Doul's"]['review_overall']
        print(odouls)

        # Question 8:Plot a histogram of O'Douls overall scores (may need to close window to continue)
        print("\n8. Plot a histogram of O'Douls overall scores:")
        odouls.hist()
        plt.show()

        #Question 9:For O'Douls, what are the mean and standard deviation for the O'Doul's overall scores?
        print("\n9. For O'Douls, what are the mean and standard deviation for the O'Doul's overall scores?")
        mean_deviation = odouls.mean()
        std_deviation = odouls.std()
        print("Mean Deviation: " + str(mean_deviation) + ", Standard Deviation: " + str(std_deviation))

        #Question 10:Draw a boxplot of the low_abv data (may need to close window to continue)
        print("\n10. Draw a boxplot of the low_abv data")
        low_abv.boxplot(figsize=(12,10))
        plt.show()

    except sqlite3.Error as error:
        logging.error("Error executing query", error)
    finally:
        if con:
            con.close()
            logging.debug("[info] db Closed".format())
    print('\nDone - check completed')
    logging.info("Completed")

if __name__ == "__main__":
    main()