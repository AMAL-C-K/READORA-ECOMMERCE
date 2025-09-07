from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator


def home(request):
    genres = Genre.objects.all()
    books = Book.objects.all().order_by('-created_at')
    

    paginator = Paginator(books,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj':page_obj,'genres':genres}
    return render(request, 'index.html',context)

def genrewise_list(request,slug):
    book = Book.objects.filter(genre__slug=slug)

    paginator = Paginator(book,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={'page_obj':page_obj, 'slug':slug,}
    return render(request, 'genrewise.html',context)

def book(request,g_slug,b_slug):
    try:
        book = Book.objects.get(genre__slug=g_slug,slug=b_slug)
    
    except Exception as error:
        raise error
    context = {'book':book}
    return render(request, 'book.html',context)


def search(request):
    query = request.GET.get('q', '').strip()       # safely get and clean the search input
    products = []

    if query:                                   # only search if there's a non-empty query
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__genre__icontains=query) |
            Q(slug__icontains=query)
           
        ).distinct()                            # optional: use distinct to avoid duplicates if you have joins

        paginator = Paginator(books,12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page('page_number')


    return render(request, 'search.html', {'page_obj': page_obj,'query': query})


def price_filter(request):
    min_price= request.GET.get('min_price','').strip()
    max_price= request.GET.get('max_price','').strip()
    sort_order = request.GET.get('sort')

    books = Book.objects.all()

    if min_price.isdigit():
        min_price_value = int(min_price)
        if min_price_value >0:
            books =Book.objects.filter(price__gte=int(min_price_value))
    
    if max_price.isdigit():
        max_price_value = int(max_price)
        if max_price_value >0:
            books = Book.objects.filter(price__lte=int(max_price_value))

    if sort_order=='asc':
        books=books.order_by('price')
    elif sort_order=='desc':
        books=books.order_by('-price')
    

    



    return render(request,'price_filter.html',{'books':books,'min_price':min_price,'max_price':max_price})