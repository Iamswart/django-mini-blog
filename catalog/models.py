from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 200, help_text = "Enter a category (e.g technology)")

    def __str__(self):
        return self.name

class Blogpost(models.Model):
    title = models.CharField(max_length = 200, help_text = "Enter a title")
    category = models.ManyToManyField(Category, help_text = "Select a category for this post")
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null = True)
    content = models.TextField(max_length = 1000, help_text = "Enter your post content")

    def display_category(self):
        """ Create a string for category. this is required to display category in admin"""
        return ', '.join(category.name for category in self.category.all()[:3])
    
    display_category.short_description = 'Category'
        

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """returns the url to access a blogpost detail"""
        return reverse('blogpost-detail', args =[str(self.id)])
        
class Comment(models.Model):
    blogpost = models.ForeignKey(Blogpost, on_delete=models.CASCADE)
    post_comment = models.TextField(max_length = 1000, help_text = "Enter comment about blog here")
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_posted"]

    def __str__(self):
        """
        String for representing the Model object.
        """
        comment_title=75
        if len(self.post_comment)>comment_title:
            titlestring=self.post_comment[:comment_title] + '...'
        else:
            titlestring=self.post_comment
        return titlestring

class Author(models.Model):
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    picture = models.ImageField(upload_to = 'images/%Y/%m/%d', blank=True,)
    
    class Meta:
        ordering = ['first_name', 'last_name']
        permissions = (("can_create_author", "create new author"),)

    def get_absolute_url(self):
        return reverse('author-detail', args =[str(self.id)])
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
        

                
            
    
        
        
    
        
        

    
        
    
        
