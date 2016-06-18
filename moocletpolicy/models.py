from django.db import models

# Prompt
class Mooclet(models.Model):
	# id
	name = models.CharField(max_length=100)
	#policy = models.ForeignKey(Policy)
	def __unicode__(self):
		return self.name


# Prompt version, e.g. "why did you take this course"
class Version(models.Model):
	# MOOClets
	mooclet = models.ForeignKey(Mooclet)
	name = models.CharField(max_length=100)
	text = models.CharField(max_length=1024, null=True, blank=True)

	def __unicode__(self):
		return self.name

# null=true allows null values 
# blank allows leaving fields blank when adding them e.g. via admin interface
class SubGroup(models.Model):
	var1 = models.IntegerField(null=True, blank=True)
	var2 = models.IntegerField(null=True, blank=True)
	var3 = models.IntegerField(null=True, blank=True)
	var4 = models.IntegerField(null=True, blank=True)
	var5 = models.IntegerField(null=True, blank=True)
	var6 = models.IntegerField(null=True, blank=True)
	var7 = models.IntegerField(null=True, blank=True)

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
#	policy = models.ForeignKey(Policy)

	def __unicode__(self):
		return str(self.id)
	

# 0.2
class VersionProbability(models.Model):
	version = models.ForeignKey(Version)
	subgroup_probability_array = models.ForeignKey(SubGroupProbabilityArray)
	probability = models.FloatField()

	def __unicode__(self):
		return str(self.id)


class Policy(models.Model):
	name = models.CharField(max_length=100) #e.g. "egreedy" or "sample_without_replacement"
	policy_function = models.CharField(max_length=100) #the name of the actual python function we run to assign a version based on this policy


class Student(models.Model):
	user_id = models.CharField(max_length=100, primary_key=True)

class UserVarNum(models.Model):
	student = models.ForeignKey(Student)
	label = models.CharField(max_length=100) #REASON
	value = models.FloatField(null=True, blank=True) #TODO: does this make sense?
	descriptor = models.CharField(max_length=250, null=True, blank=True)


class UserVarText(models.Model):
	student = models.ForeignKey(Student)
	label = models.CharField(max_length=100) #REASON
	value = models.CharField(null=True, blank=True, max_length=2000) 
	descriptor = models.CharField(max_length=250)

class UserVarMoocletVersion(models.Model):
	student = models.ForeignKey(Student)
	mooclet = mooclet = models.ForeignKey(Mooclet)
	version = models.ForeignKey(Version)
	policy = models.ForeignKey(Policy)


# class Record(models.Model):
# 	version = models.ForeignKey(Version)
# 	subgroup = models.ForeignKey(SubGroup)
# 	mooclet = models.ForeignKey(Mooclet)
# 	policy = models.ForeignKey(Policy)
#	student = models.ForeignKey(Student)
# 	reward = models.FloatField(null=True, blank=True)




# class CustomVariable(models.Model):
# 	name = model.integerField()

# class CustomVariableValue(models.Model):
# 	variable = model.ForeignKey(CustomVariable)
# 	value = model.FloatField()

#class Reward(models.Model):
