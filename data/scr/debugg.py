# This module is specifically to address missing breakp() function from TemplePlus
import debug

def breakp(v):
	""" Debug option for TemplePlus.
	Keyword arguments:
	v --- string or None (default None)
	"""
	if ("breakp" in dir(debug)):
		debug.breakp(v)
	return
