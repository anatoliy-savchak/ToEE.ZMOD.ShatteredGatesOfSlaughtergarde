import toee, debug, utils_storage, utils_item

def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	print("san_use {} {}".format(attachee, triggerer))
	#debug.breakp("san_use")

	if (not triggerer): 
		print("py05001_bag_of_holding::san_use triggerer is none, exit")
		return toee.SKIP_DEFAULT

	bag = find_bag(triggerer)
	#bag = triggerer.obj_get_obj(toee.obj_f_container_notify_npc)
	if (not bag): 
		print("py05001_bag_of_holding::san_use bag is none, exit")
		return toee.SKIP_DEFAULT

	ctrl = CtrlBagOfHolding.ensure(bag)
	assert isinstance(ctrl, CtrlBagOfHolding)

	#tell somehow, that it was already swpawned
	already_spwawned = attachee.object_flags_get() & toee.OF_STONED
	print("already_spwawned: {}".format(already_spwawned))
	#debug.breakp("already_spwawned")
	if (not already_spwawned):
		utils_item.item_clear_all(attachee)
		ctrl.spawn(attachee)
		attachee.object_flag_set(toee.OF_STONED)

	return toee.RUN_DEFAULT

def san_transfer(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	print("sn_transfer {} {}".format(attachee, triggerer))
	#debug.breakp("sn_transfer")

	if (not triggerer): 
		print("py05001_bag_of_holding::san_transfer triggerer is none, exit")
		return toee.SKIP_DEFAULT

	bag = find_bag(triggerer)
	#if (not bag): 
	#	print("py05001_bag_of_holding::san_transfer bag is none, exit")
	#	return toee.SKIP_DEFAULT

	print("Bag_Of_Holding_timed_elicit go")
	Bag_Of_Holding_timed_elicit(bag, attachee, 1)
	return toee.RUN_DEFAULT

def Bag_Of_Holding_timed_elicit(bag, chest, time):
	assert isinstance(bag, toee.PyObjHandle)
	assert isinstance(chest, toee.PyObjHandle)
	toee.game.timevent_add(_Bag_Of_Holding_elicit_on_timeevent, (bag, chest), time, 1) # 1000 = 1 second
	return

def _Bag_Of_Holding_elicit_on_timeevent(bag, chest):
	assert isinstance(bag, toee.PyObjHandle)
	assert isinstance(chest, toee.PyObjHandle)
	#print("_Bag_Of_Holding_elicit_on_timeevent")
	if (not bag or bag.object_flags_get() & toee.OF_DESTROYED or not chest or chest.object_flags_get() & toee.OF_DESTROYED): 
		#print("_Bag_Of_Holding_elicit_on_timeevent::san_transfer bag is none, exit")
		return 1

	CtrlBagOfHolding.eject_incompatible(chest)
	max_weight = 0
	if (bag.proto == 12501):
		max_weight = 250
	elif (bag.proto == 12502):
		max_weight = 500
	elif (bag.proto == 12503):
		max_weight = 1000
	elif (bag.proto == 12504):
		max_weight = 1500
	CtrlBagOfHolding.eject_overweight(chest, max_weight)

	ctrl = CtrlBagOfHolding.ensure(bag)
	assert isinstance(ctrl, CtrlBagOfHolding)
	ctrl.elicit(chest)
	print("BAG OF HOLDING SAVED!")
	#print(ctrl.items)
	return 1


def find_bag(triggerer):
	for i in range(0, 199):
		item = triggerer.inventory_item(i)
		if (not item or item == toee.OBJ_HANDLE_NULL): continue
		if (item.proto == 12501):
			return item
	return None

class CtrlBagOfHolding(object):
	def __init__(self):
		self.items = dict()
		self.id = None
		return

	def created(self, npc):
		self.id = npc.id
		return

	@staticmethod
	def get_name():
		return "CtrlBagOfHolding"

	@classmethod
	def ensure(cls, npc):
		data = utils_storage.obj_storage(npc).data
		ctrl = None
		if (cls.get_name() in data):
			ctrl = data[cls.get_name()]
		else:
			ctrl = cls()
			ctrl.created(npc)
			utils_storage.obj_storage(npc).data[cls.get_name()] = ctrl
		return ctrl

	@classmethod
	def get_from_obj(cls, npc):
		data = utils_storage.obj_storage(npc).data
		if (cls.get_name() in data):
			return data[cls.get_name()]
		return None

	@classmethod
	def eject_incompatible(cls, chest):
		assert isinstance(chest, toee.PyObjHandle)
		#print("eject_incompatible on chest: {}".format(chest))
		leader = toee.game.leader 
		for i in range(0, 199):
			obj = chest.inventory_item(i)
			assert isinstance(obj, toee.PyObjHandle)
			if (not obj or obj == toee.OBJ_HANDLE_NULL): continue
			#print("checking incompatible {}".format(obj))
			if (cls.is_obj_incompatible(obj)):
				leader.item_get(obj)
				leader.float_text_line("Incompatible item: {}".format(obj.description), toee.tf_red)
		return

	@classmethod
	def eject_overweight(cls, chest, max_weight):
		assert isinstance(chest, toee.PyObjHandle)
		assert isinstance(max_weight, int)
		if (not max_weight): return
		#print("eject_incompatible on chest: {}".format(chest))
		leader = toee.game.leader 
		curr_weight = 0
		for i in range(0, 199):
			obj = chest.inventory_item(i)
			assert isinstance(obj, toee.PyObjHandle)
			if (not obj or obj == toee.OBJ_HANDLE_NULL): continue
			#print("checking incompatible {}".format(obj))
			weight = obj.obj_get_int(toee.obj_f_item_weight)
			if (curr_weight + weight > max_weight):
				leader.item_get(obj)
				descr = obj.description
				flags = obj.item_flags_get()
				if (flags & OIF_IS_MAGICAL and not flags & OIF_IDENTIFIED):
					descr = 'magic item'
				text = "Overweight! Item: {}, weight: {}.".format(descr, weight)
				leader.float_text_line(text, toee.tf_red)
				text = text + "\n"
				toee.game.create_history_freeform(text)
			else:
				curr_weight += weight
		return

	@classmethod
	def is_obj_incompatible(cls, obj):
		assert isinstance(obj, toee.PyObjHandle)
		if (obj.proto == 12501): return 1
		return 0

	def elicit(self, chest):
		assert isinstance(chest, toee.PyObjHandle)
		self.items = dict()
		for i in range(0, 199):
			obj = chest.inventory_item(i)
			if (not obj or obj == toee.OBJ_HANDLE_NULL): continue
			item = HoldingItem()
			item.assign(obj)
			self.items[item.id] = item
		return
	
	def spawn(self, chest):
		assert isinstance(chest, toee.PyObjHandle)
		items = self.items
		if (not items): return
		for id, item in items.iteritems():
			assert isinstance(item, HoldingItem)
			obj = item.spawn(chest.location)
			if (not obj): continue
			chest.item_get(obj)
		return

class HoldingItem(object):
	def _init_(self):
		self.id = ""
		self.proto = 0
		self.item_flags = 0
		self.ammo_quantity = 0
		self.worth = 0
		return

	def assign(self, obj):
		assert isinstance(obj, toee.PyObjHandle)
		self.id = obj.id
		self.proto = obj.proto
		print("assigned obj: {}, id: {}, proto: {}".format(obj, self.id, self.proto))
		otype = obj.type
		# IsEquipment
		if (otype >= toee.obj_t_weapon and otype <= toee.obj_t_generic or otype <= toee.obj_t_bag):
			self.item_flags = obj.obj_get_int(toee.obj_f_item_flags)
			self.worth = obj.obj_get_int(toee.obj_f_item_worth)
		if (otype == toee.obj_t_ammo):
			self.ammo_quantity = obj.obj_get_int(toee.obj_f_ammo_quantity)
		return

	def spawn(self, loc):
		obj = toee.game.obj_create(self.proto, loc)
		if (not obj): return None
		self.id = obj.id
		otype = obj.type
		# IsEquipment
		if (otype >= toee.obj_t_weapon and otype <= toee.obj_t_generic or otype <= toee.obj_t_bag):
			obj.obj_set_int(toee.obj_f_item_flags, self.item_flags)
			obj.obj_set_int(toee.obj_f_item_worth, self.worth)
		if (otype == toee.obj_t_ammo):
			obj.obj_set_int(toee.obj_f_ammo_quantity, self.ammo_quantity)
		return obj