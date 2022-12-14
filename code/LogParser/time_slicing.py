#!/usr/bin/env python3

import sys
import argparse, re, math
from candb import CanDB
from log_parser import asciiInput, asciiOutput
from collections import namedtuple, deque
from enum import Enum

Transform = namedtuple('Transform', ['action', 'begin', 'end'])
valid_human_time = re.compile('^(?:[0-9]+)(?::[0-9]+){0,2}(?:\.[0-9]{1,3})?$')
valid_timestamp = re.compile('^[0-9]+(?:\.[0-9]+)?$')
valid_transform_regex = re.compile(r'^\s*((?:keep)|(?:discard))\s+((?:[0-9]+)(?::[0-9]+){0,2}(?:\.[0-9]{1,3})?)\s*\.\.\.?\s*((?:[0-9]+)(?::[0-9]+){0,2}(?:\.[0-9]{1,3})?)\s*$')

class Action(Enum):
	Keep = 0
	Discard = 1

	@staticmethod
	def from_str(s):
		assert s in ['keep', 'discard']
		return Action.Keep if s == 'keep' else Action.Discard

def transform_to_string(transform):
	return f'{"keep" if transform.action == Action.Keep else "discard":>8} from {timestamp_to_human_time(transform.begin):>12} ({transform.begin:>10.3f} s) to {timestamp_to_human_time(transform.end):>12} ({transform.end:>10.3f} s)'

def human_time_to_timestamp(human_time):
	assert re.search(valid_human_time, human_time)
	parts = human_time.split(':')
	ms_extra = 0
	if '.' in parts[-1]: # ms specified as well
		s, ms = parts[-1].split('.')
		parts[-1] = s
		ms_extra = int(ms) / 1000

	return sum(60**power * part for power, part in enumerate(map(int, reversed(parts)))) + ms_extra

def timestamp_to_human_time(timestamp):
	if timestamp == math.inf:
		return "end of time"
	frac, whole = math.modf(timestamp)
	whole = int(whole)

	parts = []
	while whole != 0:
		parts.append(f'{whole % 60:02}')
		whole = whole // 60
	if not parts:
		parts = ['0']
	return ':'.join(reversed(parts)) + f'.{frac:.3f}'[2:]

def parse_time(time_str):
	if re.search(valid_human_time, time_str):
		return human_time_to_timestamp(time_str)
	elif re.search(valid_timestamp, time_str):
		return float(time_str)
	else:
		assert False

def is_fully_nested_within(inner, outer):
	return inner.begin >= outer.begin and inner.end <= outer.end

def canonicalize_transforms(transform_list):
	transform_list = list(map(lambda s:s.lower(), transform_list))
	canonical = []

	index = 0
	while index < len(transform_list):
		tranform_str = transform_list[index]
		while not re.search(valid_transform_regex, tranform_str):
			if index == len(transform_list) - 1:
				print(f'Could not parse string "{tranform_str}" as a valid transformation. Exiting...')
				sys.exit(1);
			index += 1
			tranform_str += ' ' + transform_list[index]
		match = re.match(valid_transform_regex, tranform_str);
		assert match
		begin = parse_time(match.group(2))
		end = parse_time(match.group(3))
		canonical.append(Transform(action=Action.from_str(match.group(1)), begin=begin, end=end))
		index += 1

	return canonical

def can_be_merged(first, second):
	return first.action == second.action or is_fully_nested_within(second, first)


def merge_transforms(first, second):
	if first.action != second.action:
		assert is_fully_nested_within(second, first)
		return [Transform(action = first.action, begin=first.begin, end = second.begin),
		 second,
		 Transform(action = first.action, begin=second.end, end = first.end)]
	else:
		return [Transform(action = first.action, begin = min(first.begin, second.begin), end = max(first.end, second.end))]

