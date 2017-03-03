print("\n\n\t\t\t JAMES BITHELL 2017 \n\t\t\t Raspberry Pi Weather Station \n\t\t\t Core Logging Function")

import time #For timestamp handling
import sqlite3  # SQLITE system
import os #For Paths
_dir = os.path.dirname(os.path.abspath(__file__)) # Setup _dir as __DIR__ PHP Equivalent
import requests #For connecting to web to upload data
import threading #Multi-threading support

print("Opening database")
def dict_factory(cursor, row): #Function from SO used to convert row to dictionary
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
conn = sqlite3.connect(str(_dir) + '/datastore.sqlite3', check_same_thread=False, timeout=30000) #Connect to local db
conn.row_factory = dict_factory
conncursor = conn.cursor()
print("Database connection open")

print("Getting Settings from DB")
conncursor.execute('SELECT * FROM settings LIMIT 1;')
settings = conncursor.fetchone()
if (len(settings) < 1):
    raise Exception("Could not find system settings - make sure you're running the correct script & following setup instructions ")
print("****SETTINGS RETRIEVED****")
print(settings)
print("****END       SETTINGS****")

currentdata = {"windspeed": 0, "winddirectioncompass": "ERROR", "winddirectiondegrees": "0", "realvalues": True} #Initialise the current data

def upload_data(windspeed, winddirectioncompass, winddirectiondegrees):
    global settings
    try:
        request = requests.get(str(settings['uploadurl']) + "?windspeed=" + str(windspeed) + "&winddirectioncompass=" + str(winddirectioncompass) + "&winddirectiondegrees=" + str(winddirectiondegrees) + str(settings['request_append']))
        if (int(request.status_code) == 200 and str(request.content) == str(settings['request_success_response'])):
            return True
        else:
            print("UNKNOWN ISSUE WITH WEB REQUEST - Returned:")
            print(request.status_code)
            print(request.content)
            return False
    except requests.exceptions.HTTPError as e:
        print("HTTP Error - Consider a retry later")
        return False
    except requests.exceptions.SSLError as e:
        print("SSL ERROR")
        return False
    except requests.exceptions.Timeout as e:
        print("TIMEOUT ERROR")
        return False
    except requests.exceptions.RetryError as e:
        print("RETRY ERROR")
        return False
    except requests.exceptions.RequestException as e:
        print("**************MAJOR EXCEPTION - SOME KIND OF HTTP PROBLEM**************")
        print(e)
        print("ABORTING UPLOAD - WITHOUT DUMP TO SQL")
        return False
    except Exception as e:
        print("**************MAJOR EXCEPTION - UNKNOWN DETAILS**************")
        print(e)
        print("ABORTING UPLOAD - WITHOUT DUMP TO SQL")
        return False

def log_failed_request(windspeed, winddirectioncompass, winddirectiondegrees): #Log a failed request into the DB so we still have it and can upload it later
    global settings
    try:
        conncursor.execute('INSERT INTO `cache_upload_fails`(`utctimestamp`,`wind_speed`,`wind_direction_degrees`,`wind_direction_compass`) VALUES (' + str(round(time.time(),0)) + ',' + str(windspeed) + ',' + str(winddirectiondegrees) + ',"' + str(winddirectioncompass) + '");')
        conn.commit()
        print("Inserted failed request into table")
        return True
    except Exception as e:
        print(e)
        print("************************FAILED - COULD NOT INSERT FAILED REQUEST INTO DB************************ \n Ignoring and moving on")
        return False

def uploadfailedrequests(): #Upload all the requests that have recently failed
    global settings
    threading.Timer(int(2*60), uploadfailedrequests).start() #How often to try and upload failed requests in seconds
    print("~~~~~~~~~~Attempting to Upload Failed Requests~~~~~~~~~~")

    print("~~~~~~~~~~COMPLETED     Upload Failed Requests~~~~~~~~~~")

def processdata():
    threading.Timer(settings["upload_frequency"], processdata).start()  # How often to try and upload some readings - in seconds
    if (currentdata["realvalues"] != True):
        #There hasn't been any real data actually set yet - so we should wait for that to happen later
        return False
    print("Attempting Upload")
    if (upload_data(currentdata["windspeed"],currentdata["winddirectioncompass"],currentdata["winddirectiondegrees"]) != True):
        print("Request failed - logging")
        log_failed_request(currentdata["windspeed"],currentdata["winddirectioncompass"],currentdata["winddirectiondegrees"])

def main():
    uploadfailedrequests()
    processdata()
    while True:
        #currentdata #Set this all the time
        pass #Logging etc goes here

main()