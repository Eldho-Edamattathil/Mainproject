from django.shortcuts import render,redirect,get_object_or_404
from app1.models import Product,Category,ProductImages,Coupon,wallet
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from admindash.forms import CreateProductForm,ProductImagesForm,CouponForm
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.core.paginator import Paginator
from app1.models import CartOrder,CartOrderItems
import calendar
from django.db.models.functions import ExtractMonth
from django.db.models import Count,Avg


@login_required(login_url='adminside:admin_login')  # Use the named URL pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    # if not request.user.is_authenticated:
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')

    product_count=Product.objects.count()
    category_count=Category.objects.count()
    orders= CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month","count")
    month=[]
    total_orders=[]
    for i in orders:
        month.append(calendar.month_name[i["month"]])
        total_orders.append(i["count"])
    
    context={
        'product_count':product_count,
        'category_count':category_count,
        'month':month,
        'total_orders':total_orders
        
    }

    return render(request, 'adminside/admin_index.html', context)
  
  
def admin_products_list(request):
  
  products = Product.objects.all()
  p=Paginator(Product.objects.all(),10)
  page=request.GET.get('page')
  productss=p.get_page(page)
  
  context ={
    "products":products ,
    "productss":productss
  }
  return render(request,'adminside/admin_products_list.html', context)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def admin_products_details(request, pid):
#     print(pid)
#     if not request.user.is_authenticated:
#         return redirect('adminside:admin_login')

#     try:
#         product = Product.objects.get(pid=pid)
       
#     except Product.DoesNotExist:
#         return HttpResponse("Product not found", status=404)

#     if request.method == 'POST':
#         form = CreateProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             # Save the form including the image
#             product = form.save(commit=False)
#             product_image = form.cleaned_data['new_image']
#             if product_image is not None:
#                 product.image=product_image
            
#             product.save()
            
#             return redirect('admindash:admin_products_list')
#         else:
#             print(form.errors)
#             context = {
#                 'form': form,
#                 'product': product,
                
#             }
#             return render(request, 'adminside/admin_products_details.html', context)

#     else:
#         initial_data = {'new_image': product.image.url if product.image else ''}
#         form = CreateProductForm(instance=product, initial=initial_data)
#         # print(form)
    
#     context = {
#         'form': form,
#         'product': product,
        
#     }
#     return render(request, 'adminside/admin_products_details.html', context)

# gpt

@login_required(login_url='adminside:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_products_details(request, pid):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    # if not request.user.is_superadmin:
    #     return redirect('adminside:admin_login')

    try:
        product = Product.objects.get(pid=pid)
        product_images = ProductImages.objects.filter(product=product)
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)

    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Save the form including the image
            product = form.save(commit=False)
            product_image = form.cleaned_data['new_image']
            if product_image is not None:
                product.image = product_image
            product.save()

            # Update or create additional images
            for i in product_images:
                image_field_name = f'product_image{i.id}'
                image = request.FILES.get(image_field_name)

                if image:
                    i.Images = image
                    i.save()

            return redirect('admindash:admin_products_list')
        else:
            print(form.errors)
            context = {
                'form': form,
                'product': product,
                'product_images': product_images,
            }
            return render(request, 'adminside/admin_products_details.html', context)
    else:
        initial_data = {'new_image': product.image.url if product.image else ''}
        form = CreateProductForm(instance=product, initial=initial_data)

    context = {
        'form': form,
        'product': product,
        'product_images': product_images,
    }
    return render(request, 'adminside/admin_products_details.html', context)


#gtp









# def admin_products_details(request, pid):
#     print(pid)
#     if not request.user.is_authenticated:
#         return redirect('adminside:admin_login')

#     try:
#         product = Product.objects.get(pid=pid)
#     except Product.DoesNotExist:
#         return HttpResponse("Product not found", status=404)

#     ProductImagesFormSet = inlineformset_factory(Product, ProductImages, form=ProductImagesForm)

#     if request.method == 'POST':
#         ProductImagesFormSet = inlineformset_factory(Product, ProductImages, form=ProductImagesForm)
#         product_form = CreateProductForm(request.POST, request.FILES, instance=product)
#         images_formset = ProductImagesFormSet(request.POST, request.FILES, instance=product)

#         if product_form.is_valid() and images_formset.is_valid():
#             product = product_form.save(commit=False)
#             product.image = product_form.cleaned_data['new_image']
#             product.save()

#             images_formset.save()

#             return redirect('admindash:admin_products_list')
#         else:
#             print(product_form.errors)
#             print(images_formset.errors)

