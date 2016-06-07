from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.forms import formset_factory,inlineformset_factory, ModelForm
from django.http import HttpResponse, JsonResponse
import numpy as np

from .models import *



#get a mooclet version based on the mooclet & vars
#resuest is a GET with mooclet id, user_id, var1, var2, var3
def get_mooclet_version(request):
	"""
	
	"""
	#mooclet = Mooclet.objects.get(name=mooclet)

	policy = returnWeights(request.GET('mooclet'), request.GET('var1'), request.GET('var2'), request.GET('var3'))
	policy_array = []
	version_names = []
	for key in policy:
		version_names.append(key)
		policy_array.append(policy[key])

	mooclet_version = np.random.choice(version_names, p=policy_array)

	return JsonResponse({'version': mooclet_version})

def returnWeights(mooclet_id, var1, var2, var3):

	policy = {}

	subgroup = SubGroup.objects.first(var1=var1, var2=var2, var3=var3)
	subgroup_probability_array = SubGroupProbabilityArray.objects.get(mooclet_id, subgroup)

	# for each probability in the probability partition
	for version_probability in subgroup_probability_array.version_probability_set:
		# create dict entry that looks like {version_id: probability value}, e.g. {3: 0.5}
		policy[version_policy.version.name] = version_policy.probability

	return policy
