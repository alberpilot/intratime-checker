# Intratime checker

Simple script for check-in/out using Intratime API

_Tip: you may want to use in combination with cronjobs._

#### How to use it

```
Usage: ./intratime_checker.sh [OPTIONS]

    -u, --user        [Required] Intratime user
    -p, --password    [Required] Intratime password
    -a, --action      [Required] Clock in/out action: 0 = Check in; 1 = Check out; 2 = Pause; 3 = Return
    -d, --date        [Optional] Clock in/out date. E.g: 2019-06-16"
    -t, --time        [Optional] Clock in/out time. E.g: 09:00:00"
    -h, --help        Show this help.
```

**Example**

```
./intratime_checker.sh -u user@email.com -p 1234 -a 0 -d 2019-06-16 -t 09:00:00
```

#### Contributing

Fork this repository, then make a pull request. The team will review it as soon as possible.

#### I don't like bash, what to do?

It would be nice to receive ports for other languages, feel free to make your own port.