#             context = {
#                 'product_form': product_form,
#                 'images_formset': images_formset,
#                 'product': product,
#             }

#             return render(request, 'adminside/admin_products_details.html', context)

#     else:
#         initial_data = {'new_image': product.image.url if product.image else ''}
#         product_form = CreateProductForm(instance=product, initial=initial_data)
#         images_formset = ProductImagesFormSet(instance=product)

#     context = {
#         'product_form': product_form,
#         'images_formset': images_formset,
#         'product': product,
#     }

#     return render(request, 'adminside/admin_products_details.html', context)






  

@login_required(login_url='adminside:admin_login') 
def block_unblock_products(request, pid):
    
  if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
  product = get_object_or_404(Product, pid=pid)
  if product.status:
    product.status=False
  else:
      product.status=True
  product.save()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
  
    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def add_product(request):
#     if not request.user.is_authenticated:
#         return HttpResponse("Unauthorized", status=401)
#     categories = Category.objects.all()
   

#     if request.method == 'POST':
#         product_name= request.POST.get('title')
#         product_stock_count= request.POST.get('stock_count')
#         description= request.POST.get('description')
#         max_price= request.POST.get('old_price')
#         sale_price= request.POST.get('price')
#         category_name= request.POST.get('category')
        
       
       

#         category = get_object_or_404(Category, title=category_name)
        

#         product = Product(
#             title=product_name,
#             stock_count=product_stock_count,
#             category=category,
            
#             description=description,
#             old_price=max_price,
#             price=sale_price,
#             image=request.FILES['image_feild']  # Make sure your file input field is named 'product_image'
#         )
#         product.save()
        

#         return redirect('admindash:admin_products_list')
#     else:
#         form=CreateProductForm()
#     content = {
#         'categories': categories,
          
#         'form': form
#     }
#     return render(request,'adminside/admin_add_product.html', content)


# new add produt


