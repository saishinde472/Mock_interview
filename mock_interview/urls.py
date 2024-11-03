from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from admin_panel import views as admin_panel_views
from interview import views as interview_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    # User-related URLs
    path('register/', user_views.register_view, name='register'),  # Add registration URL
    path('login/', user_views.login_view, name='login'),  # Add login URL
    path('', user_views.profile_view, name='profile'),
    path('admin/update_password/<int:user_id>/', user_views.update_password_view, name='update_password'),  # Admin update password
    
    # Admin panel URLs
    path('dashboard/', admin_panel_views.admin_dashboard, name='admin_dashboard'),  # Changed here
    path('user_management/', admin_panel_views.user_management, name='user_management'),
    path('update_user/<int:user_id>/', admin_panel_views.update_user, name='update_user'),


    # Resume builder URLs
    path('resume/', user_views.resume_builder, name='resume_builder'),  # Resume builder
   
    path('resume/pdf/', user_views.generate_pdf, name='generate_pdf'),
     
  # Admin URLs for managing programming languages and questions
    path('add_language/', interview_views.add_language, name='add_language'),
    path('add_question/', interview_views.add_question, name='add_question'),
    
    # User URLs for starting the interview and submitting answers
     path('select_language/', interview_views.select_language, name='select_language'),  # Add this line
        path('interview/start/<int:language_id>/', interview_views.start_interview, name='start_interview'), 
    path('submit_answers/', interview_views.submit_answers, name='submit_answers'),
    
    # URLs for viewing the interview report
    path('interview_report/', interview_views.interview_report, name='interview_report'),
    path('interview_report_pdf/', interview_views.interview_report_pdf, name='interview_report_pdf'),

]

