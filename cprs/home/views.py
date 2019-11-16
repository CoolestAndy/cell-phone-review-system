from django.shortcuts import render
from django.views import View

class HomeView(View):
    template = 'home/index.html'

    def get(self, request):
        return render(request, self.template)

class SignInView(View):
    template = 'home/sign-in.html'

    def get(self, request):
        return render(request, self.template)

class DetailsView(View):
    template = 'home/details.html'

    def get(self, request):
        return render(request, self.template)
