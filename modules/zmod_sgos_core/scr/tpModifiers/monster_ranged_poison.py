import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Monster_Ranged_Poison"

print("Registering " + GetConditionName())
###################################################

def Monster_Ranged_Poison_OnDealingDamage2(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjDamage)

	if (args.get_arg(3) == 0):
		args.condition_remove()

	target = evt_obj.attack_packet.target
	if (not target): return 0

	args.set_arg(3, args.get_arg(3) - 1)
	poison_id = args.get_arg(0)
	if (not poison_id): return 0
	target.condition_add_with_args("Poisoned", poison_id, args.get_arg(1), args.get_arg(2))
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 5) # 0 poisonid, 1 duration, 2 dc, 3 arrows left
modObj.AddHook(toee.ET_OnDealingDamage2, toee.EK_NONE, Monster_Ranged_Poison_OnDealingDamage2, ())

