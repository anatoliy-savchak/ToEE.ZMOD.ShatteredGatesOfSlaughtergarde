from toee import *
from debugg import breakp
from const_toee import *

def npc_feats_print(npc):
	assert isinstance(npc, PyObjHandle)
	feats = npc.feats
	for f in feats:
		print("Feat Code: {}".format(f))
		print("Feat Name{}".format(game.get_feat_name(f)))
	return

def npc_generate_hp(npc):
	assert isinstance(npc, PyObjHandle)
	npc.obj_set_int(obj_f_hp_pts, -65535)
	hp = npc.stat_level_get(stat_hp_current)
	#print("Current HP: {}".format(hp))
	return hp

def npc_money_set(npc, copper):
	assert isinstance(npc, PyObjHandle)
	assert isinstance(copper, int)
	diff = npc.money_get()
	diff = copper - diff
	npc.money_adj(diff)
	return diff
