#!/bin/bash

help() {
    
    echo
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "    -u, --user        [Required] Intratime user"
    echo "    -p, --password    [Required] Intratime password"
    echo "    -a, --action      [Required] Clock in/out action: 0 = Check in; 1 = Check out; 3 = Pause; 4 = Return"
    echo "    -h, --help        Show this help."
    echo "NOTE: Please review if you have installed jq"
    echo
    exit $1

}

clock_in_out() {

    DATE=$(date +%F)

    TOKEN=$(curl -s --location --request POST "http://newapi.intratime.es/api/user/login" --header "Accept: application/vnd.apiintratime.v1+json" --header "Content-Type: application/x-www-form-urlencoded; charset:utf8" --data "user=${USER}&pin=${PASSWORD}" | jq ".USER_TOKEN" -r )
   
    if [ "$(echo $TOKEN)" == "null" ]; then
        echo "Token operation failed"
    else
        CLOCK_ACTION=$(curl -s --location --request POST "http://newapi.intratime.es/api/user/clocking" --header "Accept: application/vnd.apiintratime.v1+json" --header "token: ${TOKEN}" --form "user_action=${ACTION}" --form "user_timestamp=${DATE}" --form "user_use_server_time=true" | jq ".INOUT_CREATETIME" -r )
        echo "Register created at: $CLOCK_ACTION"
    fi

}

main() {
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
                    help 1 
                fi
                ;;
            "-p"|"--password")
                if [ -n "$2" ]; then
                    PASSWORD="$2"
                    shift 2
                else
                    help 1 
                fi
                ;;
            "-a"|"--action")
                if [ -n "$2" ]; then
                    ACTION="$2"
                    shift 2
                else
                    help 1 
                fi
                ;;
            *)
                help 1  
            esac             
        done
    
    if [ -n ${USER} ] && [ -n ${PASSWORD} ] && [ -n ${ACTION} ]; then
        clock_in_out 
    else 
        help 1 
    fi
}   

main "$@"