import toee, templeplus.pymod, tpdp, debug, sys, traceback

###################################################

def GetConditionName():
	return "Bag_Of_Holding"

print("Registering " + GetConditionName())
###################################################

Bag_Of_Holding_Support = "Bag_Of_Holding_Support"

def Bag_Of_Holding_OnBuildRadialMenuEntry(attachee, args, evt_obj):
	radial_action = tpdp.RadialMenuEntryPythonAction("Bag of Holding", toee.D20A_PYTHON_ACTION, 3006, 0, "TAG_INTERFACE_HELP")
	#assert isinstance(radial_action, tpdp.RadialMenuEntryParent)
	radial_action.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Items)
	return 0

def Bag_Of_Holding_OnD20PythonActionPerform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	#debug.breakp("Lodged_Quills_OnD20PythonActionPerform start")
	try:
		#debug.breakp("Bag_Of_Holding_OnD20PythonActionPerform")
		for pc in toee.game.party:
			pc.condition_add(Bag_Of_Holding_Support)

		prev_bag = FindBag()
		if (prev_bag): prev_bag.destroy()
		bag = toee.game.obj_create(1300, attachee.location)
		do_invisible = "anim_goal_use_object" in dir(attachee)
		#do_invisible = 0
		if (do_invisible):
			bag.object_flag_set(toee.OF_DONTDRAW)
			bag.move(attachee.location)
			attachee.anim_goal_use_object(bag)
			#attachee.container_open_ui(bag)
	except Exception, e:
		print "Bag_Of_Holding_OnD20PythonActionPerform:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
	return 1

def FindBag():
	for obj in toee.game.obj_list_vicinity(toee.game.leader.location, toee.OLC_CONTAINER):
		if (obj.proto == 1300 and not obj.object_flags_get() & toee.OF_DESTROYED):
			return obj
	return None

def Bag_Of_Holding_S_Inventory_Update(attachee, args, evt_obj):
	#print("Bag_Of_Holding_S_Inventory_Update {}".format(attachee))
	#debug.breakp("Bag_Of_Holding_S_Inventory_Update")
	bag = FindBag()
	if (not bag): return 0
	#print("toee.game.char_ui_display_type: {}".format(toee.game.char_ui_display_type))
	bag.object_script_execute(attachee, 0x20) #sn_transfer
	
	# check if Bag_Of_Holding_timed_destroy started running
	if (not bag.object_flags_get() & toee.OF_INVISIBLE):
		bag.object_flag_set(toee.OF_INVISIBLE)
		bag.object_flag_set(toee.OF_DONTDRAW)
		Bag_Of_Holding_timed_destroy(bag, 1000)
	return 0

def Bag_Of_Holding_timed_destroy(bag, time):
	assert isinstance(bag, toee.PyObjHandle)
	toee.game.timevent_add(_Bag_Of_Holding_destroy_on_timeevent, (bag), time) # 1000 = 1 second
	return

def _Bag_Of_Holding_destroy_on_timeevent(bag):
	assert isinstance(bag, toee.PyObjHandle)
	#print("_Bag_Of_Holding_destroy_on_timeevent toee.game.char_ui_display_type: {}".format(toee.game.char_ui_display_type))
	if (not bag.object_flags_get() & toee.OF_DESTROYED):
		is_invetory_screen_opened = 0
		if ("anim_goal_use_object" in dir(toee.game)):
			is_invetory_screen_opened = toee.game.char_ui_display_type

		is_invetory_screen_opened = 0
		if (not is_invetory_screen_opened):
			print("Bag_Of_Holding_S_Inventory_Update destroying bag {}".format(bag))
			bag.destroy()
		else:
			Bag_Of_Holding_timed_destroy(bag, 1000)
	return 1

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - type
modObj.AddHook(toee.ET_OnBuildRadialMenuEntry, toee.EK_NONE, Bag_Of_Holding_OnBuildRadialMenuEntry, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3006, Bag_Of_Holding_OnD20PythonActionPerform, ())
#modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_Inventory_Update, Bag_Of_Holding_S_Inventory_Update, ())

modObj2 = templeplus.pymod.PythonModifier(Bag_Of_Holding_Support, 2) # 
modObj2.AddHook(toee.ET_OnD20Signal, toee.EK_S_Inventory_Update, Bag_Of_Holding_S_Inventory_Update, ())