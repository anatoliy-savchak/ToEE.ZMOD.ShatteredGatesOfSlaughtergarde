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
		s = npc_stat_generate(evt_obj.d20a.target)
		toee.game.alert_show(s, "Close")
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

def npc_stat_generate(npc):
	assert isinstance(npc, toee.PyObjHandle)

	print("stat_inspect.StatInspect")
	inspect = stat_inspect.StatInspect(npc)
	print(inspect)
	values = inspect.build()
	print("stat_generator.StatGenerator")
	result = stat_generator.StatGenerator(values).generate()
	print(result)
	return result

