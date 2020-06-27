import toee
import copy

def find_pc_closest_to_origin(loc):
	f = None
	fdist = 0.0
	for obj in toee.game.party:
		assert isinstance(obj, toee.PyObjHandle)
		if (f is None): 
			f = obj
			fdist = obj.distance_to(loc)
			continue
		dist = obj.distance_to(loc)
		if (dist < fdist):
			f = obj
			fdist = dist
	return f, fdist

class AITargetList(object):
	def __init__(self, npc, option_include_pc = 1, option_include_npc = 0, measures = None, option_scan_range = 120):
		assert isinstance(npc, toee.PyObjHandle)
		self.npc = npc
		self.option_include_pc = option_include_pc
		self.option_include_npc = option_include_npc
		self.option_scan_range = option_scan_range
		self.list = list()
		self.measures = measures
		if (self.measures is None):
			self.measures = AITargetMeasure()
		self.aggr = AITargetMeasure()
		return

	def __str__(self):
		s = "AITargetList: "
		first = 0
		for target in self.list:
			if (first): first = 0
			else: s += "\n"
			s += str(target)
		return s

	def rescan(self, do_measure = 1, do_qualify = 1):
		self.list = list()
		if (self.option_include_pc):
			for obj in toee.game.party:
				self.list.append(AITarget(self.npc, obj, self.measures))
		if (self.option_include_npc):
			#for obj in toee.game.obj_list_range(self.npc.location, self.option_scan_range, toee.OLC_NPC):
			for obj in toee.game.obj_list_vicinity(self.npc.location, toee.OLC_NPC):
				assert isinstance(obj, toee.PyObjHandle)
				if (self.npc == obj): continue
				oflags = obj.object_flags_get()
				if ((oflags & toee.OF_DONTDRAW) or (oflags & toee.OF_DESTROYED) or (oflags & toee.OF_OFF)): 
					print("obj {} is skipped due to flags: {}".format(obj, oflags))
					continue
				self.list.append(AITarget(self.npc, obj, self.measures))

		print("rescan found {} objects in scan range {}".format(len(self.list), self.option_scan_range))
		if (do_measure):
			self.measure()

		print(self)
		if (do_qualify):
			self.qualify()
		return self

	def measure(self):
		for target in self.list:
			assert isinstance(target, AITarget)
			target.measure()
		self.aggregate()
		return self

	def qualify(self):
		new_list = list()
		for target in self.list:
			assert isinstance(target, AITarget)
			if (target.qualify()):
				new_list.append(target)
			else: 
				print("target {} disqualified ".format(target.target))
		self.list = new_list
		return self

	def aggregate(self):
		if (not self.list): return
		for t in self.list:
			assert isinstance(t, AITarget)
			if (t.measures.value_range_is_within_melee):
				self.aggr.value_range_is_within_melee +=1
			if (t.measures.value_weapon_melee):
				self.aggr.value_weapon_melee +=1
			if (t.measures.value_weapon_ranged):
				self.aggr.value_weapon_ranged +=1
		return

	def sort_default(self):
		self.list.sort(cmp = _AITargetList_cmp_default)
		return self

	def top(self):
		result = 0
		assert isinstance(result, toee.PyObjHandle)
		target = self.topt()
		if (not target is None):
			assert isinstance(target, AITarget)
			result = target.target
		return result

	def bottom(self):
		result = 0
		assert isinstance(result, toee.PyObjHandle)
		if (len(self.list)):
			target = self.list[len(self.list)-1]
			assert isinstance(target, AITarget)
			result = target.npc
		return result

	def topt(self):
		result = None
		assert isinstance(result, AITarget)
		if (len(self.list)):
			target = self.list[0]
			assert isinstance(target, AITarget)
			result = target
		return result

