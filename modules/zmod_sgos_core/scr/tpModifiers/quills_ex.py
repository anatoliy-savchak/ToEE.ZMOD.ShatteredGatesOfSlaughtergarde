import toee, templeplus.pymod, tpdp, debug, sys

###################################################

def GetConditionName():
	return "Quills_Ex"

print("Registering " + GetConditionName())
###################################################

def Quills_Ex_OnDealingDamage(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjDamage)
	
	#print("evt_obj.attack_packet.event_key: {}".format(evt_obj.attack_packet.event_key))
	#print("evt_obj.attack_packet.action_type: {}".format(evt_obj.attack_packet.action_type))
	#debug.breakp("Lodged_Quills_OnDealingDamage")

	if (evt_obj.attack_packet.event_key - 1000 >= args.get_arg(0)):
		evt_obj.attack_packet.target.condition_add_with_args("Lodged_Quills", 1, 0)
	return 0

def Quills_Ex_OnGetBonusAttacks(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	
	if (evt_obj.bonus_list):
		quill_attacks = toee.dice_new("1d4").roll()
		# assume critter has at least two
		add_quill_attacks = quill_attacks - 1
		if (add_quill_attacks > 0):
			evt_obj.bonus_list.add(add_quill_attacks, 34, "Quills")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - min attack number of effect; 1 - dice side, default 4;
modObj.AddHook(toee.ET_OnDealingDamage, toee.EK_NONE, Quills_Ex_OnDealingDamage, ())
modObj.AddHook(toee.ET_OnGetBonusAttacks, toee.EK_NONE, Quills_Ex_OnGetBonusAttacks, ())

