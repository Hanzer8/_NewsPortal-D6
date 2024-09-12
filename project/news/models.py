from django.contrib.auth.models import User
from django.db import models
GRADE = [(1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6),(7, 7),(8, 8),(9, 9),(10, 10),]
from django.urls import reverse



class Author(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   reting = models.SmallIntegerField(default=0)

   def update_rating(self):
      post_ratings = Post.objects.filter(author=self).aggregate(total=models.Sum('rating'))['total'] or 0

      comment_ratings = Comment.objects.filter(user=self.user).aggregate(total=models.Sum('rating'))['total'] or 0

      self.rating = post_ratings * 3 + comment_ratings
      self.save()

class Category(models.Model):
   name = models.CharField(max_length=32, unique=True)
   subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

   def __str__(self):
      return self.name


class Post(models.Model):
   author = models.ForeignKey(Author, on_delete=models.CASCADE)

   NEWS = 'NW'
   ARTICLE='AR'
   choose= (
      {'NEWS', 'NW'},
      {'ARTICLE', 'AR'},
   )
   choise = models.CharField(max_length=7, choices=choose, default='Статья')
   pdatetime = models.DateTimeField(auto_now_add=True)
   category = models.ManyToManyField(Category, through='PostCategory')
   title = models.CharField(max_length=32)
   text = models.TextField()
   reting = models.SmallIntegerField(choices=GRADE, default=0, editable=True)

   def __str__(self):
      return f"{self.choise} {self.category.name} {self.title} {self.text}"

   def get_absolute_url(self):
      return f'/news/{self.id}'

   def preview(self):
      return self.text[:100]

class PostCategory(models.Model):
   post = models.ForeignKey(Post, on_delete=models.CASCADE)
   category = models.ForeignKey(Category, on_delete=models.CASCADE)

   def __str__(self):
      return f"{self.post} {self.category}"

class Comment(models.Model):
   post = models.ForeignKey(Post, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   text = models.TextField(max_length=256)
   datetime = models.DateTimeField(auto_now_add=True)
   reting = models.SmallIntegerField(choices=GRADE, default=0, editable=True)

   def like(self):
      self.reting += 1
      self.save()

   def dislike(self):
      self.reting -= 1
      self.save()

