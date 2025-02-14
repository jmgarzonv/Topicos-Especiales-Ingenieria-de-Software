from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Comment


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
