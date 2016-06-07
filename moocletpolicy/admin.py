from django.contrib import admin
from django.apps import apps
from .models import *



app = apps.get_app_config('moocletpolicy')

class MoocletAdmin (admin.ModelAdmin):
	list_display = ['id','name']

class VersionAdmin (admin.ModelAdmin):
	list_display = ['id', 'mooclet__id', 'name']
	list_filter = ('mooclet__id')

	def get_mooclet_id(self,obj):
		return obj.mooclet.id

class SubGroupAdmin (admin.ModelAdmin):
	list_display = ['id', 'var1', 'var2', 'var3', 'var4', 'var5', 'var6', 'var7']

class SubGroupProbabilityArrayAdmin (admin.ModelAdmin):
	list_display = ['id', 'mooclet', 'subgroup']

class VersionProbabilityAdmin (admin.ModelAdmin):
	list_display = ['id', 'version__mooclet__id', 'version__name', 'subgroup_probability_array__id', 'probability']
	list_filter = ('version__mooclet__id', 'version__name', 'subgroup_probability_array__id')

	def get_version_name(self,obj):
		return obj.version.name

	def get_mooclet_id(self,obj):
		return obj.version.mooclet.id

	def get_subgroup_probability_array_id(self,obj):
		return obj.subgroup_probability_array.id


admin.site.register(Mooclet, MoocletAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(SubGroup, SubGroupAdmin)
admin.site.register(SubGroupProbabilityArray, SubGroupProbabilityArrayAdmin)
admin.site.register(VersionProbability, VersionProbabilityAdmin)
