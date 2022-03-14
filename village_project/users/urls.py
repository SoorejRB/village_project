from django.urls import path
from .views import (ComplaintDetailsView, HomeView, index,loginview, employee_registrationview, panchayath_registrationview, enduser_registrationview, logoutview, EmployeeListView, AddNews, ViewNews, register_complaint, salary_updation_view, SalaryDetailsView, SalaryListView, ComplaintForm,ComplaintListView,resolve_complaint,PanchayathProfileDetailsview,EmployeeProfileDetailsview,EnduserProfileDetailsView )
app_name = 'users'

urlpatterns = [
    path('',HomeView.as_view(), name= 'home'),
    path('login/',loginview, name= 'login'),
    path('logout/',logoutview, name= 'logout'),
   


    path('employee-registration/',employee_registrationview, name= 'employee_registration'),
    path('panchayath-registration/',panchayath_registrationview, name= 'panchayath_registration'),
    path('user-registration/',enduser_registrationview, name= 'enduser_registration'),
    
    path('home/',index, name= 'index'),
    path('employee-list/', EmployeeListView.as_view(), name='employee_list'),
    path('add-news/', AddNews, name='add_news'),
    path('news/', ViewNews.as_view(), name='news'),
    path('salary-updation/<int:employee_id>', salary_updation_view, name='update_salary'),
    path('salary-list/', SalaryListView.as_view(), name='salary_list'),
    path('salary-details/(?P<pk>\d+)$', SalaryDetailsView.as_view(), name='salary_details'),
    path('complaint-registration/', register_complaint, name= 'complaint_registration'),
    path('complaint-list/', ComplaintListView.as_view(), name= 'complaint_list'),
    path('complaint-details/(?P<pk>\d+)$', ComplaintDetailsView.as_view(), name='complaint_details'),
    path('<int:complaint_id>/solve', resolve_complaint, name='solve'),
    path('unduser-profile/(?P<pk>\d+)$',EnduserProfileDetailsView.as_view(), name='enduser_profile'),
    path('employee-profile/(?P<pk>\d+)$',EmployeeProfileDetailsview.as_view(), name='employee_profile'),
    path('panchayath-profile/(?P<pk>\d+)$',PanchayathProfileDetailsview.as_view(), name='panchayath_profile'),
    # path('salary-registration/', salary_registrationview, name= 'salary_registration'),
    # path('news-registration/', news_registrationview, name= 'news_registration'),
    # path('complaint-registration/', complaint_registrationview, name= 'complaint_registration'),



    
]