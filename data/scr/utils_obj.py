from toee import *
from debugg import breakp
from const_toee import *
import utils_toee

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

def obj_timed_destroy(obj, time):
	assert isinstance(obj, PyObjHandle)
	game.timevent_add( _destroy_on_timeevent, ( obj ), time) # 1000 = 1 second
	return

def _destroy_on_timeevent(obj):
	obj.destroy()
	return 1

def obj_timed_off(obj, time):
	assert isinstance(obj, PyObjHandle)
	game.timevent_add( _off_on_timeevent, ( obj ), time) # 1000 = 1 second
	return

def _off_on_timeevent(obj):
	obj.object_flag_set(OF_OFF)
	return 1

def obj_float_line_dialog(obj, method, lineId, npc):
	assert isinstance(obj, PyObjHandle)
	scriptId = obj.scripts[sn_dialog]
	if (scriptId <=0): return 0
	if (method == 0): 
		attachee.float_line(lineId, npc)
		return 1
	#print("obj_float_line_dialog({}, {}, {})".format(obj, method, lineId))
	#breakp("obj_float_line_dialog")
	fileName = utils_toee.find_dialog_file_name(scriptId)
	#print(fileName)
	#breakp("obj_float_line_dialog 2")
	if (fileName is None): return 0
	#obj.float_mesfile_line(fileName, lineId, White)
	#if (1==1): return 1
	fileName = "data\\dlg\\" + fileName
	line = utils_toee.readMesLine(fileName, lineId)
	lineshort = ""
	if (method == 3):
		lines = line.split('.')
		lineshort = lines[0]
		if (len(lines) > 1): lineshort = lineshort + ".."
	else: lineshort = line

	#print("utils_toee.readMesLine = {}".format(line))
	#breakp("obj_float_line_dialog 3")
	if ((line is None) or (line == "")): return 0
	#breakp("obj_float_line_dialog 4")
	obj.float_text_line(lineshort, White)
	line = line + "\n\n"
	game.create_history_freeform(line)
	return 1

def obj_get_id(obj):
	assert isinstance(obj, PyObjHandle)
	if (hasattr(obj, 'id')):
		return obj.id
	s = obj.__getstate__()
	print("obj_get_id({}) = {}".format(obj, s))
	#breakp("obj_get_id")
	return s