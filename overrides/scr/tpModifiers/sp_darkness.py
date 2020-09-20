import toee, templeplus.pymod, sys, tpdp, traceback, debug

###################################################
def GetConditionName():
	return "sp-Darkness"

print("Registering " + GetConditionName())
###################################################

def sp_darkness_OnConditionAdd(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)

	radius = args.get_arg(3)
	if (not radius): radius = 20

	radius_feet = radius + (attachee.radius / 12.0)
	obj_evt_id = attachee.object_event_append(toee.OLC_CRITTERS, radius_feet)
	args.set_arg(2, obj_evt_id) # store evt_id

	spell_id = args.get_arg(0)
	spell_packet = tpdp.SpellPacket(spell_id)
	spell_obj = attachee

	spell_partsys_id = toee.game.particles("sp-Solid Fog", spell_obj)
	spell_packet.add_spell_object(spell_obj, spell_partsys_id) # store the spell obj and the particle sys

	spell_packet.update_registry()
	return

def sp_darkness_OnEnterAoE(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjObjectEvent)
	try:
		print("sp_darkness_OnEnterAoE attachee: {}, evt_obj.target: {}".format(attachee, evt_obj.target))

		obj_evt_id = args.get_arg(2)
		if (obj_evt_id != evt_obj.evt_id):
			return 0

		target = evt_obj.target
		if (not attachee or not target): return 0
		f = target.object_flags_get()
		if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): return 0

		spell_id = args.get_arg(0)
		spell_packet = tpdp.SpellPacket(spell_id)
		if (not spell_packet):
			print("spell_packet is null!")
			debug.breakp("spell_packet is null")
			return 0

		spell_packet.trigger_aoe_hit()

		duration = args.get_arg(1)
		if (target != attachee):
			partsys_id = toee.game.particles( "sp-Solid Fog-hit", target)
			spell_packet.add_target(target, partsys_id)
			spell_packet.update_registry()

		target.condition_add_with_args('sp-Darkness hit', spell_id, duration, obj_evt_id)
	except Exception, e:
		print "sp_darkness_S_Combat_End error:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debug.breakp("error")
	return 0

def sp_darkness_S_Combat_End(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	print("sp_darkness_S_Combat_End attachee: {}".format(attachee))
	try:
		spellId = args.get_arg(0)
		spell_packet = tpdp.SpellPacket(spellId)
		if (spell_packet.spell_enum == 0):
			print("sp_darkness_S_Combat_End attachee: {} spell_packet.spell_enum == 0!!".format(attachee))
			return
		print("sp_darkness_S_Combat_End attachee: {} removing spell!".format(attachee))
		#args.remove_spell()

		spell_packet.end_target_particles(attachee)

		lst = list()
		for i in range(0, 20):
			target = spell_packet.get_target(i)
			if (not target): continue
			#if (target == attachee): continue
			lst.append(target)

		print(lst)

		for target in lst:
			print("target.d20_send_signal(toee.EK_S_Spell_End, {}) for {}".format(spellId, target))
			spell_packet.end_target_particles(target)
			target.d20_send_signal(toee.EK_S_Spell_End-toee.EK_S_HP_Changed, spellId)
			spell_packet.remove_target(target)
		lst = None

		spell_packet.update_registry()
		#spell_packet.remove_target(attachee)
		args.remove_spell_with_key(toee.EK_S_Killed)
		args.remove_spell_mod()
		args.set_arg(1, 0)
	except Exception, e:
		print "sp_darkness_S_Combat_End error:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debug.breakp("error")
	return 0

sp_darkness_mod = templeplus.pymod.PythonModifier(GetConditionName(), 4) # 0 - spell_id, 1 - duration, 2 - event ID, 3 - radius
sp_darkness_mod.AddHook(toee.ET_OnConditionAdd, toee.EK_NONE, sp_darkness_OnConditionAdd, ())
sp_darkness_mod.AddHook(toee.ET_OnObjectEvent, toee.EK_OnEnterAoE, sp_darkness_OnEnterAoE, ())
sp_darkness_mod.AddHook(toee.ET_OnD20Signal, toee.EK_S_Combat_End, sp_darkness_S_Combat_End, ())
sp_darkness_mod.AddHook(toee.ET_OnD20Signal, toee.EK_S_Killed, sp_darkness_S_Combat_End, ())
sp_darkness_mod.AddSpellCountdownStandardHook()
sp_darkness_mod.AddAoESpellEndStandardHook()

###################################################
def GetConditionName():
	return "sp-Darkness hit"

print("Registering " + GetConditionName())
###################################################

def sp_darkness_hit_EndSpellMod(attachee, args, evt_obj):
	spell_id = args.get_arg(0)
	if (evt_obj.data1 == spell_id):
		print ("Ending mod for spell ID: {}".format(spell_id))
		args.remove_spell_mod() # does a .condition_remove() with some safety checks
		print("sp-Darkness hit removed from  {} (sp_darkness_hit_EndSpellMod)".format(attachee))
	return 0

def sp_darkness_hit_OnLeaveAoE(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjObjectEvent)

	obj_evt_id = args.get_arg(2)
	if (obj_evt_id != evt_obj.evt_id):
		return 0

	target = evt_obj.target
	if (not attachee or not target): return 0
	f = target.object_flags_get()
	if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): return 0

	spell_id = args.get_arg(0)
	spell_packet = tpdp.SpellPacket(spell_id)
	if (not spell_packet):
		print("spell_packet is null!")
		debug.breakp("spell_packet is null")
		return 0

	spell_packet.end_target_particles(target)
	spell_packet.remove_target(target)
	args.remove_spell_mod()
	print("sp-Darkness removed from  {} (sp_darkness_hit_OnLeaveAoE)".format(attachee))
	return 0

