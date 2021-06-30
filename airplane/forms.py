from django import forms
import datetime

class AirplaneSearchForm(forms.Form):
    flight_name = forms.CharField(label = "Airline's Name", max_length=150, widget = forms.TextInput(attrs = {
            'placeholder' : "Airline's Name"
        }))
    flight_number = forms.IntegerField(label = 'Flight Number', widget = forms.NumberInput(attrs = {
            'placeholder' : 'Flight Number'
        }))
    date = forms.DateField(initial=datetime.date.today, widget = forms.DateInput(attrs = {
            'type' : 'date'
        }))
