from django.contrib import admin
from django.apps import apps
from .models import *

#inline version in admin - click the mooclet id!
class VersionInline(admin.StackedInline):
    model = Version



class VersionProbabilityInline(admin.StackedInline):
    model = VersionProbability

# Admin classes define model display in admin interface
class MoocletAdmin (admin.ModelAdmin):
	#what fields to display, in what order
	list_display = ['id','name']
	inlines = [VersionInline,]

class VersionAdmin (admin.ModelAdmin):
	list_display = ['id', 'mooclet', 'name']
	#what fields to allow filtering on
	list_filter = ['mooclet',]
	inlines = [VersionProbabilityInline,]


class SubGroupAdmin (admin.ModelAdmin):
	list_display = ['id', 'var1', 'var2', 'var3', 'var4', 'var5', 'var6', 'var7']

class SubGroupProbabilityArrayAdmin (admin.ModelAdmin):
	list_display = ['id', 'mooclet', 'subgroup']
	inlines = [VersionProbabilityInline,]

class VersionProbabilityAdmin (admin.ModelAdmin):
	list_display = ['id', 'version', 'subgroup_probability_array', 'probability']

	#__ signifies looking up property of mooclet ForeignKey
	list_filter = ['version', 'subgroup_probability_array']

	def get_mooclet(self, obj):
		return obj.version.mooclet



	




#register the Models with their Admins
admin.site.register(Mooclet, MoocletAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(SubGroup, SubGroupAdmin)
admin.site.register(SubGroupProbabilityArray, SubGroupProbabilityArrayAdmin)
admin.site.register(VersionProbability, VersionProbabilityAdmin)
