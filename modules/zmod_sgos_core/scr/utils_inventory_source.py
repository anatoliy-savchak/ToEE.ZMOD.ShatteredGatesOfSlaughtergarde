import os, json
import toee, utils_item

# import utils_inventory_source
# utils_inventory_source.inventory_source_parse_one(123).print_items()

def inventory_source_parse_one(id, file_path = None):
	assert isinstance(id, int)

	print(os.getcwd())
	mes_dic = None
	if (file_path is None):
		file_path = "overrides\\rules\\InvenSource.mes"
		if (not os.path.isfile(file_path)):
			print("File {} not found!".format(file_path))
			file_path = "data\\rules\\InvenSource.mes"
	print("Opening mes file {} ...".format(file_path))
	mes_dic = readMes(file_path)
	if (not mes_dic):
		print("mes file {} failed to open!".format(file_path))
		return None

	if (not id in mes_dic): return None
	mes_line = mes_dic[id][0]
	result = InventorySourceItem.create(mes_line)
	if (result): result.id = id
	return result

def inventory_source_parse(file_path = None):
	mes_dic = None
	print(os.getcwd())
	if (file_path is None):
		file_path = "overrides\\rules\\InvenSource.mes"
		if (not os.path.isfile(file_path)):
			print("File {} not found!".format(file_path))
			file_path = "data\\rules\\InvenSource.mes"
	print("Opening mes file {} ...".format(file_path))
	mes_dic = readMes(file_path)
	if (not mes_dic):
		print("mes file {} failed to open!".format(file_path))
		return None

	result = dict()
	for id in mes_dic.iterkeys():
		mes_line = mes_dic[id][0]
		if not (mes_line): continue
		item = InventorySourceItem.create(mes_line)
		if (item):
			item.id = id
			result[id] = item
	return result

def inventory_source_respawn(obj, num = None, file_path = None):
	assert isinstance(obj, toee.PyObjHandle)

	inventory_obj = obj.substitute_inventory
	if (not inventory_obj):
		inventory_obj = obj

	if (not num):
		if (inventory_obj.type == toee.obj_t_npc):
			num = inventory_obj.obj_get_int(toee.obj_f_critter_inventory_source)
		elif (inventory_obj.type == toee.obj_t_container):
			num = inventory_obj.obj_get_int(toee.obj_f_container_inventory_source)
		else:
			print("inventory_source_respwan:: Wrong type for inventory_obj: {}".format(inventory_obj))
			return
		
	entry = inventory_source_parse_one(num, file_path)
	if (not entry):
		print("inventory_source_respwan:: entry {} not found!".format(num))
		return

	utils_item.item_clear_all(inventory_obj)
	entry.spawn_in_inventory(inventory_obj)
	return

