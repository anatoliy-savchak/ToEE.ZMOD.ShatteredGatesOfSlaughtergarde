import toee, templeplus.pymod, tpdp, debug

###################################################

def GetConditionName():
	return "Construct_Max_HP"

print("Registering " + GetConditionName())
###################################################

def OnGetMaxHP(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjBonusList)

	size = attachee.stat_base_get(toee.stat_size)
	hp_bonus = 0
	if (size <= toee.STAT_SIZE_SMALL): hp_bonus = 10
	elif (size == toee.STAT_SIZE_MEDIUM): hp_bonus = 20
	elif (size == toee.STAT_SIZE_LARGE): hp_bonus = 30
	elif (size == toee.STAT_SIZE_HUGE): hp_bonus = 40
	elif (size == toee.STAT_SIZE_GARGANTUAN): hp_bonus = 60
	elif (size == toee.STAT_SIZE_COLOSSAL): hp_bonus = 80

	if (hp_bonus):
		evt_obj.bonus_list.add(hp_bonus, 0, "Construct trait")
		#evt_obj.bonus_list.modify(hp_bonus, 0, 0)
		#print("Construct_Max_HP, size: {}, hp_bonus: {}, flags: {}, sum: {}".format(size, hp_bonus, evt_obj.flags, evt_obj.bonus_list.get_sum()))
		#debug.breakp("Construct trait")

	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 
modObj.AddHook(toee.ET_OnGetMaxHP, toee.EK_NONE, OnGetMaxHP, ())

