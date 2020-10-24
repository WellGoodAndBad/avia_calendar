from api_test_work.models import PriceOfTicket
from django.views.generic.list import ListView


class CaledarPageView(ListView):
    model = PriceOfTicket
    template_name = "avia_calendar/home.html"
    context_object_name = "posts"
    ordering = ['date']

