from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.forms import formset_factory,inlineformset_factory, ModelForm
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import *
import json
import numpy as np
import random

from .models import *



#get a mooclet version based on the mooclet & vars
#request is a GET with mooclet id, user_id, var1, var2, var3
def get_mooclet_version(request):
	#make sure essential vars are in request
	if 'mooclet' not in request.GET:
		return HttpResponse('mooclet not found in GET parameters')
	if 'var1' not in request.GET:
		return HttpResponse('var1 not found in GET parameters')
	if 'var2' not in request.GET:
		return HttpResponse('var2 not found in GET parameters')
	if 'var3' not in request.GET:
		return HttpResponse('var3 not found in GET parameters')

	#get the policy based on user vars
	policy,version_names = returnWeights(request.GET['mooclet'], request.GET['var1'], request.GET['var2'], request.GET['var3'])
	
	#choose version where version_names = [version1, version2, ...]
	#and policy_array is [probability_version1, probability_version2, ...]
	mooclet_version = np.random.choice(version_names, p=policy)

	return JsonResponse({'version': mooclet_version, 'wentwrong': '0'})

def get_mooclet_version_without_replacement_policy(request):
	"""
	look up what conditions past users have been in
	if any past version has 
	"""
	#stub for multiple policies
	if 'policy' not in request.GET:
		policy = Policy.objects.get_or_create(name="sample_without_replacement")
	else:
		policy = Policy.objects.get_or_create(name=request.GET['policy'])

	student, created = Student.objects.get_or_create(user_id=request.GET['user_id'])
	
	#get the user vars and update them
	user_variables = request.GET.copy().dict()
	#assume all vars other than user id and mooclet are user vars
	del user_variables['user_id']
	del user_variables['mooclet']
	#attempt to coerce strings to floats
	for key in user_variables:
		try:
			user_variables[key] = float(user_variables[key])
		except ValueError:
			pass
	if user_variables['father_ed'] == 13.0 or user_variables['father_ed'] == 17.0 :
		user_variables['father_ed'] = user_variables['father_ed'] * -1.0

	if user_variables['mother_ed'] == 13.0 or user_variables['mother_ed'] == 17.0 :
		user_variables['mother_ed'] = user_variables['mother_ed'] * -1.0
	

	max_ed = max(user_variables['father_ed'], user_variables['mother_ed'])
	user_variables['max_education'] = max_ed


	#store ALL user vars, but delete ones we're uninterested in from dict
	json_user_vars = json.dumps(user_variables)
	update_student_vars(request.GET['user_id'], json_user_vars)
	del user_variables['father_ed']
	del user_variables['mother_ed']

	


	mooclet = Mooclet.objects.get(name=request.GET['mooclet'])
	mooclet_version_assigned_name = ''

	if (not created) and UserVarMoocletVersion.objects.filter(student=student, mooclet=mooclet).exists():
		#we've logged this user in the past and they have a mooclet
		#they have already been assigned to a version
		mooclet_version_assigned_name = UserVarMoocletVersion.objects.get(student=student, mooclet=mooclet).version.name
	else:
		mooclet_version_assigned, mooclet_version_assigned_name = get_version_without_replacement(student, mooclet, policy, user_variables)


	return JsonResponse({'version': mooclet_version_assigned_name, 'wentwrong': '0'})
	

def get_precourse_intervention(request):


	if 'policy' not in request.GET:
		policy = Policy.objects.get_or_create(name="sample_without_replacement")
	else:
		policy = Policy.objects.get_or_create(name=request.GET['policy'])

	mooclet = Mooclet.objects.get(name=request.GET['mooclet'])


	student = Student.objects.create()

	user_variables = request.GET.copy().dict()
	#assume all vars other than user id and mooclet are user vars

	del user_variables['mooclet']
	for key in user_variables:
		#coerce variable values to float. if a var can't be coerced, set it to None
		try:
			user_variables[key] = float(user_variables[key])
		except ValueError:
			user_variables[key] = None

	#check if it = None, then assign to bucket
	if user_variables['intent_assess']:
		if user_variables['intent_assess'] > 2:
			user_variables['intent_assess'] = 1.0
		else: 
			user_variables['intent_assess'] = 0.0
	else:
		user_variables['intent_assess'] = 0.0


	if user_variables['hours']:
		if user_variables['hours'] >= 6:
			user_variables['hours'] = 1.0
		else: 
			user_variables['hours'] = 0.0
	else:
		user_variables['hours'] = 0.0

	if user_variables['courses_completed']:
		if user_variables['courses_completed'] >= 4:
			user_variables['courses_completed'] = 2.0
		elif user_variables['courses_completed'] >= 1 and user_variables['courses_completed'] <= 3:
			user_variables['courses_completed'] = 1.0
		else: 
			user_variables['courses_completed'] = 0.0
	else:
		user_variables['courses_completed'] = 0.0

	#education is reverse coded: 1 = phd, 10 = none
	if user_variables['education']:
		#phd, ma, professions
		if user_variables['education'] >= 1 and user_variables['education'] <= 3:
			user_variables['education'] = 2.0
		#bachelors
		elif user_variables['education'] == 4:
			user_variables['education'] = 1.0
		#bachelors or below
		else: 
			user_variables['education'] = 0.0
	else:
		user_variables['education'] = 0.0

	json_user_vars = json.dumps(user_variables)
	update_student_vars(student, json_user_vars)

	#of the form belonging0plans0
	mooclet_version_assigned, mooclet_version_assigned_name = get_version_without_replacement(student, mooclet, policy, user_variables)
	mooclet_version_values = mooclet_version_assigned.moocletversionvalue_set.all()
	belonging = mooclet_version_values.filter(name='belonging').first()
	plan = mooclet_version_values.filter(name='plans').first()
	assigned_versions = {
		'belongingassigned':belonging.value,
		'planassigned':plan.value,
		'webservice_call_complete_server': 1,
	}
	return JsonResponse(assigned_versions)
	#return JsonResponse({'version': mooclet_version_assigned.name, 'wentwrong': '0'})




