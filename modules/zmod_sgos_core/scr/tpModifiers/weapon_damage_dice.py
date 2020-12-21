import toee, templeplus.pymod, tpdp, debug, sys

###################################################

def GetConditionName():
	return "Weapon_Damage_Dice"

print("Registering " + GetConditionName())
###################################################

def Weapon_Damage_Dice_OnGetAttackDice(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjGetAttackDice)
	
	dice_packed = args.get_arg(0)
	if (not dice_packed): return 0

	weapon_proto_filter = args.get_arg(1)
	if (not weapon_proto_filter or (not evt_obj.weapon and weapon_proto_filter == 1000) or (evt_obj.weapon and evt_obj.weapon.proto == weapon_proto_filter)):
		evt_obj.dice_packed = dice_packed
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 8, 0) # 0 - dice_packed, 0 - weapon_proto_filter
modObj.AddHook(toee.ET_OnGetAttackDice, toee.EK_NONE, Weapon_Damage_Dice_OnGetAttackDice, ())

