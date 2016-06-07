from django.db import models

# Prompt
class Mooclet(models.Model):
	# id
	name = models.CharField(max_length=100)
	def __unicode__(self):
		return self.name


# Prompt version, e.g. "why did you take this course"
class Version(models.Model):
	# MOOClets
	mooclet = models.ForeignKey(Mooclet)
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class SubGroup(models.Model):
	var1 = models.IntegerField(null=True)
	var2 = models.IntegerField(null=True)
	var3 = models.IntegerField(null=True)
	var4 = models.IntegerField(null=True)
	var5 = models.IntegerField(null=True)
	var6 = models.IntegerField(null=True)
	var7 = models.IntegerField(null=True)

	def __unicode__(self):
		field_names = self._meta.get_all_field_names()
		#this is bad, change this.
		val_str = '%s:%s|%s:%s|%s:%s|%s:%s|%s:%s|%s:%s|%s:%s' % (field_names[0], 
			self.var1,field_names[1], self.var2,field_names[2], self.var3,field_names[3], self.var4,field_names[4], self.var5,
			field_names[5], self.var6,field_names[6], self.var7,)

		return val_str
		#return str(self.id)

# [0.2, 0.3, 0.5]
class SubGroupProbabilityArray(models.Model):
	mooclet = models.ForeignKey(Mooclet)
	subgroup = models.ForeignKey(SubGroup)

	def __unicode__(self):
		return str(self.id)
	

# 0.2
class VersionProbability(models.Model):
	version = models.ForeignKey(Version)
	subgroup_probability_array = models.ForeignKey(SubGroupProbabilityArray)
	probability = models.FloatField()

	def __unicode__(self):
		return str(self.id)





# class CustomVariable(models.Model):
# 	name = model.integerField()

# class CustomVariableValue(models.Model):
# 	variable = model.ForeignKey(CustomVariable)
# 	value = model.FloatField()