def get_version_without_replacement(student, mooclet, policy, user_variables={}):


	mooclet_versions = Version.objects.filter(mooclet=mooclet).order_by('name')
	mooclet_version_assigned = None
	mooclet_version_assigned_name = ''


	#the user is new or has not been assigned to this mooclet, so we definitely need to assign them
	version_assignments = {}
	#count the previous assignments
	for version in mooclet_versions:
		#get all previously recorded user variables that match the current vars
		#assumes we only care about numbers for now
		stratum = UserVarNum.objects.filter(label__in=user_variables.keys())
		#get only those instances whose values match the current user
		stratum  = stratum.filter(value__in=[val for val in user_variables.values() if type(val) is float])
		#print stratum.count()
		#get the users. values('student_id') b/c it is the primary key (id) of the student model
		stratum_users = Student.objects.filter(pk__in=stratum.values('student_id'))
		#print stratum_users.count()
		previous_assignments = UserVarMoocletVersion.objects.filter(mooclet=mooclet, version=version, student__in=stratum_users).count()
		version_assignments[version.name] = previous_assignments
	print version_assignments
	highest = max(version_assignments.values())
	versions_with_max = [k for k,v in version_assignments.items() if v == highest]
	if len(versions_with_max) == len(mooclet_versions):
		#all versions are equal; select randomly
		rand_version = random.randrange(len(mooclet_versions))
		mooclet_version_assigned = mooclet_versions[rand_version]
		mooclet_version_assigned_name = mooclet_version_assigned.name
	else:
		#remove all max from the list
		for max_version in versions_with_max:
			del version_assignments[max_version]
		#select from remainder
		#print version_assignments
		version_name = random.choice(version_assignments.keys())
		mooclet_version_assigned = mooclet_versions.get(name=version_name)
		mooclet_version_assigned_name = mooclet_version_assigned.name
	selected = UserVarMoocletVersion.objects.create(student=student, mooclet=mooclet, version=mooclet_version_assigned, policy=policy[0])

	return mooclet_version_assigned, mooclet_version_assigned_name

	pass

def get_mooclet_version_from_policy(request, policy_name):
	#if policy_name = "egreedy"
	#elif policy_name = "sample_without_replacement"
	pass

def returnWeights(mooclet_id, var1, var2, var3):
	#change this to subgroup probabilites
	policy = []
	version_names = []

	subgroup = SubGroup.objects.filter(var1=var1, var2=var2, var3=var3)[0]
	subgroup_probability_array = SubGroupProbabilityArray.objects.get(mooclet=mooclet_id, subgroup=subgroup)

	# for each probability in the probability partition
	for version_probability in subgroup_probability_array.versionprobability_set.all():
		# add the version name and probability to respective lists
		version_names.append(version_probability.version.name)
		policy.append(version_probability.probability)

	return policy,version_names

def accept_version_request(request):
	"""
	create user in database and add init vars
	"""
	pass

def policy1(student_id, mooclet_id):
	pass

#where vars is a JSON object
def update_student_vars(student_id, vars):
	student = student_id #Student.objects.get(student_id)
	dict_types = '' 
	student_vars = json.loads(vars)
	for label, value in student_vars.iteritems():
		if type(value) is str or type(value) is unicode:
			student_var, student_var_created = UserVarText.objects.update_or_create(student=student, label=label, value=value)
		elif type(value) is int or type(value) is float:
			if type(value) is int:
				value = float(value)
			student_var, student_var_created = UserVarNum.objects.update_or_create(student=student, label=label, value=value)


