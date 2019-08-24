from django.shortcuts import render
from django.views import View

class DashView(View):
    def get(self, request):
        return render(request, 'dashboard/index.html', {} )