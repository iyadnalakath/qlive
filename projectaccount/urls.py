from django.urls import path
from rest_framework_nested import routers
from .views import (
    LoginView,
    RegisterUserView,
    UpdateStaffPasswordView,
    LogoutView
)



urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/staff/", RegisterUserView.as_view(), name="register"),
    path("staff/<int:pk>/", RegisterUserView.as_view(), name="user-detail"),
    path("staff/update-password/<int:pk>/", UpdateStaffPasswordView.as_view(), name="update-password"),
]


router = routers.DefaultRouter()
# router.register("userslist", views.SingleUserView),

# router.register("event_management_users", views.EventManagementUsersView)
# router.register('eventteamlistsubcatagory',views.EventManagementSubcategoryViewSet,basename='MyModel')


urlpatterns = router.urls + urlpatterns
