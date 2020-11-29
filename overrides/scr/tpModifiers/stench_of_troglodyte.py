import toee, templeplus.pymod, sys, tpdp, traceback, debug

###################################################
def GetConditionName():
	return "Stench_Of_Troglodyte"

print("Registering " + GetConditionName())
###################################################

def Stench_Of_Troglodyte_Check(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	evt_obj.return_val = 0 #AEC_OK
	return 1

def Stench_Of_Troglodyte_Perform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	try:
		print("Stench_Of_Troglodyte_Perform")
		#debug.breakp("Stench_Of_Troglodyte_Perform")
		toee.game.particles("Trap-poisonGas", attachee)
		range = args.get_arg(3)
		if (not range): range = 30

		dc = args.get_arg(2)
		affected = toee.game.obj_list_range(attachee.location, range, toee.OLC_CRITTERS)
		for target in affected:
			assert isinstance(target, toee.PyObjHandle)

			flags = target.object_flags_get()
			if ((flags & toee.OF_OFF) or (flags & toee.OF_DESTROYED) or (flags & toee.OF_DONTDRAW)): continue
			if (target.d20_query(toee.Q_Dead)): continue
			if (target.d20_query(toee.Q_Critter_Is_Immune_Poison)): 
				print("Stench_Of_Troglodyte_Perform immune to poison {}".format(target))
				continue
			if (target.d20_query("Immune to Stench of Troglodyte")): 
				print("Stench_Of_Troglodyte_Perform Immune to Stench of Troglodyte {}".format(target))
				continue
			
			saved = target.saving_throw(dc, toee.D20_Save_Fortitude, toee.D20STD_F_POISON, attachee)
			if (not saved):
				print("condition_add_with_args(Stench_Of_Troglodyte_Hit, {}, {}, {}, 1) on {}".format(args.get_arg(0), args.get_arg(1), args.get_arg(2), target))
				target.condition_add_with_args("Stench_Of_Troglodyte_Hit", args.get_arg(0), args.get_arg(1), args.get_arg(2), 1)
				if ("anim_goal_push_hit_by_weapon" in dir(attachee)):
					attachee.anim_goal_push_hit_by_weapon(target)
			else:
				print("Stench_Of_Troglodyte_Perform saved {}".format(target))

	except Exception, e:
		print "Stench_Of_Troglodyte_ error:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debug.breakp("error")
	return 0

def Stench_Of_Troglodyte_OnD20PythonQuery(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)
	evt_obj.return_val = 1
	print("Stench_Of_Troglodyte_OnD20PythonQuery :: evt_obj.return_val = {}".format(evt_obj.return_val))
	#debug.breakp("Stench_Of_Troglodyte_OnD20PythonQuery")
	return 0

Stench_Of_Troglodyte = templeplus.pymod.PythonModifier(GetConditionName(), 6) # 0 - spell_id/critter num, 1 - duration, 2 - dc 13, 3 - range 30
Stench_Of_Troglodyte.AddHook(toee.ET_OnD20PythonActionCheck, 3020, Stench_Of_Troglodyte_Check, ())
Stench_Of_Troglodyte.AddHook(toee.ET_OnD20PythonActionPerform, 3020, Stench_Of_Troglodyte_Perform, ())
Stench_Of_Troglodyte.AddHook(toee.ET_OnD20PythonQuery, "Immune to Stench of Troglodyte", Stench_Of_Troglodyte_OnD20PythonQuery, ())

###################################################
def GetConditionName():
	return "Stench_Of_Troglodyte_Hit"

print("Registering " + GetConditionName())
###################################################

def Stench_Of_Troglodyte_Hit_OnConditionAddPre(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjModifier)

	if (evt_obj.is_modifier("sp-Neutralize Poison") or evt_obj.is_modifier("sp-Delay Poison")):
		args.condition_remove()
	return 0

def Stench_Of_Troglodyte_Hit_OnConditionAdd(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)

	if (not args.get_arg(3)): return 0

	if (attachee.d20_query(toee.Q_Critter_Is_Immune_Poison)): 
		args.set_arg(3, 0)
		return 0
	return 0

def Stench_Of_Troglodyte_Hit_OnGetSkillLevel(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)
	
	if (not args.get_arg(3)): return 0
	evt_obj.bonus_list.add(-2, 0, "Sickened")
	return 0

def Stench_Of_Troglodyte_Hit_OnToHitBonus2(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)
	
	if (not args.get_arg(3)): return 0
	evt_obj.bonus_list.add(-2, 0, "Sickened")
	return 0

def Stench_Of_Troglodyte_Hit_OnGetAbilityCheckModifier(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjObjectBonus)
	
	if (not args.get_arg(3)): return 0
	evt_obj.bonus_list.add(-2, 0, "Sickened")
	return 0

def Stench_Of_Troglodyte_Hit_OnSaveThrowLevel(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)
	
	if (not args.get_arg(3)): return 0
	evt_obj.bonus_list.add(-2, 0, "Sickened")
	return 0

def Stench_Of_Troglodyte_Hit_OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjEffectTooltip)
	if (not args.get_arg(3)): return 0
	remaining = args.get_arg(1)
	evt_obj.append("Sickened: {}".format(remaining))
	return 0

