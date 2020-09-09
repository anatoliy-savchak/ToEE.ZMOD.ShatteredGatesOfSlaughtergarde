import toee, shattered_consts, utils_item, const_proto_armor, tpdp

from toee import *
from utilities import *
from scripts import *

def san_dialog( attachee, triggerer ):
	assert isinstance(triggerer, toee.PyObjHandle)
	if not attachee.has_met(triggerer):
		triggerer.begin_dialog(attachee, 1)
		return toee.SKIP_DEFAULT
	else:
		if (toee.game.quests[4].state == toee.qs_completed):
			triggerer.begin_dialog(attachee, 300)
			return toee.SKIP_DEFAULT
		elif (toee.game.quests[4].state == toee.qs_accepted):
			triggerer.begin_dialog( attachee, 150 )
			return toee.SKIP_DEFAULT
		else:
			maug_dipl(attachee, triggerer)
			return toee.SKIP_DEFAULT
	return toee.SKIP_DEFAULT

def san_first_heartbeat( attachee, triggerer ):
	return toee.RUN_DEFAULT

def san_dying(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	if (toee.game.quests[shattered_consts.QUEST_MAUG].state != qs_completed):
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE_MASTERWORK2, attachee)
	return toee.RUN_DEFAULT

def san_resurrect( attachee, triggerer ):
	return toee.RUN_DEFAULT

def san_spell_cast(attachee, triggerer, spell):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	assert isinstance(spell, toee.PySpell)

	if (spell.spell == toee.spell_detect_evil):
		toee.game.global_flags[shattered_consts.GLOBAL_FLAG_MAUG_DETECT_EVIL] = 1
	elif (spell.spell == toee.spell_detect_magic):
		toee.game.global_flags[shattered_consts.GLOBAL_FLAG_MAUG_DETECT_MAGIC] = 1

	return toee.RUN_DEFAULT

def set_KOS_flag1(attachee):
	toee.game.timevent_add(set_KOS_flag2, (attachee), 10000 )
	return

def set_KOS_flag2(attachee):
	attachee.npc_flag_set(toee.ONF_KOS )
	return

def just_floatin(attachee, triggerer):
	attachee.float_line( 30, triggerer )
	return

def maug_dipl_prev(attachee, triggerer):
	ddc = get_ddc(attachee, triggerer)
	o = game.random_range(1,20)
	if (o < 10): o = 10 # take 10
	skill_modd = triggerer.skill_level_get(attachee, skill_diplomacy)
	p = o + skill_modd
	if p >= ddc:    ## friednly
		attachee.turn_towards(triggerer)
		if not attachee.has_met( triggerer ):
			triggerer.begin_dialog( attachee, 40 )
			return
		else:
			triggerer.begin_dialog( attachee, 40 )
			return
	elif p <= (ddc-10):     ## unfriendly
		triggerer.begin_dialog( attachee, 10 )
		return
	else:       ## indifferent
		if not attachee.has_met( triggerer ):
			triggerer.begin_dialog( attachee, 1 )
			return
		else:
			triggerer.begin_dialog( attachee, 220 )
	return

def get_ddc(attachee, triggerer):
	dip_start = 0
	ddc = 0
	## are they a chaotic cleric?
	if (triggerer.stat_level_get(stat_alignment) == CHAOTIC_NEUTRAL or triggerer.stat_level_get(stat_alignment) == NEUTRAL_EVIL or triggerer.stat_level_get(stat_alignment) == CHAOTIC_EVIL) and triggerer.stat_level_get(stat_level_cleric) >= 1:
		dip_start -= 4
	## are they a lawful cleric?
	if (triggerer.stat_level_get(stat_alignment) == LAWFUL_NEUTRAL or triggerer.stat_level_get(stat_alignment) == NEUTRAL_GOOD or triggerer.stat_level_get(stat_alignment) == LAWFUL_GOOD) and triggerer.stat_level_get(stat_level_cleric) >= 1:
		dip_start += 2
	## are they a paladin?
	if triggerer.stat_level_get(stat_level_paladin) >= 1:
		dip_start += 2
	## have they Detected Magic on the circles?
	if game.global_flags[15] == 1:
		dip_start += 4
	## have they killed the howler?
	if game.global_flags[103] == 1:
		dip_start += 8
	## for returning scenarios, npc_1 and npc_2 indicate Maug was antagonised
	if get_1(attachee):
		dip_start -= 2
	if get_2(attachee):
		dip_start -= 4
	## standard DC to change attitude is 15
	ddc = (15 - dip_start)
	if ddc < 2:
		ddc = 2
	return ddc

