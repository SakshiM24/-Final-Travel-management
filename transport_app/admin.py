from django.contrib import admin
from .models import Stop, Bus, EnrollmentRequest, ExitRequest

@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_no', 'stop', 'status')
    list_filter = ('status',)

@admin.register(EnrollmentRequest)
class EnrollmentRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity', 'role', 'emp_id', 'status', 'applied_at')
    list_filter = ('status', 'role')
    search_fields = ('name', 'emp_id', 'entity')

@admin.register(ExitRequest)
class ExitRequestAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'entity', 'department', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('employee_name', 'entity', 'bus_no')


from django.contrib import admin
from .models import FAQQuestion

@admin.register(FAQQuestion)
class FAQQuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'question', 'asked_at', 'is_answered')
    list_filter = ('is_answered',)


from django.contrib import admin
from .models import EmployeeQuestion

admin.site.register(EmployeeQuestion)

