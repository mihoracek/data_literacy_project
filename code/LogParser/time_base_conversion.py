#!/usr/bin/env python3

import sys
import argparse
import shutil
from enum import Enum
from candb import CanDB
from log_parser import asciiInput, asciiOutput

class TimeBase(Enum):
	Relative = 0
	Absolute = 1

	@staticmethod
	def from_str(s):
		assert s in ['relative', 'absolute']
		return TimeBase.Relative if s == 'relative' else TimeBase.Absolute


def convert_time_base(input_file_name, output_file_name, desired_base : TimeBase):
	input_stream = asciiInput(input_file_name)
	input_metadata = input_stream.get_log_metadata()

	has_relative = input_metadata.relative_timestamps
	wants_relative = desired_base == TimeBase.Relative

	if has_relative == wants_relative: # the source and destination time base match. Copy is sufficient
		shutil.copyfile(input_file_name, output_file_name)
		return


	output_stream = asciiOutput(output_file_name, input_metadata._replace(relative_timestamps = wants_relative))
	for message in input_stream:
		output_stream.append(message)




if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'Converts CAN log file between relative and absolute timestamps.')

	parser.add_argument('--in', metavar="file", dest='input_file', type=str, help='path to input file')
	parser.add_argument('--out', metavar="file", dest='output_file', type=str, help='path to output file')
	parser.add_argument('destination_format', choices=['relative', 'absolute'], help='format to be used by the processed log.')

	args = parser.parse_args()
	if args.input_file is None or args.output_file is None:
		print('You must specify both the input file as well as output file!')
		sys.exit(1)


	convert_time_base(args.input_file, args.output_file, TimeBase.from_str(args.destination_format))
