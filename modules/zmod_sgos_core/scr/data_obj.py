from toee import PyObjHandle
import utils_storage

class DataObj(object):
	def __init__(self, attachee):
		assert isinstance(attachee, PyObjHandle)
		self.obj = attachee
		return

	@classmethod
	def get(cls, attachee):
		assert isinstance(attachee, PyObjHandle)
		data = utils_storage.obj_storage(attachee).data
		code = cls.get_code()
		o = None
		if (code in data):
			o = data[code]
		else:
			o = cls(attachee)
			data[code] = o
		return o

	@classmethod
	def get_code(cls):
		return cls.__name__

