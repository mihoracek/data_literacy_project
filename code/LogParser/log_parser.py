import candb

"""
Reads .asc log file and yields can messages
"""

from collections import namedtuple

RawMessage = namedtuple('RawMessage', ['timestamp', 'bus', 'id', 'is_extended', 'data'])
LogMetadata = namedtuple('LogMetadata', ['date_line', 'number_base', 'relative_timestamps'])

class asciiInput:

	def parse_message(self, tokens):
		# Each log record must have tokens [timestamp, bus, id, Rx, D, length]
		# If it does not, it is incomplete (e.g. the datalogger did not flush filesystem buffers)
		if len(tokens) < 6:
			print(f"Incomplete log record {tokens} discarded!")
			return None

		log_timestamp = float(tokens[0])
		if self.relative_timestamps:
			self.timestamp += log_timestamp
		else:
			self.timestamp = log_timestamp

		msg_bus = int(tokens[1], self.number_base)
		msg_is_ext = tokens[2][-1].lower() == 'x'
		if msg_is_ext:
			tokens[2] = tokens[2][:-1]
		msg_id = int(tokens[2], self.number_base)
		# Tx frames are currently ignored
		# TODO is it correct to ignore Tx frames?
		if tokens[3] == 'Tx':
			print(f'Ignoring TX message {tokens}.')
			return None
		assert tokens[3] == 'Rx' and tokens[4] == 'D'
		msg_data = list(map(lambda hex_code: int(hex_code, self.number_base), tokens[6:]))
		# Make sure there are no more bytes of data than expected
		assert int(tokens[5]) >= len(msg_data)
		if int(tokens[5]) < len(msg_data):
			print(f"Incomplete log record {tokens} discarded!")
			return None

		return RawMessage(timestamp = self.timestamp, bus = msg_bus, id = msg_id, is_extended = msg_is_ext, data=msg_data)

#  0.021740 2  338        Rx D 7 255 255 128   0   0   0   1
	def __init__(self, log_file_name : str):
		self.log_file = open(log_file_name)

		date_line = self.log_file.readline().split()
		assert date_line[0] == 'date'
		self.date_line = ' '.join(date_line[1:]) #ignore the first word 'date'

		base_stamps_list = self.log_file.readline().split()
		assert base_stamps_list[0] == 'base' and base_stamps_list[2] == 'timestamps'
		assert base_stamps_list[1] in ['hex', 'dec']
		assert base_stamps_list[3] in ['relative', 'absolute']

		self.number_base = 16 if base_stamps_list[1] == 'hex' else 10
		self.relative_timestamps = base_stamps_list[3] == 'relative'
		self.log_file.readline() # ignore Begin Triggerblock line

		self.timestamp = 0

	def __iter__(self):
		return self

	def __next__(self):
		line = self.log_file.readline()
		# TODO it may be incorrect to ignore log trigger events
		while line == '\n' or 'log trigger event' in line:
			line = self.log_file.readline()

		if not line or ('end' in line.lower() and 'triggerblock' in line.lower()):
			raise StopIteration

		msg = self.parse_message(line.split())
		if msg is None:
			return self.__next__()
		return msg

	def __del__(self):
		self.log_file.close()

	def get_log_metadata(self) -> LogMetadata:
		return LogMetadata(date_line = self.date_line, number_base = self.number_base, relative_timestamps = self.relative_timestamps)

class asciiOutput:

	def __init__(self, output_file_name : str, metadata : LogMetadata):
		assert metadata.number_base in [10, 16]
		self.output_file = open(output_file_name, 'w')
		self.output_file.write(f'date {metadata.date_line}\n')
		base_line = f'base {"dec" if metadata.number_base == 10 else "hex"} timestamps {"relative" if metadata.relative_timestamps else "absolute"}\n'
		self.output_file.write(base_line)
		self.output_file.write(f'Begin Triggerblock {metadata.date_line}\n')
		self.output_file.write('\n')

		self.prev_timestamp = None
		self.number_base = metadata.number_base
		self.relative_timestamps = metadata.relative_timestamps

	def append(self, msg : RawMessage):

		timestamp = msg.timestamp if not self.relative_timestamps else msg.timestamp - (0 if self.prev_timestamp is None else self.prev_timestamp)
		self.prev_timestamp = msg.timestamp

		id = hex(msg.id)[2:] if self.number_base == 16 else str(msg.id)
		if msg.is_extended:
			id += 'x'
		# TODO add indentation for hex
		tokens = [f'{timestamp:.6f}', msg.bus, str(id).ljust(10), 'Rx', 'D', str(len(msg.data)).rjust(3),
                  *list(map(lambda byte: hex(byte)[2:] if self.number_base == 16 else str(byte).rjust(3), msg.data))]
		self.output_file.write(' '.join(map(str, tokens)) + '\n')


	def __del__(self):
		self.output_file.write('End Triggerblock\n')
		self.output_file.close()
