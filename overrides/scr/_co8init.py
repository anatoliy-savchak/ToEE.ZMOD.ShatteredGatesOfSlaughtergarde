##DLL calls these functions to enable the persistent data scheme - Spellslinger
import _include
from co8Util.Logger import Logger
from co8Util.PersistentData import Co8PersistentData
from utils_storage import Storage
#from utils_storage import storage_load, storage_save

def save(savename):
	Storage.save(savename)
	print "Executing Co8 Save Hook"
	Co8PersistentData.save(savename)

def load(savename):
	Storage.load(savename)
	Co8PersistentData.load(savename)

def init():
	pass
