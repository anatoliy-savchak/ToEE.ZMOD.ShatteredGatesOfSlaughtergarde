import toee, templeplus.pymod, sys, tpdp, math, traceback, debug

###################################################
def GetConditionName():
	return "Wand_Attack"

print("Registering " + GetConditionName())
###################################################

def OnToHitBonusBase(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)

	evt_obj.attack_packet.set_flags(evt_obj.attack_packet.get_flags() | toee.D20CAF_TOUCH_ATTACK)
	return 0

def OnDealingDamage(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjDamage)
	primary_weapon = attachee.item_worn_at(toee.item_wear_weapon_primary)
	print("Wand_Attack OnDealingDamage primary_weapon: {}".format(primary_weapon))
	if (primary_weapon):
		attachee.refresh_turn()
		attachee.use_item(primary_weapon, evt_obj.attack_packet.target)
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 4) # reserved
modObj.AddHook(toee.ET_OnToHitBonusBase, toee.EK_NONE, OnToHitBonusBase, ())
modObj.AddHook(toee.ET_OnDealingDamage, toee.EK_NONE, OnDealingDamage, ())
modObj.AddHook(toee.ET_OnDealingDamage2, toee.EK_NONE, OnDealingDamage, ())

