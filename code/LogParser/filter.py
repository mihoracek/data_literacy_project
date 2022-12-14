#!/usr/bin/env python3

import sys
import argparse
from candb import CanDB
from log_parser import asciiInput, asciiOutput

parser = argparse.ArgumentParser(description="Filters input file using specified predicate and stores the result in output file."
        "Only messages for which 'cond' evaluates to true are kept, the rest is discarded. Timestamps and ASCII file encoding are preserved.")

parser.add_argument('--json', metavar="file", dest='json_files', type=str, action='append', help='add candb json file to parse')
parser.add_argument('--in', metavar="file", dest='input_file', type=str, help='path to input file. If ommited, stdin is used')
parser.add_argument('--out', metavar="file", dest='output_file', type=str, help='path to output file, If ommited, stdout is used')
parser.add_argument('--predicate', metavar="cond", dest='predicate', type=str, help='Python boolean expression evaluated for each message.')
parser.add_argument('--invert', action='store_true', help='If specified, logically negate the predicate after evaluation.')
parser.add_argument('--keep-unknown', dest='keep_unknown', action='store_true', help='If specified, unknown messages are kept. Otherwise they are discarded from output.')

args = parser.parse_args()

if None in [args.json_files, args.predicate]:
    parser.print_help()
    sys.exit(0)

db = CanDB(args.json_files)

input_stream = asciiInput(args.input_file if args.input_file is not None else sys.stdin)
output_stream = asciiOutput(args.output_file if args.output_file is not None else sys.stdout, input_stream.get_log_metadata())

if args.invert:
    args.predicate = f'not ({args.predicate})'

compiled_predicate = compile(args.predicate, "<string>", "eval")

for message in input_stream:

    msg = db.parseData(message.id, message.data, message.timestamp)

    if msg is None:
        if args.keep_unknown:
            output_stream.append(message)
        print("Unknow msg ID: '" + str(message) + "'")
        continue


    if eval(compiled_predicate):
        output_stream.append(message)