def det_mag(attachee, triggerer):
	party_transfer_to( attachee, 6334 )
	scroll = attachee.item_find(6334)
	if scroll != OBJ_HANDLE_NULL:
		scroll.destroy()
	game.particles( 'sp-Detect Magic', attachee )
	game.global_flags[15] = 1
	return

def get_attitude_bonus_list(pc, npc):
	result = tpdp.BonusList()
	tpdp.dispatch_skill(pc, toee.skill_diplomacy, result, npc, 1)

	if (pc.stat_level_get(toee.stat_level_cleric)):
		aligm = pc.stat_level_get(toee.stat_alignment)
		if (aligm == toee.CHAOTIC_NEUTRAL):
			result.add(-4, 0, "PC is Chaotic Neutral Cleric")
		elif (aligm == toee.NEUTRAL_EVIL):
			result.add(-4, 0, "PC is Neutral Evil Cleric")
		elif (aligm == toee.CHAOTIC_EVIL):
			result.add(-4, 0, "PC is Chaotic Evil Cleric")
		elif (aligm == toee.LAWFUL_NEUTRAL):
			result.add(2, 0, "PC is Lawful Neutral Cleric")
		elif (aligm == toee.NEUTRAL_GOOD):
			result.add(2, 0, "PC is Neutral Good Cleric")
		elif (aligm == toee.LAWFUL_GOOD):
			result.add(2, 0, "PC is Lawful Good Cleric")

	if (pc.stat_level_get(toee.stat_level_paladin)):
		result.add(2, 0, "PC is Paladin")

	used_detect_magic = 0
	if (toee.game.global_flags[shattered_consts.GLOBAL_FLAG_MAUG_DETECT_MAGIC]):
		used_detect_magic = 4

	result.add(used_detect_magic, 0, "PC used Detect Magic scroll")

	howler_killed = 0
	if (toee.game.global_flags[shattered_consts.GLOBAL_FLAG_HOWLER_KILLED]):
		howler_killed = 8

	result.add(howler_killed, 0, "Howler killed")

	if (get_1(npc)):
		result.add(-2, 0, "PC suggested to abandon Maug's post")

	if (get_2(npc)):
		result.add(-4, 0, "PC defaced the circles")
	return result

def maug_dipl(npc, pc):
	bonlist = get_attitude_bonus_list(pc, npc)
	assert isinstance(bonlist, tpdp.BonusList)
	bonus = bonlist.get_total()
	dc = 15

	dice = toee.dice_new("1d20")
	roll = dice.roll()
	total = roll + bonus
	hist_id = tpdp.create_history_dc_roll(pc, dc, dice, roll, "Maug attitude", bonlist)
	toee.game.create_history_from_id(hist_id)

	if total >= dc:    ## friednly
		npc.turn_towards(pc)
		if not npc.has_met( pc ):
			pc.begin_dialog( npc, 40 )
			return
		else:
			pc.begin_dialog( npc, 40 )
			return
	elif total <= (dc-10):     ## unfriendly
		pc.begin_dialog( npc, 10 )
		return
	else:       ## indifferent
		if not npc.has_met( pc ):
			pc.begin_dialog( npc, 1 )
			return
		else:
			pc.begin_dialog( npc, 220 )
	return
