import toee, templeplus.pymod, tpdp, traceback, sys

###################################################

def GetConditionName():
	return "Armor Blurring"

print("Registering " + GetConditionName())
###################################################

def Armor_Blurring_OnBuildRadialMenuEntry(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	# evt_obj is None

	if (args.get_arg(1)): 
		# skip when active
		return 0

	#if (args.get_arg(4) >= 3): # used of 3 per day
	#	print("args.get_arg(4): {}".format(args.get_arg(4)))
	#	# skip when used
	#	return 0

	used = args.get_arg(4)
	text = "Armor"
	item_wear = args.get_arg(0)
	if (item_wear):
		worn_item = attachee.item_worn_at(item_wear)
		if (worn_item):
			text = worn_item.description
	parent_item = tpdp.RadialMenuEntryParent(text)
	parent_item_id = parent_item.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Items)

	left_usage = 3 - used
	text = "Activate Blurring {} / {}".format(left_usage, 3)

	radial_action = tpdp.RadialMenuEntryPythonAction(text, toee.D20A_PYTHON_ACTION, 3020, toee.spell_blur, "TAG_INTERFACE_HELP")
	#assert isinstance(radial_action, tpdp.RadialMenuEntryParent)
	spell_data = tpdp.D20SpellData(toee.spell_blur)
	spell_data.set_spell_level(5)
	radial_action.set_spell_data(spell_data)
	#radial_action.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Items)
	radial_action.add_as_child(attachee, parent_item_id)
	return 0

def Armor_Blurring_OnD20PythonActionPerform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	try:
		print("EventObjD20Action.d20a.spell_data.spell_enum: {}".format(evt_obj.d20a.spell_data.spell_enum))
		if (evt_obj.d20a.spell_data.spell_enum != toee.spell_blur):
			return 0
		if (args.get_arg(1)): 
			# skip when active
			return 0
		used = args.get_arg(4)
		if (used >= 3): return 0
		partsys_id = toee.game.particles("sp-Blur", attachee)
		args.set_arg(1, 5) # duration
		args.set_arg(3, partsys_id) # partsys_id
		args.set_arg(4, used + 1) # used of 3 per day
	except Exception, e:
		print "Inspect_OnD20PythonActionPerform:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
	return 1

def Armor_Blurring_OnGetDefenderConcealmentMissChance(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)
	if (not args.get_arg(1)): 
		# skip when not active
		return 0

	if (not evt_obj.attack_packet.attacker.d20_query(toee.Q_Critter_Has_True_Seeing)):
		evt_obj.bonus_list.add(20, 19, 184) #{184}{~Blur~[TAG_SPELLS_BLUR]}
	return 0

def Armor_Blurring_OnBeginRound(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)
	countdown = args.get_arg(1)
	if (not countdown): 
		# skip when not active
		return 0

	countdown -= 1
	args.set_arg(1, countdown)
	if (countdown == 0):
		partsys_id = args.get_arg(3)
		if (partsys_id):
			toee.game.particles_end(partsys_id)
		args.set_arg(3, 0)
	return 0

def Armor_Blurring_OnGetEffectTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjEffectTooltip)
	countdown = args.get_arg(1)
	if (not countdown): 
		# skip when not active
		return 0

	evt_obj.append(12, toee.spell_blur, "\n(Armor) Duration: {}/5".format(countdown))
	return 0

def Armor_Blurring_OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTooltip)
	countdown = args.get_arg(1)
	if (not countdown): 
		# skip when not active
		return 0
	evt_obj.append("Blurring (Armor)")
	return 0

def Armor_Blurring_OnNewDay(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	# evt_obj is None

	if (args.get_arg(4)): # used => 0
		args.set_arg(4, 0)
	return 0

def Armor_Blurring_OnBuildItemDescription(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjBonusList)
	evt_obj.bonus_list.add(1, 0, "")
	evt_obj.bonus_list.add(1, 0, "Armor Property: Blurring")
	evt_obj.bonus_list.add(1, 0, "This armor appears indistinct, as though its edges were smeared.")
	evt_obj.bonus_list.add(1, 0, "When you activate this armor, your appearance becomes distorted and hazy, as if you were affected by a blur spell.")
	evt_obj.bonus_list.add(1, 0, "The blurring property functions three times per day, and the effect lasts for 5 rounds.")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 6) # 0 item_wear_armor, 1 countdown, 2 inv_idx, 3 partsys_id, 4 used this day, 5 reserved
modObj.AddHook(toee.ET_OnBuildRadialMenuEntry, toee.EK_NONE, Armor_Blurring_OnBuildRadialMenuEntry, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3020, Armor_Blurring_OnD20PythonActionPerform, ())
modObj.AddHook(toee.ET_OnGetDefenderConcealmentMissChance, toee.EK_NONE, Armor_Blurring_OnGetDefenderConcealmentMissChance, ())
modObj.AddHook(toee.ET_OnBeginRound, toee.EK_NONE, Armor_Blurring_OnBeginRound, ())
modObj.AddHook(toee.ET_OnGetEffectTooltip, toee.EK_NONE, Armor_Blurring_OnGetEffectTooltip, ())
modObj.AddHook(toee.ET_OnNewDay, toee.EK_NONE, Armor_Blurring_OnNewDay, ())
#modObj.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, Armor_Blurring_OnGetTooltip, ())