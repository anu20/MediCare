
from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseBadRequest,\
                        HttpResponseForbidden
from MediCare.products.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.template.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from MediCare.decorators import ajax_required
from .models import Product, ProductImage

def search(request):
	try:
		q = request.GET.get('q')
	except:
		q = None
	
	if q:
		products = Product.objects.filter(title__icontains=q)
		context = {'query': q, 'products': products}
		template = 'products/results.html'	
	else:
		template = 'products/products.html'	
		context = {}
	return render(request, template, context)


def products(request):
	template = 'products/products.html' 
	return render(request, template,)


def products_all(request):
	products = Product.objects.all()
	context = {'products': products}
	template = 'products/products_all.html'	
	return render(request, template, context)


def product(request,slug):
		product = Product.objects.get(slug=slug)
		#images = product.productimage_set.all()
		images = ProductImage.objects.filter(product=product)
		context = {'product': product, 'images' : images}
		template = 'products/product.html'	
		return render(request, template,context)

