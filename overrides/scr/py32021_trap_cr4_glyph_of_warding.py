import toee, debug

def san_trap(trap, triggerer):
	assert isinstance(triggerer, toee.PyObjHandle)
	assert isinstance(trap, toee.PyTrap)

	trap_trigger_glyph_of_warding(trap.obj, triggerer, trap.partsys)
	return toee.SKIP_DEFAULT

# for manual triggering
def san_use(attachee, triggerer):
	# TODO or SKIP
	return toee.RUN_DEFAULT

def trap_trigger_glyph_of_warding(attachee, triggerer, partsys):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)

	if (partsys):
		toee.game.particles(partsys, attachee)
	toee.game.sound(4029, 1)
	dice = toee.dice_new("2d8")
	radius_ft = 7
	for obj in toee.game.obj_list_range(attachee.location, radius_ft, toee.OLC_CRITTERS):
		f = obj.object_flags_get()
		if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
		obj.reflex_save_and_damage(attachee, 14, toee.D20_Save_Reduction_Half, 0x4 | 0x2000 | 0x20, dice, toee.D20DT_ACID, toee.D20DAP_MAGIC, toee.D20A_NONE, 0)

	return