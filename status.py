






class Status:
	""" maintain status of function calls throughout the user's request """
	

	def __init__(self):
		self.success = True			# true if success
		self.description = ''

	def setSuccess(self, success):
		self.success = success

	def setDescription(self, description):
		self.description = description

	def success(self):
		return self.success

	def description(self):
		return self.description

	def toDict(self):
		return {
			'description': self.description,
			'success': self.success
		}