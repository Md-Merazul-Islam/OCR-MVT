from django.shortcuts import render
from ocr.models import OCRResult
from django.db.models import Count
from django.utils import timezone
import pandas as pd
import plotly.express as px
from django.shortcuts import render
from django.db.models import Count, Sum

def home(request):
    end_date = timezone.now().date()
    start_date = end_date - timezone.timedelta(days=30)

    # Filter results for the last 30 days
    ocr_results_last_30_days = OCRResult.objects.filter(uploaded_at__date__range=[start_date, end_date])
    total_days = (end_date - start_date).days + 1
    total_transactions_last_30_days = ocr_results_last_30_days.count()
    total_amount_last_30_days = ocr_results_last_30_days.aggregate(total_amount=Sum('monto'))['total_amount'] or 0

    # Filter results for today
    ocr_results_today = OCRResult.objects.filter(uploaded_at__date=end_date)
    total_transactions_today = ocr_results_today.count()
    total_amount_today = ocr_results_today.aggregate(total_amount=Sum('monto'))['total_amount'] or 0

    # Get transaction counts by date for the graph
    data = ocr_results_last_30_days.extra({'date': 'DATE(uploaded_at)'}).values('date').annotate(count=Count('id')).order_by('date')
    dates = [entry['date'] for entry in data]
    counts = [entry['count'] for entry in data]

    context = {
        'dates': dates,
        'counts': counts,
        'total_amount_today': total_amount_today,
        'total_transactions_today': total_transactions_today,
        'total_amount_last_30_days': total_amount_last_30_days,
        'total_transactions_last_30_days': total_transactions_last_30_days,
    }
    return render(request, 'index.html', context)




def About(request):
    return render(request, 'about.html')





def graph_view(request):
    ocr_results = OCRResult.objects.all().order_by('uploaded_at')
    data = {
        'date': [result.uploaded_at.date() for result in ocr_results],
        'amount': [result.monto for result in ocr_results]  
    }
    df = pd.DataFrame(data)
    start_date = df['date'].min()
    end_date = df['date'].max()
    all_dates = pd.date_range(start=start_date, end=end_date).date
    full_date_df = pd.DataFrame({'date': all_dates})
    df = full_date_df.merge(df, on='date', how='left').fillna(0)
    fig = px.line(df, x='date', y='amount', labels={'date': 'Upload Date', 'amount': 'Amount'}, title='All transaction ')
    graph_html = fig.to_html(full_html=False)
    return render(request, 'graph.html', {'graph': graph_html})
