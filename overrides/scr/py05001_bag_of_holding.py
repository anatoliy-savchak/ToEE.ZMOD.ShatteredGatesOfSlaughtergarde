import toee, debug, utils_storage

def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	print("san_use {} {}".format(attachee, triggerer))
	#debug.breakp("san_use")

	if (not triggerer): 
		print("py05001_bag_of_holding::san_use triggerer is none, exit")
		return toee.SKIP_DEFAULT
	bag = find_bag(triggerer)
	if (not bag): 
		print("py05001_bag_of_holding::san_use bag is none, exit")
		return toee.SKIP_DEFAULT

	ctrl = CtrlBagOfHolding.ensure(bag)
	assert isinstance(ctrl, CtrlBagOfHolding)
	ctrl.spawn(attachee)

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
	if (not bag): 
		print("py05001_bag_of_holding::san_transfer bag is none, exit")
		return toee.SKIP_DEFAULT

	ctrl = CtrlBagOfHolding.ensure(bag)
	assert isinstance(ctrl, CtrlBagOfHolding)
	#ctrl.elicit(attachee)
	#print(ctrl.items)
	Bag_Of_Holding_timed_elicit(bag, attachee, 1)
	return toee.RUN_DEFAULT

def Bag_Of_Holding_timed_elicit(bag, chest, time):
	assert isinstance(bag, toee.PyObjHandle)
	assert isinstance(chest, toee.PyObjHandle)
	toee.game.timevent_add(_Bag_Of_Holding_elicit_on_timeevent, (bag, chest), time) # 1000 = 1 second
	return

def _Bag_Of_Holding_elicit_on_timeevent(bag, chest):
	assert isinstance(bag, toee.PyObjHandle)
	assert isinstance(chest, toee.PyObjHandle)
	if (not bag or bag.object_flags_get() & toee.OF_DESTROYED or not chest or chest.object_flags_get() & toee.OF_DESTROYED): return 1

	ctrl = CtrlBagOfHolding.ensure(bag)
	assert isinstance(ctrl, CtrlBagOfHolding)
	ctrl.elicit(chest)
	print(ctrl.items)
	return 1


def find_bag(triggerer):
	for i in range(0, 199):
		item = triggerer.inventory_item(i)
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

	def elicit(self, chest):
		assert isinstance(chest, toee.PyObjHandle)
		self.items = dict()
		for i in range(0, 199):
			obj = chest.inventory_item(i)
			if (not obj): continue
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
		return

	def assign(self, obj):
		assert isinstance(obj, toee.PyObjHandle)
		self.id = obj.id
		self.proto = obj.proto
		print("assigned obj: {}, id: {}, proto: {}".format(obj, self.id, self.proto))

		if (obj.type == toee.obj_t_generic):
			self.item_flags = obj.obj_get_int(toee.obj_f_item_flags)

		return

	def spawn(self, loc):
		obj = toee.game.obj_create(self.proto, loc)
		if (not obj): return None
		if (obj.type == toee.obj_t_generic):
			obj.obj_set_int(toee.obj_f_item_flags, self.item_flags)
		return obj