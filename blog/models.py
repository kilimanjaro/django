from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.

class Post(models.Model):
  title = models.CharField(verbose_name="TITLE", max_length=50)
  slug = models.SlugField("SLUG", unique=True, allow_unicode=True, help_text='one word for alias')
  description = models.CharField("DESCRIPTION", max_length=100, blank=True, help_text='simple descriptin text')
  content = models.TextField('CONTENT')
  create_dt = models.DateTimeField('CREATE_DATE', auto_now_add=True)
  modify_dt = models.DateTimeField('MODIFY_DATE', auto_now=True)
  tags = TaggableManager(blank=True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='OWNER', blank=True, null=True)


  class Meta:
    verbose_name = 'post'
    verbose_name_plural= 'posts'
    db_table = 'blog_posts'
    ordering = ('-modify_dt',)




  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse('blog:post_detail', args=(self.slug,))
    # reverse는 {% url %} 과 동일한 기능을 한다.
  
  def get_previos(self):
    return self.get_previos_by_modify_dt()
  
  def get_next(self):
    return self.get_next_by_modify_dt()

  def save(self, *args, **kwargs):
      self.slug = slugify(self.title, allow_unicode=True)
      super().save(*args, **kwargs)

