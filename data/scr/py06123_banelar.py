from toee import *
from debugg import *
import utils_obj
from const_toee import *

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)

	breakp("san_enter_combat banelar")
	attachee.cast_spell(spell_mage_armor, attachee)
	return RUN_DEFAULT

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)

	breakp("san_start_combat banelar")
	attachee.cast_spell(spell_mage_armor, attachee)
	return RUN_DEFAULT
