import toee

def zmod_conditions_apply_pc():
	for pc in toee.game.party:
		pc.condition_add("Break_Object")
		pc.condition_add("Smash_Object")
		pc.condition_add("Inspect")
	return
