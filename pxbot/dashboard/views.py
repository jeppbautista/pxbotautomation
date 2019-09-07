import datetime

from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View, generic
from django.contrib import messages

from .models import User
from .forms import UserCreateForm, UserEditForm, UserUpdateActiveForm
from .crawler import pxbot as px

import logging

logger = logging.getLogger(__name__)


class DashView(View):
    def get(self, request):
        total_users = User.objects.count()
        total_active = User.objects.filter(is_active=True).count()
        total_inactive = User.objects.filter(is_active=False).count()

        top_earners = User.objects.order_by('-total_earned')[:5]
        ready_for_buying = User.objects.order_by('-payout')[:5]
        near_expiration = User.objects.order_by('-expiration')[:5]
        # near_px_expiration = User.objects.order_by('-px_expiration')[:5]
        px_expirations = User.objects.filter(px_expiration="Never")[:5]

        return render(request, 'dashboard/index.html', {'header': 'Admin dashboard', 'total_users': total_users,
                                                        'total_inactive': total_inactive, 'total_active': total_active,
                                                        'top_earners': top_earners, 'ready_for_buying': ready_for_buying,
                                                        'near_expiration': near_expiration, 'near_px_expiration': px_expirations})


class UserView(generic.ListView):
    model = User
    paginate_by = 10
    template_name = 'dashboard/users.html'

    def get_queryset(self):
        return User.objects.all().order_by('username')

    def post(self, request):
        id = request.POST['user_id']
        instance = User.objects.get(id=id)
        form = UserUpdateActiveForm(request.POST, instance=instance)

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
    # try:
    #     users = User.objects.filter(is_active=True)
    # except User.DoesNotExist:
    #     return HttpResponseRedirect(reverse("dashboard:index"))
    #
    # pxbot = px.Pxbot()
    # wallet = 'payout'
    #
    # for user in users:
    #     if pxbot.authenticate(user.username, user.password):
    #         metrics = pxbot.init_update()
    #         if metrics['expired'] != "Never":
    #             while metrics['earnings'] + metrics[wallet] >= 10.0:
    #                 if 'successfully' in pxbot.transfer_finance(metrics['earnings'], wallet):
    #                     metrics['earnings'] -= 10
    #                     pxbot.buy_revshares(wallet)
    #
    #         elif metrics['expired'] == "Never":
    #             while metrics['earnings'] >= 25:
    #                 if 'successfully' in pxbot.transfer_finance(25, wallet):
    #                     metrics['earnings'] -= 25
    #                     pxbot.upgrade_membership(wallet)
    #
    #         user.deposit = metrics['deposit']
    #         user.payout = metrics['payout']
    #         user.earnings = metrics['earnings']
    #         user.total_earned = metrics['total_earned']
    #         user.px_expiration = metrics['expired']
    #         user.save()
    #         pxbot.end()
    #     else:
    #         print("User does not exist: {}".format(user.username))

    return HttpResponseRedirect(reverse("dashboard:index"))


def expiration(request):
    for user in User.objects.filter(is_active=True):
        print(datetime.date.today())
        print(user.expiration)
        if datetime.date.today() >= user.expiration:
            user.is_active = False
            user.save()

    return HttpResponseRedirect(reverse("dashboard:index"))