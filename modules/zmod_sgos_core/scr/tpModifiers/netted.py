import toee, templeplus.pymod, debug, sys, tpdp, traceback

###################################################

def GetConditionName():
	return "netted"

print("Registering " + GetConditionName())
###################################################

def netted_OnAdd(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)

	has_web_on = attachee.d20_query_has_spell_condition(toee.spell_web)
	if (has_web_on): 
		args.condition_remove()
		return 0

	attachee.float_text_line("Entangled!", toee.tf_red)
	print("netted_OnAdd")
	partid = toee.game.particles("sp-Web Hit", attachee)
	args.set_arg(3, partid)
	return 0

def netted_OnAddPre(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjModifier)

	if (evt_obj.is_modifier("sp-Web On")):
		evt_obj.return_val = 0

	return 0

def netted_remove(args, cr = 0):
	assert isinstance(args, tpdp.EventArgs)
	partId = args.get_arg(3)
	if (partId > 0):
		print("netted_remove, partId: {}".format(partId))
		toee.game.particles_kill(partId)
	args.set_arg(3, 0)
	if (cr):
		print("condition_remove")
		args.condition_remove()
	return 0

def netted_OnRemove(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	print("netted_OnRemove, attachee: {}".format(attachee))
	netted_remove(args, 0)
	return 0

def netted_OnD20Query_CritterHasCondition(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)

	if (not "get_condition_ref" in dir(tpdp)): return 0

	cond_netted = tpdp.get_condition_ref(GetConditionName())
	print("cond_netted: {}, data1: {}, data2: {}".format(cond_netted, evt_obj.data1, evt_obj.data2))
	if (cond_netted == evt_obj.data1):
		evt_obj.return_val = 1

	#cond_web_on = tpdp.get_condition_ref("sp-Web On")
	#print("cond_web_on: {}, data1: {}, data2: {}".format(cond_web_on, evt_obj.data1, evt_obj.data2))
	#if (cond_netted == evt_obj.data1):
		#evt_obj.return_val = 1
	return 0

def netted_OnD20PythonQuery(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)
	evt_obj.return_val = 1
	print("netted_OnD20PythonQuery :: evt_obj.return_val = {}".format(evt_obj.return_val))
	return 0

def OnQueryReturnTrue(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)
	
	evt_obj.return_val = 1
	return 0

def OnQueryReturnFalse(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)
	
	evt_obj.return_val = 0
	return 0

def netted_OnAbilityScoreLevel_dex(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjBonusList)
	
	evt_obj.bonus_list.add(-4, toee.EK_STAT_DEXTERITY, 230) #bonus.mes: {230}{~Web~[TAG_SPELLS_WEB]}
	return 0

def netted_OnToHitBonus2(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)
	
	evt_obj.bonus_list.add(-2, 12, 230) #bonus.mes: {230}{~Web~[TAG_SPELLS_WEB]}
	return 0

def netted_OnGetMoveSpeed(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjMoveSpeed)
	
	movespeedCap = evt_obj.bonus_list.get_sum()
	if (movespeedCap > 5):
		movespeedCap = movespeedCap / 2
	#walk
	evt_obj.bonus_list.set_overall_cap(1, movespeedCap, 0, 230) #bonus.mes: {230}{~Web~[TAG_SPELLS_WEB]}
	#run?
	#evt_obj.bonus_list.set_overall_cap(2, movespeedCap, 0, 230) #bonus.mes: {230}{~Web~[TAG_SPELLS_WEB]}
	return 0

def netted_OnGetEffectTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjEffectTooltip)

	#evt_obj.append(tpdp.hash("NETTED"), -1, "")
	return 0

def netted_OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTooltip)

	evt_obj.append("Entanged")
	return 0

def netted_OnBuildRadialMenuEntry(attachee, args, evt_obj):
	#int __cdecl WebBreakfreeRadial(DCA args)
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	possible = attachee.d20_query(toee.Q_Is_BreakFree_Possible)
	if (not possible): return 0

	radial_action = tpdp.RadialMenuEntryPythonAction(5061, toee.D20A_BREAK_FREE, 0, 0, "TAG_RADIAL_MENU_BREAK_FREE")
	radial_action.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Movement)
	return 0

def netted_Q_Is_BreakFree_Possible(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)
	
	evt_obj.return_val = 1
	return 0

def netted_S_BreakFree(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)
	#int __cdecl sub_100D3BC0(DispCallbackArgs args)
	print "netted_S_BreakFree"
	try:
		dc = args.get_arg(0) # dc break free
		bonuslist = tpdp.BonusList()
		bonus = tpdp.dispatch_stat(attachee, toee.stat_str_mod, bonuslist)
		dice = toee.dice_new("1d20")
		roll = dice.roll()
		check = roll + bonus >= dc 
		hist_id = tpdp.create_history_dc_roll(attachee, dc, dice, roll, "Str", bonuslist)
		toee.game.create_history_from_id(hist_id)
		if (not check):
			attachee.float_mesfile_line("mes\\spell.mes", 20027, toee.tf_red) # {20027} {Entangled!}
			evt_obj.return_val = 0
		else:
			attachee.float_mesfile_line("mes\\spell.mes", 21003, toee.tf_red) #{21003} {Escaped!}
			evt_obj.return_val = 1
			netted_remove(args, 1)
	except Exception, e:
		print "netted_S_BreakFree error:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debug.breakp("error")
	return 0

def netted_do_remove(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	print("netted_do_remove, attachee: {}".format(attachee))
	netted_remove(args, 1)
	return 0

def netted_remove_check(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	print("netted_remove_check, attachee: {}".format(attachee))
	if (not toee.game.combat_is_active()):
		netted_remove(args, 1)
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 4, 1) # 0 - dc break free, dc escape artist, partId, reserved
modObj.AddHook(toee.ET_OnConditionAdd, toee.EK_NONE, netted_OnAdd, ())
modObj.AddHook(toee.ET_OnConditionAddPre, toee.EK_NONE, netted_OnAddPre, ())
modObj.AddHook(toee.ET_OnConditionRemove, toee.EK_NONE, netted_OnRemove, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_Critter_Has_Condition, netted_OnD20Query_CritterHasCondition, ())
modObj.AddHook(toee.ET_OnD20PythonQuery, "Is Netted", netted_OnD20PythonQuery, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_AOOPossible, OnQueryReturnFalse, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_Is_BreakFree_Possible, netted_Q_Is_BreakFree_Possible, ())
modObj.AddHook(toee.ET_OnAbilityScoreLevel, toee.EK_STAT_DEXTERITY, netted_OnAbilityScoreLevel_dex, ())
modObj.AddHook(toee.ET_OnToHitBonus2, toee.EK_NONE, netted_OnToHitBonus2, ())
modObj.AddHook(toee.ET_OnGetMoveSpeed, toee.EK_NONE, netted_OnGetMoveSpeed, ())
modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_Combat_End, netted_do_remove, ())
modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_Killed, netted_do_remove, ())
modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_BreakFree, netted_S_BreakFree, ())
modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_BeginTurn, netted_remove_check, ())
modObj.AddHook(toee.ET_OnGetEffectTooltip, toee.EK_NONE, netted_OnGetEffectTooltip, ())
modObj.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, netted_OnGetTooltip, ())
modObj.AddHook(toee.ET_OnBuildRadialMenuEntry, toee.EK_NONE, netted_OnBuildRadialMenuEntry, ())
# S_Teleport_Prepare? - skip for now
# S_Teleport_Reconnect ? - skip for now
# ET_OnGetTooltip - description
