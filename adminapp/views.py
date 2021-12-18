from django.db.models import F
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     context = {
#         'object_list': ShopUser.objects.all().order_by('-is_active')
#     }
#     return render(request, 'adminapp/users.html', context)


class AccessMixin:

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))
    else:
        user_form = ShopUserAdminEditForm(instance=current_user)

    context = {
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        if current_user.is_active:
            current_user.is_active = False
        else:
            current_user.is_active = True
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:user_list'))
    context = {
        'object': current_user
    }
    return render(request, 'user_delete.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     context = {
#
#     }
#     return render(request, '', context)


class ProductCategoryCreateView(AccessMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    success_url = reverse_lazy('adminapp:category_list')
    # fields = '__all__'
    form_class = ProductCategoryEditForm


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'object_list': ProductCategory.objects.all().order_by('-is_active')
    }
    return render(request, 'adminapp/categories.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request):
#     context = {
#
#     }
#     return render(request, '', context)


class ProductCategoryUpdateView(AccessMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:category_list')
    # fields = '__all__'
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование категории'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data.get('discount')
            if discount:
                self.object.product_set.update(
                    price=F('price') * (1 - discount/100)
                )
        return super().form_valid(form)


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request):
#     context = {
#
#     }
#     return render(request, '', context)


class ProductCategoryDeleteView(AccessMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:category_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        return HttpResponseRedirect(self.success_url)

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request):
#     context = {
#
#     }
#     return render(request, '', context)


class ProductCreateView(AccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('adminapp:product_list', args=[self.kwargs['pk']])


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     context = {
#         'category': get_object_or_404(ProductCategory, pk=pk),
#         'object_list': Product.objects.filter(category__pk=pk).order_by('-is_active')
#     }
#     return render(request, 'adminapp/products.html', context)


class ProductsListView(AccessMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request):
#     context = {
#
#     }
#     return render(request, '', context)


class ProductUpdateView(AccessMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request):
#     context = {
#
#     }
#     return render(request, '', context)


class ProductDeleteView(AccessMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(reverse('adminapp:product_list', args=[self.object.category_id]))


# @user_passes_test(lambda u: u.is_superuser)
# def product_detail(request):
#     context = {
#
#     }
#     return render(request, '', context)


class ProductDetailView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'
