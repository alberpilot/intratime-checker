# intratime-checker
Simple script for check-in/out using Intratime API

This script facilitate the check-in/out operation using the Intratime API. It could be used with cronjobs. 

How to use it: 
```
Usage: ./intratime_checker.sh [OPTIONS]

    -u, --user        [Required] Intratime user
    -p, --password    [Required] Intratime password
    -a, --action      [Required] Clock in/out action: 0 = Check in; 1 = Check out; 3 = Pause; 4 = Return
    -h, --help        Show this help.
```

NOTE: Please review if you have installed `jq`

Example: 
```
./intratime_checker.sh -u user@email.com -p 1234 -a 0
```