def Stench_Of_Troglodyte_Hit_OnDealingDamage2(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjDamage)
	if (not args.get_arg(3)): return 0
	evt_obj.damage_packet.bonus_list.add(-2, 0, "Sickened")
	return 0

def Stench_Of_Troglodyte_Hit_OnBeginRound(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)

	if (not args.get_arg(3)): 
		if (not attachee.is_active_combatant()):
			args.condition_remove()
		return 0
	duration = args.get_arg(1)
	if (duration > 0):
		duration -= 1
		args.set_arg(1, duration)

	if (duration <= 0):
		args.set_arg(3, 0)
	return 0


Stench_Of_Troglodyte_Hit = templeplus.pymod.PythonModifier(GetConditionName(), 6) # 0 - spell_id/critter num, 1 - duration, 2 - dc 13, 3 - active, 
Stench_Of_Troglodyte_Hit.AddHook(toee.ET_OnConditionAddPre, toee.EK_NONE, Stench_Of_Troglodyte_Hit_OnConditionAddPre, ())
Stench_Of_Troglodyte_Hit.AddHook(toee.ET_OnConditionAdd, toee.EK_NONE, Stench_Of_Troglodyte_Hit_OnConditionAdd, ())
Stench_Of_Troglodyte_Hit.AddHook(toee.ET_OnGetSkillLevel, toee.EK_NONE, Stench_Of_Troglodyte_Hit_OnGetSkillLevel, ())
Stench_Of_Troglodyte_Hit.AddHook(toee.ET_OnToHitBonus2, toee.EK_NONE, Stench_Of_Troglodyte_Hit_OnToHitBonus2, ())
Stench_Of_Troglodyte_Hit.AddHook(toee.ET_OnGetAbilityCheckModifier, toee.EK_NONE, Stench_Of_Troglodyte_Hit_OnGetAbilityCheckModifier, ())
Stench_Of_Troglodyte_Hit.AddHook(toee.ET_OnSaveThrowLevel, toee.EK_NONE, Stench_Of_Troglodyte_Hit_OnSaveThrowLevel, ())
Stench_Of_Troglodyte_Hit.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, Stench_Of_Troglodyte_Hit_OnGetTooltip, ())
Stench_Of_Troglodyte_Hit.AddHook(toee.ET_OnDealingDamage2, toee.EK_NONE, Stench_Of_Troglodyte_Hit_OnDealingDamage2, ())
Stench_Of_Troglodyte_Hit.AddHook(toee.ET_OnBeginRound, toee.EK_NONE, Stench_Of_Troglodyte_Hit_OnBeginRound, ())
#Stench_Of_Troglodyte_Hit.AddSpellCountdownStandardHook()
