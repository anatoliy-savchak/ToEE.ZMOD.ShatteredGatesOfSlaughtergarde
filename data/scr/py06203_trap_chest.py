import toee, debugg

def san_trap(trap, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(trap, toee.PyTrap)
	#debugg.breakp("san_trap")
	toee.game.particles(trap.partsys, trap.obj)
	toee.game.sound(4029, 1)
	dice = toee.dice_new("1d4+1")
	dice_crit = toee.dice_new("2d4+2")
	for obj in toee.game.obj_list_range(trap.obj.location, 7, toee.OLC_CRITTERS):
		f = obj.object_flags_get()
		if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
		caf = trap.attack(obj, 10, 20, 1)
		if (not (caf & toee.D20CAF_HIT)): 
			print("missed")
			continue
		dce = dice
		if (caf & toee.D20CAF_CRITICAL): dce = dice_crit
		obj.damage(trap.obj, toee.D20DT_PIERCING, dce, toee.D20DAP_NORMAL, toee.D20A_UNSPECIFIED_ATTACK)
	return toee.SKIP_DEFAULT