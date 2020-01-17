import serial
import pynmea2
 
port = "/dev/serial0"

lat =0.0
lon =0.0
gpsPoint=[0,0]

def parseGPS(str):
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)
        #print "Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s -- Satellites: %s" % (msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units,msg.num_sats)
        #lat = msg.lat #msg.lat_dir
        #lon = msg.lon #msg.lon_dir
        #gpsPoint[0]= float(lat)/10
        #gpsPoint[1]= float(lon)/10
        print("location is ",msg.lat, msg.lon)
        
        
 
serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.5)
while True:
    str = serialPort.readline()
    parseGPS(str)
    #print("run")
