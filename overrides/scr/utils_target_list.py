import toee
import copy

class AITargetList(object):
	def __init__(self, npc, option_include_pc = 1, option_include_npc = 0, measures = None):
		assert isinstance(npc, toee.PyObjHandle)
		self.npc = npc
		self.option_include_pc = option_include_pc
		self.option_include_npc = option_include_npc
		self.list = list()
		self.measures = measures
		if (self.measures is None):
			self.measures = AITargetMeasure()
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
			for obj in toee.game.obj_list_range(npc.location, 60, toee.OLC_NPC):
				self.list.append(AITarget(self.npc, obj, self.measures))

		if (do_measure):
			self.measure()

		if (do_qualify):
			self.qualify()
		return self

	def measure(self):
		for target in self.list:
			assert isinstance(target, AITarget)
			target.measure()
		return self

	def qualify(self):
		new_list = list()
		for target in self.list:
			assert isinstance(target, AITarget)
			if (target.qualify()):
				new_list.append(target)
		self.list = new_list
		return self

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

		self.option_distance_over_reach_allowed = 0.0
		self.option_can_path_flags = 0

		#self.value_is_destroyed = 0
		self.value_stat_ac = 0
		self.value_stat_hp = 0
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
			if (self.measures.value_stat_hp_max > 0):
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
		return s

	def qualify(self):
		#if (self.measures.measure_is_destroyed):
		#	if (self.measures.qualify_is_destroyed_not and self.measures.value_is_destroyed): return 0
		if (self.measures.measure_has_los):
			if (self.measures.qualify_has_los and not self.measures.value_has_los): return 0
		return 1


def _AITargetList_cmp_default(m1, m2):
	assert isinstance(m1, AITarget)
	assert isinstance(m2, AITarget)
	return m2.measures.weight - m1.measures.weight
