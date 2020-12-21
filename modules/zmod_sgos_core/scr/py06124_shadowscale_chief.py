import toee
import debugg
import utils_storage
import utils_obj
import const_toee
import utils_tactics
import utils_npc
import utils_target_list

class ShadowscaleChief(object):
	def __init__(self):
		self.name = ShadowscaleChief.get_name()
		self.round = 0
		self.countdown_status = 0 #0 - not started, 1 - started, 2 - finished
		self.already_went_to_center = 0
		return

	@staticmethod
	def get_name():
		return "ShadowscaleChief"


def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	attachee.critter_flag_set(OCF_SLEEPING)
	#breakp("san_first_heartbeat")
	utils_storage.obj_storage(attachee).data[ShadowscaleChief.get_name()] = ShadowscaleChief()
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	print("san_heartbeat")
	print("san_heartbeat({}, {})".format(attachee, triggerer))
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)

	dude = utils_storage.obj_storage(attachee).data[ShadowscaleChief.get_name()]
	print("dude.countdown_status: {}".format(dude.countdown_status))
	if (dude.countdown_status == 0):
		#debugg.breakp("san_heartbeat chief")
		if (triggerer != attachee): # got triggerer from a minion
			print("from minion: {}".format(triggerer))
			if (1 or triggerer.critter_flags_get() & toee.OCF_COMBAT_MODE_ACTIVE):
				dude.countdown_status = 1
				print("chief_on_timeevent go")
				toee.game.timevent_add(chief_on_timeevent, ( attachee ), 100, 0) # lets wait two rounds
	elif (dude.countdown_status == 1):
		# wait period
		attachee.float_text_line("What is going on in here!", const_toee.Red)
	else:
		# we dont need it anymore
		attachee.scripts[const_toee.sn_heartbeat] = 0

	return toee.RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	dude = utils_storage.obj_storage(attachee).data[ShadowscaleChief.get_name()]
	dude.round = 0
	#debugg.breakp("san_enter_combat chief")
	if (dude.countdown_status < 2):
		attachee.ai_stop_attacking()
		return toee.SKIP_DEFAULT
	return toee.RUN_DEFAULT

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	#debugg.breakp("san_start_combat chief")
	dude = utils_storage.obj_storage(attachee).data[ShadowscaleChief.get_name()]
	dude.round += 1
	tac = utils_tactics.TacticsHelper(ShadowscaleChief.get_name())
	while(1==1):
		if (dude.countdown_status < 2):
			tac.add_stop()
			break

		measures = utils_target_list.AITargetMeasure()
		measures.measure_has_los = 1
		measures.mult_has_los = 100
		measures.measure_distance = 1
		measures.mult_distance = 1
		measures.measure_can_path = 1
		measures.mult_can_path = 100
		tl = utils_target_list.AITargetList(attachee, 1, 0, measures).rescan()
		aitarget = tl.topt() #AITarget
		if (aitarget):
			if (not aitarget.measures.value_can_path):
				if (not dude.already_went_to_center):
					dude.already_went_to_center = 1
					tac.add_goto(462, 477)
				else: 
					tac.add_total_defence()
					break

		tac.add_target_closest()
		tac.add_attack()
		break
	
	if (tac.count > 0):
		tac.set_strategy(attachee)

	#debugg.breakp("san_start_combat chief end")
	return toee.RUN_DEFAULT

def chief_on_timeevent(obj):
	assert isinstance(obj, toee.PyObjHandle)
	print("chief_on_timeevent here")
	#debugg.breakp("chief_on_timeevent")
	if (not utils_npc.npc_is_alive(obj)): return
	dude = utils_storage.obj_storage(obj).data[ShadowscaleChief.get_name()]
	dude.countdown_status = 2
	obj.npc_flag_set(ONF_KOS)
	obj.npc_flag_unset(ONF_NO_ATTACK)
	obj.faction_add(1)
	print("chief_on_timeevent move")
	obj.move(utils_obj.sec2loc(452, 475))
	#obj.move(utils_obj.sec2loc(453, 471))
	#obj.move(utils_obj.sec2loc(460, 478))
	return