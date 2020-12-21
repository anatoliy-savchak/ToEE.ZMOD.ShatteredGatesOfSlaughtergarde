import toee, debug

def san_trap(trap, triggerer):
	assert isinstance(triggerer, toee.PyObjHandle)
	assert isinstance(trap, toee.PyTrap)
	print("san_trap trap_trigger_poison_gas_pressurized_ungol_dust")
	trap_trigger_poison_gas_pressurized_ungol_dust(trap.obj, triggerer, trap.partsys, trap)
	return toee.SKIP_DEFAULT

def trap_trigger_poison_gas_pressurized_ungol_dust(attachee, triggerer, partsys, trap):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	assert isinstance(trap, toee.PyTrap)

	if (partsys):
		toee.game.particles(partsys, attachee)
	toee.game.sound(4021, 1)
	triggerer.condition_add_with_args("Poisoned", 31, 0)

	radius_ft = 7
	for obj in toee.game.obj_list_range(attachee.location, radius_ft, toee.OLC_CRITTERS):
		f = obj.object_flags_get()
		if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
		if (obj == triggerer): continue
		triggerer.condition_add_with_args("Poisoned", 31, 0)
	return