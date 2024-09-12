from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from .models import Post, Category
from .filters import PostFilter
from django.contrib.auth.decorators import login_required


# Create your views here.
class PostsList(ListView):
   model = Post
   ordering = 'author'
   template_name = 'flatpages/posts.html'
   context_object_name = 'posts'
   paginate_by = 2


   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['filterset'] = PostFilter(self.request.GET, queryset=self.get_queryset())
      # context['is_not_auter'] = not self.request.user.groups.filterset(name='authors').exists()
      return context


   def get_queryset(self):
      queryset = super().get_queryset()
      self.filterset = PostFilter(self.request.GET, queryset)
      return self.filterset.qs


   # def get_context_data(self, **kwargs):
   #    context = super().get_context_data(**kwargs)
   #    context['filterset'] = self.filterset
   #    return context

   # def get_queryset(self):
   #    queryset = super().get_queryset()
   #    self.filterset = PostFilter(self.request.GET, queryset)
   #    return self.filterset.qs


class PostDetail(DetailView):
   model = Post
   template_name = 'flatpages/post.html'
   context_object_name = 'post'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['time_no2w'] = datetime.utcnow()
      return context

class PostCreate(PermissionRequiredMixin, CreateView):
   permission_required = ('news.add_post',)
   form_class = PostForm
   model = Post
   template_name = 'flatpages/post_create.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
   permission_required = ('news.change_post',)
   form_class = PostForm
   model = Post
   template_name = 'flatpages/post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
   permission_required = ('news.delete_post',)
   model = Post
   template_name = 'flatpages/post_delite.html'
   success_url = reverse_lazy('posts')


class CategoryListView(PostsList):
   model = Post
   template_name = 'flatpages/category_list.html'
   context_object_name = 'category_news_list'

   def get_queryset(self):
      self.category = get_object_or_404(Category, id=self.kwargs['pk'])
      queryset = Post.objects.filter(category=self.category).order_by('-pdatetime')
      return queryset

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
      context['category'] = self.category
      return context

@login_required()
def subscribe(request, pk):
   user = request.user
   category = Category.objects.get(id=pk)
   category.subscribers.add(user)

   massage = 'Вы успешно подписплись на рассылку новостей категории'
   return render(request, 'flatpages/subscribe.html', {'category': category, 'massage': massage})