from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class PublishedManager(models.Model):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')
    

class Post(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('home:post_detail', kwargs={'year': self.publish.year,
                                                   'month': self.publish.strftime('%m'),
                                                   'day': self.publish.strftime('%d'),
                                                   'post': self.slug,
                                                   'pk': self.pk}
                       )

    def __str__(self):
        return self.title


