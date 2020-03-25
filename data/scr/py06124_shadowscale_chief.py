from toee import *
from debugg import *
import utils_storage
import utils_obj

class ShadowscaleChief(object):
	def __init__(self):
		self.name = ShadowscaleChief.get_name()
		self.round = 0
		self.aware_of_combat = 0
		return

	@staticmethod
	def get_name():
		return "ShadowscaleChief"


def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	#breakp("san_first_heartbeat")
	utils_storage.obj_storage(attachee).data[ShadowscaleChief.get_name()] = ShadowscaleChief()
	return RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	#breakp("san_heartbeat chief")
	if (attachee.critter_flags_get() & OCF_COMBAT_MODE_ACTIVE): 
		attachee.scripts[sn_heartbeat] = 0
		return RUN_DEFAULT

	chief_store = utils_storage.obj_storage(attachee).data[ShadowscaleChief.get_name()]
	assert isinstance(chief_store, ShadowscaleChief)

	door = do_chief_manage_door(0)
	if (not chief_store.aware_of_combat):
		print("CHECK NEW_AWARE_OF_COMBAT")
		new_aware_of_combat = 0
		for obj in game.obj_list_range(attachee.location, 50, OLC_NPC):
			if (obj.critter_flags_get() & OCF_COMBAT_MODE_ACTIVE and obj.leader_get() == attachee):
				new_aware_of_combat = 1
				break
		if (new_aware_of_combat):
			chief_store.aware_of_combat = 1
			door = do_chief_manage_door(2)

	if (not door):
		attachee.move(utils_obj.sec2loc(452, 474))
	return RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	chief = utils_storage.obj_storage(attachee).data[ShadowscaleChief.get_name()]
	chief.round = 0
	do_chief_manage_door(2)
	return RUN_DEFAULT

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	#breakp("san_start_combat chief")
	chief = utils_storage.obj_storage(attachee).data[ShadowscaleChief.get_name()]
	chief.round += 1
	return RUN_DEFAULT


def do_chief_manage_door(shall_destroy):
	door = None
	for obj in game.obj_list_range(utils_obj.sec2loc(448, 474), 10, OLC_PORTAL):
		assert isinstance(obj, PyObjHandle)
		if (not (obj.object_flags_get() & OF_DESTROYED)):
			door = obj
		break

	print(door)
	#breakp("do_chief_manage_door 1")
	if (door and shall_destroy == 1):
		door.destroy()
		door = None
	elif (door and shall_destroy > 1 and not (door.portal_flags_get() & OPF_OPEN)):
		#breakp("do_chief_manage_door do destroy")
		door.portal_toggle_open()
		#door.portal_flag_set(OPF_BUSTED)
		game.timevent_add(_door_destroy_postcall, ( door ), 2000, 0) # 1000 = 1 second

	return door

def _door_destroy_postcall(obj):
	#breakp("do_chief_manage_door on destroy")
	obj.destroy()
	return 1

def find_closest_pc(loc):
	#attachee.obj_get_obj(obj_f_npc_combat_focus)
	closest_one = None
	closest_one_dist = 10000
	for pc in game.party:
		if (pc == closest_one): continue
		dist = attachee.distance_to(pc)
		if (dist < closest_one_dist):
			closest_one = pc
			closest_one_dist = dist
	return closest_one