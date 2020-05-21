import toee

def san_wield_on(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)

	subject_race = triggerer.obj_get_int(toee.obj_f_critter_race)
	subject_gender = triggerer.obj_get_int(toee.obj_f_critter_gender)
	#print("san_wield_on - subject_race: {}, subject_gender: {}, subject: {}".format(subject_race, subject_gender, triggerer))

	if (subject_race != toee.race_dwarf or subject_gender != toee.gender_male):
		triggerer.float_text_line("Incompatible subject!", toee.tf_red)
		toee.game.timevent_add(on_time_do_wield_off, (triggerer, attachee), 100, 1)

	return toee.RUN_DEFAULT

def make_test():
	obj = toee.game.obj_create(6026, toee.game.leader.location) # Barbarian Helm
	obj.scripts[24] = 630 # san_wield_on
	return obj

def on_time_do_wield_off(owner, item):
	assert isinstance(owner, toee.PyObjHandle)
	assert isinstance(item, toee.PyObjHandle)
	#print("on_time_do_wield_off:: owner: {}, item: {}".format(owner, item))
	slot_worn = None
	for i in range(toee.item_wear_helmet, toee.item_wear_lockpicks):
		item_worn = owner.item_worn_at(i)
		if (item_worn == item):
			slot_worn = i
			break

	#print("slot_worn: {}".format(slot_worn))
	if (not slot_worn is None):
		owner.item_worn_unwield(slot_worn, 0)
	return
