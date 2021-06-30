from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests, json
from .forms import HotelsSearchForm, HotelsFilterForm, HotelsSortForm
from django.contrib import messages

def getDestinationCode(data, headers):
	destination_url = 'https://hotels4.p.rapidapi.com/locations/search'
	d_response = requests.request('GET', destination_url, headers = headers, params = data).json()

	try:
		E = d_response['suggestions'][0]['entities'][0]['destinationId']
	except IndexError as e:
		return None
	else:
		return E

def getHotelImage(hotelId, headers):
	url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

	querystring = {"id": hotelId}

	response = requests.request("GET", url, headers=headers, params=querystring).json()

	size_type = response['hotelImages'][0]['sizes'][0]['suffix']
	image_url = response['hotelImages'][0]['baseUrl']
	temp = image_url.split('{size}')
	image_url = str(temp[0]+size_type+temp[1])

	return image_url

# Create your views here.
def hotelLists(request):
	if request.method == 'POST':
		form = HotelsSearchForm(request.POST)
		filter_form = HotelsFilterForm(request.POST)
		sort_form = HotelsSortForm(request.POST)

		if form.is_valid() and filter_form.is_valid() and sort_form.is_valid():
			# Calling the api and storing its data in 'api_result'

			headers = {
			    'x-rapidapi-key': "e272c4ddb1msh83099e81aa634d0p1dda2ejsne0b7bc58b157",
			    'x-rapidapi-host': "hotels4.p.rapidapi.com"
			    }

			url = "https://hotels4.p.rapidapi.com/properties/list"
			destination_id = getDestinationCode(
				{"query":form.cleaned_data['destination'],
				"locale":"en_US"},
				headers
			)

			if destination_id == None:
				messages.error(request, 'Destination Incorrect Or Not Found')
				return redirect('hotels')
				
			querystring = {
				# required
				"adults1":form.cleaned_data['adults'],
				"pageNumber":"1",
				"destinationId":destination_id,
				"pageSize":"25",
				"checkOut":form.cleaned_data['check_out'],
				"checkIn":form.cleaned_data['check_in'],
				"locale":"en_IN",
				"currency":form.cleaned_data['currency'],

				# filters
				"priceMin" : filter_form.cleaned_data['min_price'],
				"priceMax" : filter_form.cleaned_data['max_price'],
				"guestRatingMin" : filter_form.cleaned_data['guest_rating'],

				#sort order
				"sortOrder":sort_form.cleaned_data['sort_order'],
			}
			
			con = {'results' : []}
			response = requests.request("GET", url, headers=headers, params=querystring).json()

			# showing the data
			

			try:
				results = response['data']['body']['searchResults']['results']
			except KeyError as e:
				messages.error(request,'Something Went Wrong..Make Sure The Details Given Were Correct!')
				return redirect('hotels')

			for i in results:
				# try the name if this fails the user probably entered the details wrong
				try:
					name = i['name']
				except KeyError:
					messages.error(request,'Something Went Wrong..Make Sure The Details Were Correct!')
					return redirect('hotels')
				else:
					# Now try the address if this fails the details are probably not available
					try:
						address = i['address']['streetAddress']
						address += str(' ' + i['address']['locality'])
						address += str(' ' +i['address']['postalCode'])
						image = getHotelImage(i['id'], headers)
					except KeyError:
						con['results'].append({ 
							'name' : i['name'],
							'price': i['ratePlan']['price']['current'],
							'address' : i['address']['countryName'],
						})

						continue
					else:
						# Now the "image" and "address" we are using are from the try line above
						con['results'].append({ 
							'name' : i['name'],
							'price': i['ratePlan']['price']['current'],
							'address': address,
							'star_rating' : i['starRating'] ,
							'image' : image,
						})
						continue
            
			return render(request, 'hotels/hotels-data.html', con)
	else:
		form = HotelsSearchForm()
		filter_form = HotelsFilterForm()
		sort_form = HotelsSortForm()

		con = {'form': form, 'f_form' : filter_form, 's_form' : sort_form}
	
	return render(request, 'hotels/hotels-form.html',con)
