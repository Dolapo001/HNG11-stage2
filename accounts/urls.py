from django.urls import path
from .views import *
urlpatterns = [
    path('auth/register', UserRegistrationView.as_view(), name='register'),
    path('auth/login', UserLoginView.as_view(), name='login'),
    path('api/users/<str:pk>', UserDetailView.as_view(), name='user-detail'),
    path('api/organisations', OrganizationListView.as_view(), name='organisation-list'),
    path('api/organisations/<str:pk>', OrganizationDetailsView.as_view(), name='organisation-detail'),
    path('api/organisations/create', OrganizationCreateView.as_view(), name='organisation-create'),
    path('api/organisations/<str:org_id>/add_user', AddUserToOrganizationView.as_view(), name='add-user-to-org'),
]