from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/posts/', views.admin_post_list, name='admin_post_list'),
    path('admin/posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('admin/posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('admin/posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('admin/categories/', views.CategoryListView.as_view(), name='category_list'),
    path('admin/categories/new/', views.CategoryCreateView.as_view(), name='category_create'),
    path('admin/categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('admin/categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
]
