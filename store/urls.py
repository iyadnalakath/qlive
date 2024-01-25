from django.urls import path
from rest_framework_nested import routers
from . import views
from .views import *

urlpatterns = [
    # path("popular/", PopularityViewSetList.as_view(), name="popular-product-list"),
    # path('location/', LocationCreateAPIView.as_view(), name='location_create'),
    # path('location/', LocationView.as_view(), name='location'),
]

router = routers.DefaultRouter()
router.register("subject", views.SubjectViewSet)
router.register("teacher", TeacherViewSet, basename='teacher')


urlpatterns = router.urls + urlpatterns