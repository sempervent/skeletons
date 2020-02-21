#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" this provides a skeleton for a python script that uses argparse """
import sys
import logging
import argparse

# initialize with a verbosity of 0
VERBOSITY = 0


# modify the logging format to fit your need
FORMAT = "[%(asctime)s - %(levelname)4s - %(filename)8s:%(funcName)s"
FORMAT += ':%(lineno)s] %(message)s'

LOG_FILE = f'/tmp/{__name__}.log'

logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="%Y/%m/%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)


def create_parser():
    """ create a parser for arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", type=int,
                        help="increase output verbosity",
                        target='VERBOSITY', action=add)
    return parser


def main():
    logging.debug('Creating parser')
    parser = create_parser()
    logging.debug('Created parser')
    args = parser.parse_args()
    logging.debug('Retrieved arguments')
    if args.verbosity > 0:
        logging.info('Beginning main logic')


if __name__ == "__main__":
    main()
