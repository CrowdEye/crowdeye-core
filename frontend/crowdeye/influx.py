from influxdb import InfluxDBClient
import datetime
import pytz


def writeEntry(nodeID, crossed_left, crossed_right, total_crossed, total_people):
    """
    writeEntry is a function to write data read the from the nodes into an InfluxDB database \n
    The params are, in order: nodeID, crossed_left, crossed_right, total_crossed, total_people
    """
    #Get the current time in the RFC3339 format for InfluxDB
    t = datetime.datetime.utcnow()
    t = t.isoformat("T") + "Z" #Z is for Zulu timezone, idk why I need it but stackoverflow says to
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
    client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'db')
    client.write_points(json_body)

