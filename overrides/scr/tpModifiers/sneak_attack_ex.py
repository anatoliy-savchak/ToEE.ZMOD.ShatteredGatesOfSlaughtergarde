import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Sneak_Attack_Ex"

print("Registering " + GetConditionName())
###################################################

def is_ranged_weapon(weap):
	if weap == toee.OBJ_HANDLE_NULL:
		return 0
	weap_flags = weap.obj_get_int(toee.obj_f_weapon_flags)
	if not (weap_flags & toee.OWF_RANGED_WEAPON):
		return 0
	return 1

def SneakAttackEx_TargetIsNOTEligible(attacker, target, evt_obj):
	if (target == toee.OBJ_HANDLE_NULL): return 1
	assert isinstance(target, toee.PyObjHandle)
	assert isinstance(attacker, toee.PyObjHandle)

	if (not (attacker.can_sneak_attack(target))): return 2 # cannot sense (see)
	weapon_used = evt_obj.attack_packet.get_weapon_used()
	if (not is_ranged_weapon(weapon_used)):
		if (target.has_feat(toee.feat_blind_fight)): return 3 # feat_blind_fight
	
	if (target.d20_query(toee.Q_Critter_Is_Blinded)):
		blindsightDistance = target.d20_query("Blindsight Range")
		if (blindsightDistance > 0):
			distance = target.distance_to(attacker)
			if (distance <= blindsightDistance):
				return 5 # target can see even blinded
		return 4 # target is blinded, therefore no invisibility bonus
	return 0 # no obsticles

def SneakAttackEx_OnGetAcModifierFromAttacker(attachee, args, evt_obj):
	if (not (attachee.critter_flags_get() & toee.OCF_MOVING_SILENTLY)): return 0
	notEligible = SneakAttackEx_TargetIsNOTEligible(attachee, evt_obj.attack_packet.target, evt_obj)
	if (notEligible): 
		if (notEligible == 3):
			evt_obj.bonus_list.add_zeroed(164) # {Dex bonus retained due to ~Blind-Fight~[TAG_BLIND_FIGHT]}
		#if (notEligible == 4):
		#	evt_obj.bonus_list.add_zeroed(337) # {337}{Dex bonus retained due to target is ~Blinded~[TAG_BLINDED]}
		return 0
	if (evt_obj.attack_packet.target.has_feat(toee.feat_uncanny_dodge)):
		evt_obj.bonus_list.add_zeroed(165) # {165}{Dex bonus retained due to ~Uncanny Dodge~[TAG_CLASS_FEATURES_UNCANNY_DODGE]}
	else:
		evt_obj.bonus_list.add_cap(8, 0, 153, "Sneak Attack") # {153}{Condition: ~Flatfooted~[TAG_FLAT_FOOTED]}
		evt_obj.bonus_list.add_cap(3, 0, 153, "Sneak Attack")
	return 0

def SneakAttackEx_OnGetToHitBonusBase(attachee, args, evt_obj):
	if (not (attachee.critter_flags_get() & toee.OCF_MOVING_SILENTLY)): return 0

	if (evt_obj.attack_packet.target != toee.OBJ_HANDLE_NULL):
		notEligible = SneakAttackEx_TargetIsNOTEligible(attachee, evt_obj.attack_packet.target, evt_obj)
		if (notEligible): 
			#if (notEligible == 3):
			#	evt_obj.bonus_list.add_zeroed(335) # {335}{Invisibility bonus lost due to ~Blind-Fight~[TAG_BLIND_FIGHT]}
			#if (notEligible == 4):
			#	evt_obj.bonus_list.add_zeroed(336) # {336}{Invisibility bonus lost due to target is ~Blinded~[TAG_BLINDED]}
			return 0
				
	# to-do: check if already has invisible bonus
	evt_obj.bonus_list.add(2, 0, 161) # {161}{Attacker is not Visible}
	return 0

def SneakAttackEx_OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTooltip)
	if (not (attachee.critter_flags_get() & toee.OCF_MOVING_SILENTLY)): return 0
	evt_obj.append("Hidden")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2)
#modObj.MapToFeat(toee.feat_sneak_attack)
modObj.AddHook(toee.ET_OnGetAcModifierFromAttacker, toee.EK_NONE, SneakAttackEx_OnGetAcModifierFromAttacker, ())
modObj.AddHook(toee.ET_OnToHitBonusBase, toee.EK_NONE, SneakAttackEx_OnGetToHitBonusBase, ())
modObj.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, SneakAttackEx_OnGetTooltip, ())