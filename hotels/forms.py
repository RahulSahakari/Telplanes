from django import forms
import datetime

class HotelsSearchForm(forms.Form):
	adults = forms.IntegerField(initial = 1, required = True, widget=forms.NumberInput(attrs = {
			'placeholder' : 'No of Adults'
		}))
	# children = forms.IntegerField()
	children = forms.CharField(required = False, widget = forms.TextInput(attrs = {
			'placeholder' : "Child's age(seprated by comma)"
		}))
	destination = forms.CharField(required = True, max_length= 250, widget = forms.TextInput(attrs = {
			'placeholder' : 'Your Destination'
		}))
	check_in = forms.DateField(initial = datetime.date.today, required = True, widget = forms.DateInput(attrs = {
			'placeholder' : 'Date of Check In',
			'type' : 'date'
		}))
	check_out = forms.DateField(required = True, widget = forms.DateInput(attrs = {
			'type' : 'date',
			'placeholder' : 'Date of Check Out'
		}))
	currency = forms.CharField(initial = 'USD', required = True, widget = forms.TextInput(attrs = {
			'placeholder' : 'Currency Format'
		}))

class HotelsFilterForm(forms.Form):
	# sort_options = (
	# 	('1', '1'),
	# 	('2', '2'),
	# 	('3', '3'),
	# 	('4', '4'),
	# 	('5', '5'),
	# 	('6', '6'),
	# 	('7', '7'),
	# 	('8', '8'),
	# 	('9', '9'),
	# 	('10', '10'),
	# )

	min_price = forms.IntegerField(required = False, widget = forms.NumberInput(attrs = {
			'placeholder' : 'Minimum Price'
		}))
	max_price = forms.IntegerField(required = False, widget = forms.NumberInput(attrs = {
			'placeholder' : 'Maximum Price'
		}))
	guest_rating = forms.IntegerField(required = False, widget = forms.TextInput(attrs = {
			'placeholder' : 'Ratings(1-10)'
		}))

class HotelsSortForm(forms.Form):
	sort_options = (
		('BEST_SELLER', 'Best Seller'),
		('STAR_RATING_LOWEST_FIRST', 'Star Rating(Lowest 1st)'),
		('DISTANCE_FROM_LANDMARK', 'Distance from destination'),
		('GUEST_RATING', 'Guest Ratings'),
		('PRICE_HIGHEST_FIRST', 'Price (Higest 1st)'),
		('PRICE', 'Price (Lowest 1st)'),
		('STAR_RATING_HIGHEST_FIRST', 'Star Rating (Higest 1st)'),
	)

	sort_order = forms.MultipleChoiceField(required = False, choices = sort_options)

