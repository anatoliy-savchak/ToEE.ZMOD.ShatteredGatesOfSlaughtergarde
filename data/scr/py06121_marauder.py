from toee import *
from debugg import *
from utils_obj import obj_scripts_clear
from const_toee import *
from utils_obj import sec2loc

def san_heartbeat( attachee, triggerer ):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	#breakp("py06121_marauder san_heartbeat 1")
	if (game.combat_is_active()): return RUN_DEFAULT
	#breakp("py06121_marauder san_heartbeat 2")
	# only do this for the Leader, use OCF_UNRESSURECTABLE for it 
	if (not (attachee.critter_flags_get() & OCF_UNRESSURECTABLE)): return RUN_DEFAULT
	#breakp("py06121_marauder san_heartbeat 3")
	if (attachee.npc_flags_get() & ONF_KOS): return RUN_DEFAULT
	#breakp("py06121_marauder san_heartbeat 4")
	foundTuple = game.obj_list_range(attachee.location, 10, OLC_PC)
	if (len(foundTuple) > 0):
		#breakp("py06121_marauder san_heartbeat 5")
		attachee.scripts[sn_heartbeat] = 0
		attachee.npc_flag_set(ONF_KOS)
		attachee.unconceal()
		baddies = game.obj_list_range(attachee.location, 40, OLC_NPC)
		for b in baddies:
			if (b.proto == attachee.proto):
				b.npc_flag_set(ONF_KOS)
				b.unconceal()
		#foundTuple[0].float_text_line("You hear a soft sibilant hiss in the darkness,\n and then several dark-scaled lizardfolk rush you from\nthe shadows of this low, muddy chamber!", White)
		attachee.float_line(11, foundTuple[0])
		game.create_history_freeform("You hear a soft sibilant hiss in the darkness,\n and then several dark-scaled lizardfolk rush you from\nthe shadows of this low, muddy chamber!\n\n\n")
	#breakp("py06121_marauder san_heartbeat 6")
	return RUN_DEFAULT

def san_enter_combat( attachee, triggerer ):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)

	if (1): # leader logic once only
		leader = attachee.obj_get_obj(obj_f_critter_fleeing_from)
		if (leader): 
			print("leader: {}".format(leader))
			if (not (leader.critter_flags_get() & OCF_COMBAT_MODE_ACTIVE)):
				attachee.float_text_line("Boss, help!", Red)
				leader.object_script_execute(attachee, sn_heartbeat)
			print("unsetting leader")
			attachee.obj_set_obj(obj_f_critter_fleeing_from, OBJ_HANDLE_NULL)

	# only do this for the Leader, use OCF_UNRESSURECTABLE for it 
	if (not (attachee.critter_flags_get() & OCF_UNRESSURECTABLE)): return RUN_DEFAULT
	#breakp("py06121_marauder san_enter_combat 3")
	if (attachee.distance_to(sec2loc(511, 487)) < 30):
		attachee.float_line(12, game.party[0])
		game.create_history_freeform("One of the lizardfolk hefts a clay jar and hurls it at you. It shatters at your feet and a thick black snake angrily snaps at you from the shards of broken pottery.\n\n\n")
		#breakp("py06121_marauder san_enter_combat 4")
		PROTO_NPC_SMALL_VIPER = 14385
		monster = game.obj_create(PROTO_NPC_SMALL_VIPER, sec2loc(516, 480))
		assert isinstance(monster, PyObjHandle)
		obj_scripts_clear(monster)
		monster.faction_add(1)
		monster = game.obj_create(PROTO_NPC_SMALL_VIPER, sec2loc(517, 473))
		assert isinstance(monster, PyObjHandle)
		obj_scripts_clear(monster)
		monster.faction_add(1)
	if (attachee.distance_to(sec2loc(460, 460)) < 30):
		attachee.float_line(13, game.party[0])
		game.create_history_freeform("One of the lizardfolk picks up a clay jar and throws it at your feet. It shatters and an insectlike creature the size of a cat fl aps into the air on batlike wings. It seems dazed for a moment but then it points its deadly needle nose in your direction.\n\n\n")
		#breakp("py06121_marauder san_enter_combat 4")
		PROTO_NPC_STIRGE = 14834
		monster = game.obj_create(PROTO_NPC_STIRGE, sec2loc(454, 464))
		assert isinstance(monster, PyObjHandle)
		obj_scripts_clear(monster)
		monster.faction_add(1)
		monster = game.obj_create(PROTO_NPC_STIRGE, sec2loc(454, 468))
		assert isinstance(monster, PyObjHandle)
		obj_scripts_clear(monster)
		monster.faction_add(1)

	#breakp("py06121_marauder san_enter_combat 5")
	obj_scripts_clear(attachee)
	return RUN_DEFAULT