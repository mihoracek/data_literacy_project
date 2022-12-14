#!/usr/bin/env python3

"""
Classes which represent canDB messages, fields, enums etc. Parsed from json file.
They parse values from packets if raw data given.
"""
import copy
import json
import math
from collections import OrderedDict
from collections import namedtuple
from enum import Enum
from typing import List, Dict, Union, NamedTuple, Type, Any

WARN_ON_INVALID_VALUES = True
IGNORE_RECEIVED_FLOATS = True

def validate_not_empty(src, fallback):
	if src is None:
		return fallback
	elif isinstance(src, str) and not src:
		return fallback
	else:
		return src


def toFloat(s: Any, fallback: float) -> float:
	s = validate_not_empty(s, fallback)
	if isinstance(s, int) or isinstance(s, float):
		return float(s)

	if "0x" in s:
		return float(int(s, 16))  # can handle strings line 0xAA and such
	else:
		return float(s)

def compute_value(numList: bytearray) -> int:
	data = 0
	for index, byte in enumerate(numList):
		data += (byte << (8 * index))

	return data

def extractBits(value: int, offset: int, size: int) -> int:

	# merge all bytes into one number
	# probably fine for CAN, in future, CAN FD should do it more efficiently
	data = value

	data = (data >> offset)  # align to bottom
	data = data & ((1 << size) - 1)  # mask out non related bits

	return data


def toSignedNumber(number: int, bitLength: int) -> int:
	mask = (1 << bitLength) - 1
	if number & ~(mask >> 1):
		return number | ~mask
	else:
		return number & mask


def toUnsignedNumber(number: int, bitLength: int) -> int:
	if not isinstance(number, int):
		raise Exception("number must be integer, was {}".format(type(number)))

	if number >= 0:
		return number

	if -number > (1 << bitLength) / 2:
		raise Exception("number {} does not fit into {} bits".format(number, bitLength))

	mask = (1 << bitLength) - 1
	return mask ^ (-number - 1)


def extractUnsignedInt(message_value: int, offset: int, size: int) -> int:
	return extractBits(message_value, offset, size)


def extractSignedInt(message_value: int, offset: int, size: int) -> int:
	return toSignedNumber(extractBits(message_value, offset, size), size)


def insertBits(dataU8List: bytearray, integer: int, offset: int, size: int):
	if not isinstance(integer, int):
		raise Exception("integer must be instance of int, was {}".format(type(integer)))

	if integer < 0:
		integer = toUnsignedNumber(integer, size)

	if integer > (1 << size) - 1:
		raise Exception("bitsize {} too small for number {}".format(size, integer))

	if offset + size > len(dataU8List) * 8:
		raise Exception("buffer too small, required {}, available {}".format(offset + size, len(dataU8List) * 8))

	byteOffset = int(offset / 8)
	subByteOffset = offset % 8

	# split number to list of 8bit chunks (necessary for conversion to bytes)
	splitBits = []
	integer <<= subByteOffset
	while integer > 0:
		splitBits.append(integer & 0xFF)
		integer >>= 8

	for b in splitBits:
		dataU8List[byteOffset] |= b
		byteOffset += 1


class Custom_enum_element:
	def __init__(self, name: str, value: int = None, description: str = None):
		self.value: int = value
		self.name: str = name
		self.description: str = description


class Custom_enum:
	def __init__(self, name, owner = None, description = None):
		self.name: str = name
		self.owner: str = owner
		self.description: str = description
		self.enum: OrderedDict[int, Custom_enum_element] = OrderedDict()
		self.type: str = "candb_enum_{}_t".format(self.name)

	def append(self, element: Custom_enum_element, implicitIsFine: bool = False) -> None:
		if not isinstance(element, Custom_enum_element):
			raise Exception("Enum element is not instance of Custom_enum_element, but: {}".format(type(element)))
		if validate_not_empty(element.name, None) is None:
			print("\tempty enum key, ignoring")
			return
		if element.value in self.enum:
			raise Exception("Enum already has value {} ,called {}".format(element.value, element.name))

		if element.value is None:
			# print("WARNING: implicit value in enum!")
			if not implicitIsFine:
				print("WARNING: implicit value in enum!")
			if len(self.enum) == 0:  # if empty
				element.value = 0  # start with zero
			else:
				element.value = max(self.enum) + 1  # othwerwise take previous value and add 1
		self.enum[element.value] = element

	def min(self) -> Custom_enum_element:
		return self.enum[min(self.enum.keys())]

	def max(self) -> Custom_enum_element:
		return self.enum[max(self.enum.keys())]

