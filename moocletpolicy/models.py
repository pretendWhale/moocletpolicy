from django.db import models

# Prompt
class Mooclet(models.Model):
	# id
	name = models.CharField(max_length=100)


# Prompt version, e.g. "why did you take this course"
class Version(models.Model):
	# MOOClets
	mooclet = models.ForeignKey(Mooclet)
	name = models.CharField(max_length=100)

class SubGroup(models.Model):
	var1 = models.IntegerField()
	var2 = models.IntegerField()
	var3 = models.IntegerField()
	var4 = models.IntegerField()
	var5 = models.IntegerField()
	var6 = models.IntegerField()

# [0.2, 0.3, 0.5]
class SubGroupProbabilityArray(models.Model):
	mooclet = models.ForeignKey(Mooclet)
	subgroup = models.ForeignKey(SubGroup)
	

# 0.2
class VersionProbability(models.Model):
	version = models.ForeignKey(Version)
	subgroup_probability_array = models.ForeignKey(SubGroupProbabilityArray)
	probability = models.FloatField()





# class CustomVariable(models.Model):
# 	name = model.integerField()

# class CustomVariableValue(models.Model):
# 	variable = model.ForeignKey(CustomVariable)
# 	value = model.FloatField()
