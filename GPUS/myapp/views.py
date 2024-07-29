# views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Sum,Avg,functions as Fu
from .models import Performance
import datetime
from .forms import PerformanceForm 
from django.views.decorators.http import require_POST

def home(request):
    return render(request, 'home.html')

from django.db.models import Sum, Avg, F, Q, Case, When, IntegerField
import datetime

def performance_pivot(request):
    performances = Performance.objects.all()

    selected_year = request.GET.get('year', None)
    selected_month = request.GET.get('month', None)

    # Apply filters if provided
    if selected_year:
        performances = performances.filter(date__year=selected_year)
    
    if selected_month:
        performances = performances.filter(date__month=selected_month)

    # Group by month and year
    pivot_data = performances.annotate(
        month=F('date__month'),
        year=F('date__year')
    ).values('month', 'year').annotate(
        total_Tonnage_dosage=Sum('Tonnage_dosage'),
        total_Humidite_entree=Avg(
            Case(
                When(Humidite_entree__gt=0, then='Humidite_entree'),
                default=None
            )
        ),
        total_Production_totale=Sum('Production_totale'),
        total_HM=Sum('HM'),
        total_Cs_Gas=Avg(
            Case(
                When(Cs_Gas__gt=0, then='Cs_Gas'),
                default=None
            )
        ),
        total_Cs_gazoline=Avg(
            Case(
                When(Cs_gazoline__gt=0, then='Cs_gazoline'),
                default=None
            )
        ),
        total_Cs_Fuel=Avg(
            Case(
                When(Cs_Fuel__gt=0, then='Cs_Fuel'),
                default=None
            )
        ),
    ).order_by('year', 'month')

    # Prepare month choices
    month_choices = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]

    current_year = datetime.date.today().year
    return render(request, 'performance.html', {
        'pivot_data': pivot_data,
        'month_choices': month_choices,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'current_year': current_year,
    })

def performance_daily(request, year, month):
    performances = Performance.objects.filter(date__year=year, date__month=month).order_by('date')
    return render(request, 'performance_daily.html', {
        'performances': performances,
        'year': year,
        'month': month
    })

    # Filter performances for the given year and month
    performances = Performance.objects.filter(
        date__year=year, date__month=month
    ).order_by('date')

    context = {
        'year': year,
        'month': month,
        'performances': performances,
    }
    return render(request, 'performance_daily.html', context)


def add_performance(request):
    if request.method == 'POST':
        form = PerformanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('performance')  # Redirigez vers la vue de performance après l'ajout
    else:
        form = PerformanceForm()
    
    return render(request, 'add_performance.html', {'form': form})



@require_POST
def delete_performance(request, year, month, performance_id):
    performance = get_object_or_404(Performance, id=performance_id)
    performance.delete()
    return redirect('performance_daily', year=year, month=month)





# views.py

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from .models import Performance
import matplotlib.dates as mdates
from django.db.models.functions import TruncMonth
from django.utils.dateparse import parse_date
import calendar

# views.py
def graph_performance(request):
    attribute = request.GET.get('attribute', 'Tonnage_dosage')
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')

    performances = Performance.objects.all().order_by('date')
    if year and month:
        performances = performances.filter(date__year=year, date__month=month)
    elif year:
        performances = performances.filter(date__year=year)
    elif month:
        performances = performances.filter(date__month=month)

    dates = [performance.date for performance in performances]
    values = [getattr(performance, attribute) for performance in performances]

    plt.figure(figsize=(18, 6))
    plt.bar(dates, values, color='b')
    plt.title(f'{attribute} over Time')
    plt.xlabel('Date')
    plt.ylabel(attribute)
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')

    for i, (date, value) in enumerate(zip(dates, values)):
        plt.text(date, value, f'{value}', ha='center', va='bottom')

    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    plt.subplots_adjust(left=0.05)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    years = Performance.objects.dates('date', 'year', order='DESC').distinct()
    months = list(calendar.month_name)[1:]

    context = {
        'plot_data': plot_data,
        'attribute': attribute,
        'years': years,
        'months': months,
        'selected_year': year,
        'selected_month': month,
    }
    return render(request, 'graph_performance.html', context)




def edit_performance(request, year, month, performance_id):
    performance = get_object_or_404(Performance, id=performance_id)
    
    if request.method == 'POST':
        form = PerformanceForm(request.POST, instance=performance)
        if form.is_valid():
            form.save()
            return redirect('performance_daily', year=year, month=month)
    else:
        form = PerformanceForm(instance=performance)
    
    return render(request, 'edit_performance.html', {'form': form, 'year': year, 'month': month})


