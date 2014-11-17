from django.contrib import admin
from tool_share.models import *
class ToolUserAdmin(admin.ModelAdmin):
	prepopulated_fields = {}
	list_display = ('user','name','address','zipCode')
	search_fields = ['email','zipCode']

class ToolAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('toolId',)}
	list_display = ('owner','toolType','currentUser')

class ShedAdmin(admin.ModelAdmin):
	list_display = ('name','coordinator','zipCode', 'id')

class UpdateAdmin(admin.ModelAdmin):
	list_display = ('subject','published')

class SystemMessageAdmin(admin.ModelAdmin):
	list_display = ('subject','date')

class ToolRequestAdmin(admin.ModelAdmin):
	list_display = ('tool','requester','date')

admin.site.register(ToolUser, ToolUserAdmin)
admin.site.register(Tool, ToolAdmin)
admin.site.register(Shed, ShedAdmin)
admin.site.register(Update, UpdateAdmin)
admin.site.register(SystemMessage, SystemMessageAdmin)
admin.site.register(ToolRequest)
admin.site.register(Message)