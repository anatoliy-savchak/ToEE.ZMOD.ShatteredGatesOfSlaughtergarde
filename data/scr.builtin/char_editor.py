import toee

def get_max_spell_level(handle, classEnum, characterLvl):
	assert isinstance(handle, toee.PyObjHandle)
	assert isinstance(classEnum, int)
	assert isinstance(characterLvl, int)

	return 1

def get_learnable_spells(handle, classEnum, maxSpellLvl, is_domain_spell_class):
	assert isinstance(handle, toee.PyObjHandle)
	assert isinstance(classEnum, int)
	assert isinstance(maxSpellLvl, int)
	assert isinstance(is_domain_spell_class, int)

	return list()

def spell_known_add(ksi):
	assert isinstance(ksi, list)
	return

def spell_known_add2(ksi, handle):
	assert isinstance(ksi, list)
	assert isinstance(handle, toee.PyObjHandle)
	return