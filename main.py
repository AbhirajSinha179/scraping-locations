# simple python script to scrape website for locations near bangalore
# and search in maps if it's nearby another specified location (kormangala)

import requests
from bs4 import BeautifulSoup

notIncluded = ["Register Now", "Learn More!", "Private Pad", "Studio Room", "Double Occupancy",
               "Studio Room", "Private Room", "Get a Tour"]
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Initialize the Nominatim geocoder
geolocator = Nominatim(user_agent="my_app")

def find_nearby_locations(locations, reference_locality, radius=7):
    """
    Find locations within a specified radius from the reference locality.

    Args:
        locations (list): A list of location names.
        reference_locality (str): The name of the reference locality.
        radius (int or float, optional): The search radius in kilometers. Default is 50.

    Returns:
        list: A list of nearby location names.
    """
    nearby_locations = []
    ref_loc = geolocator.geocode(reference_locality)

    if ref_loc:
        ref_point = ref_loc.point
        for location in locations:
            loc = geolocator.geocode(location)
            if loc:
                loc_point = loc.point
                distance = geodesic(ref_point, loc_point).km
                if distance <= radius:
                    nearby_locations.append((location, distance))

    return nearby_locations
def listLocations():
    """
        Scrapes the website and finds the locations listed, making sure redundant elements are not chosen
    :return: List of locations in Bangalore
    """
    # Make a request to the website
    url = "https://www.ff21.in"
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # print(soup)

    # Find all the desired span elements
    span_elements = soup.find_all('span', class_='l7_2fn')
    locations=[]
    # Print the text content of each span element
    for span in span_elements:
        if span.get_text() not in notIncluded:
            locations.append(span.get_text())
            print(span.get_text())
    return locations



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    locs = listLocations()
    nearby_locs = find_nearby_locations(locs, "Kormangala")
    print(nearby_locs)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
