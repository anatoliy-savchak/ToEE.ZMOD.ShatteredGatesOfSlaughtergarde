import toee, templeplus.pymod, tpdp, debug, sys

###################################################

def GetConditionName():
	return "Skill_Appraise_Bonus"

print("Registering " + GetConditionName())
###################################################

def OnGetSkillLevel(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjObjectBonus)
	
	skill_bonus = args.get_arg(0)
	if (not skill_bonus): skill_bonus = 19

	if (skill_bonus):
		evt_obj.bonus_list.add(skill_bonus, 12, "RAW")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2, 0) # 0 - skill bonus
modObj.AddHook(toee.ET_OnGetSkillLevel, toee.EK_SKILL_APPRAISE, OnGetSkillLevel, ())
