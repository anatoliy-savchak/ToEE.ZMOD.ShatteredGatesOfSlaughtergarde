from toee import *
from debugg import breakp
from toee_const import *

def sec2loc( x, y ):
	# initialize loc to be a LONG integer
	loc = 0L + y
	loc = ( loc << 32 ) + x
	return loc

def obj_scripts_clear(obj):
	assert isinstance(obj, PyObjHandle)
	mob_scripts = obj.scripts
	mob_scripts[sn_examine] = 0
	mob_scripts[sn_use] = 0
	mob_scripts[sn_destroy] = 0
	mob_scripts[sn_unlock] = 0
	mob_scripts[sn_get] = 0
	mob_scripts[sn_drop] = 0
	mob_scripts[sn_throw] = 0
	mob_scripts[sn_hit] = 0
	mob_scripts[sn_miss] = 0
	mob_scripts[sn_dialog] = 0
	mob_scripts[sn_first_heartbeat] = 0
	mob_scripts[sn_catching_thief_pc] = 0
	mob_scripts[sn_dying] = 0
	mob_scripts[sn_enter_combat] = 0
	mob_scripts[sn_exit_combat] = 0
	mob_scripts[sn_start_combat] = 0
	mob_scripts[sn_end_combat] = 0
	mob_scripts[sn_buy_object] = 0
	mob_scripts[sn_resurrect] = 0
	mob_scripts[sn_heartbeat] = 0
	mob_scripts[sn_leader_killing] = 0
	mob_scripts[sn_insert_item] = 0
	mob_scripts[sn_will_kos] = 0
	mob_scripts[sn_taking_damage] = 0
	mob_scripts[sn_wield_on] = 0
	mob_scripts[sn_wield_off] = 0
	mob_scripts[sn_critter_hits] = 0
	mob_scripts[sn_new_sector] = 0
	mob_scripts[sn_remove_item] = 0
	mob_scripts[sn_leader_sleeping] = 0
	mob_scripts[sn_bust] = 0
	mob_scripts[sn_dialog_override] = 0
	mob_scripts[sn_transfer] = 0
	mob_scripts[sn_caught_thief] = 0
	mob_scripts[sn_critical_hit] = 0
	mob_scripts[sn_critical_miss] = 0
	mob_scripts[sn_join] = 0
	mob_scripts[sn_disband] = 0
	mob_scripts[sn_new_map] = 0
	mob_scripts[sn_trap] = 0
	mob_scripts[sn_true_seeing] = 0
	mob_scripts[sn_spell_cast] = 0
	mob_scripts[sn_unlock_attempt] = 0
	return