class InventorySourceItem:
	def __init__(self):
		self.id = 0
		self.name = "" # zorro's entries:
		self.money_copper = (0,0) # min max
		self.money_silver = (0,0)
		self.money_gold = (0,0)
		self.money_platinum = (0,0)
		self.money_gems = (0,0)
		self.one_of_entries = list() # (123,456) (789,0)
		self.items = list() # (proto, percentage), buy_list_num,X percentage,proto percentage,proto
		self.buy_list_num = 0
		return

	@staticmethod
	def create(mes_line):
		assert isinstance(mes_line, str)
		result = InventorySourceItem()
		if (not result.parse(mes_line)): return None
		return result

	def parse(self, mes_line):
		assert isinstance(mes_line, str)
		print(mes_line)
		pos = mes_line.find(':')
		if (pos == -1):
			print("Cannot determine descriptive name!")
			return 0
		self.name = mes_line[:pos]
		tokens = mes_line[pos+1:].split(" ")
		for token in tokens:
			assert isinstance(token, str)
			if (not token): continue
			if (token.startswith("buy_list_num")):
				self.buy_list_num = try_int(token[len("buy_list_num,"):], 0)

			elif (token.startswith("(")): # one_of_entries
				sublist = list()
				for subtoken in token[1:-1].split(","):
					proto = try_int(subtoken)
					if (proto):
						sublist.append(proto)
				if (sublist):
					self.one_of_entries.append(sublist)

			elif (token.startswith("copper")):
				self.money_copper = InventorySourceItem.parse_min_max(token)

			elif (token.startswith("silver")):
				self.money_silver = InventorySourceItem.parse_min_max(token)

			elif (token.startswith("gold")):
				self.money_gold = InventorySourceItem.parse_min_max(token)

			elif (token.startswith("platinum")):
				self.money_platinum = InventorySourceItem.parse_min_max(token)

			elif (token.startswith("gems")):
				self.money_gems = InventorySourceItem.parse_min_max(token)

			else: # item entry: percentage,proto
				subtokens = token.split(",")
				if (len(subtokens) < 2): 
					print("Token parse failed item entry split comma: {}".format(token))
					continue
				percentage = try_int(subtokens[0])
				if (not percentage): 
					print("Token parse failed item entry percentage: {}".format(token))
					continue
				proto = try_int(subtokens[1])
				if (not percentage): 
					print("Token parse failed item entry percentage: {}".format(token))
					continue
				subitems = (proto, percentage)
				self.items.append(subitems)
		return 1

	@staticmethod
	def parse_min_max(token):
		assert isinstance(token, str)
		pos = token.find(",")
		minmax = token[pos+1:].split("-")
		min = try_int(minmax[0], 0)
		max = min
		if (len(minmax) > 1):
			max = try_int(minmax[1], min)
		return min, max

	@staticmethod
	def save_obj(obj, file_name):
		f = open(file_name, "w")
		dm = json.dumps(obj, indent = 2)
		f.write(dm)
		f.close()
		return

	def spawn_in_inventory(self, inventory_obj):
		assert isinstance(inventory_obj, toee.PyObjHandle)

		if (self.money_copper[1] or self.money_silver[1] or self.money_gold[1] or self.money_platinum[1]):
			platinum = toee.game.random_range(self.money_platinum[0], self.money_platinum[1])
			gold = toee.game.random_range(self.money_gold[0], self.money_gold[1])
			silver = toee.game.random_range(self.money_silver[0], self.money_silver[1])
			copper = toee.game.random_range(self.money_copper[0], self.money_copper[1])
			utils_item.item_money_create_in_inventory(inventory_obj, platinum, gold, silver, copper)

		if (self.one_of_entries):
			for entry in self.one_of_entries:
				if (not entry): continue
				random_index = toee.game.random_range(0, len(entry)-1)
				proto = entry[random_index]
				if (not proto): continue
				utils_item.item_create_in_inventory(proto, inventory_obj)

		if (self.items):
			for protoPercent in self.items:
				proto = protoPercent[0]
				percent = protoPercent[1]
				if (not percent or percent < 1): continue
				roll = toee.game.random_range(1, 100)
				if (roll > percent): continue
				utils_item.item_create_in_inventory(proto, inventory_obj)
		return

	def print_items(self):
		print("InventorySourceItem id: {}, platinum ({}, {}), gold ({}, {}), silver ({}, {}), copper ({}, {})".format(self.id, self.money_platinum[0], self.money_platinum[1], self.money_gold[0], self.money_gold[1], self.money_silver[0], self.money_silver[1], self.money_copper[0], self.money_copper[1]))

		if (self.one_of_entries):
			print("one_of_entries: {}".format(len(self.one_of_entries)))
			for entry in self.one_of_entries:
				if (not entry): continue
				print("entry:")
				for proto in entry:
					if (not proto): continue
					item = toee.game.obj_create(proto, toee.game.leader.location)
					print("{}: {}".format(proto, item))
					item.destroy()

		if (self.items):
			for protoPercent in self.items:
				proto = protoPercent[0]
				percent = protoPercent[1]
				if (not percent or percent < 1): continue
				item = toee.game.obj_create(proto, toee.game.leader.location)
				print("{}%: {}: {}".format(percent, proto, item))
				item.destroy()
		return

def try_int(s, default = None):
	assert isinstance(s, str)
	if (not default is None): assert isinstance(default, int)
	try: 
		return int(s)
	except ValueError:
		return default
	return default

def readMes(mesfile):
	""" Read the mesfile into a dictionary indexed by line number. """
	mesFile = file(mesfile,'r')
	mesDict = {}
	for line in mesFile.readlines():
		# Remove whitespace.
		line = line.strip()
		# Ignore empty lines.
		if not line:
			continue
		# Ignore comment lines.
		if line[0] != '{':
			continue
		# Decode the line.  Just standard python string processing.
		line = line.split('}')[:-1]
		for i in range(len(line)):
			line[i] = line[i].strip()
			line[i] = line[i][1:]
		contents = line[1:]
		# Insert the line into the mesDict.
		mesDict[int(line[0])] = contents
	mesFile.close()
	# print 'File read'
	return mesDict
