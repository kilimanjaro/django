from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, TodayArchiveView
from blog.models  import Post
from django.conf import settings

from django.views.generic import FormView    # generic View : 공통적인 로직을 만들어 놓은 뷰
from blog.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render          # shortcut : 자주 사용되는 함수, 내장함수


from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin



# Create your views here.

class PostLV(ListView):
  model = Post
  template_name = "blog/post_all.html"  # 어떤 템플릿으로 연결할 지 정함. 서버재시작 필요없음.
  context_object_name = 'posts'
  paginate_by = 2

class PostDV(DetailView):
  model = Post

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}"
    context['disqus_id'] = f"post-{self.object.id}-{self.object.slug}"
    context['disqus_url'] = f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}"
    context['disqus_title'] = f"{self.object.slug}"
    return context


class PostAV(ArchiveIndexView):
  model = Post
  date_field = 'modify_dt'


class PostYAV(YearArchiveView):
  model = Post
  date_field = 'modify_dt'
  make_object_list = True

class PostMAV(MonthArchiveView):
  model = Post
  date_field = 'modify_dt'  

class PostDAV(DayArchiveView):
  model = Post
  date_field = 'modify_dt'  

class PostTAV(TodayArchiveView):
  model = Post
  date_field = 'modify_dt' 


class TagCloudTV(TemplateView):
  template_name = "taggit/taggit_cloud.html"

class TaggedObjectLV(ListView):
  template_name = "taggit/taggit_post_list.html"
  model = Post

  def get_queryset(self):
    return Post.objects.filter(tags_name= self.kwargs.get('tag'))

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['name']= self.kwargs['tag']
    return context

class SearchFormView(FormView):
  form_class = PostSearchForm
  template_name = "blog/post_search.html"

  def form_valid(self, form):
    searchWord = form.cleaned_data['search_word']
    post_list = Post.objects.filter(Q(title__icontains=searchWord) | Q(description__icontains=searchWord) | Q(content__icontains=searchWord)).distinct()

    context = {}
    context['form'] = form
    context['search_term'] = searchWord
    context['object_list'] = post_list


    return render(self.request , self.template_name,  context)
  
  

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tags']
    initial = {'slug': 'auto-filling-do-not-input'} 
    #fields = ['title', 'description', 'content', 'tags'] 
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PostChangeLV(LoginRequiredMixin, ListView):
    template_name = 'blog/post_change_list.html'

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)


class PostUpdateView(OwnerOnlyMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tags']
    success_url = reverse_lazy('blog:index')


class PostDeleteView(OwnerOnlyMixin, DeleteView) :
    model = Post
    success_url = reverse_lazy('blog:index')