class Candb_msg_field_type(Enum):
	BOOL = 0
	UINT = 1
	INT = 2
	FLOAT = 3
	ENUM = 4
	MUX = 5

	def __str__(self) -> str:
		return '{0}'.format(self.name)

	@staticmethod
	def from_str(s) -> 'Candb_msg_field_type':
		if "uint" in s:
			return Candb_msg_field_type.UINT
		elif "int" in s:
			return Candb_msg_field_type.INT
		elif "bool" in s:
			return Candb_msg_field_type.BOOL
		elif "multiplex" in s:
			return Candb_msg_field_type.MUX
		elif "enum" in s:
			return Candb_msg_field_type.ENUM
		elif "float" in s:
			return Candb_msg_field_type.FLOAT
		else:
			raise Exception("Unknown field type: " + s)


class Candb_msg_field:
	def __init__(self, name : str, description : str, field_type: Candb_msg_field_type, count, bits, pos_offset, unit,
				 available_enums, vmin=0, vmax=0,
				 voffset=0, vfactor=1):
		if not isinstance(description, str) or not isinstance(name, str):
			raise Exception(f"Description {type(description)} and name {type(name)} must be instances of class str.")

		self.name = name
		self.description = description
		self.field_type = Candb_msg_field_type.from_str(field_type)
		self.field_type_raw = field_type
		self.nestLevel = 0  # used for indent calculation in __Str__

		self.bits = bits
		self.pos_offset = pos_offset
		self.count = count
		self.unit = unit
		self.vmin = toFloat(vmin, -math.inf)
		self.vmax = toFloat(vmax, math.inf)
		self.voffset = toFloat(voffset, 0)
		self.vfactor = toFloat(vfactor, 1)
		if self.vfactor == 0:
			print("error, field '{} | {}' has factor 0, resetting to 1".format(self.name, self.description))
			self.vfactor = 1
		defvalue = self.vmin

		if self.field_type == Candb_msg_field_type.MUX:
			if self.count != 1:
				raise Exception("Mux and array at the same time is not suported")
			else:
				self.muxedFields = [[] for _ in range(int(self.vmax - self.vmin) + 1)]
		else:
			self.muxedFields = None  # used in muxed type field

			if self.field_type == Candb_msg_field_type.UINT:
				if self.vmin < 0:
					defvalue = 0  # because uints cant go below 0...

			elif self.field_type == Candb_msg_field_type.INT:
				# signed values probably have idle value on 0 and not on min
				if 0 > self.vmin and 0 < self.vmax:
					defvalue = 0

			elif self.field_type == Candb_msg_field_type.ENUM:
				# link corresponding enum to this field
				enum_name = self.field_type_raw.split(" ")[1]  # eg "enum ECUF_CAL_STWIndex" > ECUF_CAL_STWIndex
				self.linked_enum = None
				for e in available_enums:
					if f'{e.owner}_{e.name}' == enum_name:
						self.linked_enum = e
				if self.linked_enum is None:
					raise Exception("matching enum not found ({})".format(enum_name))
				# set correct min/max
				self.vmin = self.linked_enum.min().value
				self.vmax = self.linked_enum.max().value
				defvalue = self.linked_enum.min().value

			elif self.field_type == Candb_msg_field_type.BOOL:
				self.vmin = False
				self.vmax = True
				defvalue = self.vmin

		self.value = list([defvalue] * self.count)

	def __str__(self) -> str:
		indent = "    " * (self.nestLevel + 1)
		v = ""
		for idx in range(self.count):
			if self.field_type in [Candb_msg_field_type.INT, Candb_msg_field_type.UINT, Candb_msg_field_type.BOOL]:
				v += "{:7.{prec}f} ".format(self.value[idx], prec=int(math.log10(max([int(1 / self.vfactor), 1]))))
			elif self.field_type is Candb_msg_field_type.FLOAT:
				v += "{:7.3f} ".format(float(self.value[idx]))
			elif self.field_type is Candb_msg_field_type.ENUM:
				v += "{} (={:2d})".format(self.linked_enum.enum[self.value[idx]].name,
										  self.linked_enum.enum[self.value[idx]].value)
			elif self.field_type is Candb_msg_field_type.MUX:
				v += "{:7d} ".format(int(self.value[idx]))
			else:
				v = "N/A "

		# eg: UINT   (56:52)    [ 4]  = 0  SEQ | Message up counter for safety
		v = indent + "{:5} ({:2}:{:2} = {:2}) [{:1}] = {} {} | {}".format(self.field_type.name, self.pos_offset + self.bits,
																	 self.pos_offset, self.bits, self.count, v,
																	 self.name, self.description)

		# FIXME indentation works only for 1 level
		if self.field_type is Candb_msg_field_type.MUX:
			v += "\n"
			for m in range(int(self.vmax - self.vmin) + 1):
				v += indent + "{}[{}]\n".format(self.name, m)
				for sub in self.muxedFields[m]:
					v += "{}\n".format(sub)
			else:
				pass
		return v

	def addMuxedSubfield(self, field: 'Candb_msg_field') -> None:
		if self.field_type != Candb_msg_field_type.MUX:
			raise Exception("this field is not MUX type, but {}".format(type(field)))
		for sub in self.muxedFields:
			if len(sub) > 0 and sub[-1].isMux():
				# nested muxes, forward vield to submux
				sub[-1].addMuxedSubfield(field)
			else:
				sub.append(copy.deepcopy(field))
				sub[-1].nestLevel = self.nestLevel + 1

	def isMux(self) -> bool:
		return self.field_type == Candb_msg_field_type.MUX

	def isArray(self) -> bool:
		return self.count > 1

	def parseFromPacket(self, message_value: int, dataList: bytearray):

		if IGNORE_RECEIVED_FLOATS and self.field_type == Candb_msg_field_type.FLOAT:
			# Silently return early if floating point is to be parsed and it is not yet supported
			self.value = [math.nan * self.count]
			return

		for arr in range(self.count):
			if self.field_type in [Candb_msg_field_type.UINT, Candb_msg_field_type.BOOL, Candb_msg_field_type.MUX]:
				raw = extractUnsignedInt(message_value, self.pos_offset + arr * self.bits, self.bits)
			elif self.field_type == Candb_msg_field_type.INT:
				raw = extractSignedInt(message_value, self.pos_offset + arr * self.bits, self.bits)
			elif self.field_type == Candb_msg_field_type.ENUM:
				key = extractUnsignedInt(message_value, self.pos_offset + arr * self.bits, self.bits)
				if key not in self.linked_enum.enum:
					print(key)
					print(self.linked_enum.name)
				raw = self.linked_enum.enum[key].value  # translate number to enum element (value, name)
			# No special handling of floats, they are handled by early return
			else:
				raise Exception("paring of type '{}' not yet supported".format(self.field_type))

			if self.field_type in [Candb_msg_field_type.UINT, Candb_msg_field_type.INT]:
				raw *= self.vfactor
				raw += self.voffset

			self.value[arr] = raw

			if WARN_ON_INVALID_VALUES:
				if raw > self.vmax:
					print("WARNING: {} value above allowed range ({} > {})".format(self.name, raw, self.vmax))
				elif raw < self.vmin:
					print("WARNING: {} value below allowed range ({} < {})".format(self.name, raw, self.vmin))

		if self.isMux():
			# forward data parsing to muxed subfields
			index = int(self.value[0] - self.vmin)
			if 0 <= index < len(self.muxedFields):
				for f in self.muxedFields[index]:
					f.parseFromPacket(dataList)
			elif WARN_ON_INVALID_VALUES:
				print("WARNING: ignored MUX parsing, index out of range!")

	def assemble(self, values: List, buff: bytearray) -> List:
		"""
		Assemble message from list of values to bytearray

		:param values: values from which message should be assembled
		:param buff: output buffer
		:return: values
		"""
		if self.field_type == Candb_msg_field_type.MUX:
			print("MUXfield", self.name, self.text, self.field_type, self.field_type_raw)
			value = int(values.pop(0))
			muxBranch = int(value - self.vmin)
			if 0 <= muxBranch < len(self.muxedFields):
				for f in self.muxedFields[muxBranch]:
					values = f.assemble(values, buff)
			else:
				print("WARNING: ignored MUX parsing, index out of range!")

		elif self.field_type in [Candb_msg_field_type.UINT, Candb_msg_field_type.BOOL, Candb_msg_field_type.MUX,
								 Candb_msg_field_type.INT, Candb_msg_field_type.ENUM]:
			for _ in range(self.count):
				# try:
				value = int(values.pop(0))
				insertBits(buff, int((value - self.voffset) / self.vfactor), self.pos_offset, self.bits)
			# except Exception as e:
			# 	print("failed bit insertion, index {}".format(i), e)
		else:
			raise Exception("this field type assembly not implemented, type {}".format(self.field_type))

		return values


