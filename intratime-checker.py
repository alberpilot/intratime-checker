
#  Intratime-checker
#  -----------------
#  @jmv74211
#  License: GNU General Public License v3.0
#  Versión 1.1

import argparse
import requests
import json
import sys
import random
import yaml # PyYAML version 5.1 or greeter due to CVE
from datetime import datetime

# ---------------------------------------------------------------------------------------------------------------------
# GLOBAL VARS
# ---------------------------------------------------------------------------------------------------------------------

CONFIG_FILE = "config.yaml"
API_URL = "http://newapi.intratime.es"
API_LOGIN_PATH =  "/api/user/login"
API_CLOCKING_PATH = "/api/user/clocking"
API_APPLICATION_HEADER = "Accept: application/vnd.apiintratime.v1+json"
API_HEADER = {
                "Accept": "application/vnd.apiintratime.v1+json",
                "Content-Type": "application/x-www-form-urlencoded", 
                "charset":"utf8"
             }

# ---------------------------------------------------------------------------------------------------------------------
# AUXILIARY FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------

"""
    Function to print error messages

    Parameters:
        - error_message(String): Error message
"""

def print_error(error_message):

    ERROR_COLOR = '\033[91m'

    print("\n{0} Error: {1}\n".format(ERROR_COLOR,error_message))

# ---------------------------------------------------------------------------------------------------------------------

"""
    Function to print success messages

    Parameters:
        - message(String): Success message
"""

def print_success(message):

    OKGREEN_COLOR = '\033[92m'

    print("\n{0} SUCCESS: {1}\n".format(OKGREEN_COLOR, message))

# ---------------------------------------------------------------------------------------------------------------------

"""
    Function to store all arguments entered by the user in a dictionary

    Parameters:
        - args(argsparse): User arguments
    
    Return
        (Dictionary): User arguments
"""

def set_parameters(args):

    parameters = {}
    parameters['user'] = args.user
    parameters['password'] = args.password
    parameters['action'] = args.action

    # These parameters can be None
    parameters['date'] = args.date
    parameters['time'] = args.time

    return parameters

# ---------------------------------------------------------------------------------------------------------------------

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

    failed = False

    if date != None:
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print_error("Incorrect data format, should be YYYY-MM-DD")
            failed = True

    if time != None:
        try:
            datetime.strptime(time, '%H:%M:%S')
        except ValueError:
            print_error("Incorrect time format, should be HH:MM:SS")
            failed = True

    if failed:
        sys.exit(1)

# ---------------------------------------------------------------------------------------------------------------------

"""
    Function to transform an action into its respective code

    Parameters:
        - action(String): example --> ['in, out, pause, return]
    
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
        print_error("Invalid action. Choose from 'in', 'out', 'pause', 'return' ")
        sys.exit(1)

# ---------------------------------------------------------------------------------------------------------------------

"""
    Function to get the current date and time
    
    Return
        (String): example --> 2019-10-10 20:00:05
"""

def get_current_date_time():

    now = datetime.now()
    date_time = "{0} {1}".format(now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"))
 
    return date_time

# ---------------------------------------------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------------------------------------------

"""
    Function to obtain the arguments entered by the user interactively
    
    Return
        (Dictionary): User arguments
"""

def set_parameters_interactive():

    parameters = {}

    parameters['date'] =  input("Enter the date [YYYY-MM-DD] (default current date): ") 
    parameters['time'] =  input("Enter the time [HH:MM:SS] (default current time): ")
    parameters['action'] =  input("Enter the action [in, pause, return, out]: ")

    with open(CONFIG_FILE, 'r') as ymlfile:
        config_data = yaml.load(ymlfile, Loader=yaml.FullLoader)

    parameters['user'] = config_data['authentication']['user']
    parameters['password'] = config_data['authentication']['password'] 

    if parameters['date'] == '':
        parameters['date'] =  get_current_date_time().split(" ")[0].strip()
    
    if parameters['time'] == '':
        parameters['time'] =  get_current_date_time().split(" ")[1].strip()

    return parameters

# ---------------------------------------------------------------------------------------------------------------------

"""
    Function to check and validate the arguments entered by the user interactively

    Parameters:
        - parameters(Dictionary): User parameters
"""

def check_parameters_interactive(parameters):

    failed = False
    allowed_actions = ['in', 'pause', 'return', 'out']

    if parameters['user'] == '' or parameters['user'] == None:
        print_error("User can not be empty")
        failed = True

    if parameters['password'] == '' or parameters['password'] == None:
        print_error("Password can not be empty")
        failed = True

    if parameters['action'] == '' or parameters['action'] == None:
        print_error("Action can not be empty")
        failed = True

    elif parameters['action'] not in allowed_actions:
        print_error("The action is incorrect: Allowed values {0}".format(allowed_actions))
        failed = True

    check_date_time_format(parameters['date'], parameters['time'])

    if failed:
        sys.exit(1)

# ---------------------------------------------------------------------------------------------------------------------
# MAIN FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------

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
        print_error("Invalid username or password")
        sys.exit(1)
    
    return token

# ---------------------------------------------------------------------------------------------------------------------

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
            print_success("Registration successfully: [ action: {0}, date_time: {1}, user_coordinates: ({2},{3}) ]"
                .format(action, date_time, wazuh_location_w, wazuh_location_n))
        else:
            print_error("Registration failed, please try again")
            sys.exit(1) 
    except:
        print_error("The request could not be sent to intratime API. Status code = {0}".format(request.status_code))
        raise

# ---------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    # If script mode
    if len(sys.argv) > 1:

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("-u", "--user", type=str, required=True, help="Intratime username.")
        arg_parser.add_argument("-p", "--password", type=str, required=True, help="Intratime user password")
        arg_parser.add_argument("-a", "--action", type=str, required=True,  choices=['in','out','pause','return'], 
                                help="Action")
        arg_parser.add_argument("-d", "--date", type=str, help="Format YYYY-mm-dd")
        arg_parser.add_argument("-t", "--time", type=str, help="Format: hh:mm:ss")
        args = arg_parser.parse_args()
        
        parameters = set_parameters(args)

        check_date_time_format(parameters['date'], parameters['time'])

        token = get_login_token(parameters['user'], parameters['password'])

        clocking(parameters['action'], token, parameters['date'], parameters['time'])
    
    # If interactive mode
    else:
        
        parameters = set_parameters_interactive()

        check_parameters_interactive(parameters)

        token = get_login_token(parameters['user'], parameters['password'])

        clocking(parameters['action'], token, parameters['date'], parameters['time'])