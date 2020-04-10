from toee import *
from debugg import *
import os
import sys
import json
from json import JSONEncoder
import utils_obj
import inspect
import imp

def obj_storage(obj):
	assert isinstance(obj, PyObjHandle)
	return Storage.getObjectStorage(obj)

def obj_storage_by_id(id):
	assert isinstance(obj, PyObjHandle)
	return Storage.getObjectStorageByName(id)

class ObjectStorage(object):
	def __init__(self, aname):
		self.name = aname
		self.data = dict()
		return

class MyEncoder(JSONEncoder):
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

	@property
	def objs(self):
		return type(self)._objs

	@objs.setter
	def objs(self, val):
		type(self)._objs = val
		return

	@staticmethod
	def getObjectStorage(obj):
		assert isinstance(obj, PyObjHandle)
		#breakp("obj.__getstate__({})".format(obj))
		name = utils_obj.obj_get_id(obj)
		#print(name)
		#breakp("getObjectStorage({})".format(obj))
		ss = Storage()
		oo = ss.objs
		#print(oo)
		#breakp("getObjectStorage oo = {}".format(oo))
		
		if (name in oo):
			return oo[name]
		objStorage = ObjectStorage(name)
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
		ss = Storage()
		oo = ss.objs
		oo.clear()
		files = os.listdir(dirname)
		loaded_modules = dict()
		for fileName in files:
			o = Storage.loadObjectStorage(dirname, fileName, loaded_modules)
			if (not (o is None)):
				oo[o.name] = o
		return

	@staticmethod
	def loadObjectStorage(dirname, fileName, loaded_modules):
		filePath = os.path.join(dirname, fileName)
		print("loadObjectStorage: filePath {}".format(filePath))
		#breakp("loadObjectStorage")
		try:
			f = open(filePath, "r")
			o = json.load(f)
			f.close()
			print("loadObjectStorage: json.load o = {}".format(o))
			#breakp("loadObjectStorage o")
			o = Storage.makeObjects(o, loaded_modules)
			ostorage = ObjectStorage(o["name"])
			ostorage.__dict__ = o
			return ostorage
		except Exception, e:
			print "Storage.loadObjectStorage error:", sys.exc_info()[0]
			print(str(e))
			f.close()
		breakp("loadObjectStorage end")
		return

	@staticmethod
	def makeObjects(odict, loaded_modules):
		#breakp("makeObjects 0")
		assert isinstance(odict, dict)
		r = dict()
		for k in odict.iterkeys():
			propval = odict[k]
			print("{}({}): {}".format(k, type(propval), propval))
			#breakp("makeObjects item")
			if (isinstance(propval, dict)):
				#breakp("makeObjects is dict")
				if ("_isofclass" in propval):
					isofclass = propval["_isofclass"]
					print(isofclass)
					#breakp("makeObjects isofclass")
					inst = object()
					inst_loaded = 0
					try:
						try:
							inst2 = eval(isofclass)()
							inst = inst2
							inst_loaded = 1
						except Exception, e:
							print "makeObjects inst eval error:", sys.exc_info()[0]
							print(str(e))
						if (not inst_loaded and "_isofmodule" in propval):
							isofmodule = propval["_isofmodule"]
							print(isofmodule)
							modlename = None
							if (isofmodule):
								modlename = os.path.basename(isofmodule)
								if (modlename): modlename = modlename.split('.')[0]
							print(modlename)
							#breakp("makeObjects isofmodule")
							if (modlename):
								isofmoduledir = os.path.join(os.getcwd(), "overrides", "scr")
								found = None
								md = None
								if (not loaded_modules is None and modlename in loaded_modules):
									md = loaded_modules[modlename]
								if (not md):
									try:
										try:
											found = imp.find_module(modlename)
										except Exception, e:
											print "imp.find_module(modlename) error1:", sys.exc_info()[0]
											print(str(e))
										if (not found):
											found = imp.find_module(modlename, isofmoduledir)
										if (found):
											print(found)
											fullname = modlename + "." + isofclass
											print(fullname)
											#breakp("makeObjects find_module")
											try:
												inst2 = eval(fullname)()
												inst = inst2
												inst_loaded = 1
											except Exception, e:
												print "makeObjects inst eval error:", sys.exc_info()[0]
												print(str(e))

											if (not inst_loaded):
												print("len of found: {}".format(len(found)))
												#breakp("makeObjects load_module")
												md = imp.load_module(modlename, found[0], found[1], found[2])
									except Exception, e:
										print "imp.find_module(modlename):", sys.exc_info()[0]
										print(str(e))
									if (not found):
										print("imp.load_source")
										print(isofmodule)
										#dir_path = os.path.dirname(os.path.realpath(__file__))
										#isofmodulefull = os.path.join(dir_path, modlename +".py")
										isofmodulefull = os.path.join(isofmoduledir, modlename +".py")
										print(isofmodulefull)
										#breakp("makeObjects load_source")
										#isofmodule = "D:\\Temple\\Temple of Elemental Evil\\overrides\\scr\\py06211_shuttered_monster.py" 
										md = imp.load_source(modlename, isofmodulefull)
								print(md)
								#breakp("makeObjects inst2")
								if (md):
									if (not loaded_modules is None and not modlename in loaded_modules):
										print("caching...: {} ({})".format(modlename, md))
										#breakp("loaded_modules[modlename] = md")
										loaded_modules[modlename] = md
										print("cached: {} ({})".format(modlename, md))
									c = getattr(md, isofclass)
									print(c)
									#breakp("makeObjects class")
									if (c):
										inst2 = c()
										if (inst2): 
											inst = inst2
											inst.__dict__ = Storage.makeObjects(propval, loaded_modules)
											inst_loaded = 1
					except Exception, e:
						print "!!!!!!!!!!!!! makeObjects error:", sys.exc_info()[0]
						print(str(e))
					if (inst_loaded == 0):
						inst.__dict__ = Storage.makeObjects(propval, loaded_modules)
					r[k] = inst
				else:
					r[k] = Storage.makeObjects(propval, loaded_modules)
			else: 
				r[k] = propval
		return r

def getIDfromObjHandle(objhandle):
	string = str(objhandle)
	print("getIDfromObjHandle: {} from {}".format(string, objhandle))
	ID = string.split("(")[1][:-1]
	return ID

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