from django.views import generic


class TempView(generic.TemplateView):
    template_name = 'accounts/top.html'
