### --------------------------------------------------------------------------------------
### C:\Users\jopered\AppData\Local\Programs\Python\Python39\python.exe
### Assignment 7 - Data Analysis and Databases
### Author: Jose Pereda
### SDCE Student ID: 5696529
### Submission date: June 01, 2021
### --------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import os
import logging

from numpy.core.einsumfunc import _compute_size_by_dict

def debug_config():
    logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s")

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

def main():
     # Declare database file name 
    dbfile = 'degrees2.db'
    # Declare program name
    programname = "Bachelors Degrees for US Women by Major"
    debug_config()

    print(programname)
    db_checkfile(dbfile)
    try:
        con = db_connect(dbfile)
        cur = con.cursor()

        # Declare array variables for each degree type
        allyears = []
        architecture = []
        computerscience = []
        engineering = []
        foreignlanguage = []

        # query degreees.db for the degrees data of interest
        query = 'SELECT Year, Architecture, ComputerScience, Engineering, ForeignLanguages from degrees'
        res = db_runquery(cur, query)
        
        # Put queary results into array variables
        for result in res:
            allyears.append(result[0])
            architecture.append(result[1])
            computerscience.append(result[2])
            engineering.append(result[3])
            foreignlanguage.append(result[4])

        # Plot the results
        #print_higher_ed_degrees(allyears, architecture, computerscience, engineering, foreignlanguage)

    except sqlite3.Error as error:
        logging.error("Error executing query", error)
    finally:
        if con:
            con.close()
            logging.debug("[info] db Closed".format())
    print('Done - check completed')
    logging.info("Completed")

if __name__ == "__main__":
    main()