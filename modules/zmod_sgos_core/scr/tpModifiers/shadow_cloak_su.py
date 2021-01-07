import toee, templeplus.pymod, tpdp, debug, sys

###################################################

def GetConditionName():
	return "Shadow_Cloaked_Su"

print("Registering " + GetConditionName())
###################################################

def Shadow_Cloaked_Su_OnGetDefenderConcealmentMissChance(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)
	
	if (not evt_obj.attack_packet.attacker.d20_query(toee.EK_Q_Critter_Has_True_Seeing - toee.EK_Q_Helpless)):
		miss_chance = args.get_arg(0)
		if (not miss_chance):
			miss_chance = 20
		evt_obj.bonus_list.add(miss_chance, 19, "Shadow Cloak (Su)")

	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0: miss chance %
modObj.AddHook(toee.ET_OnGetDefenderConcealmentMissChance, toee.EK_NONE, Shadow_Cloaked_Su_OnGetDefenderConcealmentMissChance, ())