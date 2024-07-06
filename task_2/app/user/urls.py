from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import Login, Register, UserDetailView, OrganisationListView, OrganisationCreateView, OrganisationDetailView, OrganisationAddUserView
urlpatterns = [
    path('auth/login/', view=Login.as_view(),  name='login'),
    path('auth/register', view=Register.as_view(), name='register'),
    path('api/users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('api/organisations/', OrganisationListView.as_view(), name='organisation-list'),
    path('api/organisations/<int:pk>/', OrganisationDetailView.as_view(), name='organisation-detail'),
    path('api/organisations/<int:pk>/users/', OrganisationAddUserView.as_view(), name='organisation-add-user'),
    path('api/organisations/create/', OrganisationCreateView.as_view(), name='organisation-create'),
]
