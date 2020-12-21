import toee, templeplus.pymod, sys, tpdp, math, traceback

###################################################

def GetConditionName():
	return "Line_Of_Acid"

print("Registering " + GetConditionName())
###################################################

def Line_Of_Acid_Check(attachee, args, evt_obj):
	return 1

def Line_Of_Acid_Perform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	try:
		radius = args.get_arg(0)
		if (not radius): radius = 40
		damage_multiplier = args.get_arg(1)
		if (not damage_multiplier): damage_multiplier = 4
		dc = args.get_arg(2)
		if (not dc): dc = 16
		caster = attachee
		targets, furthest = BreathLineGetBestTargets(caster, radius)
		print(targets)
		if (targets):
			if (not furthest): furthest = targets[0]
			target_loc = furthest.location
			target_loc_off_x = furthest.off_x
			target_loc_off_y = furthest.off_y
			target_loc_off_z = furthest.obj_get_int(toee.obj_f_offset_z)
			caster.turn_towards(furthest)
			toee.game.create_history_freeform("{} performs Breath Weapon (Su)!\n\n".format(caster.description))
			toee.game.particles("sp-Call Lightning", caster)
			#toee.game.particles("sp-Cone of Cold", caster )
			toee.game.pfx_lightning_bolt(caster, target_loc, target_loc_off_x, target_loc_off_y, target_loc_off_z )
			affected = targets
			dce = toee.dice_new("{}d4".format(damage_multiplier))
			for target in affected:
				assert isinstance(target, toee.PyObjHandle)
				if (target == caster): continue
				if (target.type != toee.obj_t_npc and target.type != toee.obj_t_pc): continue
				f = target.object_flags_get()
				if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
				descriptor = 0 #toee.D20STD_F_SPELL_DESCRIPTOR_ACID todo
				target.reflex_save_and_damage(caster, dc, toee.DAMAGE_REDUCTION_HALF, descriptor, dce, toee.D20DT_ACID, toee.D20DAP_NORMAL, toee.D20A_CLASS_ABILITY_SA, 0)
				toee.game.particles("sp-Call Lightning-hit", target)

			if (furthest > 0 and caster.anim_goal_push_attack(furthest, toee.game.random_range(0, 2), 1, 0)):
				new_anim_id = caster.anim_goal_get_new_id()
				#print("pushed new anim id: {}".format(new_anim_id))
				evt_obj.d20a.flags |= toee.D20CAF_NEED_ANIM_COMPLETED
				evt_obj.d20a.anim_id = new_anim_id
	except Exception, e:
		print "Line_Of_Acid_Perform:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debugg.breakp("error")
	return 0

def loc2sec(loc):
	y = loc >> 32
	x = loc & 4294967295
	return ( x, y )

def BreathLineGetBestTargets(caster, max_distance):
	assert isinstance(caster, toee.PyObjHandle)
	assert isinstance(max_distance, float)
	cx, cy = loc2sec(caster.location)
	obj_data = dict()
	possible_targets = toee.game.party
	for obj in possible_targets:
		assert isinstance(obj, toee.PyObjHandle)
		distance = caster.distance_to(obj)
		if (distance > max_distance): continue
		sobj = str(obj)
		obj_data[sobj] = dict()
		#spell.caster.turn_towards(obj)
		obj_data[sobj]["obj"] = obj
		ox, oy = loc2sec(obj.location)
		obj_data[sobj]["rot_grad"] = math.degrees(math.atan2(oy-cy, ox-cx))
		obj_data[sobj]["can_see"] = caster.can_see(obj)
		obj_data[sobj]["would_hit"] = 0
		obj_data[sobj]["would_hit_ally"] = 0
		obj_data[sobj]["ally"] = caster.allegiance_shared(obj)
		obj_data[sobj]["primary"] = obj in possible_targets
		obj_data[sobj]["baddies"] = dict()
		obj_data[sobj]["distance"] = distance
		obj_data[sobj]["hp"] = obj.stat_level_get(toee.stat_hp_current)
	#spell.caster.rotation = orig_rot
	#print(obj_data)
	for sobj, data in obj_data.items():
		if (not data["can_see"]): continue
		if (not data["primary"]): continue
		for sobj2, data2 in obj_data.items():
			if (sobj2 == sobj): continue
			if (not data2["can_see"]): continue
			if (abs(data2["rot_grad"] - data["rot_grad"]) < 10):
				data["would_hit"] = data["would_hit"] + 1
				if (data["ally"]):
					data["would_hit_ally"] = data["would_hit_ally"] + 1
				data["baddies"][sobj2] = data2["obj"]
	master = None
	smaster = None
	for sobj, data in obj_data.items():
		if (not data["can_see"]): continue
		if (not data["primary"]): continue
		if (data["hp"] < 0): continue
		if (data["ally"]): continue
		if (master is None):
			master = data["obj"]
			smaster = sobj
			continue
		if (obj_data[smaster]["would_hit"] < data["would_hit"]):
			master = data["obj"]
		elif (obj_data[smaster]["would_hit"] == data["would_hit"] and obj_data[smaster]["would_hit_ally"] > data["would_hit_ally"]):
			master = data["obj"]
	# fancy print
	if (1==1):
		print("obj_data, master: {}".format(master))
		for sobj, data in obj_data.items():
			print(data)

	new_targets = []
	if (master):
		d = obj_data[smaster]
		baddies = d["baddies"]
		furthest = master
		furthest_dist = d["distance"]
		#print("chosen.baddies: {}".format(baddies))
		new_targets.append(master)
		for sobj, data in baddies.items():
			new_targets.append(data)
			d = obj_data[str(data)]
			new_dist = d["distance"]
			if (new_dist > furthest_dist):
				furthest_dist = new_dist
				furthest = data

	return new_targets, furthest

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 3) # radius, damage multiplier, dc
modObj.AddHook(toee.ET_OnD20PythonActionCheck, 3010, Line_Of_Acid_Check, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3010, Line_Of_Acid_Perform, ())
