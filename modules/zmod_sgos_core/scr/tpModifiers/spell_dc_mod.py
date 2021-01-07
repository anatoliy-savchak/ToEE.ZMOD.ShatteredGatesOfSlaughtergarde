import toee, templeplus.pymod, tpdp, debug

###################################################

def GetConditionName():
	return "Spell_DC_Mod"

print("Registering " + GetConditionName())
# increase DC for a spell

###################################################

def OnGetSpellDcMod(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjSpellEntry)
	spell_id = args.get_arg(0)
	if (not spell_id or evt_obj.spell_entry.spell_enum == spell_id):
		delta = args.get_arg(1)
		if (delta):
			evt_obj.bonus_list.add(delta, 0, "Racial Bonus")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 4, 0) # 0 - add spell_id or any, 1 - delta dc, other reserver
modObj.AddHook(toee.ET_OnGetSpellDcMod, toee.EK_NONE, OnGetSpellDcMod, ())

