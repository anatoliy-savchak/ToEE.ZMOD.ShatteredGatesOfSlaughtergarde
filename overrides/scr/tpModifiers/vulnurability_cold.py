import toee, templeplus.pymod, tpdp, debug

###################################################
#draft
def GetConditionName():
	return "Vulnurability_Cold"

print("Registering " + GetConditionName())
###################################################

def OnTakingDamage(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjDamage)
	debug.breakp("OnTakingDamage")
	#print("evt_obj.damage_packet.final_damage: {}".format(evt_obj.damage_packet.final_damage))
	#see int AbilityConditionFixes::MonsterSubtypeFire(DispatcherCallbackArgs args){
	#if (evt_obj.damage_packet.final_damage )
	#D20DAP_COLD
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 
modObj.AddHook(toee.ET_OnTakingDamage, toee.EK_NONE, OnTakingDamage, ())

