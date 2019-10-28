#  Intratime-checker
#  -----------------
#  @jmv74211
#  @okynos
#  License: GNU General Public License v3.0
#  Version 1.0

import argparse
import requests
import json
import sys
import random
from datetime import datetime

#-------------------------------------------------------------------------------
# GLOBAL VARS
#-------------------------------------------------------------------------------

API_URL = "http://newapi.intratime.es"
API_LOGIN_PATH =  "/api/user/login"
API_CLOCKING_PATH = "/api/user/clocking"
API_APPLICATION_HEADER = "Accept: application/vnd.apiintratime.v1+json"
API_HEADER = {
                "Accept": "application/vnd.apiintratime.v1+json",
                "Content-Type": "application/x-www-form-urlencoded",
                "charset":"utf8"
             }

#-------------------------------------------------------------------------------
# AUXILIARY FUNCTIONS
#-------------------------------------------------------------------------------

"""
    Function to check the date and time format. Can be:
        - date format: HH:MM:SS, H:M:D
        - time format: YYYY-mm-dd, YYYY-m-d
    provided that the value of the numbers makes sense

    Parameters:
        - date(String): example -->  2019-10-22
        - time(String): example --> 20:04:23
"""

def check_date_time_format(date, time):

    if date != None:
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print("Incorrect data format, should be YYYY-MM-DD")
            sys.exit(1)

    if time != None:
        try:
            datetime.strptime(time, '%H:%M:%S')
        except ValueError:
            print("Incorrect time format, should be HH:MM:SS")
            sys.exit(1)

#-------------------------------------------------------------------------------

"""
    Function to transform an action into its respective code

    Parameters:
        - action: example --> ['in, out, pause, return]

    Return
        (int): API action code
"""

def get_action(action):

    switcher = {
        "in": 0,
        "out": 1,
        "pause": 2,
        "return": 3,
    }

    try:
        return switcher[action]
    except:
        print("ERROR: Invalid action. Choose from 'in', 'out', 'pause', 'return' ")
        sys.exit(1)

#-------------------------------------------------------------------------------

"""
    Function to get the current date and time

    Return
        (String): example --> 2019-10-10 20:00:05
"""

def get_current_date_time():

    now = datetime.now()
    date_time = "{0} {1}".format(now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"))

    return date_time

#-------------------------------------------------------------------------------

"""
    Function to obtain random coordinates around the Wazuh office (Av. del Desarrollo, 22-26, 18100)

    Return
        (Tuple-Float): example --> (37.1472542, -36086542)
"""

def get_random_coordinates():

    w = random.randint(1000,8324) # West of Greenwich meridian
    n = random.randint(5184,7163)  # North of Ecuador

    wazuh_location_w = float("37.147{0}".format(w))
    wazuh_location_n = float("-3.608{0}".format(n))

    return wazuh_location_w, wazuh_location_n

#-------------------------------------------------------------------------------
# MAIN FUNCTIONS
#-------------------------------------------------------------------------------

"""
    Function to identify yourself in the API and obtain the authentication token

    Parameters:
        - username(String): example --> user@gmail.com
        - password(String): example --> 91

    Return
        (String): Authentication token
"""

def get_login_token(username, password):

    login_api_url = "{0}{1}".format(API_URL, API_LOGIN_PATH)
    payload="user={0}&pin={1}".format(username, password)

    try:
        request = requests.post(login_api_url, data=payload, headers=API_HEADER)
        token = json.loads(request.text)['USER_TOKEN']
    except:
        print("ERROR: Invalid username or password")
        sys.exit(1)

    return token

#-------------------------------------------------------------------------------

"""
    Function to register an entry, exit, pause or return with a specific date and time

    Parameters:
        - action(String): example --> ['in, out, pause, return]
        - token(String): Authentication token
        - date(String): example --> 2019-10-10
        - time(String): example --> 17:25:05

    Note: If the date or time is None, the current date time will be selected.
"""

def clocking(action, token, date=None, time=None):

    if time == None and date == None:
        date_time = get_current_date_time()
    else:
        date_time = "{0} {1}".format(date, time)

    wazuh_location_w, wazuh_location_n = get_random_coordinates()

    api_action = get_action(action) # in --> 0, out --> 1, pause --> 3, return --> 4
    clocking_api_url = "{0}{1}".format(API_URL, API_CLOCKING_PATH)
    API_HEADER.update({ "token": token })

    payload = "user_action={0}&user_use_server_time={1}&user_timestamp={2}&user_gps_coordinates={3},{4}" \
                .format(api_action, False, date_time, wazuh_location_w, wazuh_location_n)
    try:
        request = requests.post(clocking_api_url, data=payload, headers=API_HEADER)
        if request.status_code == 201:
            print("Registration successfully: [ action: {0}, date_time: {1}, user_coordinates: ({2},{3}) ]"
                .format(action, date_time, wazuh_location_w, wazuh_location_n))
        else:
            print("ERROR: Registration failed, please try again")
            sys.exit(1)
    except:
        raise
        print("ERROR: The request could not be sent to intratime API. Status code = {0}".format(request.status_code))
        sys.exit(1)

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--user", type=str, required=True,
      metavar='<str>', help="Intratime username.")
    ap.add_argument("-p", "--password", type=str, required=True,
      metavar='<str>', help="Intratime login password.")
    ap.add_argument("-a", "--action", type=str, required=True,
      metavar='<str>', choices=['in','out','pause','return'],
      help="Action to run against intratime API.")
    ap.add_argument("-d", "--date", type=str, required=False,
      metavar='<str>', help="Date to use in action format: YYYY-mm-dd")
    ap.add_argument("-t", "--time", type=str, required=False,
      metavar='<str>', help="Time to use in action format: hh:mm:ss")
    args = ap.parse_args()

    check_date_time_format(args.date, args.time)
    token = get_login_token(args.user, args.password)
    clocking(args.action, token, args.date, args.time)
