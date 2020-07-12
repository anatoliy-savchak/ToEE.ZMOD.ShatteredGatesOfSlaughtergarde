import toee, debugg, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee
import ctrl_behaviour, py06122_cormyr_prompter, shattered_consts, py06211_shuttered_monster, const_proto_scrolls, py06401_shattered_temple_encounters, const_proto_wands, utils_npc

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print(attachee.id)
	#debugg.breakp("san_first_heartbeat")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_ARMORY): toee.RUN_DEFAULT
	for pc in toee.game.party:
		pc.condition_add("Inspect")
	ctrl = CtrlShatteredArmory.ensure(attachee)
	ctrl.place_encounters()
	return toee.RUN_DEFAULT

def csa():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(shattered_consts.SHATERRED_ARMORY_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	if (CtrlShatteredTemple.get_name() in o.data):
		result = o.data[CtrlShatteredTemple.get_name()]
	else: return None
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	return result

class CtrlShatteredArmory(object):
	def __init__(self):
		self.encounters_placed = 0
		self.monsters = dict()
		self.m2 = list()
		self.id = None
		self.haertbeats_since_sleep_status_update = 0
		return

	def created(self, npc):
		self.id = npc.id
		npc.scripts[const_toee.sn_dialog] = 6410
		return

	@staticmethod
	def get_name():
		return "CtrlShatteredArmory"

	@classmethod
	def ensure(cls, npc):
		data = utils_storage.obj_storage(npc).data
		ctrl = None
		if (cls.get_name() in data):
			ctrl = data[cls.get_name()]
		else:
			ctrl = cls()
			ctrl.created(npc)
			utils_storage.obj_storage(npc).data[cls.get_name()] = ctrl
		return ctrl

	@classmethod
	def get_from_obj(cls, npc):
		data = utils_storage.obj_storage(npc).data
		if (cls.get_name() in data):
			return data[cls.get_name()]
		return None

	def place_encounters(self):
		#if (self.encounters_placed): return
		#debugg.breakp("place_encounters")
		self.encounters_placed = 1
		#self.place_encounter_t1()
		#self.place_encounter_t2()
		#self.place_encounter_t3()
		#self.place_encounter_t4()
		#self.place_encounter_t5()
		#self.place_encounter_t6()
		#self.place_encounter_t7()
		#self.place_encounter_t8()
		#self.place_encounter_t9()
		#self.place_encounter_t10()
		#self.place_encounter_t11()
		#self.place_encounter_t12()
		#self.place_encounter_t13()
		#self.place_encounter_t14()
		#self.place_encounter_t15()
		#self.place_encounter_t16()
		#self.place_encounter_t17()
		#self.place_encounter_t18()
		#self.place_encounter_t19()
		#self.place_encounter_t20()
		#self.place_encounter_t21()
		#self.place_encounter_t22()
		#self.place_encounter_t23()
		#self.place_encounter_t24()
		#self.place_encounter_t25()
		#self.print_monsters()

		# debug
		#wizard = toee.game.party[4]
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_COLOR_SPRAY, wizard)
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_OBSCURING_MIST, wizard)
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_INVISIBILITY, wizard)
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_BLUR, wizard)
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_GLITTERDUST, wizard)
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_FIREBALL, wizard)
		#utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_MAGIC_MISSILES_1ST, wizard)
		#utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_ACID_SPLASH, wizard)
		#wizard.identify_all()
		#utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_GLAIVE_MASTERWORK, toee.game.party[1])
		#self.remove_trap_doors()
		toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 474, 518)
		utils_obj.scroll_to_leader()
		return
