from django.contrib import admin
from .models import Subject,Teachers

# Register your models here.


class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
admin.site.register(Subject, SubjectAdmin)


class TeachersAdmin(admin.ModelAdmin):
    list_display = [
        "id", 
        "teacher_name",
        "roll_no",
        "whatsapp_no",
        "email",
        "experience",
        "date",
        "remuneration_min",
        "remuneration_max",
        "video_link",
        "bank_acc_holder_name",
        "bank_name",
        "branch",
        "ifsc_code",
        "about",
        "remark",
        "qualification",
        "demo_rating",
        "english_fluency",
        "interview_rating",
        
        ]
admin.site.register(Teachers, TeachersAdmin)

