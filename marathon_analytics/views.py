from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from . models import Result
class ResultsListView(ListView):
    '''View to display marathon results'''
    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 50
    def get_queryset(self):
        
        # limit results to first 25 records (for now)
        #default quereyset with all of the records 
        qs = super().get_queryset()
        #handle search form/URL params
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            qs = Result.objects.filter(city__icontains=city) #for case insensitive
        return qs