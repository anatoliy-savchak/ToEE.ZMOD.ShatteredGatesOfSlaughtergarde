import toee, templeplus.pymod

###################################################

def GetConditionName():
	return "Ability_Check_Modifier_Attacker"

print("Registering " + GetConditionName())
###################################################

def Ability_Check_Modifier_OnGetAbilityCheckModifier(attachee, args, evt_obj):
	flags = evt_obj.flags
	if (flags & 1): # attacker bonus
		bonus = args.get_arg(0)
		stat = args.get_arg(1)
		evt_obj.bonus_list.add(bonus, stat, 112) #{112}{~Item~[TAG_MAGIC_ITEMS] or ~Tool~[TAG_TOOLS]}
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - bonus, 1 - ability
modObj.AddHook(toee.ET_OnGetAbilityCheckModifier, toee.EK_NONE, Ability_Check_Modifier_OnGetAbilityCheckModifier, ())
#breakp("Registered " + GetConditionName())

