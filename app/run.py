import multiprocessing
import os
import argparse
import sys

from app.dispatcher.dispatcher import Dispatcher

if __name__ == '__main__':
    if sys.platform.startswith("win"):
        multiprocessing.freeze_support()

    parser = argparse.ArgumentParser()
    parser.add_argument("-np", "--num_process",
                        dest="num_process", action="store", default=1, type=int, choices=range(1, os.cpu_count()))
    parser.add_argument("-nc", "--num_connection",
                        dest="num_connection", action="store", default=1, type=int)
    args = parser.parse_args()

    dispatcher = Dispatcher(num_process=args.num_process, num_connection=args.num_connection)
    dispatcher.dispatch()
