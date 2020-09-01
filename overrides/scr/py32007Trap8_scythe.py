from toee import *
from Co8 import D20CO8_F_POISON

def san_trap( trap, triggerer ):
	# numP = 210 / (game.party_npc_size() + game.party_pc_size())
	# for obj in game.obj_list_vicinity( triggerer.location, OLC_CRITTERS ):
		# obj.stat_base_set(stat_experience, (obj.stat_level_get(stat_experience) - numP))
	game.particles( trap.partsys, trap.obj )
	game.sound(4025,1)
	result = trap.attack( triggerer, 8, 20, 0 )
	if (result & D20CAF_HIT):
		for dmg in trap.damage:
			print "dmg type=", dmg.type
			if (dmg.type == D20DT_POISON):
				if (triggerer.saving_throw( 13, D20_Save_Fortitude, D20CO8_F_POISON, trap.obj ) == 0):
					triggerer.condition_add_with_args("Poisoned",dmg.damage.bonus,0)
			else:
				d = dmg.damage.clone()
				if (result & D20CAF_CRITICAL):
					d.number = d.number * 2
					d.bonus = d.bonus * 2
				triggerer.damage( trap.obj, dmg.type, d )
	game.new_sid = 0
	return SKIP_DEFAULT
