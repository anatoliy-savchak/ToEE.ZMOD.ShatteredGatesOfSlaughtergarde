import toee, templeplus.pymod

###################################################

def GetConditionName():
	return "Spell_Quicken"

print("Registering " + GetConditionName())
###################################################

def Spell_Quicken_OnMetaMagicMod(attachee, args, evt_obj):
	#breakp("Spell_Quicken_All_OnMetaMagicMod 1: {}".format(attachee))

	metaMagicData = evt_obj.meta_magic
	if metaMagicData.get_quicken() >= 1: return 0

	numLeft = args.get_arg(1)
	if (numLeft == 0): return 0
	numLeft -= 1
	args.set_arg(1, numLeft)

	metaMagicData.set_quicken(1)
	return 0

def Spell_Quicken_OnBeginRound(attachee, args, evt_obj):
	#breakp("Spell_Quicken_All_OnBeginRound 1: {}".format(attachee))
	args.set_arg(1, args.get_arg(0))
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # arg0 - number of quicken spells in one round, arg1 - reserved (used up in one round)
modObj.AddHook(toee.ET_OnMetaMagicMod, toee.EK_NONE, Spell_Quicken_OnMetaMagicMod, ())
modObj.AddHook(toee.ET_OnBeginRound, toee.EK_NONE, Spell_Quicken_OnBeginRound, ())
#breakp("Registered " + GetConditionName())
