from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape
import bleach
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
# Create your models here.

class Category(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(null=True, blank=True)
	slug = models.SlugField(unique=True)
	featured = models.BooleanField(default=None)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)


	def __unicode__(self):
             return self.title
        
        def get_category(self):
             return self.title

        def get_categories(from_lab=None):
       		if from_cat is not None:
            	   cats = Category.objects.filter(parent=None, id__lte=from_cat)
        	else:
                   cats = Category.objects.filter(parent=None)
                return cats
          
        def linkfy_category(self):
             return bleach.linkify(escape(self.title))

class Lab(models.Model):
        title = models.CharField(max_length=120)
	description = models.TextField(null=True, blank=True)
	category = models.ForeignKey(Category, null=True, blank=True)
	price = models.DecimalField(decimal_places=2, max_digits=100, default=29.99)
	sale_price = models.DecimalField(decimal_places=2, max_digits=100,null=True, blank=True)
	slug = models.SlugField(unique=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)
	update_defaults = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

        class Meta:
                unique_together = ('title', 'slug')

	def get_price(self):
		return self.price

	def get_absolute_url(self):
		return reverse("single", kwargs={"slug": self.slug})

        def get_labs(from_lab=None):
       		if from_lab is not None:
            	   labs = Lab.objects.filter(parent=None, id__lte=from_lab)
        	else:
                   labs = Lab.objects.filter(parent=None)
                return labs
        def get_labsDate(date=None):
                if date is not None:
                   labs = Lab.objects.filter(parent=None,timestamp=date)
                else:
                   labs=Lab.objects.filter(parent=None)
                return labs
        def linkfy_lab(self):
                return bleach.linkify(escape(self.title))

class LabImage(models.Model):
	lab = models.ForeignKey(Lab)
	image = models.ImageField(upload_to='/home/anushka/MediCare/media/labs/images/')
	featured = models.BooleanField(default=False)
	thumbnail = models.BooleanField(default=False)
	active = models.BooleanField(default=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
          return self.lab.title

        def get_picture(self):
        	no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        	try:
            		filename = settings.MEDIA_ROOT + '/labs/' + self.lab.slug + '.jpg'
            		picture_url = settings.MEDIA_URL + 'labs/' + self.lab.slug + '.jpg'
            		if os.path.isfile(filename):
                		return picture_url
            	        else:
                		gravatar_url = u'http://www.gravatar.com/avatar/{0}?{1}'.format(
                    		hashlib.md5(self.user.email.lower()).hexdigest(),
                    		urllib.urlencode({'d': no_picture, 's': '256'})
                    		)
                                return gravatar_url

        	except Exception, e:
            		return no_picture

