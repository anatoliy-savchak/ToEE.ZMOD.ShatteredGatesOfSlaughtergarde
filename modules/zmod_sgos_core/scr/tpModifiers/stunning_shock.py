import toee, templeplus.pymod

###################################################

def GetConditionName():
	return "Stunning_Shock"

print("Registering " + GetConditionName())
###################################################

def Stunning_Shock_DamageBonus(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)

	obj_f_field = args.get_param(1)
	if (obj_f_field):
		turnoff = attachee.obj_get_int(obj_f_field) #obj_f_npc_retail_price_multiplier
		if (turnoff): return 0

	damage_dice = dice_new("2d8")
	evt_obj.damage_packet.add_dice(damage_dice, toee.D20DT_SUBDUAL, 127)
	#evt_obj.bonus_list.add( val, 1, 139)
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - could be packed dice, 1 - turnoff field id
modObj.AddHook(toee.ET_OnDealingDamage, toee.EK_NONE, Stunning_Shock_DamageBonus, ())

