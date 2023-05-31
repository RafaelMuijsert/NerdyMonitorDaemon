#!/usr/bin/env python3

import logging
import configparser
import mariadb
import argparse
import subprocess

from time import sleep, strftime
from datetime import datetime

CPU_LOAD = True
DISK_SPACE = True
UPTIME = True

INSERT_QUERY = """
INSERT INTO Measurement ({measurement}, date, Infrastructure_component_id)
VALUES (?, ?, ?)
"""

def get_cpu_load():
    """Gets the current processor load 

    Returns:
        float: the current processor load ranging from 0.0 - 100.0
    """
    return 50.0

def get_used_disk_space():
    """gets the current amount of used disk space

    returns:
        float: the amount of used disk space in gigabytes
    """
    return 10.0

def get_total_disk_space():
    """gets the total amoutn of disk space

    returns:
        float: the total amount of disk space in gigabytes
    """
    return 120.0

def get_uptime():
    """Gets the current uptime

    Returns:
        str: uptime as a string
    """
    process = subprocess.Popen(['uptime', '-p'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode('utf-8').strip()  # Decode bytes to string and remove leading/trailing spaces
    return output

def connect_to_database(config):
    """Continuously attempt to connect to database using provided configuration.

    Args:
        config (object): containing: host, port, user, password, db

    Returns:
        MariaDB instance: a valid MariaDB connection
    """    
    logging.info(f'Connecting to database: {config["host"]}/{config["db"]}')
    db = False
    while not db:
        try:
            db = mariadb.connect(
                host=config['host'],
                port=int(config['port']),
                user=config['user'],
                password=config['password'],
                database=config['db']
            )
            logging.info('Connection to database succesful')
            return db
        except Exception as err:
            logging.error(f'Could not connect to database: {err}')
            db = False
        
        sleep(int(config['reconnect-interval']))

def main():
    """Reads configuration and continuously measures server health
    """    
    parser = argparse.ArgumentParser()
    parser.parse_args()
    
    config = configparser.ConfigParser()
    config.read('/etc/nmd/nmd.ini')

    logging.basicConfig(level=logging.INFO)

    db = connect_to_database(config['db'])
    cursor = db.cursor()
    while True:
        if CPU_LOAD:
            load = get_cpu_load()
            logging.info(f'CPU load: {load}')
            cursor.execute(
                INSERT_QUERY.format(measurement = 'processorload'), 
                (load, strftime('%Y-%m-%d %H:%M:%S'), config['nmd']['component-id'])
            )

        if DISK_SPACE:
            disk_space = get_used_disk_space()
            logging.info(f'Used disk space: {disk_space}')
            cursor.execute(
                INSERT_QUERY.format(measurement = 'used_diskspace_in_GB'), 
                (disk_space, strftime('%Y-%m-%d %H:%M:%S'), config['nmd']['component-id'])
            )
        
        if UPTIME:
            uptime = get_uptime()
            logging.info(f'Uptime: {uptime}')
            cursor.execute(
                INSERT_QUERY.format(measurement = 'uptime'), 
                (uptime, strftime('%Y-%m-%d %H:%M:%S'), config['nmd']['component-id'])
            )

        db.commit()
        sleep(int(config['nmd']['interval']))

    db.close()

if __name__ == '__main__':
    main()