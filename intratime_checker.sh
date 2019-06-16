#!/bin/bash
echo "INTRATIME CHECKER v0.0.1"

command -v jq >/dev/null 2>&1 || { echo >&2 "Software jq is required but it's not installed. Please, install it before using this script."; exit 1; }

API_URL="http://newapi.intratime.es"
API_LOGIN_PATH="/api/user/login"
API_CLOCKING_PATH="/api/user/clocking"
API_APPLICATION_HEADER="Accept: application/vnd.apiintratime.v1+json"
API_CONTENT_HEADER="Content-Type: application/x-www-form-urlencoded; charset:utf8"

help() {
    
    echo
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "    -u, --user        [Required] Intratime user"
    echo "    -p, --password    [Required] Intratime password"
    echo "    -a, --action      [Required] Clock in/out action: 0 = Check in; 1 = Check out; 3 = Pause; 4 = Return"
    echo "    -d, --date        [Optional] Clock in/out date. E.g: 2019-06-16"
    echo "    -t, --time        [Optional] Clock in/out time. E.g: 09:00"
    echo "    -h, --help        Show this help."
    echo
    exit $1
    
}

clock_in_out() {
    
    TOKEN=$(curl -s --location --request POST "$API_URL""$API_LOGIN_PATH" --header "$API_APPLICATION_HEADER" --header "$API_CONTENT_HEADER" --data "user=${USER}&pin=${PASSWORD}" | jq ".USER_TOKEN" -r )
    echo $DATE $TIME
    if [ "$(echo $TOKEN)" == "null" ]; then
        echo "Token operation failed"
    else
        USE_SYSTEM_TIME=false
        [ $TIME ] || USE_SYSTEM_TIME=true
        CLOCK_ACTION=$(curl -s --location --request POST "$API_URL""$API_CLOCKING_PATH" --header "$API_APPLICATION_HEADER" --header "token: ${TOKEN}" --form "user_action=${ACTION}" --form "user_timestamp=$DATE$TIME" --form "user_use_server_time=$USE_SYSTEM_TIME" | jq ".INOUT_CREATETIME" -r  )
        if [ "$(echo $CLOCK_ACTION)" == "null" ]
        then
            echo "Something went wrong"
        else
            echo "Register created"
        fi
    fi
    
}

main() {
    
    if [ -n "$1" ]
    then
        # Reading command line arguments
        while [ -n "$1" ]
        do
            case "$1" in
                "-h"|"--help")
                    help 0
                ;;
                "-u"|"--user")
                    if [ -n "$2" ]; then
                        USER="$2"
                        shift 2
                    else
                        echo "User parameter is required"
                        help 1
                    fi
                ;;
                "-p"|"--password")
                    if [ -n "$2" ]; then
                        PASSWORD="$2"
                        shift 2
                    else
                        echo "Password parameter is required"
                        help 1
                    fi
                ;;
                "-a"|"--action")
                    if [ -n "$2" ]; then
                        ACTION="$2"
                        shift 2
                    else
                        echo "Action parameter is required"
                        help 1
                    fi
                ;;
                "-d"|"--date")
                    if [ -n "$2" ]; then
                        DATE="$2"
                        if [[ "`date '+%Y-%m-%d' -d $DATE 2>/dev/null`" = "$DATE" ]]
                        then
                            echo "Using $DATE as date"
                        else
                            echo "Date $DATE is in an invalid format (not YYYY-MM-DD)"
                            exit 1
                        fi
                        shift 2
                    else
                        DATE=$(date +%F)
                        echo "Using $DATE as date"
                    fi
                ;;
                "-t"|"--time")
                    if [ -n "$2" ]; then
                        TIME="$2"
                        if [[ "`date '+%H:%M' -d $TIME 2>/dev/null`" = "$TIME" ]]
                        then
                            TIME="$2:00"
                            echo "Using $TIME as time"
                        else
                            echo "Time $TIME is in an invalid format (not HH:MM)"
                            exit 1
                        fi
                        shift 2
                    fi
                ;;
                *)
                    help 1
            esac
        done
    else
        help 1
    fi
    if [ -n ${USER} ] && [ -n ${PASSWORD} ] && [ -n ${ACTION} ]; then
        clock_in_out
    else
        help 1
    fi
}

main "$@"