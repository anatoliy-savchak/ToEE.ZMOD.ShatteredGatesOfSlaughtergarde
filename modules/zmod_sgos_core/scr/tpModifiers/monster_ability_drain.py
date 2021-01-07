import toee, templeplus.pymod, tpdp, traceback, sys, debug

###################################################

def GetConditionName():
	return "Monster_Ability_Drain_Su"

print("Registering " + GetConditionName())
###################################################

def Monster_Ability_Drain_Su_OnDealingDamage2(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjDamage)
	try:
		print("Monster_Ability_Drain_Su_OnDealingDamage2")
		attacks_with_drain = args.get_arg(4)
		num_nat_attack = evt_obj.attack_packet.event_key - 1000
		print("evt_obj.attack_packet.event_key: {}, mode: {}".format(evt_obj.attack_packet.event_key, attacks_with_drain))

		if (attacks_with_drain != 0): # 0 for all
			flag = 1
			if (num_nat_attack > 0):
				flag = (1 << (num_nat_attack))
			print("attacks_with_drain: {}, flag: {}".format(attacks_with_drain, flag))
			if (not (attacks_with_drain & flag)): 
				print("NOT THIS NATURAL ATTACK")
				return 0

		target = evt_obj.attack_packet.target
		dc = args.get_arg(0)
		save = args.get_arg(1)
	
		toee.game.create_history_from_pattern(68, attachee, target) # {60}{[ACTOR] strikes with ~energy drain~[TAG_ENERGY_DRAINED] on [TARGET]!}
		saved = target.saving_throw(dc, save, toee.D20STD_F_NONE, attachee)
		if (saved): 
			print("saved!")
			return 0

		ability = args.get_arg(2)
		dice_packed = int(args.get_arg(3)) #!! long will fail

		dice = toee.dice_new("1d1")
		#print("setting dice_packed: {}".format(dice_packed))
		#debug.breakp("dice_packed")
		dice.packed = dice_packed

		amount = dice.roll()
		print("target.condition_add_with_args(Temp_Ability_Loss, {}, {}) {}".format(ability, amount, target))
		target.condition_add_with_args("Temp_Ability_Loss", ability, amount)
		#toee.game.create_history_from_pattern(61, attachee, toee.OBJ_HANDLE_NULL) # {61}{[ACTOR] recieves 5 ~temporary hit points~[TAG_TEMPORARY_HIT_POINTS].}
	except Exception, e:
		print "Monster_Ability_Drain_Su_OnDealingDamage2 error:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debug.breakp("error")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 6) # 0 dc, 1 save, 2 ability, 3 dice, 4 attacks_with_drain
modObj.AddHook(toee.ET_OnDealingDamage2, toee.EK_NONE, Monster_Ability_Drain_Su_OnDealingDamage2, ())

