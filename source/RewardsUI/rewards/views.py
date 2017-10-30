import logging
import requests
from django.http import  HttpResponse
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
import json


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        print('in Rewardsview - get')

        response = requests.get("http://rewardsservice:7050/rewards")
        context['rewards_data'] = response.json()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )


class CustomersView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger
        print('in customers view init')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        print('in Customersview - get')

        response = requests.get("http://rewardsservice:7050/customers")
        context['customers_data'] = response.json()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
