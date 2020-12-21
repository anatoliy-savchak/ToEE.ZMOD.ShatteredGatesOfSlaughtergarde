from toee import *
from utilities import *
from Co8 import D20CO8_F_POISON

def san_trap( trap, triggerer ):
	return # alpha
	if (trap.id == 2):
		# numP = 210 / (game.party_npc_size() + game.party_pc_size())
		# for obj in game.obj_list_vicinity( triggerer.location, OLC_CRITTERS ):
			# obj.stat_base_set(stat_experience, (obj.stat_level_get(stat_experience) - numP))
		game.particles( trap.partsys, trap.obj )
		game.sound(4023,1)
		result = trap.attack( triggerer, 10, 20, 0 )
		if (result & D20CAF_HIT):
			if (triggerer.saving_throw( 15, D20_Save_Fortitude, D20CO8_F_POISON, trap.obj ) == 0):
				triggerer.condition_add_with_args("Poisoned",trap.damage[0].damage.bonus,0)
			d = trap.damage[1].damage.clone()
			if (result & D20CAF_CRITICAL):
				d.number = d.number * 2
				d.bonus = d.bonus * 2
			triggerer.damage( trap.obj, trap.damage[1].type, d )
		for obj in game.obj_list_vicinity( triggerer.location, OLC_CRITTERS ):
			if (obj.distance_to(trap.obj) <= 15):
				if (obj.has_los(trap.obj)):
					if (obj.saving_throw( 15, D20_Save_Fortitude, D20CO8_F_POISON, trap.obj ) == 0):
						obj.condition_add_with_args("Poisoned",trap.damage[2].damage.bonus,0)
		game.new_sid = 0

	if (trap.id == 3):
		# numP = 210 / (game.party_npc_size() + game.party_pc_size())
		# for obj in game.obj_list_vicinity( triggerer.location, OLC_CRITTERS ):
			# obj.stat_base_set(stat_experience, (obj.stat_level_get(stat_experience) - numP))
		game.particles( trap.partsys, trap.obj )
		game.sound(4023,1)
		result = trap.attack( triggerer, 8, 20, 0 )
		if (result & D20CAF_HIT):
			if (triggerer.saving_throw( 13, D20_Save_Fortitude, D20CO8_F_POISON, trap.obj ) == 0):
				triggerer.condition_add_with_args("Poisoned",trap.damage[0].damage.bonus,0)
			d = trap.damage[1].damage.clone()
			if (result & D20CAF_CRITICAL):
				d.number = d.number * 2
				d.bonus = d.bonus * 2
			triggerer.damage( trap.obj, trap.damage[1].type, d )
		game.new_sid = 0

	if (trap.id == 4):
		# numP = 210 / (game.party_npc_size() + game.party_pc_size())
		# for obj in game.obj_list_vicinity( triggerer.location, OLC_CRITTERS ):
			# obj.stat_base_set(stat_experience, (obj.stat_level_get(stat_experience) - numP))
		game.particles( trap.partsys, trap.obj )
		game.sound(4023,1)
		result = trap.attack( triggerer, 11, 20, 0 )
		if (result & D20CAF_HIT):
			if (triggerer.saving_throw( 16, D20_Save_Fortitude, D20CO8_F_POISON, trap.obj ) == 0):
				triggerer.condition_add_with_args("Poisoned",trap.damage[0].damage.bonus,0)
			d = trap.damage[1].damage.clone()
			if (result & D20CAF_CRITICAL):
				d.number = d.number * 2
				d.bonus = d.bonus * 2
			triggerer.damage( trap.obj, trap.damage[1].type, d )
		for obj in game.obj_list_vicinity( triggerer.location, OLC_CRITTERS ):
			if (obj.distance_to(trap.obj) <= 15):
				if (obj.has_los(trap.obj)):
					obj.reflex_save_and_damage( trap.obj, 20, D20_Save_Reduction_Half, D20STD_F_SPELL_DESCRIPTOR_ACID, trap.damage[2].damage, trap.damage[2].type, D20DAP_NORMAL )
		game.new_sid = 0

	if (trap.id == 7):
		# numP = 210 / (game.party_npc_size() + game.party_pc_size())
		# for obj in game.obj_list_vicinity( triggerer.location, OLC_CRITTERS ):
			# obj.stat_base_set(stat_experience, (obj.stat_level_get(stat_experience) - numP))
		game.particles( trap.partsys, trap.obj )
		game.sound(4023,1)
		result = trap.attack( triggerer, 13, 20, 0 )
		if (result & D20CAF_HIT):
			if (triggerer.saving_throw( 18, D20_Save_Fortitude, D20CO8_F_POISON, trap.obj ) == 0):
				triggerer.condition_add_with_args("Poisoned",trap.damage[0].damage.bonus,0)
			d = trap.damage[1].damage.clone()
			if (result & D20CAF_CRITICAL):
				d.number = d.number * 2
				d.bonus = d.bonus * 2
			triggerer.damage( trap.obj, trap.damage[1].type, d )
		for obj in game.obj_list_vicinity( triggerer.location, OLC_CRITTERS ):
			if (obj.distance_to(trap.obj) <= 10):
				if (obj.has_los(trap.obj)):
					if (obj.saving_throw( 18, D20_Save_Fortitude, D20CO8_F_POISON, trap.obj ) == 0):
						obj.condition_add_with_args("Poisoned",trap.damage[2].damage.bonus,0)
		game.new_sid = 0

####### code to retain TRAP!!!
	if (trap.id == 11 and triggerer.map == 5080):
		# numP = 210 / (game.party_npc_size() + game.party_pc_size())
		# for obj in game.obj_list_vicinity( triggerer.location, OLC_CRITTERS ):
			# obj.stat_base_set(stat_experience, (obj.stat_level_get(stat_experience) - numP))
		for chest in game.obj_list_vicinity(triggerer.location,OLC_CONTAINER):
			if (chest.name == 1055 and chest.distance_to(trap.obj) <= 5):
				loc1 = location_from_axis (484L, 566L)
				loc2 = location_from_axis (476L, 582L)
				loc = chest.location
				loct = trap.obj.location
				if (loc1 >= loc):
					chest.destroy()
					item = game.obj_create( 1055, location_from_axis (484L, 566L))
				if (loc2 >= loc and loc1 <= loc):
					chest.destroy()
					item = game.obj_create( 1055, location_from_axis (476L, 582L))
		npc = game.obj_create( 14605, loct)
		triggerer.begin_dialog(npc,1000)


	return SKIP_DEFAULT


