
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View, generic
from django.contrib import messages

from .models import User
from .forms import  UserCreateForm, UserEditForm, UserUpdateActiveForm


import logging

logger = logging.getLogger(__name__)


class DashView(View):
    def get(self, request):
        total_users = User.objects.count()
        total_active = User.objects.filter(is_active=True).count()
        total_inactive = User.objects.filter(is_active=False).count()
        return render(request, 'dashboard/index.html', {'header': 'Admin dashboard', 'total_users': total_users,
                                                        'total_inactive': total_inactive, 'total_active': total_active})


class UserView(generic.DetailView):
    model = User
    paginate_by = 10
    template_name = 'dashboard/users.html'

    def get_queryset(self):
        return User.objects.all().order_by('username')

    def post(self, request):
        id = request.POST['user_id']
        instance = User.objects.get(id=id)
        form = UserUpdateActiveForm(request.POST, instance=instance)

        print(id)

        if form.is_valid():
            is_active_inst = form.save()
            is_active_inst.save()
            return HttpResponseRedirect(reverse("dashboard:users"))
        return HttpResponseRedirect("")


class UserEditView(generic.edit.UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'dashboard/user_update_form.html'

    def get_success_url(self):
        return reverse("dashboard:users")

    def form_invalid(self, form):
        return HttpResponseRedirect("")


class UserCreateView(generic.edit.CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'dashboard/user_form.html'

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        messages.success(request, "Done!")
        if form.is_valid():
            user = form.save()
            user.save()
            return HttpResponseRedirect(reverse("dashboard:users"))
        return HttpResponseRedirect("")


def selenium_automation(request):
    pxbot.Pxbot()
    # return HttpResponse("Hello Selenium")
