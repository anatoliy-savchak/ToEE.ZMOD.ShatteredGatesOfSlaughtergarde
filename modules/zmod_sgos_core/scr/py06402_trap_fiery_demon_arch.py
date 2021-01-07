import toee, debug

def san_trap(trap, triggerer):
	assert isinstance(triggerer, toee.PyObjHandle)
	assert isinstance(trap, toee.PyTrap)

	trap_trigger_demon_arch(trap.obj, triggerer, trap.partsys, trap)
	return toee.SKIP_DEFAULT

def trap_trigger_demon_arch(attachee, triggerer, partsys, trap):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	assert isinstance(trap, toee.PyTrap)

	if (partsys):
		toee.game.particles(partsys, attachee)
	toee.game.sound(4029, 1)
	dice = toee.dice_new("3d6")
	triggerer.damage(attachee, trap.damage[0].type, trap.damage[0].damage, toee.D20DAP_MAGIC, toee.D20A_NONE)

	radius_ft = 7
	for obj in toee.game.obj_list_range(attachee.location, radius_ft, toee.OLC_CRITTERS):
		f = obj.object_flags_get()
		if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
		if (obj == triggerer): continue
		obj.damage(attachee, trap.damage[0].type, trap.damage[0].damage, toee.D20DAP_MAGIC, toee.D20A_NONE)

	triggerer.anim_goal_use_object(attachee)
	return