from django.shortcuts import render
import requests
from django.core.paginator import Paginator

# Create your views here.
def get_listing_latest(count=10):
    list_format_latest = []
    api_key = 'ace6f6a9-d2fb-410e-b1c1-ef3e904e329d'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'X-CMC_PRO_API_KEY': api_key,
    }
    parameters = {
        'start': '1',
        'limit': str(count),  # Replace 'BTC' with the symbol of the cryptocurrency you want to get
        'sort': 'market_cap',  # Replace 'USD' with the currency you want to convert to
    }
    response = requests.get(url, params=parameters, headers=headers)
    if response.status_code == 200:
        data = response.json()['data']
        for item in data:
            list_format_latest.append({'id': item['id'], 'name': item['name'], 'symbol': item['symbol'],
                                       'price': item['quote']['USD']['price'],
                                       'volume_change_24h': item['quote']['USD']['volume_change_24h'],
                                       'percent_change_24h': item['quote']['USD']['percent_change_24h'],
                                       'market_cap': item['quote']['USD']['market_cap']})
        return list_format_latest
    return None


def index(request):
    list_format_latest = get_listing_latest()
    if list_format_latest:
        return render(request=request, template_name="index.html", context={'list_format_latest': list_format_latest})
    return render(request=request, template_name="index.html", context={'list_format_latest': None})


def about(request):
    return render(request=request, template_name='crypto-about.html')


def market(request):
    list_format_latest = get_listing_latest(30)
    if list_format_latest:
        items_per_page = 10
        paginator = Paginator(list_format_latest, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request=request, template_name='crypto-market.html', context={'page': page})
    return render(request=request, template_name="index.html", context={'list_format_latest': None})


def token(request):
    return render(request=request, template_name='crypto-token.html')


def services(request):
    return render(request=request, template_name='crypto-services.html')


def faqs(request):
    return render(request=request, template_name='crypto-faqs.html')


def whitepapers(request):
    return render(request=request, template_name='crypto-whitepaper.html')