class Candb_msg:
	def __init__(self, name :str, description: str, owner: str, sent_by: List[str], identifier: int, frame_type : str, length: int,
				 busname: str, timeout: float, period: float, ):
		if not isinstance(description, str) or not isinstance(name, str):
			raise Exception(f"Description ({type(description)}) and name ({type(name)}) must be instances of class str.")
		self.name: str = name
		self.description: str = description
		self.sent_by: List[str] = sent_by
		try:
			self.identifier: int = int(identifier)
		except Exception:
			raise Exception(
				"In message: {}, from: {}, ID not number: {}".format(self.name, sent_by, identifier))
		assert frame_type in ['CAN_STD', 'CAN_EXT']
		self.has_ext_id = frame_type == 'CAN_EXT'
		self.length: int = int(length)
		self.timeout: float = timeout if (timeout is not None) else 0
		self.period: float = period if (period is not None) else 0
		self.fields: List[Candb_msg_field] = []
		self.timestamp: float = 0
		self.lastTSdiff: float = 0
		self.owner: str = owner
		self.busname: str = busname
		self.namedtuple: Union[None, Type] = None
		self.message_value = None

	def __getitem__(self, key) -> Candb_msg_field:
		return self.as_namedtuple().__getattribute__(key)

	# Alternatively:
	# assert isinstance(key, str)
	# for f in filter(lambda f:f.name == key, self.fields):
	#   return f
	# raise Exception(f'Message "{self.name}" does not contain field "{key}"!')

	def as_namedtuple(self) -> NamedTuple:
		return self.namedtuple(*self.fields)

	def generate_named_tuple(self):
		field_names: List[str] = [f.name for f in self.fields]
		self.namedtuple = namedtuple(self.name, field_names)

	def add_field(self, field: Candb_msg_field):
		if not isinstance(field, Candb_msg_field):
			raise Exception("field be instance of class candb_msg_field")

		if len(self.fields) > 0 and self.fields[-1].isMux():
			# previous field is MUX, so this field us "subfield" of it
			self.fields[-1].addMuxedSubfield(field)
		else:
			self.fields.append(field)

	def parseFromPacket(self, dataList: Union[bytearray, List[bytes]], timestamp: float):
		self.lastTSdiff = timestamp - self.timestamp
		self.timestamp = timestamp
		self.message_value = compute_value(dataList)
		for f in self.fields:
			f.parseFromPacket(self.message_value, dataList)

	def assemble(self, values: List, buff: bytearray) -> None:
		# print("assembling message {}".format(self.name))
		if not isinstance(values, list):
			raise Exception("values must be list type, was {}".format(type(values)))

		if len(self.fields) != len(values):
			raise Exception(
				"length of values ({}) is different than count of fields ({})".format(len(self.fields), len(values)))

		i = 0
		while len(values) > 0:
			values = self.fields[i].assemble(values, buff)
			i += 1
		if i != len(self.fields):
			raise Exception("something went wrong, value list not empty!")

	# print("assembly done! data:", end="")
	# for b in buff:
	# 	print("{:2X} ".format(b), end="")
	# print("")

	def getTimestamp(self) -> float:
		return self.timestamp

	def getTSdiff(self) -> float:
		return self.lastTSdiff

	def __str__(self) -> str:
		buff = ""
		if len(self.fields) == 0:
			buff = "\tNo FILEDS :("
		else:
			for f in self.fields:
				buff += "{}\n".format(f)

		if len(self.sent_by) > 1:
			sender = self.sent_by
		else:
			sender = self.sent_by
		return "{:4} {} {}\n{}".format(self.identifier, sender, self.name, buff)


