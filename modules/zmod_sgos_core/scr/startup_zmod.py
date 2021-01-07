import toee, tpdp, const_toee

def zmod_conditions_apply_pc():
	for pc in toee.game.party:
		pc.condition_add("Break_Object")
		pc.condition_add("Smash_Object")
		#pc.condition_add("Skill_Appraise_Bonus")
		pc.condition_add("Inspect")
	return

def zmod_templeplus_config_apply():
	# import startup_zmod
	# startup_zmod.zmod_templeplus_config_apply()
	print("zmod_templeplus_config_apply")
	if ("config_set_string" in dir(tpdp)):
		tpdp.config_set_string("hpfornpchd", "average")
		tpdp.config_set_string("hponlevelup", "average")

	if ("config_set_bool" in dir(tpdp)):
		tpdp.config_set_bool("preferuse5footstep", 1)
		tpdp.config_set_bool("disabletargetsurrounded", 1)
		tpdp.config_set_bool("disablechooserandomspell_regardinvulnerablestatus", 1)
		tpdp.config_set_bool("iszmod", 1)
	
	firstpc = toee.game.party[0]
	firstpc.scripts[const_toee.sn_new_map] = 6101
	return

def zmod_change_pcs_radius():
	# import startup_zmod
	# startup_zmod.zmod_change_pcs_radius()
	for pc in toee.game.party:
		print("pc proto: {}".format(pc.proto))
		protoobj = toee.game.getproto(pc.proto)
		protoobj.radius = 30
	return