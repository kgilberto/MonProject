from django.contrib import admin

# Register your models here.
from tutor.models import *

class Counter_admin(admin.ModelAdmin):
    list_display = ['date', 'total_today', 'total_overall']
    search_fields = ['date']
admin.site.register(Counter, Counter_admin)



class Record_Visitor_admin(admin.ModelAdmin):
    list_display = ['ip', 'date', 'total_today', 'total_overall']
    search_fields = ['ip', 'date']
admin.site.register(Record_Visitor, Record_Visitor_admin)


class Visitor_admin(admin.ModelAdmin):
    list_display = ['ip']
    search_fields = ['ip']
admin.site.register(Visitor, Visitor_admin)