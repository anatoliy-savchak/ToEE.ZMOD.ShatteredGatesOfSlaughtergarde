# This module is specifically to address missing breakp() function from TemplePlus
import debug
import json

def breakp(v):
	""" Debug option for TemplePlus.
	Keyword arguments:
	v --- string or None (default None)
	"""
	if ("breakp" in dir(debug)):
		debug.breakp(v)
	return

def debug_save_conds(file_name):
	f = open(file_name, "w")
	o = debug.dump_conds()
	dm = json.dumps(o, indent = 2)
	f.write(dm)
	f.close()
	return