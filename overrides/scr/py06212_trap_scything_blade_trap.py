import toee, debugg

def san_trap(trap, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(trap, toee.PyTrap)
	#debugg.breakp("san_trap")
	toee.game.particles("Trap-Scythe", trap.obj)
	toee.game.sound(4025, 1)
	dice = toee.dice_new("1d8")
	dice_crit = toee.dice_new("3d8")
	atk = 8
	for obj in toee.game.obj_list_range(trap.obj.location, 10, toee.OLC_CRITTERS):
		f = obj.object_flags_get()
		if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
		caf = trap.attack(obj, atk, 20, 0)
		if (not (caf & toee.D20CAF_HIT)): 
			print("missed")
			continue
		dce = dice
		if (caf & toee.D20CAF_CRITICAL): dce = dice_crit
		obj.damage(trap.obj, toee.D20DT_SLASHING, dce, toee.D20DAP_NORMAL, toee.D20A_UNSPECIFIED_ATTACK)
	return toee.SKIP_DEFAULT