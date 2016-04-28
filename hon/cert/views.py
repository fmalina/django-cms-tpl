from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hon.cert.forms import CertForm

from models import Cert, Category

def cert(request, id):
    return render(request, 'cert.html', {
            'cert': get_object_or_404(Cert, pk=id)
        })

def edit_cert(request, id):
    from django.core.urlresolvers import reverse
    url = reverse("admin:cert_cert_change", args=(id,))
    return redirect(url)

def certify(request):
    form = CertForm()
    return render(request, 'certify.html', {
            'form': form
        })

def listing(request, slug=False):
    ls = Cert.objects.filter(compliant=True).order_by('-date_init_review')
    title = 'Recently certified websites'
    if slug:
        c = get_object_or_404(Category, slug=slug)
        ls = ls.filter(Q(category1=c) | Q(category2=c) | Q(category3=c))
        title = c.name
    
    paginator = Paginator(ls, 50)
    page = request.GET.get('page')
    try:
        certs = paginator.page(page)
    except PageNotAnInteger:
        certs = paginator.page(1)
    except EmptyPage: # If page is out of range (e.g. 9999), deliver last page of results.
        certs = paginator.page(paginator.num_pages)
    
    cats = Category.objects.all()
    tree = cats # TODO: make a tree recursively, out of steam now
    
    return render(request, 'list.html', {
            'ls': certs,
            'title': title,
            'tree': tree
        })
    