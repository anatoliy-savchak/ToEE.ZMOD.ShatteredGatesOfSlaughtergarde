from templeplus.pymod import PythonModifier
from toee import *
from debugg import *

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

modObj = PythonModifier(GetConditionName(), 2) # 0 - bonus, 1 - ability
modObj.AddHook(ET_OnGetAbilityCheckModifier, EK_NONE, Ability_Check_Modifier_OnGetAbilityCheckModifier, ())
#breakp("Registered " + GetConditionName())

