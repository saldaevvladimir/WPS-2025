from django.db import models

class State(models.Model):
	id = models.AutoField(primary_key=True)
	date = models.DateField(auto_now=True)
	state1 = models.CharField(max_length=50)
	state2 = models.BooleanField()

	def return_self(self):
		return {
			"id": self.id,
			"date": str(self.date),
			"state1": self.state1,
			"state2": self.state2,
		}