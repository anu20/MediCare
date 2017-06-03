from django.contrib import admin
# Register your models here.
from .models import Lab, LabImage, Category

class LabAdmin(admin.ModelAdmin):
	date_hierarchy = 'timestamp' #updated
	search_fields = ['title', 'description']
	list_display = ['title', 'price', 'active', 'updated']
	list_editable = ['price', 'active']
	list_filter = ['price', 'active']
	readonly_fields = ['updated', 'timestamp']
	prepopulated_fields = {"slug": ("title",)}
	class Meta:
		model = Lab

admin.site.register(Lab, LabAdmin)


admin.site.register(LabImage)
admin.site.register(Category)
