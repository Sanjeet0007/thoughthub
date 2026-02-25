from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Post, Category
from .forms import PostForm, CategoryForm
import random


class AdminLoginView(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('admin_dashboard')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)


class AdminLogoutView(LogoutView):
    next_page = 'home'


def admin_login(request):
    return AdminLoginView.as_view()(request)


def admin_logout(request):
    return AdminLogoutView.as_view()(request)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('category', 'author')
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset.order_by('-created_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['related_posts'] = Post.objects.filter(
            category=post.category
        ).exclude(pk=post.pk).filter(status='published')[:3]
        return context


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Post
    template_name = 'admin/dashboard.html'
    context_object_name = 'posts'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.count()
        context['total_categories'] = Category.objects.count()
        context['total_users'] = User.objects.count()
        context['published_posts'] = Post.objects.filter(status='published').count()
        context['draft_posts'] = Post.objects.filter(status='draft').count()
        return context


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'admin/post_form.html'
    success_url = reverse_lazy('admin_post_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'admin/post_form.html'
    success_url = reverse_lazy('admin_post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'admin/post_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Post deleted successfully!')
        return super().form_valid(form)


class CategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category
    template_name = 'admin/category_list.html'
    context_object_name = 'categories'

    def test_func(self):
        return self.request.user.is_staff


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin/category_form.html'
    success_url = reverse_lazy('category_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin/category_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'admin/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Category deleted successfully!')
        return super().form_valid(form)


@login_required
def admin_post_list(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    posts_list = Post.objects.all().select_related('category', 'author').order_by('-created_at')
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'admin/post_list.html', {'posts': posts})
