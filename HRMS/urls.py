from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from HRMS.views import (
    EmployeeListView, 
    EmployeeDetailView, 
    EmployeeCreateView, 
    EmployeeUpdateView, 
    EmployeeDeleteView,
    GeneratePDF
)


urlpatterns = [
    path('', views.home, name='HRMS-home'),
    path('about/', views.about, name='HRMS-about'),
    path('employees/', EmployeeListView.as_view(), name='employees'),
    path('employees/estimate/', views.profile_method, name='profile-method'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/<int:pk>/pdf/', GeneratePDF.as_view(), name='generate-pdf'),
    path('employees/new/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('employees/<int:employee_id>/educations/', views.update_educations, name='educations-update'),
    path('employees/<int:employee_id>/experiences/', views.update_experiences, name='experiences-update'),
    path('employees/<int:employee_id>/tasks/', views.update_tasks, name='tasks-update'),
    path('employees/<int:employee_id>/languages/', views.update_languages, name='languages-update'),
    # path('tasks/', TaskListView.as_view(), name='tasks'),
    # path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    # path('tasks/new/', TaskCreateView.as_view(), name='task-create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)