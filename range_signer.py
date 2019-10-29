#  Range signer
#  -----------------
#  @okynos
#  License: GNU General Public License v3.0
#  Version 1.0

import argparse
import random
import os
import random
from datetime import datetime, date, timedelta

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--user", type=str, required=True, dest='user',
      metavar='<str>', help="Intratime username.")
    ap.add_argument("-p", "--password", type=str, required=True, dest='password',
      metavar='<str>', help="Intratime login password.")

    ap.add_argument("-f", "--from-date", type=str, required=True, dest='from_date',
      metavar='<str>', help="...")
    ap.add_argument("-t", "--to-date", type=str, required=True, dest='to_date',
      metavar='<str>', help="...")

    ap.add_argument("-i", "--in-time", type=str, required=True, dest='in_time',
      metavar='<str>', help="...")
    ap.add_argument("-s", "--pause-time", type=str, required=True, dest='pause_time',
      metavar='<str>', help="...")
    ap.add_argument("-r", "--return-time", type=str, required=True, dest='return_time',
      metavar='<str>', help="...")
    ap.add_argument("-o", "--out-time", type=str, required=True, dest='out_time',
      metavar='<str>', help="...")

    args = ap.parse_args()

    start_date = datetime.strptime(args.from_date, DATE_FORMAT)
    end_date = datetime.strptime(args.to_date, DATE_FORMAT)
    days = (end_date - start_date).days

    in_time = datetime.strptime(args.in_time, TIME_FORMAT)
    pause_time = datetime.strptime(args.pause_time, TIME_FORMAT)
    return_time = datetime.strptime(args.return_time, TIME_FORMAT)
    out_time = datetime.strptime(args.out_time, TIME_FORMAT)

    it_date = start_date
    for i in range(days):
        random_it_in_time = in_time + timedelta(minutes=random.randint(0,10), seconds=random.randint(1,59))
        os.system('python intratime_checker.py -u {0} -p {1} -a in -d {2} -t {3}'
          .format(args.user, args.password, it_date.strftime(DATE_FORMAT), random_it_in_time.strftime(TIME_FORMAT)))

        random_it_pause_time = pause_time + timedelta(minutes=random.randint(0,10), seconds=random.randint(1,59))
        os.system('python intratime_checker.py -u {0} -p {1} -a pause -d {2} -t {3}'
          .format(args.user, args.password, it_date.strftime(DATE_FORMAT), random_it_pause_time.strftime(TIME_FORMAT)))

        random_it_return_time = return_time + timedelta(minutes=random.randint(0,10), seconds=random.randint(1,59))
        os.system('python intratime_checker.py -u {0} -p {1} -a return -d {2} -t {3}'
          .format(args.user, args.password, it_date.strftime(DATE_FORMAT), random_it_return_time.strftime(TIME_FORMAT)))

        random_it_out_time = out_time + timedelta(minutes=random.randint(0,10), seconds=random.randint(1,59))
        os.system('python intratime_checker.py -u {0} -p {1} -a out -d {2} -t {3}'
          .format(args.user, args.password, it_date.strftime(DATE_FORMAT), random_it_out_time.strftime(TIME_FORMAT)))
        it_date += timedelta(days=1)
