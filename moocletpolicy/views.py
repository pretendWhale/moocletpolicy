from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.forms import formset_factory,inlineformset_factory, ModelForm
from django.http import HttpResponse, JsonResponse
import numpy as np

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

def get_mooclet_version_without_replacement(request):
	"""
	look up what conditions past users have been in
	if any past version has 
	"""
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
