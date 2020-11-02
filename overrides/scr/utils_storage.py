import toee, json, os, sys, inspect, imp, traceback, debug

def obj_storage(obj):
	assert isinstance(obj, toee.PyObjHandle)
	return Storage.getObjectStorage(obj)

def obj_storage_by_id(id):
	assert isinstance(obj, toee.PyObjHandle)
	return Storage.getObjectStorageByName(id)

class ObjectStorage(object):
	def __init__(self, aname):
		self.name = aname
		self.data = dict()
		self.origin = None
		return

	def get_data(self, name):
		if (name in self.data):
			return self.data[name]
		return None

	def storage_data_loaded_all(self):
		for o in self.data.itervalues():
			if ("storage_data_loaded_all" in dir(o)):
				o.storage_data_loaded_all()
		return

class MyEncoder(json.JSONEncoder):
	def default(self, o):
		o.__dict__["_isofclass"] = o.__class__.__name__
		#breakp("MyEncoder start")
		#print(o)
		m = inspect.getmodule(o.__class__)
		#print(m)
		if (m and hasattr(m, '__file__')):
			o.__dict__["_isofmodule"] = m.__file__
			#print(type(m.__file__))
			#print(m.__file__)
		#breakp("MyEncoder")
		return o.__dict__

class Storage(object):
	_objs = dict()

	@staticmethod
	def save(savegame):
		#breakp("Storage.save({})".format(savegame))
		try:
			saveDirBase = "modules\\ToEE\\save\\"
			saveDirName = "d" + savegame + "\\storage"
			saveDir = saveDirBase + saveDirName
			#print(saveDir)
			if (not os.path.exists(saveDir)):
				os.makedirs(saveDir)

			files = os.listdir(saveDir)
			for fileName in files:
				os.remove(os.path.join(saveDir, fileName))

			Storage.saveObjects(saveDir)
		except :
			print "Storage.save error:", sys.exc_info()[0]
		#breakp("Storage.save end({})".format(savegame))
		return

	@staticmethod
	def load(savegame):
		#breakp("Storage.load({})".format(savegame))
		saveDirBase = "modules\\ToEE\\save\\"
		saveDirName = "d" + savegame + "\\storage"
		saveDir = saveDirBase + saveDirName
		ss = Storage()
		oo = ss.objs
		oo.clear()
		if (os.path.exists(saveDir)):
			Storage.loadObjects(saveDir)
		return

	@staticmethod
	def reset():
		ss = Storage()
		oo = ss.objs
		oo.clear()
		return

	@property
	def objs(self):
		return type(self)._objs

	@objs.setter
	def objs(self, val):
		type(self)._objs = val
		return

	@staticmethod
	def getObjectStorage(obj):
		assert isinstance(obj, toee.PyObjHandle)
		#breakp("obj.__getstate__({})".format(obj))
		name = obj.id
		#print(name)
		#breakp("getObjectStorage({})".format(obj))
		ss = Storage()
		oo = ss.objs
		#print(oo)
		#breakp("getObjectStorage oo = {}".format(oo))
		
		if (name in oo):
			return oo[name]
		objStorage = ObjectStorage(name)
		objStorage.origin = obj.origin
		oo[name] = objStorage
		return objStorage

	@staticmethod
	def getObjectStorageByName(name):
		ss = Storage()
		oo = ss.objs
		if (name in oo):
			return oo[name]
		objStorage = ObjectStorage(name)
		oo[name] = objStorage
		return objStorage

	@staticmethod
	def saveObjects(dirname):
		#breakp("Storage.saveObjects({})".format(dirname))
		ss = Storage()
		oo = ss.objs
		#breakp("Storage.saveObjects oo = {}".format(oo))
		for n in oo.iterkeys():
			Storage.saveObjectStorage(dirname, n, oo[n])
		return

	@staticmethod
	def saveObjectStorage(dirname, n, v):
		if (v is None): return 0
		fileName = n + ".json"
		filePath = os.path.join(dirname, fileName)
		#print("saveObjectStorage: filePath {}".format(filePath))
		#breakp("saveObjectStorage")
		result = 1
		try:
			#print("saveObjectStorage: v {}".format(v))
			assert isinstance(v, ObjectStorage)
			if (v.name.startswith("G_")):
				npc = toee.game.get_obj_by_id(v.name)
				if (npc):
					v.origin = npc.origin
					print("set v.origin = {}, npc: {}".format(npc.origin, npc))

			dm = json.dumps(v, cls=MyEncoder, indent = 2)
			#dm = json.dumps(v.__dict__, indent = 2)
			#print("saveObjectStorage: json.dumps(v) {}".format(dm))
			f = open(filePath, "w")
			f.write(dm)
			f.close()
		except Exception, e:
			print "Storage.saveObjectStorage error:", sys.exc_info()[0]
			print(str(e))
			result = 0
		#breakp("saveObjectStorage end")
		return result

	@staticmethod
	def loadObjects(dirname):
		#breakp("Storage.loadObjects({})".format(dirname))
		try:
			ss = Storage()
			oo = ss.objs
			assert isinstance(oo, dict)
			oo.clear()
			files = os.listdir(dirname)
			mod_cache = dict()
			local_objects = list()
			for fileName in files:
				o = Storage.loadObjectStorage(dirname, fileName, mod_cache)
				if (not (o is None)):
					oo[o.name] = o
					local_objects.append(o)

			for o in local_objects:
				if ("storage_data_loaded_all" in dir(o)):
					o.storage_data_loaded_all()
		except Exception, e:
			print "!!!!!!!!!!!!! loadObjects error:"
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60		
			debug.breakp("error")
		return

	@staticmethod
	def loadObjectStorage(dirname, fileName, mod_cache):
		filePath = os.path.join(dirname, fileName)
		#print("loadObjectStorage: filePath {}".format(filePath))
		#breakp("loadObjectStorage")
		try:
			f = open(filePath, "r")
			o = json.load(f)
			f.close()
			#print("loadObjectStorage: json.load o = {}".format(o))
			#breakp("loadObjectStorage o")
			#o = Storage.makeObjects(o, loaded_modules)
			o = Storage.make_data(o, None, mod_cache)
			name = o["name"]
			ostorage = ObjectStorage(name)
			if (not "origin" in o):
				o["origin"] = None
			ostorage.__dict__ = o
			if (not name):
				print("ostorage no name!")
				debug.breakp("ostorage no name!")
				return None
			return ostorage
		except Exception, e:
			print "loadObjectStorage error:"
			print '-'*60
			f.close()
			traceback.print_exc(file=sys.stdout)
			print '-'*60		
			debug.breakp("error")
		return

	@staticmethod
	def make_data(odict, parent, mod_cache):
		assert isinstance(odict, dict)
		result = dict()
		#print("make_data start {}".format(odict))
		has_member_check = 0
		if (parent and "storage_skip_load" in dir(parent)):
			has_member_check = 1

		for key in odict.iterkeys():
			propval = odict[key]
			#print("make_data {} \ {} : {}".format(key, type(propval).__name__, propval))
			if (has_member_check and parent.storage_skip_load(key, propval)): 
				result[key] = None
				continue

			if (isinstance(propval, dict)):
				result[key] = Storage.make_instance_from_dic(propval, mod_cache)
			elif (isinstance(propval, list)):
				result[key] = Storage.make_list(propval, mod_cache)
			else:
				result[key] = propval
		return result

	@staticmethod
	def make_list(olist, mod_cache):
		assert isinstance(olist, list)
		result = list()
		#print("make_list start {}".format(olist))
		for propval in olist:
			#print("make_list {} : {}".format(type(propval).__name__, propval))
			if (isinstance(propval, dict)):
				result.append(Storage.make_instance_from_dic(propval, mod_cache))
			elif (isinstance(propval, list)):
				result.append(Storage.make_list(propval, mod_cache))
			else:
				result.append(propval)
		return result

	@staticmethod
	def make_instance_from_dic(propval, mod_cache):
		mod_class = None
		try:
			assert isinstance(propval, dict)

			#print("Contents of propval: ".format(propval))
			#for key in propval.iterkeys():
			#	print("{} : {}".format(key, propval[key]))

			isofclass = None
			if ("_isofclass" in propval):
				isofclass = propval[u'_isofclass']
			isofmodule = None
			if ("_isofmodule" in propval):
				isofmodule = propval[u'_isofmodule']

			#print("make_instance_from_dic isofclass: {}, isofmodule: {}".format(isofclass, isofmodule))
			if (not isofclass): 
				return Storage.make_data(propval, None, mod_cache)

			result = None
			if (isofmodule is None):
				result = instantinate_by_eval(isofclass)
			else:
				mod_name = os.path.basename(isofmodule).split('.')[0]
				if (not (mod_cache and isofmodule in mod_cache)):
					mod_path = os.path.join(os.getcwd(), "overrides", "scr", mod_name +".py")
					#mod_object = imp.load_source(mod_name, mod_path)
					mod_object = __import__(mod_name)
					mod_cache[isofmodule] = mod_object
				else:
					mod_object = mod_cache[isofmodule]

				mod_class = getattr(mod_object, isofclass)
				result = mod_class()
				#print("make_instance_from_dic result: {}, mod_class: {}, mod_object: {}".format(result, mod_class, mod_object))

			sub_data = Storage.make_data(propval, result, mod_cache)
			result.__dict__ = sub_data
			if ("storage_data_loaded" in dir(result)):
				result.storage_data_loaded()
		except Exception, e:
			print "!!!!!!!!!!!!! make_instance_from_dic error:"
			print '-'*60
			print("mod_class: {}, isofclass: {}, mod_object: {}, ".format(mod_class, isofclass, mod_object))
			traceback.print_exc(file=sys.stdout)
			print '-'*60		
			debug.breakp("error")
		return result

	@staticmethod
	def instantinate_by_eval(isofclass):
		result = None
		try:
			result = eval(isofclass)()
		except Exception, e:
			#print "makeObjects inst eval error:", sys.exc_info()[0]
			#print(str(e))
			pass
		return result

def get_subclass(module, base_class):
	for name in dir(module):
		obj = getattr(module, name)
		try:
			if issubclass(obj, base_class):
				return obj
		except TypeError:  # If 'obj' is not a class
			print("get_subclass error ({}, {}): {}".format(module, base_class, sys.exc_info()[0]))
			pass
	return None