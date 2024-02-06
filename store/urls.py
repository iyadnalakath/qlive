from django.urls import path
from rest_framework_nested import routers
from . import views
from .views import *

urlpatterns = [
    
]

router = routers.DefaultRouter()
router.register("subject", views.SubjectViewSet)
router.register("teacher", TeacherViewSet, basename='teacher')
router.register("grade", GradeViewSet, basename='grade')


urlpatterns = router.urls + urlpatterns