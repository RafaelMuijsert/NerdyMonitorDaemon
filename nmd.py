#!/usr/bin/env python3

import logging
import configparser
import mariadb
import argparse
import subprocess

from time import sleep, strftime
from datetime import datetime

MEASUREMENT_INSERT_QUERY = """
INSERT INTO Measurement (
    processorload,
    total_diskspace_in_gb,
    used_diskspace_in_gb,
    date,
    infrastructure_component_id,
    uptime
)
VALUES (?, ?, ?, ?, ?, ?)
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
    process = subprocess.Popen( "df -h --total | tail -n 1 | awk '{print $3 }'", stdout=subprocess.PIPE, shell=True )
    output, _ = process.communicate()
    used_disk_space = float(output.decode('utf-8').strip().strip('G'))
    return used_disk_space

def get_total_disk_space():
    """gets the total amoutn of disk space

    returns:
        float: the total amount of disk space in gigabytes
    """
    process = subprocess.Popen( "df -h --total | tail -n 1 | awk '{print $4}'", stdout=subprocess.PIPE, shell=True )
    output, _ = process.communicate()
    total_disk_space = float(output.decode('utf-8').strip().strip('G'))
    return total_disk_space

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
        load = get_cpu_load()
        logging.info(f'CPU load: {load}')

        used_disk_space = get_used_disk_space()
        total_disk_space = get_total_disk_space()
        logging.info(f'Used disk space: {used_disk_space}GB/{total_disk_space}GB')
        
        uptime = get_uptime()
        logging.info(f'Uptime: {uptime}')

        cursor.execute(
            MEASUREMENT_INSERT_QUERY,
            (load,
                total_disk_space,
                used_disk_space, 
                strftime('%Y-%m-%d %H:%M:%S'), 
                config['nmd']['component-id'], 
                uptime)
        )
        try:
            db.commit()
        except Exception as err:
            logging.error(f'Error committing measurements: {err}')
        
        sleep(int(config['nmd']['interval']))

    db.close()

if __name__ == '__main__':
    main()