def sp_darkness_hit_OnGetDefenderConcealmentMissChance(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)

	miss_chance = 20
	evt_obj.bonus_list.add(miss_chance, 19, "Concealment (Darkness)")

	return 0

def sp_darkness_hit_OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTooltip)
	evt_obj.append("Darkness")
	return 0

def sp_darkness_hit_OnImmunityTrigger(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjImmunityTrigger)

	if (1):
		evt_obj.should_perform_immunity_check = 1
		evt_obj.immunity_key = 10
		return 10 #?
	return 0

def sp_darkness_hit_OnConditionAdd(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)

	print("sp-Darkness hit added to {}".format(attachee))
	return

sp_darkness_hit_mod = templeplus.pymod.PythonModifier(GetConditionName(), 8) # 0 - spell_id, 1 - duration, 2 - event ID
sp_darkness_hit_mod.AddHook(toee.ET_OnConditionAdd, toee.EK_NONE, sp_darkness_hit_OnConditionAdd, ())
sp_darkness_hit_mod.AddHook(toee.ET_OnObjectEvent, toee.EK_OnLeaveAoE, sp_darkness_hit_OnLeaveAoE, ())
sp_darkness_hit_mod.AddHook(toee.ET_OnD20Signal, toee.EK_S_Spell_End, sp_darkness_hit_EndSpellMod, ())
sp_darkness_hit_mod.AddHook(toee.ET_OnD20Signal, toee.EK_S_Killed, sp_darkness_hit_EndSpellMod, ())
sp_darkness_hit_mod.AddHook(toee.ET_OnD20Signal, toee.EK_S_Combat_End, sp_darkness_hit_EndSpellMod, ())
sp_darkness_hit_mod.AddHook(toee.ET_OnGetDefenderConcealmentMissChance, toee.EK_NONE, sp_darkness_hit_OnGetDefenderConcealmentMissChance, ())
sp_darkness_hit_mod.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, sp_darkness_hit_OnGetTooltip, ())
sp_darkness_hit_mod.AddHook(toee.ET_OnImmunityTrigger, toee.EK_IMMUNITY_SPELL, sp_darkness_hit_OnImmunityTrigger, ())
sp_darkness_hit_mod.AddSpellCountdownStandardHook()