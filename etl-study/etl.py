#!/usr/bin/env python3
import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Process song files and insert records into the Postgres database.
    :param cur: cursor reference
    :param filepath: complete file path for the file to load
    """
    #Open song file
    df = pd.DataFrame([pd.read_json(filepath, type='series',\
                                    convert_dates=False)])
    
    for value in df.values:
        num_songs, artist_id, artist_latitude, artist_longitidue, \
        artist_location, artist_name, song_id, title, duration, year = value
        
        #Insert artist record
        artist_data = (artist_id, artist_name, artist_latitutde, artist_longitude,\
                       artist_location)
        cur.execute(artist_table_insert, artist_data)
        
        #Insert song record
        song_data = (song_id, title, artist_id, year, duration)
        cur.execute(song_table_insert, song_data)        
        
    print(f"Records insert for file {filepath}")
    

def process_log_file(cur, filepath):
    """
    Process Event log files and insert record into Postgres database.
    :param cur: cursor reference
    :param filepath: complete file path for the file to load
    """
    #Open file log
    df = pd.read_json(filepath, lines=True)
    
    #Filter by NextSong action
    df = df[df['page'] == 'NextSong'].astype({'ts' : 'datetime64[ms]'})
    
    #Convert timestamp column to datatime
    t = pd.Series(df['ts'], index=df.index)
    
    #Insert time date records
    column_labels = ["timestamp", "hour", "day", "weekofyear", "month",\
                     "year", "weekday"]
    time_data = []
    for data in t:
        time_data.append([data, data.hour, data.day, data.weekofyear, \
                          data.month, data.year, data.weekday,\
                          data.day_name()])
    
    time_df = pd.DataFrame.from_records(data=time_data, columns=column_labels)
    
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))
        
    #Load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    
    #Insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
    
    #Insert songplay records
    for i, row in df.iterrows():
        
        #Get songId and artistId from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
        
        #Insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, row.sessionId,\
                         row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)
        
        
def process_data(cur, conn, filepath, func):
    """
    Driver function to load data from songs and event log files into Postgres DB.
    :param cur: a database cursor reference
    :param conn: database connection reference
    :param filepath: parent directory where the files exist
    :param func: function to call
    """
    #Get all matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))
            
    #Get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))
    
    #Iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))
        

def main():
    """
    Driver function for loading songs and log data into Postgres Database
    """
    conn = psycopg2.connect('host=127.0.0.1 dbname=sparkifydb user=postgres\
                            password=admin')
    cur = conn.cursor()
    
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    
    conn.close()
    

if __name__ == '__main__':
    main()
    print('\n\nFinished processing.\n\n')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
