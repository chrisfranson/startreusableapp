from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class IndexView(View):
    template_name = '$app_name/index.html'

    def get(self, request):
        context = {
            'content': "$app_name Index"
        }
        return render(request, self.template_name, context)
