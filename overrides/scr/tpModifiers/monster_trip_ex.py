import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Monster_Trip_Ex"

print("Registering " + GetConditionName())
###################################################

def Monster_Trip_Ex_OnDealingDamage2(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjDamage)

	target = evt_obj.attack_packet.target
	if (not target): return 0

	mode = args.get_arg(0)
	num_nat_attack = evt_obj.attack_packet.event_key - 1000
	print("evt_obj.attack_packet.event_key: {}, mode: {}, num_nat_attack: {}".format(evt_obj.attack_packet.event_key, mode, num_nat_attack))
	if (target.d20_query(toee.Q_Prone)): return 0

	do_trip = 0
	if (mode == 0): # any attack
		print("mode any attack")
		do_trip = 1
	else:
		print("checking natural attack")
		if (mode == 1): # only natural
			if (num_nat_attack >= 0): do_trip = 1
		else: # natural specific
			flag = 1
			if (num_nat_attack > 0):
				flag = (1 << (num_nat_attack))
			attacks_with_trip = args.get_arg(1)
			print("attacks_with_trip: {}, flag: {}".format(attacks_with_trip, flag))
			if (attacks_with_trip & flag): do_trip = 1
	
	print("do_trip: {}".format(do_trip))
	if (do_trip and attachee.trip_check(target)):
		target.fall_down()
		target.condition_add("Prone")
		target.float_mesfile_line( 'mes\\combat.mes', 104, 1 ) # Tripped!
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 5) # 0 =1 only natural, =2 natural specific, 1 =attacks_with_trip
modObj.AddHook(toee.ET_OnDealingDamage2, toee.EK_NONE, Monster_Trip_Ex_OnDealingDamage2, ())

