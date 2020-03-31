import toee
import debugg

CONDITION_PRONE = "Prone"
CONDITION_SP_SLEEP = "sp-Sleep"

def cond_has(npc, cond_name):
	assert isinstance(npc, toee.PyObjHandle)
	result = npc.d20_query_has_condition(cond_name)
	print("npc.d20query_has_cond({}) = {}".format(cond_name, result))
	return 0

def cond_has_prone(npc):
	assert isinstance(npc, toee.PyObjHandle)
	result = npc.d20_query(toee.EK_Q_Prone - toee.EK_Q_Helpless)
	return result

def cond_add_prone(npc):
	assert isinstance(npc, toee.PyObjHandle)
	already_has = cond_has_prone(npc)
	if (already_has): return 0
	npc.condition_add_with_args(CONDITION_PRONE, 0, 0)
	return
