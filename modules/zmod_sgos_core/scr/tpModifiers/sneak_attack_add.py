import toee, templeplus.pymod

###################################################

def GetConditionName():
	return "Sneak_Attack_Add"

print("Registering " + GetConditionName())
###################################################

def SneakAttackAdd_SneakAttackDice(attachee, args, evt_obj):
	#breakp("SneakAttackAdd_SneakAttackDice 1: {}".format(attachee))

	evt_obj.return_val += args.get_arg(0)
	#breakp("SneakAttackAdd_SneakAttackDice 2: {}, evt_obj.return_val: {}".format(attachee, evt_obj.return_val))
	minLevel = 0
	if (args.get_arg(1) > minLevel): minLevel = args.get_arg(1)
	if (evt_obj.return_val < minLevel):
		evt_obj.return_val = minLevel
		#breakp("SneakAttackAdd_SneakAttackDice 3: {}, evt_obj.return_val: {}".format(attachee, evt_obj.return_val))
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - add Sneak Dice, 1 - min Sneak Dice
modObj.AddHook(toee.ET_OnD20PythonQuery, "Sneak Attack Dice", SneakAttackAdd_SneakAttackDice, ())
#breakp("Registered " + GetConditionName())
