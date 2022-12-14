#!/usr/bin/env python3

import sys, numpy, argparse, math, scipy
import argparse
from candb import CanDB
from log_parser import asciiInput, asciiOutput


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="Converts the input ASCII file to .mat and resamples all signals to equal time base.\n"
    "Example call: python3.9 convert_to_mat.py --json $repos/../jsons/FSE11.json --in $winhome/eForce/FSE11_2022-09-14_170930.asc --sampling-rate 100")

parser.add_argument('--json', metavar="file", dest='json_files', type=str, action='append', help='add candb json file to parse')
parser.add_argument('--in', metavar="file", dest='input_file', type=str, help='path to input file.')
parser.add_argument('--sampling-rate', metavar="freq", dest='sampling_rate', type=str, help='Common sampling frequency for all signals (default 100 Hz).')
# TODO implement interpolation parser.add_argument('--interpolation', dest='interpolation', type=str, choices=["ZOH", "FOH"], default="ZOH", help='How to interpolate between two points - piecewise constant or linear function')
# interpolate = args.interpolation == 'FOH'

args = parser.parse_args()

if None in [args.json_files, args.input_file]:
    parser.print_help()
    sys.exit(0)

db = CanDB(args.json_files)

input_stream = asciiInput(args.input_file)

sampling_interval= 1 / int(args.sampling_rate if args.sampling_rate is not None else "100")

# Dictionary of msg ID to (list of timestamps, list of numpy arrays with values of fields)
message_dict = {msg.identifier : ([], [[] for field in msg.fields]) for msg in db.parsed_messages.values()}

print('Parsing log file')

max_time = None
ignored_messages = []
next_time_to_print = 1

for message in input_stream:

    msg = db.parseData(message.id, message.data, message.timestamp)
    if message.id not in message_dict:
        if message.id not in ignored_messages:
            print(f'Ignoring message id {hex(message.id)}')
            ignored_messages.append(message.id)
        continue # unknown message, ignore it
    timestamps, field_list = message_dict[message.id]
    timestamps.append(message.timestamp)
    for i in range(len(field_list)):
        # TODO consider supporting arrays
        field_list[i].append(msg.fields[i].value[0])
    
    max_time = message.timestamp
    if max_time > next_time_to_print:
        next_time_to_print += 1
        print(f'\rParsed {max_time / 60:8.2f} minutes of messages', end='')

print(f'\nParsed {sum(len(timestamp) for timestamp, data in message_dict.values())} messages, log length {max_time:.6} seconds.')

# Considering the sampling interval, all signals will be this long:
vector_length = int(math.ceil(max_time / sampling_interval))
print(f'All vectors will be {vector_length} elements long.')
# Dictionary signal name -> list of values
time_vector = [i * sampling_interval for i in range(vector_length)]
output = {'Time' : time_vector}

for id, data in message_dict.items():
    message = db.getMsgById(id)
    if len(data[0]) == 0: # never received this message
        continue
    for field, values in zip(message.fields, data[1]):
        vector = [0.0] * vector_length
        input_index = 0
        output_index = 0
        while output_index < vector_length:
            if input_index >= len(data[0]):
                vector[output_index] = values[-1]
            else:
                vector[output_index] = values[input_index]
                while input_index < len(data[0]) and time_vector[output_index] > data[0][input_index]:
                    input_index += 1
            output_index += 1

        signal_name = f'{message.owner}_{message.name}_{field.name}'
        output[signal_name] = vector
    print(f'Resampled {message.owner}_{message.name} (received {len(data[0])} times)')

output_name = '.'.join(args.input_file.split('.')[0:-1]) + '.mat'
print(f'Writing {output_name} file with {len(output)} variables...')

scipy.io.savemat(output_name, mdict=output, do_compression=True, oned_as='column')