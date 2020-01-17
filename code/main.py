
import serial
import pynmea2
import subprocess 
import time 
import os
from moviepy.video.io.VideoFileClip import VideoFileClip  # for get advertisment duration
from geopy.distance import geodesic

#kill all older player objects
os.system('killall omxplayer.bin') 

#derectry for ad and movie
moviePath = ("/home/pi/Desktop/movies/")
advertismentPath = ("/home/pi/Desktop/advertisement/")

#open serial port
port = "/dev/serial0"
serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.5)

#default gps cordinate
gpsPoint=[0,0]
mainMovieDuration = 0

# function for stop main process and run advdrticement
def runAdvertisment(fileNoStr):
    adPath = advertismentPath+fileNoStr+".mp4" #selected ad path
    mainProcess.stdin.write(b'p') # pause main movie
    advertismentProcess = subprocess.Popen(['omxplayer', adPath, '-b'],  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)
    clip = VideoFileClip(adPath) # get advertisement duration
    dur = int(clip.duration)
    
    global mainMovieDuration
    mainMovieDuration+=dur # extend main movie duration
    time.sleep(dur-4) # wait for play advertisment
    advertismentProcess.stdin.write(b'p') 
    advertismentProcess.kill() # end advertisement process
    mainProcess.stdin.write(b'p') # play main movie 


# get GPS cordinations from nema data
def parseGPS(dataString):
    if dataString.find('GGA') > 0:
        msg = pynmea2.parse(dataString)
        print(msg)
        #print "Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s -- Satellites: %s" % (msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units,msg.num_sats)
        try:
            latitude = float(msg.lat)/10 #msg.lat_dir
            longitude = float(msg.lon)/10 #msg.lon_dir 
            gpsPoint[0]= latitude
            gpsPoint[1]= longitude
        except:
            print("GPS initilizing yet---")
            
            
            
        
        
#check distance amang two GPS points
def checkAtLocation(advPoint, gpsPoit):
    dist = ((geodesic(advPoint, gpsPoit).kilometers)/3)
    print("distination among matching points",dist,"Km")
    if(dist<1.0):
        return 1  # return 1 on location point in <1 Km erea
    else:
        return 0

# match current gps location with all advertisement locations
def matchLocation(dataArry, gpsLocation):
    locAt="N"
    for n in range(len(dataArry)-1):
        loc = dataArry[n]
        check= checkAtLocation(loc, gpsLocation)
        if(check==1): # in advertisement location
            locAt = n
            print("Location match with index",n+1)
            break
        else:
            locAt="N"
    return locAt # return advertisement index or N for null


# read advertisement location data text file and get location cordinates
file = open(advertismentPath+"AdvertismentLocations.txt", "r")
data="start"
dataArry=[] #get location data

while(data!=""):
     data=file.readline()
     dataArry.append(data)
     #print(data)
file.close()


#start a play 1st movie
movieFIle = 1
moviepath = moviePath+str(movieFIle)+".mp4"
mainProcess = subprocess.Popen(['omxplayer', moviepath, '-b'],  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)

start_time = time.time() # get movie start time
mainMovie = VideoFileClip(moviepath) # get movie duration
mainMovieDuration = int(mainMovie.duration)

print("Movie",movieFIle, "is playing")
time.sleep(5)

previousPlayIndex=-1  # store variable for previous advertisment index

#main loop
while True:
    
    #if end 1st move, then play next
    if((time.time()-start_time)>mainMovieDuration):
        
        try:
            #play next movive
            movieFIle+=1
            moviepath = moviePath+str(movieFIle)+".mp4"
            #start a movie
            mainProcess = subprocess.Popen(['omxplayer', moviepath, '-b'],  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)
            print("Movie",movieFIle, "is playing")
        except:
            #reset plalist to 1
            os.system('killall omxplayer.bin') #reset player
            movieFIle=1
            moviepath = moviePath+str(movieFIle)+".mp4"
            #start a movie from 1
            mainProcess = subprocess.Popen(['omxplayer', moviepath, '-b'],  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)
            print("Play list refreshed, Movie",movieFIle, "is playing")
            
    
    gpsData = serialPort.readline() # get GPS data string
    #print(gpsData)
    parseGPS(gpsData) # decode GPS data
    print("Current GPS location :-",gpsPoint)
    
    index = matchLocation(dataArry, gpsPoint)
    #print(index)
    if(index!="N"):
        #location detected
        if(previousPlayIndex!=index):
            #play relavent index-1
            advNumber = index+1
            runAdvertisment(str(advNumber))
            previousPlayIndex = index  # store this index for prevent repeat
            print("advertisment",advNumber,"is playing")
        else:
         print("already plaid index ",index+1)
         time.sleep(1)
        
    else:
        print("No advertising location match")
        time.sleep(1)
        



#end of programme
