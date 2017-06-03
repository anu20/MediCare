from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseBadRequest,\
                        HttpResponseForbidden
from MediCare.labs.models import Lab
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.template.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from MediCare.decorators import ajax_required
from .models import Lab, LabImage

LABS_NUM_PAGES = 10


def labs(request):
        labs = Lab.objects.all()
        context = {'labs': labs}
	template = 'labs/labs.html'	
	return render(request, template, context)


@ajax_required
def load(request):
    from_lab = request.GET.get('from_lab')
    page = request.GET.get('page')
    lab_source = request.GET.get('lab_source')
    all_labs = Lab.get_labs(from_lab)
    paginator = Paginator(all_labs, LABS_NUM_PAGES)
    try:
        labs = paginator.page(page)
    except PageNotAnInteger:
        return HttpResponseBadRequest()
    except EmptyPage:
        labs = []
    html = u''
    csrf_token = unicode(csrf(request)['csrf_token'])
    for lab in labs:
        html = u'{0}{1}'.format(html,
                                render_to_string('labs/partial_lab.html',
                                                 {
                                                    'lab': lab,
                                                    'user': request.user,
                                                    'csrf_token': csrf_token
                                                    }))

    return HttpResponse(html)

def search(request):
	try:
		q = request.GET.get('q')
	except:
		q = None
	
	if q:
		labs = Lab.objects.filter(title__icontains=q)
		context = {'query': q, 'labs': labs}
		template = 'labs/results.html'	
	else:
		template = 'labs/home.html'	
		context = {}
	return render(request, template, context)



def all(request):
	labs = Lab.get_labs()
	context = {'labs': labs}
	template = 'labs/labs.html'	
	return render(request, template, context)


def single(request, slug):
	
		lab = Lab.objects.get(slug=slug)
		#images = product.productimage_set.all()
		images = LabImage.objects.filter(lab=lab)
		context = {'lab': lab , 'images': images}
		template = 'labs/lab.html'	
		return render(request, template, context)




