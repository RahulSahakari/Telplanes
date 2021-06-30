from django.shortcuts import render
from django.http import HttpResponse
import requests, json
from .forms import *


def home(request):
    return render(request, 'airplane/home.html')

def help(request):
    return render(request, 'airplane/help.html')

# Lets the user see the query form and sends the request to the api
def main(request):
    if request.method == 'POST':
        form = AirplaneSearchForm(request.POST)
        if form.is_valid():
            params = {
                'flight_number' : form.cleaned_data['flight_number'],
                'airline_name' : form.cleaned_data['flight_name'],
            }

            url = 'http://api.aviationstack.com/v1/flights?access_key=6ca56f4ac937072abc1f858a7c703668'
            api_result = requests.get(url, params)
            api_data = api_result.json()

            con = {
                # Departure Details
                'flight_status' : api_data['data'][0]['flight_status'].capitalize(),
                'departure_airport' : api_data['data'][0]['departure']['airport'],
                'departure_scheduled': api_data['data'][0]['departure']['scheduled'],
                'departure_estimated': api_data['data'][0]['departure']['estimated'],
                'departure_actual' : api_data['data'][0]['departure']['actual'],
                # Arrival Details
                'arrival_airport' : api_data['data'][0]['arrival']['airport'],
                'arrival_scheduled': api_data['data'][0]['arrival']['scheduled'],
                'arrival_estimated': api_data['data'][0]['arrival']['estimated'],
                'arrival_actual' : api_data['data'][0]['arrival']['actual'],
                # 'arrival_terminal' : str(api_data['data'][0]['arrival']['terminal'] + '' + api_data['data'][0]['arrival']['gate']),
            }

            test = 0

            if api_data['data'][0]['arrival']['terminal'] != None and api_data['data'][0]['arrival']['gate'] != None:
                con['arrival_terminal'] = api_data['data'][0]['arrival']['terminal'] + '' + api_data['data'][0]['arrival']['gate']
                test+=1

            if api_data['data'][0]['departure']['terminal'] != None and api_data['data'][0]['departure']['gate'] != None:
                con['departure_terminal'] = str(api_data['data'][0]['departure']['terminal'] + '' + api_data['data'][0]['departure']['gate'])
                test += 2

            else:
                if test == 1:
                    con['departure_terminal'] = 'NA'
                if test == 2:
                    con['arrival_terminal'] = 'NA'
                elif test == 0:
                    con['departure_terminal'] ='NA'
                    con['arrival_terminal'] = 'NA'

            return render(request, 'airplane/airplane-data.html', con)
    else:
        form = AirplaneSearchForm()
        con = {
            'form' : form,
        }

    return render(request, 'airplane/airplane-form.html', con)