@login_required(login_url='adminside:admin_login')
def add_product(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    categories = Category.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('title')
        product_stock_count = request.POST.get('stock_count')
        description = request.POST.get('description')
        max_price = request.POST.get('old_price')
        sale_price = request.POST.get('price')
        category_name = request.POST.get('category')
        # validations
        validation_errors = []

        try:
            product_stock_count = int(product_stock_count)
            if product_stock_count < 0:
                validation_errors.append("Stock Count must be a non-negative integer.")

            max_price = float(max_price)
            if max_price < 0:
                validation_errors.append("Max Price must be a non-negative number.")

            sale_price = float(sale_price)
            if sale_price < 0:
                validation_errors.append("Sale Price must be a non-negative number.")
        except ValueError as e:
            validation_errors.append(str(e))

        if validation_errors:
            form_data = {
                'title': product_name,
                'stock_count': product_stock_count,
                'description': description,
                'old_price': max_price,
                'price': sale_price,
                'category': category_name,
            }
            form = CreateProductForm()
            content = {
                'categories': categories,
                'form': form,
                'additional_image_count': range(1, 4),
                'error_messages': validation_errors,
                'form_data': form_data,
            }
            return render(request, 'adminside/admin_add_product.html', content)
        
        # till here
        

        category = get_object_or_404(Category, title=category_name)

        product = Product(
            title=product_name,
            stock_count=product_stock_count,
            category=category,
            description=description,
            old_price=max_price,
            price=sale_price,
            image=request.FILES['image_feild']
        )
        product.save()

        # Handling additional images
        additional_image_count = 5  # Change this to the desired count of additional images
        for i in range(1, additional_image_count + 1):
            image_field_name = f'product_image{i}'
            image = request.FILES.get(image_field_name)
            if image:
                ProductImages.objects.create(product=product, Images=image)

        return redirect('admindash:admin_products_list')
    else:
        form = CreateProductForm()
        form_data = {
            'title': '',
            'stock_count': '',
            'description': '',
            'old_price': '',
            'price': '',
            'category': '',
        }

    content = {
        'categories': categories,
        'form': form,
         'additional_image_count': range(1, 4), 
         'form_data': form_data,
    }
    return render(request, 'adminside/admin_add_product.html', content)


#ends here

@login_required(login_url='adminside:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_product(request,pid):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    try:
        product = Product.objects.get(pid=pid)
        product.delete()
        return redirect('admindash:admin_products_list')
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)
    
    
    
@login_required(login_url='adminside:admin_login')  
def admin_category_list(request):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    
    categories = Category.objects.all()
    
    context = {
        'categories':categories
    }
    
    return render(request,'adminside/admin_category_list.html',context)


@login_required(login_url='adminside:admin_login')
def admin_add_category(request):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    if request.method == 'POST':
        cat_title = request.POST.get('category_name')
        if Category.objects.filter(title=cat_title).exists():
            messages.error(request, 'Category with this title already exists.')
        else:
            cat_data = Category(title=cat_title, image=request.FILES.get('category_image'))
            cat_data.save()
            messages.success(request, 'Category added successfully.')
        
        
        # cat_data = Category(title=cat_title,
        #                     image=request.FILES.get('category_image'))
    
        # cat_data.save()
    else:
        return render(request, 'adminside/admin_category_list.html')
    
    return render(request, 'adminside/admin_category_list.html')




# def admin_category_edit(request, cid):
    if not request.user.is_authenticated:
        return redirect('adminside:admin_login')

    # Using get_object_or_404 to get the Category or return a 404 response if it doesn't exist
    categories = get_object_or_404(Category, cid=cid)
    categories_title=categories.title
    categories_image=categories.image
    
    context={
        'categories_title':categories_title,
        'categories_image':categories_image
    }

    if request.method == 'POST':
        # Update the fields of the existing category object
        cat_title = request.POST.get("category_name")
        cat_image = request.FILES.get('category_image')
        categories_title=cat_title
        categories_image=cat_image
        
        categories.save()
        

        # Save the changes to the database
        return redirect('admindash:admin_category_list')
    
   
        

    # context = {
    #     "categories": categories
    # }

    # Render the template even for GET requests to display the form
    return render(request, 'adminside/admin_category_edit.html', context)
@login_required(login_url='adminside:admin_login')
def admin_category_edit(request, cid):
    if not request.user.is_authenticated:
        return redirect('adminside:admin_login')

    # Using get_object_or_404 to get the Category or return a 404 response if it doesn't exist
    categories = get_object_or_404(Category, cid=cid)

    if request.method == 'POST':
        # Update the fields of the existing category object
        cat_title = request.POST.get("category_name")
        cat_image = request.FILES.get('category_image')

        # Update the category object with the new title and image
        categories.title = cat_title
        if cat_image is not None:
            categories.image = cat_image

        
        # Save the changes to the database
        categories.save()

        # Redirect to the category list page after successful update
        return redirect('admindash:admin_category_list')

    # If the request method is GET, render the template with the category details
    context = {
        "categories_title": categories.title,
        "categories_image": categories.image,
    }

    return render(request, 'adminside/admin_category_edit.html', context)



@login_required(login_url='adminside:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_category(request,cid):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    try:
        category=Category.objects.get(cid=cid)
    except ValueError:
        return redirect('admindash:admin_category_list')
    category.delete()

    return redirect('admindash:admin_category_list')


@login_required(login_url='adminside:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def available_category(request,cid):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    category = get_object_or_404(Category, cid=cid)
    
    if category.is_blocked:
        category.is_blocked=False
       
    else:
        category.is_blocked=True
    category.save()

    
    # cat_list=Category.objects.filter(parent_id=category_id)
    # for i in cat_list.values():
    #     print(i)
    
    # for category in cat_list:
    #     if category.is_available:
    #         category.is_available=False
    #     else:
    #         category.is_available=True
    #     category.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))







# order management
@login_required(login_url='adminside:admin_login')
def order_list(request):
    if not request.user.is_authenticated and not request.user.is_superadmin:
        
        return redirect('adminside:admin_login')
    order=CartOrder.objects.all().order_by("-id")
    p=Paginator(CartOrder.objects.all().order_by("-id"),10)
    page=request.GET.get('page')
    orders=p.get_page(page)
    

    context = {
        'order': order,
        'orders':order
       
    }
    
        
    
    
    return render(request, 'adminside/order-list.html',{
        'order':order,'orders':orders
    })
    
    
    
@login_required(login_url='adminside:admin_login')   
def update_product_status(request, id):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    if request.method == 'POST':
        new_status = request.POST.get('product_status')
        order = get_object_or_404(CartOrder, id=id)
        order.product_status = new_status
        order.save()
        
        products = CartOrderItems.objects.filter(order=order)
        for p in products:
            productss = Product.objects.filter(title=p.item)
            for s in productss:
                s.stock_count = int(s.stock_count) + p.qty
                s.save()

    # Redirect back to the original page or a specific URL
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    
def admin_order_detail(request,id):
    order = get_object_or_404(CartOrder, id=id)
    print(order)

    # Use filter based on the specific order instance
    products = CartOrderItems.objects.filter(order=order)

    context = {
        'products': products,
        'order': order,
    }
    
    return render(request,'adminside/admin-order-detail.html',context)





    
    
# admin cancel order

# def admin_cancel_order(request,id):
#     order = get_object_or_404(CartOrder, id=id)
#     print(order)
#     order.product_status='cancelled'
#     order.save()
#     products = CartOrderItems.objects.filter(order=order)
#     for p in products:
#         print(p.item)
#         productss=Product.objects.filter(title=p.item)
#         for s in productss:
#             print(s.stock_count)
#             s.stock_count = int(s.stock_count)+p.qty
#             s.save()
            
            
            
    
    
    
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    

    
@login_required(login_url='adminside:admin_login')      
def admin_cancel_order(request, id):
    # if not request.user.is_superadmin:
    #     return redirect('adminside:admin_login')
    order = get_object_or_404(CartOrder, id=id)
    # user_wallet = get_object_or_404(wallet, user=request.user)
    user_wallet, created = wallet.objects.get_or_create(user=request.user)

    if order.product_status == 'cancelled':
        messages.warning(request, f"Order {order.id} is already cancelled.")
    else:
        # Update order status to 'cancelled'
        order.product_status = 'cancelled'
        order.wallet_status=True
        order.save()
        
        if order.paid_status==True:
            user_wallet.Amount+=order.price
            # credit=order.price
            # request.session['credit']=credit
            user_wallet.save()
            messages.warning(request,"Refund amount has been added to the wallet")
            

        # Update product stock count
        products = CartOrderItems.objects.filter(order=order)
        for p in products:
            productss = Product.objects.filter(title=p.item)
            for s in productss:
                s.stock_count = int(s.stock_count) + p.qty
                s.save()

        messages.success(request, f"Order {order.id} has been cancelled successfully.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))    


@login_required(login_url='adminside:admin_login')
def admin_coupon(request):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    coupon=Coupon.objects.all()
    
    
    context={
        'coupon':coupon
    }
    return render(request,'adminside/admin-coupon.html',context)

@login_required(login_url='adminside:admin_login')
def create_coupon(request):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    if request.method == 'POST':
        code = request.POST['code']
        discount = request.POST['discount']
        active = request.POST.get('active') == 'on'
        active_date = request.POST['active_date']
        expiry_date = request.POST['expiry_date']

        # Check if active_date is not greater than expiry_date
        if active_date > expiry_date:
            messages.error(request, 'Active date should not be greater than expiry date')
            return render(request, 'adminside/create-coupon.html')

        # Check if the coupon with the same code already exists
        if Coupon.objects.filter(code=code).exists():
            messages.error(request, f'Coupon with code {code} already exists')
            return render(request, 'adminside/create-coupon.html')

        coupon = Coupon(
            code=code,
            discount=discount,
            active=active,
            active_date=active_date,
            expiry_date=expiry_date
        )
        coupon.save()
        messages.success(request, 'Coupon created successfully')
        return redirect('admindash:admin-coupon')

    return render(request, 'adminside/create-coupon.html')


@login_required(login_url='adminside:admin_login')
def edit_coupon(request,id):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    
    coupon_code = get_object_or_404(Coupon, id=id)
    print(f'Active Date: {coupon_code.active_date}')
    if request.method == 'POST':
        code = request.POST['code']
        discount = request.POST['discount']
        active = request.POST.get('active') == 'on'
        active_date = request.POST['active_date']
        expiry_date = request.POST['expiry_date']
        

        # Check if active_date is not greater than expiry_date
        if active_date > expiry_date:
            messages.error(request, 'Active date should not be greater than expiry date')
            return render(request, 'adminside/create-coupon.html')
        
        coupon_code.code=code
        coupon_code.discount=discount
        coupon_code.active_date=active_date
        coupon_code.expiry_date=expiry_date
        coupon_code.active=active
        coupon_code.save()
        messages.success(request, 'Coupon Updated successfully')
        return redirect('admindash:admin-coupon')
    
        
    
    return render (request, 'adminside/edit-coupon.html',{'coupon_code':coupon_code})


@login_required(login_url='adminside:admin_login')        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_coupon(request,id):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    
    try:
        coupon= get_object_or_404(Coupon, id=id)
    except ValueError:
        return redirect('admindash:admin-coupon')
    coupon.delete()
    messages.warning(request,"Coupon has been deleted successfully")

    return redirect('admindash:admin-coupon')
    


  