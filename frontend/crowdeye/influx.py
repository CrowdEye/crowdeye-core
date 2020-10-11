from influxdb import InfluxDBClient
import datetime
import pytz
import requests

# Only prints the error once to avoid spamm
printedDBError = False

def writeEntry(nodeID, crossed_left, crossed_right, total_crossed, total_people):
    """
    writeEntry is a function to write data read the from the nodes into an InfluxDB database  
    The params are, in order: nodeID, crossed_left, crossed_right, total_crossed, total_people
    """
    global printedDBError
    # Get the current time in the RFC3339 format for InfluxDB
    t = datetime.datetime.utcnow()
    t = t.isoformat("T") + "Z" # Z is for Zulu timezone, idk why I need it but stackoverflow says to

    # Make the json body to send to the database
    json_body = [
        {
            "measurement": "people",
            "tags": {
                "nodeID": nodeID
            },
            "time":t,
            "fields": {
                "crossed_left": crossed_left,
                "crossed_right": crossed_right,
                "total_crossed": total_crossed,
                "total_people": total_people
            }
        }
    ]
    # Try to establish the connection with the database and write the data
    # If the database is not connected, fail silently
    try:
        client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'db')
        client.write_points(json_body)
    
    # Check to see if there was a connection error
    except requests.exceptions.ConnectionError:
        # Check if the error message has been printed, and if not, print it
        if not printedDBError:
            print("Not able to open the database")
            printedDBError = True