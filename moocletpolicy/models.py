from django.db import models

# Prompt
class Mooclet(models.Model):
	# id
	name = models.CharField(max_length=100)


# Prompt version, e.g. "why did you take this course"
class Version(models.Model):
	# MOOClets
	mooclet = models.ForeignKey(Mooclet)


# [0.2, 0.3, 0.5]
class SubGroupProbabilityArray(models.Model):
	mooclet = models.ForeignKey(Mooclet)
	subgroup = models.ForeignKey(SubGroup)
	

# 0.2
class VersionProbability(models.Model):
	version = models.ForeignKey(Version)
	subgroup_probability_array = models.ForeignKey(SubGroupProbabilityArray)
	probability = models.FloatField()


class SubGroup(models.Model):
	var1 = model.integerField()
	var2 = model.integerField()
	var3 = model.integerField()
	var4 = model.integerField()
	var5 = model.integerField()
	var6 = model.integerField()


# class CustomVariable(models.Model):
# 	name = model.integerField()

# class CustomVariableValue(models.Model):
# 	variable = model.ForeignKey(CustomVariable)
# 	value = model.FloatField()
