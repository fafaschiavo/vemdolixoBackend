from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create-new-member/', views.create_new_member, name='create_new_member'),
    url(r'^new-member/', views.new_member, name='new_member'),
    url(r'^login/', views.login_page, name='login_page'),
    url(r'^login-user/', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^companies/$', views.companies_page, name='companies_page'),
    url(r'^new-company/', views.new_company, name='new_company'),
    url(r'^new-company-csv/', views.new_company_csv, name='new_company_csv'),
    url(r'^receptivity/$', views.receptivity_page, name='receptivity_page'),
    url(r'^new-receptivity/', views.new_receptivity_entry, name='new_receptivity_entry'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^search-map/$', views.search_map, name='search_map'),
    url(r'^residues/$', views.residues, name='residues'),
    url(r'^similarity-rank-result/$', views.similarity_rank_result, name='similarity_rank_result'),
    url(r'^$', views.index, name='index'),
]