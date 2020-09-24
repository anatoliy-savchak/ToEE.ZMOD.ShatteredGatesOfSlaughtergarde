import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Energy_Drain_Su"

print("Registering " + GetConditionName())
###################################################

def Energy_Drain_Su_DamageBonus(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjDamage)
	print("Energy_Drain_Su_DamageBonus adding negative level")
	target = evt_obj.attack_packet.target
	target.condition_add("Temp Negative Level")
	toee.game.create_history_from_pattern(60, attachee, target) # {60}{[ACTOR] strikes with ~energy drain~[TAG_ENERGY_DRAINED] on [TARGET]!}
	attachee.condition_add_with_args("Temporary_Hit_Points", 0, 14400, 5)
	toee.game.create_history_from_pattern(61, attachee, toee.OBJ_HANDLE_NULL) # {61}{[ACTOR] recieves 5 ~temporary hit points~[TAG_TEMPORARY_HIT_POINTS].}
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) #
modObj.AddHook(toee.ET_OnDealingDamage, toee.EK_NONE, Energy_Drain_Su_DamageBonus, ())

