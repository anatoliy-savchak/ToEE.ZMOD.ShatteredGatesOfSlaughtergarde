import ConfigParser

class CormyrConfig(object):
	_cfg = None
	@property
	def cfg(self):
		if (not type(self)._cfg):
			c = ConfigParser.SafeConfigParser(allow_no_value=True)
			type(self)._cfg = c
			with open("modules\\ToEE\\rules\\cormyr.cfg", "r") as cfgfile:
				c.readfp(cfgfile)
			print(c)
		return type(self)._cfg

	@cfg.setter
	def cfg(self, val):
		type(self)._cfg = val
		return

def cormyr_get_option(section, option):
	cc = CormyrConfig()
	c = cc.cfg
	if (not c): 
		return None
	assert isinstance(c, ConfigParser.SafeConfigParser)
	r = c.get(section, option)
	print("cormyr_get_option({}, {}) = {}".format(section, option, r))
	return r