def test_update_vars(request):
	update_student_vars("test1", '{"reason": 1, "moocs": 5, "exp_text": "this is good"}')
	return HttpResponse(success)


def create_weights(mooclet_id, reason_subgroups=[1,2,3], nummoocssubgroups=[0,1,2], educationsubgroups=[1,2,3], weights=[0.33,0.33,0.34]):
	mooclet = Mooclet.objects.get(name=mooclet_id)
	mooclet_versions = Version.objects.filter(mooclet=mooclet).order_by('name')
	#create the subgroups
	#start with all null
	subgroup = SubGroup.objects.get_or_create(var1=None, var2=None, var3=None)
	subgroup_probability_array = SubGroupProbabilityArray.objects.get_or_create(mooclet=mooclet, subgroup=subgroup[0])
	for version, weight in zip(mooclet_versions, weights):
		version_probability = VersionProbability.objects.update_or_create(version=version, subgroup_probability_array=subgroup_probability_array[0], probability=weight)

	#iterate through variable values (including null)
	for reason in range(len(reason_subgroups)):
		#reason, null, null
		subgroup = SubGroup.objects.get_or_create(var1=reason_subgroups[reason], var2=None, var3=None)
		subgroup_probability_array = SubGroupProbabilityArray.objects.get_or_create(mooclet=mooclet, subgroup=subgroup[0])
		for version, weight in zip(mooclet_versions, weights):
			version_probability = VersionProbability.objects.update_or_create(version=version, subgroup_probability_array=subgroup_probability_array[0], probability=weight)

		for nummoocs in range(len(nummoocssubgroups)):
			#null, nummooocs, null
			subgroup = SubGroup.objects.get_or_create(var1=None, var2=nummoocssubgroups[nummoocs], var3=None)
			subgroup_probability_array = SubGroupProbabilityArray.objects.get_or_create(mooclet=mooclet, subgroup=subgroup[0])
			for version, weight in zip(mooclet_versions, weights):
				version_probability = VersionProbability.objects.update_or_create(version=version, subgroup_probability_array=subgroup_probability_array[0], probability=weight)
			subgroup = SubGroup.objects.get_or_create(var1=reason_subgroups[reason], var2=nummoocssubgroups[nummoocs], var3=None)
			subgroup_probability_array = SubGroupProbabilityArray.objects.get_or_create(mooclet=mooclet, subgroup=subgroup[0])
			for version, weight in zip(mooclet_versions, weights):
				version_probability = VersionProbability.objects.update_or_create(version=version, subgroup_probability_array=subgroup_probability_array[0], probability=weight)
			for education in range(len(educationsubgroups)):
				#null, null, education
				subgroup = SubGroup.objects.get_or_create(var1=None, var2=None, var3=educationsubgroups[education])
				subgroup_probability_array = SubGroupProbabilityArray.objects.get_or_create(mooclet=mooclet, subgroup=subgroup[0])
				for version, weight in zip(mooclet_versions, weights):
					version_probability = VersionProbability.objects.update_or_create(version=version, subgroup_probability_array=subgroup_probability_array[0], probability=weight)
				subgroup = SubGroup.objects.get_or_create(var1=reason_subgroups[reason], var2=None, var3=educationsubgroups[education])
				subgroup_probability_array = SubGroupProbabilityArray.objects.get_or_create(mooclet=mooclet, subgroup=subgroup[0])
				for version, weight in zip(mooclet_versions, weights):
					version_probability = VersionProbability.objects.update_or_create(version=version, subgroup_probability_array=subgroup_probability_array[0], probability=weight)
				subgroup = SubGroup.objects.get_or_create(var1=None, var2=nummoocssubgroups[nummoocs], var3=educationsubgroups[education])
				subgroup_probability_array = SubGroupProbabilityArray.objects.get_or_create(mooclet=mooclet, subgroup=subgroup[0])
				for version, weight in zip(mooclet_versions, weights):
					version_probability = VersionProbability.objects.update_or_create(version=version, subgroup_probability_array=subgroup_probability_array[0], probability=weight)
				subgroup = SubGroup.objects.get_or_create(var1=reason_subgroups[reason], var2=nummoocssubgroups[nummoocs], var3=educationsubgroups[education])
				subgroup_probability_array = SubGroupProbabilityArray.objects.get_or_create(mooclet=mooclet, subgroup=subgroup[0])
				for version, weight in zip(mooclet_versions, weights):
					version_probability = VersionProbability.objects.update_or_create(version=version, subgroup_probability_array=subgroup_probability_array[0], probability=weight)

def test_create_weightset(request):
	create_weights("Mooclet1", reason_subgroups=[1,2,3], nummoocssubgroups=[0,1,2], educationsubgroups=[1,2,3], weights=[0.30,0.36,0.34])