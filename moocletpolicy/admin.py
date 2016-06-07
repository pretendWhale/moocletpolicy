from django.contrib import admin
from django.apps import apps
from .models import *



app = apps.get_app_config('moocletpolicy')

class MoocletAdmin (admin.ModelAdmin):
	list_display = ['id','name']

class VersionAdmin (admin.ModelAdmin):
	list_display = ['id', 'mooclet', 'name']
	list_filter = ('mooclet')

class SubGroupAdmin (admin.ModelAdmin):
	list_display = ['id', 'var1', 'var2', 'var3', 'var4', 'var5', 'var6', 'var7']

class SubGroupProbabilityArrayAdmin (admin.ModelAdmin):
	list_display = ['id', 'mooclet', 'subgroup']

class VersionProbabilityAdmin (admin.ModelAdmin):
	list_display = ['id', 'version', 'subgroup_probability_array', 'probability']
	list_filter = ('version', 'subgroup_probability_array')


admin.site.register(Mooclet, MoocletAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(SubGroup, SubGroupAdmin)
admin.site.register(SubGroupProbabilityArray, SubGroupProbabilityArrayAdmin)
admin.site.register(VersionProbability, VersionProbabilityAdmin)
