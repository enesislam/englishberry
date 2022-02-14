from django.db import models
from django.db.models.signals import pre_save
from django_project.utils import unique_slug_generator
from django.shortcuts import reverse
from django.conf import settings
from PIL import Image
"""
class Profile(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	bio = models.TextField(max_length=90)
	profilepicture = models.ImageField(models.ImageField(default='default.jpg', upload_to='users_profile_pics'))

	def __str__(self):
		return self.user"""
		
class UserImg(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics',null=False, blank=False)
	date_added = models.DateTimeField(auto_now_add=True)


	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 350 or img.width > 450:
			output_size = (350, 450)
			img.thumbnail(output_size)
			img.save(self.image.path)
	def __str__(self):
		return self.image
	

class UserBio(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	text = models.TextField(max_length=90)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.text

class GelenSorular(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=200,blank=False,null=False)
	email = models.EmailField(max_length = 254)
	text = models.TextField(max_length=700)
	cevaplandi =  models.BooleanField(default=False)
	date_added = models.DateTimeField(auto_now_add=True)
	kullanıcı_kayıtlı_mı =  models.CharField(max_length=5,default='Hayır')

	def __str__(self):
		return ("'{}' kişisinden.  Mail:{}").format(self.name,self.email) 

class Category(models.Model):
	name = models.CharField(max_length=25)

	def __str__(self):
		return self.name

class AboutPosts(models.Model):
	title = models.CharField(max_length=110)
	paragraf1 = models.TextField(max_length=500)
	paragraf2 = models.TextField(max_length=500, blank=True,null=True)
	paragraf3 = models.TextField(max_length=250,blank=True,null=True)
	date_added = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.title
class Hakkimizda(models.Model):
	text = models.TextField(max_length=600)
	date_added = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.text

class Yazilar(models.Model):
	title = models.TextField(max_length=600)
	text = models.TextField(max_length=2000)
	date_added = models.DateTimeField(auto_now_add=True)
	published =  models.BooleanField(default=True)
	tags = models.TextField(max_length=23)
	image = models.ImageField(upload_to ='yazilar/%Y/%m/%d/')

	def __str__(self):
		return self.title


class Post(models.Model):
	title = models.CharField(max_length=200)
	video_link = models.CharField(max_length=11)
	image = models.ImageField(upload_to ='uploads/%Y/%m/%d/')
	date_added = models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True, related_name='likes')
	slug = models.SlugField(max_length=250,null=True, blank=True)
	published =  models.BooleanField(default=True)
	category = models.ForeignKey('Category',on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_cat_url(self):
		return ('/kategori/' + self.category.name)

	def get_absolute_url(self):
		return ('/dersler/' + self.slug)

	def get_fav_url(self):
			return ('/favori/' + self.slug)
	def total_likes(self):
		return self.likes.count()

	def get_add_to_like_url(self):
		return reverse("like", kwargs={
			'slug': self.slug
			})

def slug_generator(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


        
