from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UploadPresetForm, EditPresetForm, ReviewForm
from .models import  Preset, Review, Tags
from profiles.models import UserProfile
from profiles.models import Cart, Library
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def presets(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    tags = Tags.objects.all().filter(name__icontains = q)
    preset_items = Preset.objects.all().order_by('rateing', 'clicks').reverse().filter(name__icontains=q)


    if request.user.is_authenticated:
        library = Library.objects.filter(user = request.user).all()
        libray_items = []

        for p in library:
            libray_items.append(p.product)
    else:
        libray_items = None 

    #seach funtionality

    context = {
        'items': preset_items,
        'library': libray_items,
        'tags': tags,
    }

    return render(request, 'presets/presets.html', context)

@login_required(login_url='/login')
def preset_add(request):

    form = UploadPresetForm()

    if request.method == 'POST':
        form = UploadPresetForm(request.POST, request.FILES)

        name = request.POST['name']
        description = request.POST['description']
        file = request.FILES['file']
        cover = request.FILES['cover']
        price = request.POST['price']
        tags = request.POST['tags']

        tags_list = tags.split(',')

        if form.is_valid():
            preset = Preset.objects.create(
                seller = request.user,
                name = name,
                description = description,
                file = file,
                cover = cover,
                price = price,
            )    
            
            preset.save()
            for t in tags_list:
                preset.tags.create(name = t)
            #product_instance.save()

            return redirect('preset-detail', preset.id)

    context = {'form': form}

    return render(request, 'presets/preset-add.html', context)

def preset_detail(request, id):
    preset = Preset.objects.get(id = id)
    profile = UserProfile.objects.get(user = preset.seller)

    if request.user != preset.seller:
        preset.clicks += 1
        preset.save()

    reviews = Review.objects.all().filter(product = preset)

    review = None
    try:
        review = Review.objects.get(user = request.user, product = preset)
    except :
        review = None


    if request.user.is_authenticated:
        library = Library.objects.filter(user = request.user).all()
        libray_items = []

        for p in library:
            libray_items.append(p.product)
    else:
        libray_items = None 

    form = ReviewForm()


    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            Review.objects.create(
                user = request.user,
                product = preset,
                comment = request.POST['comment'],
                rate = request.POST['rate'],
            ).save()

            preset.rateing += int(request.POST['rate'])
            preset.save()

            return redirect('preset-detail', id)
    

    context = {
        'preset': preset,
        'form': form,
        'library': libray_items,
        'review': review,
        'reviews': reviews,
        'profile': profile,
    }

    return render(request, 'presets/preset_detail.html', context)

@login_required(login_url='/login')
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        sellected_product = Preset.objects.get(id = product_id)  
        product, created = Cart.objects.get_or_create(user = request.user, product = sellected_product)
        
        if created:
            messages.success(request, 'Item added')
        else:
            messages.error(request, 'Item already in cart')
        #add succes messages

    return redirect('/')

@login_required(login_url='/login')
def add_to_cart2(request, pk):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        sellected_product = Preset.objects.get(id = product_id)  
        product, created = Cart.objects.get_or_create(user = request.user, product = sellected_product)
        
        if created:
            messages.success(request, 'Item added')
        else:
            messages.error(request, 'Item already in cart')
        #add succes messages

    return redirect('/')


@login_required(login_url='/login')
def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        
        selected_product = Preset.objects.get(id = product_id)
        cart = Cart.objects.get(user = request.user, product = selected_product)
        cart.delete()
        return JsonResponse({'status': 'Great'})

    return redirect('/')

@login_required(login_url='/login')
def edit_preset(request, id):
    
    preset = Preset.objects.get(id = id)

    form = EditPresetForm(instance=preset)

    if request.method == 'POST':
        form = EditPresetForm(request.POST, request.FILES, instance=preset)

        if form.is_valid():
            tags = request.POST['tags']

            tags_list = tags.split(',')

            preset = form.save(commit=False)
            for t in tags_list:
                preset.tags.create(name = t)

            preset.save()

            

    context = {'form': form,
    'preset': preset,
    }

    return render(request, 'presets/preset_edit.html', context)

def tag(request, name):
    tag = Tags.objects.get(name = name)

    products = Preset.objects.all().filter(tags = tag)

    context = {
        'tag': tag,
        'items' :products,
    }

    return render(request, 'presets/tag.html', context)