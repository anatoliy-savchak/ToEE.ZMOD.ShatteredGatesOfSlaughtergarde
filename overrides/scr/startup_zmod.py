import toee, tpdp

def zmod_conditions_apply_pc():
	for pc in toee.game.party:
		pc.condition_add("Break_Object")
		pc.condition_add("Smash_Object")
		pc.condition_add("Inspect")
	return

def zmod_templeplus_config_apply():
	if ("config_set_string" in dir(tpdp)):
		tpdp.config_set_string("hpfornpchd", "average")
		tpdp.config_set_string("hponlevelup", "average")

	if ("config_set_bool" in dir(tpdp)):
		tpdp.config_set_bool("preferuse5footstep", 1)
		tpdp.config_set_bool("disabletargetsurrounded", 1)
		tpdp.config_set_bool("disablechooserandomspell_regardinvulnerablestatus", 1)
	
	return