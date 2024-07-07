from .views import Login, Register, UserDetail, OrganisationListView, AddUserToOrganizationView
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path("auth/login/", Login.as_view(), name="login"),
    path("auth/register/", Register.as_view(), name="register"),
    path("api/users/<id>/", UserDetail.as_view(), name="detail"),
    path("api/organizations/", OrganisationListView.as_view(), name="organizations" ),
    path('api/organisations/<str:orgId>/users/', AddUserToOrganizationView.as_view(), name='add-user-to-organization'),
]
