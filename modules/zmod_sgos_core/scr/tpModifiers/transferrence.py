import toee, templeplus.pymod, tpdp, debug

###################################################

def GetConditionName():
	return "Transferrence"

print("Registering " + GetConditionName())
###################################################

# game.leader.condition_add("Transferrence")

IC_Alchemy = 0,
IC_BrewPotion = 1
IC_ScribeScroll = 2
IC_CraftWand = 3
IC_CraftRod = 4
IC_CraftWondrous = 5
IC_CraftStaff = 6
IC_ForgeRing = 7
IC_CraftMagicArmsAndArmor = 8
IC_Inactive = 9

def Transferrence_OnD20PythonQuery(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)

	xp_cost = evt_obj.data1
	item_creation_type = evt_obj.data2
	#print("Transferrence_OnD20PythonQuery :: xp_cost = {}, item_creation_type: {}".format(xp_cost, item_creation_type))

	xp_cost_new = xp_cost
	if (item_creation_type <> IC_ScribeScroll):
		xp_cost_new = xp_cost / len(toee.game.party)

	#print("Transferrence_OnD20PythonQuery :: xp_cost_new = {}, item_creation_type: {}".format(xp_cost_new, item_creation_type))
	evt_obj.return_val = xp_cost_new
	#debug.breakp("Transferrence_OnD20PythonQuery")
	return 0

def Transferrence_OnD20PythonSignal(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)
	xp_drain = evt_obj.data1
	for pc in toee.game.party:
		if (pc == attachee): continue
		pc_xp = pc.obj_get_int(toee.obj_f_critter_experience)
		pc.obj_set_int(toee.obj_f_critter_experience, pc_xp - xp_drain)
	return 0


modObj = templeplus.pymod.PythonModifier(GetConditionName(), 4) # reserved
modObj.AddHook(toee.ET_OnD20PythonQuery, "Craft Item XP Cost Calc", Transferrence_OnD20PythonQuery, ())
modObj.AddHook(toee.ET_OnD20PythonSignal, "Craft Item XP Debited", Transferrence_OnD20PythonSignal, ())