def handle_overlapping_transforms(possibly_overlapping_transformations, default_action = Action.Keep):
	new_transformations = [Transform(action = default_action, begin = 0, end = possibly_overlapping_transformations[0].begin)]

	currently_open_transformations = [possibly_overlapping_transformations[0]]
	index = 1
	while True:
		transforms_remaining = index < len(possibly_overlapping_transformations)
		to_be_opened = possibly_overlapping_transformations[index] if transforms_remaining else None

		if len(currently_open_transformations) == 0:
			if not transforms_remaining:
				new_transformations.append(Transform(action = default_action, begin = new_transformations[-1].end, end = math.inf))
				break
			currently_open_transformations.append(to_be_opened)
			index += 1
			new_transformations.append(Transform(action = default_action, begin = new_transformations[-1].end, end = to_be_opened.begin))
			continue

		to_be_closed = min(currently_open_transformations, key = lambda trans: trans.end)

		if transforms_remaining and to_be_opened.begin < to_be_closed.end:
			currently_open_transformations.append(to_be_opened)
			index += 1
			continue

		# There is some transformation being closed...

		is_most_nested = to_be_closed == currently_open_transformations[-1]
		all_same_action = all(t.action == to_be_closed.action for t in currently_open_transformations)

		if all_same_action:
			currently_open_transformations.remove(to_be_closed)
			if len(currently_open_transformations) == 0:
				new_transformations.append(to_be_closed)
			continue

		if not is_most_nested:
			print('Conflicting non-nested overlapping transformations!')
			for t in currently_open_transformations: print(t)
			sys.exit(1)

		# The conflicting action is the most nested one
		for prev, next in zip(currently_open_transformations[:-1], currently_open_transformations[1:]):
			new_transformations.append(Transform(action = prev.action, begin = prev.begin, end = next.begin))
		new_transformations.append(to_be_closed)
		currently_open_transformations.remove(to_be_closed)
		currently_open_transformations = [Transform(action = t.action, begin = to_be_closed.end, end = t.end) for t in currently_open_transformations]

	return new_transformations

def merge_neighbouring_transformations(transformations):
	new_transformations = [transformations[0]]

	for transform in transformations[1:]:
		prev = new_transformations[-1]
		if transform.action == prev.action:
			new_transformations[-1] = Transform(action = transform.action, begin = prev.begin, end = transform.end)
		else:
			new_transformations.append(transform)

	return new_transformations

def filter_out_invalid_transformations(transformations):
	invalid_transformations = list(filter(lambda trans: trans.end <= trans.begin, transformations)) # Ignore transformations with end < begin
	for transform in invalid_transformations:
		transformations.remove(transform)
	return transformations, invalid_transformations

def slice_log_time(input_name, output_name, transformations, preserve_timestamps):
	input_stream = asciiInput(input_name)
	output_stream = asciiOutput(output_name, input_stream.get_log_metadata())

	transformation_index = 0
	total_time_discarded = 0
	current_transform = transformations[transformation_index]
	for message in input_stream:
		if message.timestamp >= current_transform.end:
			transformation_index += 1
			if current_transform.action == Action.Discard:
				total_time_discarded += current_transform.end - current_transform.begin
			current_transform = transformations[transformation_index]

		if current_transform.action == Action.Keep:
			if not preserve_timestamps:
				message = message._replace(timestamp = message.timestamp - total_time_discarded)
			output_stream.append(message)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'Allows cutting of CAN log files. Portions of data are cut out (discarded) or preserved in the output.')

	parser.add_argument('--in', metavar="file", dest='input_file', type=str, help='path to input file')
	parser.add_argument('--preserve_timestamps', action='store_true', help='When specified, timestamps in the log file are preserved, only specified data is discarded.When not specified, timestamps are adjusted, as if discarded data had never occured')
	parser.add_argument('--out', metavar="file", dest='output_file', type=str, help='path to output file')
	parser.add_argument('transformations', action='append', nargs='+', help='transformations to perform. Must be of form "(keep)|(discard) start...?end", where start and end are either floating point numbers representing timestamp in seconds or have the form [0-9]+(:[0-9]+)+(\.[0-9])? matching the timestamp format hh:mm:ss.ms')
	parser.add_argument('--default', dest='default_action',default='keep', choices=['discard', 'keep'], help='The default transformation used for time spans without transformation specified')

	args = parser.parse_args()

	if args.input_file is None or args.output_file is None:
		print('You must specify both the input file as well as output file!')
		sys.exit(1)

	transformations = canonicalize_transforms(args.transformations[0])

	transformations, discarded_transforms = filter_out_invalid_transformations(transformations)
	print(f'Ignoring {len(discarded_transforms)} transformation{"s" if len(discarded_transforms) > 1 else ""}:')
	for transform in discarded_transforms:
		print(transform_to_string(transform))
	print()

	transformations.sort(key = lambda trans:trans.begin)

	transformations = handle_overlapping_transforms(transformations, Action.from_str(args.default_action))
	transformations = merge_neighbouring_transformations(transformations)


	print('Transformations to carry out:')
	for transform in transformations:
		print(transform_to_string(transform))

	slice_log_time(args.input_file, args.output_file, transformations, args.preserve_timestamps)
