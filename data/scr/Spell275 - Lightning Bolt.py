from toee import *
import math
import sys

def location_to_axis( loc ):
	if type(loc) == type(OBJ_HANDLE_NULL):
		loc = loc.location
		# in case the object was given as an argument instead of its location
	y = loc >> 32
	x = loc & 4294967295
	return ( x, y )

def OnBeginSpellCast( spell ):
	print "Lightning Bolt OnBeginSpellCast"
	print "spell.target_list=", spell.target_list
	print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
	game.particles( "sp-evocation-conjure", spell.caster )

def OnSpellEffect( spell ):
	print "Lightning Bolt OnSpellEffect"
	try:
		npc_mode = spell.caster.type == obj_t_npc
		caster = spell.caster

		# spell.target_list is PySpellTargets, not List
		target_objects = []
		for spell_target_entry in spell.target_list: target_objects.append(spell_target_entry.obj)

		target_loc = spell.target_loc
		target_loc_off_x = spell.target_loc_off_x
		target_loc_off_y = spell.target_loc_off_y
		target_loc_off_z = spell.target_loc_off_z

		#lx, ly = location_to_axis(target_loc)
		#print("orig target_loc: {} ({} {}), target_loc_off_x: {}, target_loc_off_y: {}, target_loc_off_z: {}".format(target_loc, lx, ly, target_loc_off_x, target_loc_off_y, target_loc_off_z))

		furthest = None
		if (npc_mode and len(target_objects) > 1):
			possible_targets = []
			for obj in target_objects:
				possible_targets.append(obj)
				for sibling in game.obj_list_range(obj.location, 20, OLC_NPC):
					if (obj != sibling and sibling != caster and not sibling in possible_targets):
						possible_targets.append(sibling)
			#orig_rot = caster.rotation
			cx, cy = location_to_axis(caster.location)
			obj_data = dict()
			for obj in possible_targets:
				sobj = str(obj)
				obj_data[sobj] = dict()
				#spell.caster.turn_towards(obj)
				obj_data[sobj]["obj"] = obj
				ox, oy = location_to_axis(obj.location)
				obj_data[sobj]["rot_grad"] = math.degrees(math.atan2(oy-cy, ox-cx))
				obj_data[sobj]["can_see"] = caster.can_see(obj)
				obj_data[sobj]["would_hit"] = 0
				obj_data[sobj]["would_hit_ally"] = 0
				obj_data[sobj]["ally"] = caster.allegiance_shared(obj)
				obj_data[sobj]["primary"] = obj in target_objects
				obj_data[sobj]["baddies"] = dict()
				obj_data[sobj]["distance"] = caster.distance_to(obj)
			#spell.caster.rotation = orig_rot
			#print(obj_data)
			for sobj, data in obj_data.items():
				if (not data["can_see"]): continue
				if (not data["primary"]): continue
				for sobj2, data2 in obj_data.items():
					if (sobj2 == sobj): continue
					if (not data2["can_see"]): continue
					if (abs(data2["rot_grad"] - data["rot_grad"]) < 10):
						data["would_hit"] = data["would_hit"] + 1
						if (data["ally"]):
							data["would_hit_ally"] = data["would_hit_ally"] + 1
						data["baddies"][sobj2] = data2["obj"]
			master = None
			smaster = None
			for sobj, data in obj_data.items():
				if (not data["can_see"]): continue
				if (not data["primary"]): continue
				if (data["ally"]): continue
				if (master is None):
					master = data["obj"]
					smaster = sobj
					continue
				if (obj_data[smaster]["would_hit"] < data["would_hit"]):
					master = data["obj"]
				elif (obj_data[smaster]["would_hit"] == data["would_hit"] and obj_data[smaster]["would_hit_ally"] > data["would_hit_ally"]):
					master = data["obj"]
			# fancy print
			if (1==0):
				print("obj_data:")
				for sobj, data in obj_data.items():
					print(data)

			#print("chosen: {} (smaster: {})".format(master, smaster))
			#print(obj_data)
			new_targets = []
			if (master):
				d = obj_data[smaster]
				baddies = d["baddies"]
				furthest = master
				furthest_dist = d["distance"]
				#print("chosen.baddies: {}".format(baddies))
				new_targets.append(master)
				for sobj, data in baddies.items():
					new_targets.append(data)
					d = obj_data[str(data)]
					new_dist = d["distance"]
					if (new_dist > furthest_dist):
						furthest_dist = new_dist
						furthest = data

			target_objects = new_targets
			#print("new target_objects: ")

		if (furthest is None and len(target_objects)):
			furthest = target_objects[0]

		if (not target_loc and not furthest is None):
			target_loc = furthest.location
			target_loc_off_x = furthest.off_x
			target_loc_off_y = furthest.off_y
			caster.turn_towards(furthest)

		#print(target_objects)
		#lx, ly = location_to_axis(target_loc)
		#print("new target_loc: {} ({} {}), target_loc_off_x: {}, target_loc_off_y: {}, target_loc_off_z: {}".format(target_loc, lx, ly, target_loc_off_x, target_loc_off_y, target_loc_off_z))

		if (len(target_objects) > 0):
			remove_list = []
			damage_dice = dice_new( '1d6' )
			damage_dice.number = min( 1 * spell.caster_level, 10 )
			game.pfx_lightning_bolt(caster, target_loc, target_loc_off_x, target_loc_off_y, target_loc_off_z )
			for target_item in target_objects:
				game.particles( 'sp-Lightning Bolt-hit', target_item )
				if target_item.reflex_save_and_damage( spell.caster, spell.dc, D20_Save_Reduction_Half, D20STD_F_NONE, damage_dice, D20DT_ELECTRICITY, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id ) > 0:
					# saving throw successful
					target_item.float_mesfile_line( 'mes\\spell.mes', 30001 )
				else:
					# saving throw unsuccessful
					target_item.float_mesfile_line( 'mes\\spell.mes', 30002 )

				remove_list.append( target_item)
			spell.target_list.remove_list( remove_list )
		else:
			spell.caster.float_text_line("No targets!", 1)
	except Exception, e:
		print "Lightning Bolt OnSpellEffect error:", sys.exc_info()[0]
		print(str(e))
	finally:
		spell.spell_end(spell.id)
	return

def OnBeginRound( spell ):
	print "Lightning Bolt OnBeginRound"

def OnEndSpellCast( spell ):
	print "Lightning Bolt OnEndSpellCast"