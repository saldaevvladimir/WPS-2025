from django.db import models
import base64

class State(models.Model):
	id = models.AutoField(primary_key=True)
	date = models.DateField(auto_now=True)
	population_size = models.IntegerField(default=11)
	frame_with_boxes = models.BinaryField(default=b"123")

	def return_self(self):
		return {
			"id": self.id,
			"date": str(self.date),
			"population_size": self.population_size,
			"frame_with_boxes": base64.b64encode(self.frame_with_boxes).decode(),
		}