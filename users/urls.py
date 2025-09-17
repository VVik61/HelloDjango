from django.urls import path
from .views import (
    UserDashboardView,
    PatientListView,
    ProfileUpdateView,
    register,
    CustomLogoutView,
    AssignPatientsView,
    assign_doctor,
)

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("dashboard/", UserDashboardView.as_view(), name="dashboard"),
    path("patients/", PatientListView.as_view(), name="patient_list"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("assign-patients/", AssignPatientsView.as_view(), name="assign_patients"),
    path("assign-doctor/", assign_doctor, name="assign_doctor"),
]
