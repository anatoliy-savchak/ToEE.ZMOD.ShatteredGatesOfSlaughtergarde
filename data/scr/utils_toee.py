from toee import *
from math import sqrt, atan2
import _include
from co8Util.PersistentData import *
import os

#########################################
# Persistent flags/vars/strs		#
# Uses keys starting with		#
# 'Flaggg', 'Varrr', 'Stringgg' 	#
#########################################

def get_f(flagkey):
	flagkey_stringized = 'Flaggg' + str(flagkey)
	tempp = Co8PersistentData.getData(flagkey_stringized)
	if isNone(tempp):
		return 0
	else:
		return int(tempp) != 0

def set_f(flagkey, new_value = 1):
	flagkey_stringized = 'Flaggg' + str(flagkey)
	Co8PersistentData.setData(flagkey_stringized, new_value)

def get_v(varkey):
	varkey_stringized = 'Varrr' + str(varkey)
	tempp = Co8PersistentData.getData(varkey_stringized)
	if isNone(tempp):
		return 0
	else:
		return int(tempp)

def set_v(varkey, new_value):
	varkey_stringized = 'Varrr' + str(varkey)
	Co8PersistentData.setData(varkey_stringized, new_value)
	return get_v(varkey)

def inc_v(varkey, inc_amount = 1):
	varkey_stringized = 'Varrr' + str(varkey)
	Co8PersistentData.setData(varkey_stringized, get_v(varkey) + inc_amount)
	return get_v(varkey)

def get_s(strkey):
	strkey_stringized = 'Stringgg' + str(strkey)
	tempp = Co8PersistentData.getData(strkey_stringized)
	if isNone(tempp):
		return ''
	else:
		return str(tempp)

def set_s(strkey, new_value):
	new_value_stringized = str(new_value)
	strkey_stringized = 'Stringgg' + str(strkey)
	Co8PersistentData.setData(strkey_stringized, new_value_stringized)


#########################################
# Bitwise NPC internal flags			#
# 1-31									#
# Uses obj_f_npc_pad_i_4			 	#
# obj_f_pad_i_3 is sometimes nonzero    #
# pad_i_4, pad_i_5 tested clean on all  #
# protos								#
#########################################

def npc_set(attachee,flagno):
	# flagno is assumed to be from 1 to 31
	exponent = flagno - 1
	if exponent > 30 or exponent < 0:
		print('error!')
	else:
		abc = pow(2,exponent)
	tempp = attachee.obj_get_int(obj_f_npc_pad_i_4) | abc
	attachee.obj_set_int(obj_f_npc_pad_i_4, tempp)
	return	

def npc_unset(attachee,flagno):
	# flagno is assumed to be from 1 to 31
	exponent = flagno - 1
	if exponent > 30 or exponent < 0:
		print ('error!')
	else:
		abc = pow(2,exponent)
	tempp = (attachee.obj_get_int(obj_f_npc_pad_i_4) | abc) - abc
	attachee.obj_set_int(obj_f_npc_pad_i_4, tempp)
	return	

def npc_get(attachee,flagno):
	# flagno is assumed to be from 1 to 31
	exponent = flagno - 1
	if exponent > 30 or exponent < 0:
		print ('error!')
	else:
		abc = pow(2,exponent)
	return attachee.obj_get_int(obj_f_npc_pad_i_4) & abc != 0

def readMes(mesfile):
	""" Read the mesfile into a dictionary indexed by line number. """
	mesFile = file(mesfile,'r')
	mesDict = {}
	for line in mesFile.readlines():
		# Remove whitespace.
		line = line.strip()
		# Ignore empty lines.
		if not line:
			continue
		# Ignore comment lines.
		if line[0] != '{':
			continue
		# Decode the line.  Just standard python string processing.
		line = line.split('}')[:-1]
		for i in range(len(line)):
			line[i] = line[i].strip()
			line[i] = line[i][1:]
		contents = line[1:]
		# Insert the line into the mesDict.
		mesDict[int(line[0])] = contents
	mesFile.close()
	# print 'File read'
	return mesDict

def supports_custom_name():
	if (hasattr(game, 'make_custom_name') and callable(getattr(game, 'make_custom_name'))):
		return 1
	return 0

def make_custom_name(new_name):
	if supports_custom_name():
		return game.make_custom_name(new_name)
	return -1

def readMesLine(mesfile, lineId):
	result = ""
	mesFile = file(mesfile,'r')
	for line in mesFile.readlines():
		# Remove whitespace.
		line = line.strip()
		# Ignore empty lines.
		if not line:
			continue
		if line[0] != '{':
			continue
		line = line.split('}')[:-1]
		if (len(line) < 2): continue
		s = unicode(line[0][1:])
		if (not s.isnumeric()): continue
		if (int(line[0][1:]) == lineId): 
			result = line[1][1:]
			break
	mesFile.close()
	return result

def find_dialog_file_name(scriptId):
	files = os.listdir("data\\dlg")
	starts = "{:0>5d}".format(scriptId)
	for fileName in files:
		if (starts in fileName): return fileName
	return None