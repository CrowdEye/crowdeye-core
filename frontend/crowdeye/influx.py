from influxdb import InfluxDBClient
import datetime
import pytz
import requests
import logging

logger = logging.getLogger(__name__)

# Only prints the error once to avoid spamm
# printedDBError = False

def writeEntry(DATA):
    """
    writeEntry is a function to write data read the from the nodes into an InfluxDB database  
    The only param should be an array of dicts where DATA[n]{node_id, crossed_left, crossed_right, total_crossed, total_people}
    """
    # global printedDBError
    # Get the current time in the RFC3339 format for InfluxDB
    t = datetime.datetime.utcnow()
    t = t.isoformat("T") + "Z" # Z is for Zulu timezone, idk why I need it but stackoverflow says to

    # Make the json body to send to the database
    json_body = []

    # Make a loop to add all of the json blocks
    l = len(DATA)
    for i in range(l):
        a = {
            "measurement": "people",
            "tags": {
                "nodeID": DATA[i]["node_id"]
            },
            "time":t,
            "fields": {
                "crossed_left": DATA[i]["crossed_left"],
                "crossed_right": DATA[i]["crossed_right"],
                "total_crossed": DATA[i]["total_crossed"],
                "total_people": DATA[i]["total_people"]
            }
        }
        json_body.append(a)
    # Try to establish the connection with the database and write the data
    # If the database is not connected, fail silently
    try:
        client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'db')
        client.write_points(json_body)
        logger.debug("Logged to the database.")
    
    # Check to see if there was a connection error
    except requests.exceptions.ConnectionError:
        # Check if the error message has been printed, and if not, print it
        if not printedDBError:
            logger.warning("Not able to open the database")
            # printedDBError = True