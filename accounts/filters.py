import django_filters
from django_filters import DateFilter 
from .models import *

class DateInput(django_filters.DateFilter):
    input_type = 'date'

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model= Order
        fields = {'product','status'}