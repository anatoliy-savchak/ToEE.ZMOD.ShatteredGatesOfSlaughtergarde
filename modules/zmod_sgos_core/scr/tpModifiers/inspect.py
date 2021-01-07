import toee, templeplus.pymod, tpdp, debug, sys, traceback
import stat_generator, stat_inspect

###################################################

def GetConditionName():
	return "Inspect"

print("Registering " + GetConditionName())
###################################################

def Inspect_OnBuildRadialMenuEntry(attachee, args, evt_obj):
	radial_action = tpdp.RadialMenuEntryPythonAction("Inspect", toee.D20A_PYTHON_ACTION, 3005, 0, "TAG_INTERFACE_HELP")
	#assert isinstance(radial_action, tpdp.RadialMenuEntryParent)
	spell_data = tpdp.D20SpellData(3210)
	spell_data.set_spell_level(1)
	radial_action.set_spell_data(spell_data)
	radial_action.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Skills)
	return 0

def Inspect_OnD20PythonActionCheck(attachee, args, evt_obj):
	#debug.breakp("Inspect_OnD20PythonActionCheck")
	return 1

def Inspect_OnD20PythonActionPerform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	#debug.breakp("Lodged_Quills_OnD20PythonActionPerform start")
	try:
		#debug.breakp("Inspect_OnD20PythonActionPerform")

		bon_list = tpdp.BonusList()
		skill_value = tpdp.dispatch_skill(attachee, toee.skill_knowledge_nature, bon_list, toee.OBJ_HANDLE_NULL, 1)
		dice = toee.dice_new("1d20")
		roll_result = dice.roll()

		inspect = stat_inspect.StatInspect(evt_obj.d20a.target)
		values = inspect.build()
		cr = 1
		if ("cr" in values):
			cr = values["cr"]

		dc = cr + 10
		success = skill_value + roll_result >= dc
		hist_id = tpdp.create_history_dc_roll(attachee, dc, dice, roll_result, "Inspect check", bon_list)
		toee.game.create_history_from_id(hist_id)

		if (success):
			s = stat_generator.StatGenerator(values).generate()
			#s = npc_stat_generate(evt_obj.d20a.target)
			toee.game.alert_show(s, "Close")
		else: 
			attachee.float_text_line("Failure!", toee.tf_red)
	except Exception, e:
		print "Inspect_OnD20PythonActionPerform:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		#print "Inspect_OnD20PythonActionPerform error:", sys.exc_info()[0]
		#print(str(e))
		#debug.breakp("Lodged_Quills_OnD20PythonActionPerform error")
	return 1

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2, 1)
modObj.AddHook(toee.ET_OnBuildRadialMenuEntry, toee.EK_NONE, Inspect_OnBuildRadialMenuEntry, ())
#modObj.AddHook(toee.ET_OnD20PythonActionCheck, 3005, Inspect_OnD20PythonActionCheck, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3005, Inspect_OnD20PythonActionPerform, ())
