from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from carts.models import Cart
from .models import Product, ProductManager
from viewed_products.models import Viewed_Product_User, Viewed_Product_User_Manager, Viewed_Product_Object


class ProductFeaturedListView(ListView):
    template_name = "products/list.html"


    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all().featured() 
    template_name = "products/featured-detail.html"



class ProductListView(ListView):
    context_object_name = 'list'
    template_name = "products/list.html"
    queryset = Product.objects.all()

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()

    
    def all(self):
        print("all")
        return self.get_queryset().active()

    def get_context_data(self, *args, **kwargs):
        user_session = Viewed_Product_User.objects.new_or_get(self.request)

        user_viewed_objects = Viewed_Product_Object.objects.filter(user=user_session[0]).order_by('-id')

        object_list = Product.objects.all()

        context = {
            'object_list': object_list,
            'user_viewed_objects': user_viewed_objects,

        }

        return context

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self. request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not Foud..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm")


        user_session, new_obj = Viewed_Product_User.objects.new_or_get(self.request)

        if slug is not None:
            try:
                product_obj = Product.objects.get(slug=slug, active=True)
                product_obj_filtered = Product.objects.filter(slug=slug, active=True).values_list('title')
            except Product.DoesNotExist:
                print("Show message to user, product is gone?")
                return redirect("viewed_product_user:home")
            user_viewed_objects_title_values = Viewed_Product_Object.objects.filter(user=user_session).values_list('title')
            print('user_viewed_objects:  ', user_viewed_objects_title_values) 
            print('product_obj---------: ', product_obj_filtered)


            product_in_the_set = False
            if not user_viewed_objects_title_values:
                Viewed_Product_Object.objects.create(user=user_session, title=product_obj.title,
                    slug=product_obj.title, description=product_obj.description, 
                    image=product_obj.image, price=product_obj.price, 
                    featured=product_obj.featured, active=product_obj.active)
                
                user_viewed_objects_title_values = Viewed_Product_Object.objects.filter(user=user_session).values_list('title')


            for obj in user_viewed_objects_title_values:
                
                if obj in product_obj_filtered:

                    product_in_the_set = True

                    print('ITS IN there')  
                    break
            if product_in_the_set == False:
                print('NOT IN THERE product_obj_filtered', product_obj_filtered)
                print('obj------', obj)
                Viewed_Product_Object.objects.create(user=user_session, title=product_obj.title, 
                    slug=product_obj.title, description=product_obj.description, 
                    image=product_obj.image, price=product_obj.price, 
                    featured=product_obj.featured, active=product_obj.active)
                   
            user_viewed_products = Viewed_Product_Object.objects.filter(user=user_session).values()

            if len(user_viewed_products) > 5:

                deleting_objects = Viewed_Product_Object.objects.filter(user=user_session)[0:2]
                print('prod objects sliced: ', deleting_objects)
                Viewed_Product_Object.objects.filter(pk__in=Viewed_Product_Object.objects.filter(user=user_session).values_list('pk',flat=True)[0:2]).delete()

            print("user_viewed_objects filtered", user_viewed_objects_title_values)


        return instance


