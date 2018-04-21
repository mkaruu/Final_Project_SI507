import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
import csv
import sqlite3 as sqlite
import sqlite3 as Error
import pandas as pd

DBNAME = 'mass_shootings.db'
MJONESCSV = 'MJonesUSMassShootings.csv'

# Creates a database called mass_shootings.db
# def create_shootings_db():
try:
    conn = sqlite.connect('mass_shootings.db')
    cur = conn.cursor()
except Error as e:
    print(e)

statement = '''
    DROP TABLE IF EXISTS 'MJonesdata';
'''
cur.execute(statement)
conn.commit()

shootings_table_statement = '''
    CREATE TABLE 'MJonesdata' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Case' TEXT NOT NULL, 
        'Location' TEXT,
        'City' TEXT,
        'State' TEXT,
        'State_Id' TEXT,
        'Date' TEXT,
        'Year'TEXT NOT NULL,
        'Summary' TEXT,
        'Fatalities' INTEGER,
        'Injured' INTEGER,
        'Total Victims' REAL NOT NULL,
        'Venue' TEXT,
        'Prior Signs of Mental Health Issues' TEXT,
        'Mental Health Details' TEXT,
        'Weapons' TEXT,
        'Where Obtained' TEXT,
        'Type of Weapons' TEXT,
        'Weapon Details' TEXT,
        'Race' TEXT,
        'Gender' TEXT,
        'Sources' TEXT,
        'Mental Health Sources' TEXT,
        'Latitude' TEXT,
        'Longitude' TEXT,
        'Type' TEXT  
    );
'''   
# BroadBeanOriginId and CompanyLocationId are foreign keys pointing to countries data
cur.execute(shootings_table_statement)
conn.commit() #needed anytime you make changes to the DB including DROP, CREATE, INSERT, DELETE, and UPDATE  
print("THIS PART WORKS!!!!!")

f = open("MJonesUSMassShootings.csv", encoding='utf-8')
shootings_csv = csv.reader(f)
next(shootings_csv, None)

for params in shootings_csv:
    # print(row)
    Case = params[0]
    # print(Case)  
    Location = params[1]
    City = params[2]
    State  = params[3]
    State_id = params[4]
    Date = params[5]
    Year = params[6]
    Summary = params[7]
    Fatalities = params[8] 
    Injured = params[9]
    TotalVictims = params[10]
    Venue = params[11]
    PriorSignsofMentalHealthIssues = params[12]
    MentalHealthDetails = params[13]
    Weapons = params[14]
    WhereObtained = params[15]
    TypeofWeapons = params[16]
    Weapon_Details = params[17]
    Race = params[18]
    Gender = params[19]
    Sources = params[20]
    MentalHealthSources = params[21]
    Latitude = params[22]
    Longitude = params[23]
    Longitude = params[24]
    Type = params[24]
    values = (None, Case, Location, City, State, State_id, Date,Year, Summary, Fatalities, Injured, TotalVictims, Venue,PriorSignsofMentalHealthIssues, MentalHealthDetails, Weapons, WhereObtained, TypeofWeapons, Weapon_Details, Race, Gender, Sources, MentalHealthSources, Latitude, Longitude, Type)

    statement= 'INSERT INTO "MJonesdata"'
    statement += ' VALUES (?,?,?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?)' #not sure if null or ? for the primary
    cur.execute(statement, values)
    conn.commit()
conn.close()