class AITargetMeasure(object):
	def __init__(self):
		#self.measure_is_destroyed = 1
		self.measure_stat_ac = 0
		self.measure_stat_hp = 0
		self.measure_stat_save_fortitude = 0
		self.measure_stat_save_reflexes = 0
		self.measure_stat_save_willpower = 0
		self.measure_has_los = 0
		self.measure_range_is_within_melee = 0
		self.measure_distance = 0
		self.measure_can_path = 0
		self.measure_weapons = 0
		self.measure_prone = 0

		self.option_distance_over_reach_allowed = 0.0
		self.option_can_path_flags = 0

		#self.value_is_destroyed = 0
		self.value_stat_ac = 0
		self.value_stat_hp = 1
		self.value_stat_hp_max = 0
		self.value_stat_hp_percent = 0
		self.value_stat_save_fortitude = 0
		self.value_stat_save_reflexes = 0
		self.value_stat_save_willpower = 0
		self.value_has_los = 0
		self.value_distance_to_target = 0
		self.value_reach = 0
		self.value_distance_over_reach = 0
		self.value_range_is_within_melee0 = 0
		self.value_range_is_within_melee = 0
		self.value_can_path = 0
		self.value_weapon_melee = 0
		self.value_weapon_ranged = 0
		self.value_prone = 0
		
		#self.mult_is_destroyed = -1000
		self.mult_stat_ac = 0
		self.mult_stat_hp = 0
		self.mult_stat_hp_max = 0
		self.mult_stat_hp_percent = 0
		self.mult_stat_save_fortitude = 0
		self.mult_stat_save_reflexes = 0
		self.mult_stat_save_willpower = 0
		self.mult_has_los = 0
		self.mult_range_is_within_melee = 0
		self.mult_distance = 0
		self.mult_can_path = 0
		
		#self.qualify_is_destroyed_not = 1
		self.qualify_has_los = 0
		self.qualify_range_is_within_melee = 0
		self.qualify_stat_hp = 1

		self.weight = 0
		return
	
	@classmethod
	def by_ac(cls, highest = 1):
		measures = cls()
		measures.measure_stat_ac = 1
		measures.mult_stat_ac = 1
		if (not highest): measures.mult_stat_ac = -1
		measures.measure_has_los = 1
		measures.qualify_has_los = 1
		return measures

	@classmethod
	def by_will(cls, highest = 1):
		measures = cls()
		measures.measure_stat_save_willpower = 1
		measures.mult_stat_save_willpower = 1
		if (not highest): measures.mult_stat_save_willpower = -1
		measures.measure_has_los = 1
		measures.qualify_has_los = 1
		return measures

	@classmethod
	def by_has_los(cls):
		measures = cls()
		measures.measure_has_los = 1
		measures.qualify_has_los = 1
		return measures

	@classmethod
	def by_has_los_stay(cls):
		measures = cls()
		measures.measure_has_los = 1
		measures.qualify_has_los = 0
		return measures

	@classmethod
	def by_none(cls):
		measures = cls()
		return measures

	@classmethod
	def by_melee(cls):
		# unfinished
		measures = cls()
		measures.measure_has_los = 1
		measures.qualify_has_los = 0
		measures.measure_can_path = 1
		measures.measure_distance = 1
		measures.measure_range_is_within_melee = 1
		measures.qualify_range_is_within_melee = 1
		measures.measure_weapons = 1
		measures.measure_stat_hp = 1
		measures.measure_stat_ac = 1
		measures.measure_prone = 1
		return measures

def btoi(b):
	if (b): return 1
	return 0

