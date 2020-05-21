import toee, debugg, const_proto_items

def item_create_in_inventory(item_proto_num, npc, quantity = 1):
	assert isinstance(item_proto_num, int)
	assert isinstance(npc, toee.PyObjHandle)
	item = toee.game.obj_create(item_proto_num, npc.location)
	if (item != toee.OBJ_HANDLE_NULL):
		npc.item_get(item)
	if (quantity > 1):
		for i in range(2, quantity):
			item = toee.game.obj_create(item_proto_num, npc.location)
			if (item != toee.OBJ_HANDLE_NULL):
				npc.item_get(item)
	return item

def item_create_in_inventory_buy(item_proto_num, npc):
	assert isinstance(item_proto_num, int)
	assert isinstance(npc, toee.PyObjHandle)
	item = toee.game.obj_create(item_proto_num, npc.location)
	if (item != toee.OBJ_HANDLE_NULL):
		worth = item.obj_get_int(toee.obj_f_item_worth)
		left = npc.money_get()
		print("{}: {} gp | {}".format(item.description, worth // 100, left // 100))
		if (left >= worth):
			npc.money_adj(-worth)
			npc.item_get(item)
		else: 
			print("Lack of money!")
			item.destroy()
			item = None
	return item

def item_place_into_inventory(item, npc):
	assert isinstance(npc, toee.PyObjHandle)
	assert isinstance(item, toee.PyObjHandle)
	if (item != OBJ_HANDLE_NULL):
		npc.item_get(item)
	return item

def item_create_in_inventory_mass(npc, protos):
	assert isinstance(npc, toee.PyObjHandle)
	for item_proto_num in protos:
		item_create_in_inventory(item_proto_num, npc)
	return

def item_clear_all(npc):
	assert isinstance(npc, toee.PyObjHandle)
	#breakp("inventory clear_all")
	item_unwield_all(npc)
	otype = npc.type
	invenField = 0
	invenNumField = 0
	if ((otype == toee.obj_t_npc) or (otype == toee.obj_t_pc)):
		invenField = toee.obj_f_critter_inventory_list_idx
		invenNumField = toee.obj_f_critter_inventory_num
	elif ((otype == toee.obj_t_container) or (otype == toee.obj_t_bag)):
		invenField = toee.obj_f_container_inventory_list_idx
		invenNumField = toee.obj_f_container_inventory_num
	else:
		invenField = toee.obj_f_critter_inventory_list_idx
		invenNumField = toee.obj_f_critter_inventory_num

	#print("invenField: {}, invenNumField: {}".format(invenField, invenNumField))
	numItems = npc.obj_get_int(invenNumField)
	#print("Inventory count {} for obj {}".format(numItems, npc))
	if (numItems > 0):
		for i in range(0, 199):
			#itemProto = npc.obj_get_idx_obj(invenField, i)
			#item = npc.item_find(4077)
			item = npc.inventory_item(i)
			#print("Item at {}: {}".format(i, item))
			if (item != toee.OBJ_HANDLE_NULL):
				numItems = numItems - 1
				item.destroy()
			if (numItems <=0): break

	return numItems

def item_clear_by_proto(npc, proto_id):
	assert isinstance(npc, toee.PyObjHandle)
	assert isinstance(proto_id, int)
	#breakp("inventory clear_all")
	item_unwield_by_proto(npc, proto_id)
	otype = npc.type
	invenField = 0
	invenNumField = 0
	if ((otype == toee.obj_t_npc) or (otype == toee.obj_t_pc)):
		invenField = toee.obj_f_critter_inventory_list_idx
		invenNumField = toee.obj_f_critter_inventory_num
	elif ((otype == toee.obj_t_container) or (otype == toee.obj_t_bag)):
		invenField = toee.obj_f_container_inventory_list_idx
		invenNumField = toee.obj_f_container_inventory_num
	else:
		invenField = toee.obj_f_critter_inventory_list_idx
		invenNumField = toee.obj_f_critter_inventory_num

	#print("invenField: {}, invenNumField: {}".format(invenField, invenNumField))
	numItems = npc.obj_get_int(invenNumField)
	#print("Inventory count {} for obj {}".format(numItems, npc))
	if (numItems > 0):
		for i in range(0, 199):
			#itemProto = npc.obj_get_idx_obj(invenField, i)
			#item = npc.item_find(4077)
			item = npc.inventory_item(i)
			#print("Item at {}: {}".format(i, item))
			if (item != toee.OBJ_HANDLE_NULL):
				numItems = numItems - 1
				if (item.proto == proto_id): 
					item.destroy()
			if (numItems <=0): break

	return numItems

def item_unwield_all(npc):
	assert isinstance(npc, toee.PyObjHandle)
	for i in range(toee.item_wear_helmet, toee.item_wear_lockpicks):
		npc.item_worn_unwield(i, 0)
	return

def item_unwield_by_proto(npc, proto_id):
	assert isinstance(npc, toee.PyObjHandle)
	for i in range(toee.item_wear_helmet, toee.item_wear_lockpicks):
		item = npc.item_worn_at(i)
		if (item and item.proto == proto_id):
			npc.item_worn_unwield(i, 0)
	return

def item_do_use_getset(attachee, new_used = None):
	assert isinstance(attachee, toee.PyObjHandle)
	result = attachee.object_flags_get() & toee.OF_UNUSED_40000 != 0
	if (new_used is None): return result
	if (new_used):
		attachee.object_flag_set(toee.OF_UNUSED_40000)
	else:
		attachee.object_flag_unset(toee.OF_UNUSED_40000)
	return result

def item_get_marker(attachee):
	assert isinstance(attachee, toee.PyObjHandle)
	return attachee.obj_get_int(toee.obj_f_hp_pts)

def item_get_dialog_hint_id(attachee):
	assert isinstance(attachee, toee.PyObjHandle)
	return attachee.obj_get_int(toee.obj_f_hp_damage)

def item_money_create_in_inventory(obj, platinum, gold = None, silver = None, copper = None):
	assert isinstance(obj, toee.PyObjHandle)
	if (platinum):
		item = item_create_in_inventory(const_proto_items.PROTO_MONEY_PLATINUM, obj)
		item.obj_set_int(toee.obj_f_money_quantity, platinum)
	if (gold):
		item = item_create_in_inventory(const_proto_items.PROTO_MONEY_GOLD, obj)
		item.obj_set_int(toee.obj_f_money_quantity, gold)
	if (silver):
		item = item_create_in_inventory(const_proto_items.PROTO_MONEY_SILVER, obj)
		item.obj_set_int(toee.obj_f_money_quantity, silver)
	if (copper):
		item = item_create_in_inventory(const_proto_items.PROTO_MONEY_COPPER, obj)
		item.obj_set_int(toee.obj_f_money_quantity, copper)
	return
