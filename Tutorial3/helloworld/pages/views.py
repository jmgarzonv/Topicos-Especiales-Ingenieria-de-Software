from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Comment
from django.shortcuts import render, redirect
from django.views import View
from .utils import ImageLocalStorage  # Asegurar que está bien importado


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "About us - Online Store",
                "subtitle": "About us",
                "description": "This is an about page ...",
                "author": "Developed by: JUAN GARZON",
            }
        )
        return context


class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.objects.all(),  # Acceder a la base de datos
        }
        return render(request, self.template_name, viewData)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["description"]


class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        form = CommentForm()
        viewData = {
            "title": f"{product.name} - Online Store",
            "subtitle": f"{product.name} - Product Information",
            "product": product,
            "form": form,
        }
        return render(request, self.template_name, viewData)

    def post(self, request, id):
        product = get_object_or_404(Product, pk=id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product  # Asociar el comentario al producto
            comment.save()
            return redirect("show", id=product.id)  # Redirigir al producto
        else:
            viewData = {
                "title": f"{product.name} - Online Store",
                "subtitle": f"{product.name} - Product Information",
                "product": product,
                "form": form,
            }
            return render(request, self.template_name, viewData)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price


class ProductCreateView(View):
    template_name = "products/create.html"

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create Product",
            "form": form,
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar en la base de datos
            return redirect("index")  # Redirigir a la lista de productos
        else:
            viewData = {
                "title": "Create Product",
                "form": form,
            }
            return render(request, self.template_name, viewData)
class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        # Simulación de base de datos de productos
        products = {
            121: {'name': 'Tv samsung', 'price': '1000'},
            11: {'name': 'Iphone', 'price': '2000'}
        }

        # Obtener productos del carrito desde la sesión
        cart_products = {}
        cart_product_data = request.session.get('cart_product_data', {})

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        # Preparar los datos para la vista
        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products
        }

        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        # Agregar un producto al carrito en la sesión
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data[product_id] = product_id
        request.session['cart_product_data'] = cart_product_data

        return redirect('cart_index')
    
class CartRemoveAllView(View):
    def post(self, request):
        # Eliminar todos los productos del carrito en la sesión
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']

        return redirect('cart_index')
    
def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'images/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')

    return ImageView

class ImageViewNoDI(View):
    template_name = 'images/index.html'

    def get(self, request):
        image_url = request.session.get('image_url', '')
        return render(request, self.template_name, {'image_url': image_url})

    def post(self, request):
        image_storage = ImageLocalStorage()  # Se instancia directamente aquí
        image_url = image_storage.store(request)
        request.session['image_url'] = image_url
        return redirect('imagenodi_index')
