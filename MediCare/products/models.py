from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
# Create your models here.

class ProdCategory(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(null=True, blank=True)
	slug = models.SlugField(unique=True)
	featured = models.BooleanField(default=None)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)


	def __unicode__(self):
		return self.title



class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(null=True, blank=True)
	category = models.ForeignKey(ProdCategory, null=True, blank=True)
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
		return reverse("product", kwargs={"slug": self.slug})

        def get_description(self):
		return self.description


class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to='/home/anushka/MediCare/media/products/images/')
	featured = models.BooleanField(default=False)
	thumbnail = models.BooleanField(default=False)
	active = models.BooleanField(default=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.product.title

        def get_picture(self):
        	no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        	try:
            		filename = settings.MEDIA_ROOT + '/products/' + self.product.slug + '.jpg'
            		picture_url = settings.MEDIA_URL + 'products/' + self.product.slug + '.jpg'
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


