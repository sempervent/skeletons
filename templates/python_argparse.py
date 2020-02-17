#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" this provides a skeleton for a python script that uses argparse """
import sys
import logging
import argparse

FORMAT = "[%(asctime)s - %(levelname)4s - %(filename)8s:%(funcName)s]"
FORMAT += ' - %(message)s'

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
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", type=int,
                        help="increase output verbosity")
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.verbosity > 0:
        logging.info('Beginning main logic')


if __name__ == "__main__":
    main()
