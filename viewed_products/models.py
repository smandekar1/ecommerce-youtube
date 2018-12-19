import uuid

from django.conf import settings
from django.db import models

from products.models import Product


User = settings.AUTH_USER_MODEL


def upload_image_path(instance, filename):
    print(instance)  
    print(filename)
    new_filename = random.randint(1,3910334555)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )

class Viewed_Product_User_Manager(models.Manager):
    def new_or_get(self, request):
        viewed_product_id = request.session.get("viewed_product_id", None)
        qs = self.get_queryset().filter(id=viewed_product_id)
        if qs.count() == 1:
            new_obj = False
            viewed_product_obj = qs.first()
            if request.user.is_authenticated and viewed_product_obj.user is None:
                viewed_product_obj.user = request.user
                viewed_product_obj.save()
        else:
            viewed_product_obj = Viewed_Product.objects.new(user=request.user)
            new_obj = True
            request.session['viewed_product_id'] = viewed_product_obj.id
        return viewed_product_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Viewed_Product_User(models.Model):
    user        = models.ForeignKey(User,  on_delete=models.CASCADE, null=True, blank=True)

    objects = Viewed_Product_User_Manager()

    # def __str__(self):
    #     return str(self.id)



class Viewed_Product_ObjectQuerySet(models.query.QuerySet):
    def active(self):
        viewed_product_obj = Viewed_Product.objects.filter(user=request.user)

        return self.filter(user=viewed_product_obj)


class Viewed_Product_ObjectManager(models.Manager):

    def get_queryset(self):
        return Viewed_Product_ObjectQuerySet(self.model, using=self.db)

    def all(self):

        return self.get_queryset().all()

class Viewed_Product_Object(models.Model):
    # id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.ForeignKey(Viewed_Product_User,  on_delete=models.CASCADE)
    # products    = models.CharField(max_length=200)
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True)
    description = models.TextField(default='1')
    price       = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image       = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    objects = Viewed_Product_ObjectManager()

    queried_objects = Viewed_Product_ObjectQuerySet()

    # def __str__(self):
    #     return '%s %s' % (self.user, self.title)