class AITarget(object):
	def __init__(self, npc, target, measures):
		assert isinstance(npc, toee.PyObjHandle)
		assert isinstance(target, toee.PyObjHandle)
		assert isinstance(measures, AITargetMeasure)
		self.npc = npc
		self.target = target
		self.measures = copy.copy(measures)
		return

	def measure(self):
		self.measures.weight = 0
		#if (self.measures.measure_is_destroyed):
		#	self.measures.value_is_destroyed = self.target.object_flags_get() & toee.OF_DESTROYED
		#	self.measures.weight += self.measures.mult_is_destroyed * self.measures.value_is_destroyed

		if (self.measures.measure_stat_ac):
			self.measures.value_stat_ac = self.target.stat_level_get(toee.stat_ac)
			self.measures.weight += self.measures.mult_stat_ac * self.measures.value_stat_ac

		if (self.measures.measure_stat_hp):
			self.measures.value_stat_hp = self.target.stat_level_get(toee.stat_hp_current)
			self.measures.weight += self.measures.mult_stat_hp * self.measures.value_stat_hp
			self.measures.value_stat_hp_max = self.target.stat_level_get(toee.stat_hp_max)
			self.measures.weight += self.measures.mult_stat_hp_max * self.measures.value_stat_hp_max
			self.measures.value_stat_hp_percent = 0
			if (self.measures.value_stat_hp_max > 0 and self.measures.value_stat_hp):
				self.measures.value_stat_hp_percent = self.measures.value_stat_hp / self.measures.value_stat_hp
			self.measures.weight += self.measures.mult_stat_hp_percent * self.measures.value_stat_hp_percent

		if (self.measures.measure_stat_save_fortitude):
			self.measures.value_stat_save_fortitude = self.target.stat_level_get(toee.stat_save_fortitude)
			self.measures.weight += self.measures.mult_stat_save_fortitude * self.measures.value_stat_save_fortitude

		if (self.measures.measure_stat_save_reflexes):
			self.measures.value_stat_save_reflexes = self.target.stat_level_get(toee.stat_save_reflexes)
			self.measures.weight += self.measures.mult_stat_save_reflexes * self.measures.value_stat_save_reflexes

		if (self.measures.measure_stat_save_willpower):
			self.measures.value_stat_save_willpower = self.target.stat_level_get(toee.stat_save_willpower)
			self.measures.weight += self.measures.mult_stat_save_willpower * self.measures.value_stat_save_willpower

		if (self.measures.measure_has_los):
			self.measures.value_has_los = self.npc.has_los(self.target)
			self.measures.weight += self.measures.mult_has_los * self.measures.value_has_los

		dist_to_target = None
		value_reach = None
		if (self.measures.measure_range_is_within_melee or self.measures.measure_distance):
			dist_to_target = self.npc.distance_to(self.target)
			value_reach = 0.00 + self.npc.obj_get_int(toee.obj_f_critter_reach)
			if (value_reach < 0.01): value_reach = 5.0

			weapon_npc = self.target.item_worn_at(toee.item_wear_weapon_primary)
			if (not weapon_npc):
				weapon_npc = self.target.item_worn_at(toee.item_wear_weapon_secondary)
			if (weapon_npc):
				wt = weapon_npc.get_weapon_type()
				if (wt == toee.wt_glaive or wt == toee.wt_guisarme or wt == toee.wt_longspear or wt == toee.wt_ranseur or wt == toee.wt_spike_chain): 
					value_reach += 3.0

		if (self.measures.measure_distance):
			self.measures.value_distance = dist_to_target
			self.measures.weight += self.measures.mult_distance * self.measures.value_distance

		if (self.measures.measure_range_is_within_melee):
			self.measures.value_distance_to_target = dist_to_target
			self.measures.value_reach = value_reach
			self.measures.value_distance_over_reach = self.measures.value_distance_to_target - self.measures.value_reach
			self.measures.value_range_is_within_melee0 = btoi(self.measures.value_distance_over_reach <= 0)
			self.measures.value_range_is_within_melee = btoi(self.measures.value_distance_over_reach <= self.measures.option_distance_over_reach_allowed)
			self.measures.weight += self.measures.mult_range_is_within_melee * self.measures.value_range_is_within_melee

		if (self.measures.measure_can_path):
			self.measures.value_can_path = self.npc.can_find_path_to_obj(self.target, self.measures.option_can_path_flags)
			self.measures.weight += self.measures.mult_can_path * self.measures.value_can_path

		if (self.measures.measure_weapons):
			weapon = self.target.item_worn_at(toee.item_wear_weapon_primary)
			if (not weapon):
				weapon = self.target.item_worn_at(toee.item_wear_weapon_secondary)
			if (weapon):
				wt = weapon.get_weapon_type()
				self.measures.value_weapon_melee = toee.game.is_melee_weapon(wt)
				if (not self.measures.value_weapon_melee):
					self.measures.value_weapon_ranged = toee.game.is_ranged_weapon(wt)

		if (self.measures.measure_prone):
			self.measures.value_prone = self.target.d20_query(toee.EK_Q_Prone - toee.EK_Q_Helpless)
				
		return

	def __str__(self):
		s = "{}| weight({})=".format(self.target, self.measures.weight)
		frmt = "+ ({}: {}*{})"
		#if (self.measures.measure_is_destroyed):
		#	s += frmt.format("is_destroyed", self.measures.mult_is_destroyed, self.measures.value_is_destroyed)

		if (self.measures.measure_stat_ac):
			s += frmt.format("stat_ac", self.measures.mult_stat_ac, self.measures.value_stat_ac)

		if (self.measures.measure_stat_hp):
			s += frmt.format("stat_hp", self.measures.mult_stat_hp, self.measures.value_stat_hp)
			s += frmt.format("stat_hp_max", self.measures.mult_stat_hp_max, self.measures.value_stat_hp_max)
			s += frmt.format("stat_hp_percent", self.measures.mult_stat_hp_percent, self.measures.value_stat_hp_percent)

		if (self.measures.measure_stat_save_fortitude):
			s += frmt.format("stat_save_fortitude", self.measures.mult_stat_save_fortitude, self.measures.value_stat_save_fortitude)

		if (self.measures.measure_stat_save_reflexes):
			s += frmt.format("stat_save_fortitude", self.measures.mult_stat_save_fortitude, self.measures.value_stat_save_fortitude)

		if (self.measures.measure_stat_save_willpower):
			s += frmt.format("stat_save_willpower", self.measures.mult_stat_save_willpower, self.measures.value_stat_save_willpower)

		if (self.measures.measure_has_los):
			s += frmt.format("has_los", self.measures.mult_has_los, self.measures.value_has_los)
			if (self.measures.qualify_has_los): s += "!"

		if (self.measures.measure_distance):
			s += frmt.format("distance", self.measures.mult_distance, self.measures.value_distance)

		if (self.measures.measure_range_is_within_melee):
			s += "+ ({}: {}*{}, reach: {}, distance: {})".format("range_is_within_melee", self.measures.mult_range_is_within_melee, self.measures.value_range_is_within_melee, self.measures.value_reach, self.measures.value_distance_to_target)

		if (self.measures.measure_can_path):
			s += frmt.format("can_path", self.measures.mult_can_path, self.measures.value_can_path)

		if (self.measures.measure_weapons):
			s += " weapon_melee: {}, weapon_ranged: {}".format(self.measures.value_weapon_melee, self.measures.value_weapon_ranged)

		if (self.measures.measure_prone):
			s += " prone: {}".format(self.measures.value_prone)
		return s

	def qualify(self):
		#if (self.measures.measure_is_destroyed):
		#	if (self.measures.qualify_is_destroyed_not and self.measures.value_is_destroyed): return 0
		if (self.measures.measure_stat_hp):
			if (self.measures.qualify_stat_hp and not self.measures.value_stat_hp >= 0): return 0
		if (self.measures.measure_has_los):
			if (self.measures.qualify_has_los and not self.measures.value_has_los): return 0
		if (self.measures.measure_range_is_within_melee):
			if (self.measures.qualify_range_is_within_melee and not self.measures.value_range_is_within_melee): return 0
			
		return 1


def _AITargetList_cmp_default(m1, m2):
	assert isinstance(m1, AITarget)
	assert isinstance(m2, AITarget)
	return m2.measures.weight - m1.measures.weight

def _AITargetList_cmp_closest(m1, m2):
	assert isinstance(m1, AITarget)
	assert isinstance(m2, AITarget)
	return m2.measures.value_distance - m1.measures.value_distance