class Candb_unit:
	def __init__(self, name : str, description: str, package : str):
		if not isinstance(description, str) or not isinstance(name, str):
			raise Exception(f"Description ({type(description)}) and name ({type(name)}) must be instances of class str.")
		self.name: str = name
		self.description: str = description
		self.package = package
		#TODO add list of owned messages and enumerations

def escape_whitespace(str):
	if str is None: # Handle empty descriptions
		return ''
	return str.replace('\r', '\\r').replace('\n', '\\n').replace('\t', '\\t')

class CanDB:
	def __init__(self, jsonList: List[str], debug_parsing=False):
		# follows parsing of json
		self.parsed_messages: Dict[int, Candb_msg] = {}
		self.parsed_enums: List[Custom_enum] = []
		self.parsed_units : Disc[str, Candb_unit] = {}

		for jFileName in jsonList:  # iterate over all json files
			with open(jFileName, 'r') as jfile:
				data = jfile.read()

			# parse file
			j = json.loads(data)
			if j.get("version") != 2:
				raise Exception("Wrong json version, expected {:d}, got {:d}".format(2, j.get("version")))
			for pkg in j.get("packages"):
				# for now, we don't distinguish between packages
				for unit in pkg.get("units"):  # iterate over units (owners of messages)
					msg_owner = unit.get("name")

					self.parsed_units[pkg.get('name') + msg_owner] = Candb_unit(unit.get("name"), escape_whitespace(unit.get("description")), pkg.get('name'))

					for j_enum in unit.get("enum_types"):  # parse enums
						enum = Custom_enum(j_enum.get("name"), msg_owner, escape_whitespace(j_enum.get("description")))
						for item in j_enum.get("items"):
							enum.append(Custom_enum_element("{}".format(item.get("name")), item.get("value"),
															escape_whitespace(item.get("description"))))
						self.parsed_enums.append(enum)

					for msg in unit.get("messages"):
						# print(msg)
						# try:
						bus = msg.get("bus")
						if bus is None:
							bus = "UNDEFINED"

						sent_by_full = msg.get("sent_by")
						sent_by = [src.split(".")[-1] for src in sent_by_full]  # ignore parent package

						m = Candb_msg(name=msg.get("name"),
									  description=escape_whitespace(msg.get("description")),
									  owner=msg_owner,
									  sent_by=sent_by,  # ignore parent package
									  identifier=msg.get("id"),
									  frame_type=msg.get("frame_type"),
									  length=msg.get("length"),
									  timeout=msg.get("timeout"),
									  period=msg.get("tx_period"),
									  busname=bus.split(".")[-1])  # full bus name includes package name, ignore it
						if debug_parsing:
							print("message: ", m)
						# except Exception as e:
						# 	print("\tInvalid message, ",e)
						# 	#traceback.print_exc()
						# 	continue

						for field in msg.get("fields"):
							name = field.get("name")
							# print("\tfield ",name)
							if field.get("type") == "reserved":
								pass

							elif name is not None and len(name) > 0:
								# print("ftype",field.get("type"))
								f = Candb_msg_field(
									name=field.get("name"),
									description=escape_whitespace(field.get('description')),
									field_type=field.get("type"),
									count=field.get("count"),
									bits=field.get("bits"),
									pos_offset=field.get("start_bit"),
									unit=field.get("unit"),
									vmin=field.get("min"),
									vmax=field.get("max"),
									voffset=field.get("offset"),
									vfactor=field.get("factor_num"),
									available_enums=self.parsed_enums)
								# print("adding field: ",f)
								m.add_field(f)
							else:
								if debug_parsing:
									print("\tnoname field, ignored!")
						if debug_parsing:
							print("message: ", m)

						m.generate_named_tuple()
						self.parsed_messages[m.identifier] = m

	def isMsgKnown(self, msgId: int) -> bool:
		assert isinstance(msgId, int)
		return msgId in self.parsed_messages

	def getEnumByName(self, owner : str, name : str) -> Custom_enum:
		try:
			return next(e for e in self.parsed_enums if e.name == name and e.owner == owner)
		except:
			raise Exception(f"Enum {owner}::{name} is not recognized!")

	def getMsgByName(self, owner : str, name : str) -> Candb_msg:
		assert isinstance(owner, str) and isinstance(name, str)
		try:
			return next(msg for id, msg in self.parsed_messages.items() if msg.owner == owner and msg.name == name)
		except:
			raise Exception(f"Message {owner}::{name} is not recognized!")

	def getMsgById(self, msgId: int) -> Candb_msg:
		assert isinstance(msgId, int)
		return self.parsed_messages[msgId]

	def parseData(self, msgId: int, dataList: bytearray, timestamp: Union[int, float]) -> Candb_msg:
		assert isinstance(msgId, int)
		if not self.isMsgKnown(msgId):
			return None # ignore unknown message

		if not isinstance(timestamp, int) and not isinstance(timestamp, float):
			raise Exception("timestamp must be number, but it was {}".format(type(timestamp)))

		msg = self.getMsgById(msgId)
		msg.parseFromPacket(list(dataList), timestamp)
		return msg
