#!/usr/bin/env python3

"""
Extract a period from dataset
author@: Gerald Lonlas
github@: https://github.com/glonlas/freqtrade-strategies
"""

import logging
import argparse
import sys
import json
import os
from datetime import datetime


logger = logging.getLogger('Bittrex_Extractor')


def list_files(directory, extension):
    return [f for f in os.listdir(directory) if f.endswith('.' + extension)]


def arg_valid_date(arg):
    try:
        return datetime.strptime(arg, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(arg)
        raise argparse.ArgumentTypeError(msg)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Bittrex ticker extractor. Extract data period from Bittrex ticker file"
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Switch the script to logger DEBUG',
        action='store_const',
        dest='loglevel',
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        '-f', '--folder',
        help='Source Folder that contains the JSON files',
        dest='source',
        default=os.path.join('user_data', 'data'),
        type = str,
        metavar = 'PATH',
    )
    parser.add_argument(
        '-d', '--destination',
        help='Destination folder where to store the new files',
        dest='destination',
        required=True,
        type=str,
        metavar='PATH',
    )
    parser.add_argument(
        '-s', '--start',
        help='Start date. Format YYYY-MM-DD',
        dest='start',
        required = True,
        type=arg_valid_date
    )
    parser.add_argument(
        '-e', '--e',
        help='End date Format YYYY-MM-DD',
        dest='end',
        required=True,
        type=arg_valid_date
    )
    return parser.parse_args(args)


def init_logger(loglevel):
    logging.basicConfig(
        level=loglevel,
        format='%(asctime)s - %(message)s',
    )


def main(args):
    logger.info('Start Bittrex ticker extractor')
    logger.info('------------------------------')
    logger.info('source: %s' % args.source)
    logger.info('Destination: %s' % args.destination)
    logger.info('From: %s to: %s' % (args.start, args.end))

    source = args.source
    destination = args.destination
    files = list_files(source, 'json')

    start = args.start
    end = args.end

    for file in files:
        with open(os.path.join(source, file)) as json_file:
            logger.info('Opening: %s' % os.path.join(source, file))
            tickers = json.load(json_file)

            logger.info('Parsing tickers')
            new_data = []
            for ticker in tickers:
                date = datetime.strptime(ticker['T'], "%Y-%m-%dT%H:%M:%S")
                if start <= date < end:
                    new_data.append(ticker)


            dest_file = os.path.join(destination, file)
            with open(dest_file, 'w') as outfile:
                logger.info('Writing new file: %s', dest_file)
                json.dump(new_data, outfile)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    init_logger(args.loglevel)
    main(args)

