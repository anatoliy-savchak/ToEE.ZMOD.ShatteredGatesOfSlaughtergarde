from templeplus.pymod import PythonModifier
from toee import *
from debugg import *

###################################################

def GetConditionName():
	return "Spell_Quicken_All"

print("Registering " + GetConditionName())
###################################################

def Spell_Quicken_All_OnMetaMagicMod(attachee, args, evt_obj):
	#breakp("Spell_Quicken_All_OnMetaMagicMod 1: {}".format(attachee))
	metaMagicData = evt_obj.meta_magic
	
	#Don't quicken more than once
	if metaMagicData.get_quicken() < 1:
		metaMagicData.set_quicken(1)
	return 0

modObj = PythonModifier(GetConditionName(), 2)
modObj.AddHook(ET_OnMetaMagicMod, EK_NONE, Spell_Quicken_All_OnMetaMagicMod, ())
#breakp("Registered " + GetConditionName())
