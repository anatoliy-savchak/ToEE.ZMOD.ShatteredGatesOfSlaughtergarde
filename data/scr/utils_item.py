from toee import *
from debugg import *

def item_create_in_inventory(item_proto_num, npc):
	assert isinstance(item_proto_num, int)
	assert isinstance(npc, PyObjHandle)
	item = game.obj_create(item_proto_num, npc.location)
	if (item != OBJ_HANDLE_NULL):
		npc.item_get(item)
	return item

def item_clear_all(npc):
	assert isinstance(npc, PyObjHandle)
	#breakp("inventory clear_all")
	item_unwield_all(npc)
	otype = npc.type
	invenField = 0
	invenNumField = 0
	if ((otype == obj_t_npc) or (otype == obj_t_pc)):
		invenField = obj_f_critter_inventory_list_idx
		invenNumField = obj_f_critter_inventory_num
	elif ((otype == obj_t_container) or (otype == obj_t_bag)):
		invenField = obj_f_container_inventory_list_idx
		invenNumField = obj_f_container_inventory_num
	else:
		invenField = obj_f_critter_inventory_list_idx
		invenNumField = obj_f_critter_inventory_num

	#print("invenField: {}, invenNumField: {}".format(invenField, invenNumField))
	numItems = npc.obj_get_int(invenNumField)
	#print("Inventory count {} for obj {}".format(numItems, npc))
	if (numItems > 0):
		for i in range(0, 199):
			#itemProto = npc.obj_get_idx_obj(invenField, i)
			#item = npc.item_find(4077)
			item = npc.inventory_item(i)
			#print("Item at {}: {}".format(i, item))
			if (item != OBJ_HANDLE_NULL):
				numItems = numItems - 1
				item.destroy()
			if (numItems <=0): break

	return numItems

def item_unwield_all(npc):
	assert isinstance(npc, PyObjHandle)
	for i in range(item_wear_helmet, item_wear_lockpicks):
		npc.item_worn_unwield(i, 0)
	return

def item_do_use_getset(attachee, new_used = None):
	assert isinstance(attachee, PyObjHandle)
	result = attachee.object_flags_get() & OF_UNUSED_40000 != 0
	if (new_used is None): return result
	if (new_used):
		attachee.object_flag_set(OF_UNUSED_40000)
	else:
		attachee.object_flag_unset(OF_UNUSED_40000)
	return result

def item_get_marker(attachee):
	assert isinstance(attachee, PyObjHandle)
	return attachee.obj_get_int(obj_f_hp_pts)

def item_get_dialog_hint_id(attachee):
	assert isinstance(attachee, PyObjHandle)
	return attachee.obj_get_int(obj_f_hp_damage)