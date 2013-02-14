from django.db import models 

# Create your models here.
class Users(models.Model):
	name = models.CharField(max_length=128, primary_key=True, blank=False)
	password = models.CharField(max_length=128)
	count = models.IntegerField()
	def __unicode__(self):
		return str((self.name, self.password, self.count))
