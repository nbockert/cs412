from django.shortcuts import render
from django.views.generic import ListView,DetailView
import datetime
from django.db.models.query import QuerySet
# Create your views here.
from .models import Voter
from typing import Any


import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go
from django.db.models import Count
from django import forms
from .forms import VoterFilterForm
from django.db.models import Count
from django.db.models.functions import ExtractYear

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'  # Template file for listing voters
    context_object_name = 'voters'  # Context name to use in the template
    paginate_by = 100  # Display 100 voters per page
   
    def get_queryset(self) -> QuerySet[Any]:
        '''Limit the results to a small number of records'''
        print(self.request.GET)
        queryset = super().get_queryset().order_by('last_name', 'first_name')
        # Get filter criteria from GET parameters
        party_affiliation = self.request.GET.get('party_affiliation')
        min_birth_year = self.request.GET.get('min_birth_year')
        max_birth_year = self.request.GET.get('max_birth_year')
        voter_score = self.request.GET.get('voter_score')
        
        # Election participation filters
        elections = {
            'v20state': self.request.GET.get('v20state'),
            'v21town': self.request.GET.get('v21town'),
            'v21primary': self.request.GET.get('v21primary'),
            'v22general': self.request.GET.get('v22general'),
            'v23town': self.request.GET.get('v23town'),
        }

        # Apply filters
        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)
        if min_birth_year:
            queryset = queryset.filter(date_of_birth__year__gte=min_birth_year)
        if max_birth_year:
            queryset = queryset.filter(date_of_birth__year__lte=max_birth_year)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        
        for election, participated in elections.items():
            if participated == 'on':
                queryset = queryset.filter(**{election: True})

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the current filters to the context for form persistence
        context['party_affiliation_choices'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        current_year = datetime.datetime.now().year
        context['years'] = range(current_year, 1900, -1)
        context['voter_score_choices'] = Voter.objects.values_list('voter_score', flat=True).distinct()
        context['selected_filters'] = self.request.GET
        return context


class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voter = self.get_object()
        # Create Google Maps URL for the address
        address = f"{voter.address_street}+Newton+MA+{voter.address_zip}"
        context['map_url'] = f"https://www.google.com/maps/search/?api=1&query={address}"
        return context




class VoterGraphsView(ListView):
    """View to display voter analytics graphs"""
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Get filtered queryset
            queryset = self.get_queryset()
            
            # Add filter form to context
            context['form'] = VoterFilterForm(self.request.GET)
            
            # Create graphs
            context['birth_year_graph'] = self.create_birth_year_histogram(queryset)
            context['party_graph'] = self.create_party_pie_chart(queryset)
            context['election_graph'] = self.create_election_histogram(queryset)
            
            # Add summary statistics
            context['voter_count'] = queryset.count()
            
        except Exception as e:
            context['error'] = f"Error generating graphs: {str(e)}"
        
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)
        
        if form.is_valid():
            if party := form.cleaned_data.get('party_affiliation'):
                queryset = queryset.filter(party_affiliation=party)
                
            if min_year := form.cleaned_data.get('min_birth_year'):
                queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
                
            if max_year := form.cleaned_data.get('max_birth_year'):
                queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
                
            if score := form.cleaned_data.get('voter_score'):
                queryset = queryset.filter(voter_score=int(score))
                
            # Election participation filters
            for election in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if form.cleaned_data.get(election):
                    queryset = queryset.filter(**{election: True})
        
        return queryset

    def create_birth_year_histogram(self, queryset):
        """Create simple histogram of voter birth years"""
        birth_years = (
            queryset
            .annotate(birth_year=ExtractYear('date_of_birth'))
            .values('birth_year')
            .annotate(count=Count('id'))
            .order_by('birth_year')
        )
        
        fig = go.Figure(data=[
            go.Bar(
                x=[year['birth_year'] for year in birth_years],
                y=[year['count'] for year in birth_years],
                text=[year['count'] for year in birth_years],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Voter Distribution by Birth Year',
            xaxis_title='Birth Year',
            yaxis_title='Number of Voters',
            showlegend=False,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig.to_html(full_html=False)

    def create_party_pie_chart(self, queryset):
        """Create simple pie chart of party affiliations"""
        party_counts = (
            queryset
            .values('party_affiliation')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        fig = go.Figure(data=[
            go.Pie(
                labels=[party['party_affiliation'] for party in party_counts],
                values=[party['count'] for party in party_counts],
                textinfo='label+percent',
            )
        ])
        
        fig.update_layout(
            title='Voter Distribution by Party Affiliation',
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
            showlegend=True
        )
        
        return fig.to_html(full_html=False)

    def create_election_histogram(self, queryset):
        """Create histogram of election participation"""
        elections = {
            'v20state': '2020 State',
            'v21town': '2021 Town',
            'v21primary': '2021 Primary',
            'v22general': '2022 General',
            'v23town': '2023 Town'
        }
        
        participation = []
        for field, name in elections.items():
            count = queryset.filter(**{field: True}).count()
            participation.append({
                'election': name,
                'count': count
            })
        
        fig = go.Figure(data=[
            go.Bar(
                x=[p['election'] for p in participation],
                y=[p['count'] for p in participation],
                text=[p['count'] for p in participation],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Voter Participation by Election',
            xaxis_title='Election',
            yaxis_title='Number of Voters',
            showlegend=False,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig.to_html(full_html=False)