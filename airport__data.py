import json
import requests
from io import StringIO

def fetch_airport_data():
    """Fetch airport data from ourairports.com"""
    try:
        # Get the data directly from ourairports.com
        url = "http://ourairports.com/data/airports.csv"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            # Fallback to sample data if API fails
            return get_sample_airport_data()
        
        # Parse CSV and convert to list of dictionaries
        import csv
        reader = csv.DictReader(StringIO(response.text))
        airports = []
        
        for row in reader:
            # Only include airports with IATA codes and type 'large_airport' or 'medium_airport'
            if row.get('iata_code') and row.get('type') in ['large_airport', 'medium_airport']:
                airports.append({
                    'ident': row.get('ident'),
                    'name': row.get('name'),
                    'iata_code': row.get('iata_code'),
                    'icao_code': row.get('icao_code'),
                    'municipality': row.get('municipality'),
                    'iso_country': row.get('iso_country'),
                    'iso_region': row.get('iso_region'),
                    'continent': row.get('continent'),
                    'coordinates': row.get('coordinates', ''),
                    'elevation_ft': row.get('elevation_ft'),
                })
                
                # Limit to 200 airports for performance
                if len(airports) >= 200:
                    break
        
        return airports
        
    except Exception as e:
        print(f"Error fetching airport data: {e}")
        return get_sample_airport_data()

def get_sample_airport_data():
    """Return sample airport data if API fails"""
    return [
        {
            'ident': 'KJFK',
            'name': 'John F Kennedy International Airport',
            'iata_code': 'JFK',
            'icao_code': 'KJFK',
            'municipality': 'New York',
            'iso_country': 'US',
            'iso_region': 'US-NY',
            'continent': 'NA',
            'coordinates': '-73.7822222222, 40.6397222222',
            'elevation_ft': '13'
        },
        {
            'ident': 'KLAX',
            'name': 'Los Angeles International Airport',
            'iata_code': 'LAX',
            'icao_code': 'KLAX',
            'municipality': 'Los Angeles',
            'iso_country': 'US',
            'iso_region': 'US-CA',
            'continent': 'NA',
            'coordinates': '-118.4081666667, 33.9425',
            'elevation_ft': '125'
        },
        {
            'ident': 'KORD',
            'name': "O'Hare International Airport",
            'iata_code': 'ORD',
            'icao_code': 'KORD',
            'municipality': 'Chicago',
            'iso_country': 'US',
            'iso_region': 'US-IL',
            'continent': 'NA',
            'coordinates': '-87.9073333333, 41.9786111111',
            'elevation_ft': '672'
        },
        {
            'ident': 'KDFR',
            'name': 'Dallas/Fort Worth International Airport',
            'iata_code': 'DFW',
            'icao_code': 'KDFW',
            'municipality': 'Dallas-Fort Worth',
            'iso_country': 'US',
            'iso_region': 'US-TX',
            'continent': 'NA',
            'coordinates': '-97.0402222222, 32.8968333333',
            'elevation_ft': '603'
        },
        {
            'ident': 'KATL',
            'name': 'Hartsfield-Jackson Atlanta International Airport',
            'iata_code': 'ATL',
            'icao_code': 'KATL',
            'municipality': 'Atlanta',
            'iso_country': 'US',
            'iso_region': 'US-GA',
            'continent': 'NA',
            'coordinates': '-84.4277222222, 33.6367222222',
            'elevation_ft': '1026'
        },
        {
            'ident': 'KDEN',
            'name': 'Denver International Airport',
            'iata_code': 'DEN',
            'icao_code': 'KDEN',
            'municipality': 'Denver',
            'iso_country': 'US',
            'iso_region': 'US-CO',
            'continent': 'NA',
            'coordinates': '-104.6737222222, 39.8616666667',
            'elevation_ft': '5431'
        },
        {
            'ident': 'EGLL',
            'name': 'London Heathrow Airport',
            'iata_code': 'LHR',
            'icao_code': 'EGLL',
            'municipality': 'London',
            'iso_country': 'GB',
            'iso_region': 'GB-ENG',
            'continent': 'EU',
            'coordinates': '-0.4614166667, 51.4700222222',
            'elevation_ft': '83'
        },
        {
            'ident': 'LFPG',
            'name': 'Charles de Gaulle International Airport',
            'iata_code': 'CDG',
            'icao_code': 'LFPG',
            'municipality': 'Paris',
            'iso_country': 'FR',
            'iso_region': 'FR-75',
            'continent': 'EU',
            'coordinates': '2.5479166667, 49.0127777778',
            'elevation_ft': '392'
        },
        {
            'ident': 'EDDF',
            'name': 'Frankfurt am Main Airport',
            'iata_code': 'FRA',
            'icao_code': 'EDDF',
            'municipality': 'Frankfurt am Main',
            'iso_country': 'DE',
            'iso_region': 'DE-HE',
            'continent': 'EU',
            'coordinates': '8.5621666667, 50.0333333333',
            'elevation_ft': '364'
        },
        {
            'ident': 'RJTT',
            'name': 'Tokyo Haneda Airport',
            'iata_code': 'HND',
            'icao_code': 'RJTT',
            'municipality': 'Tokyo',
            'iso_country': 'JP',
            'iso_region': 'JP-13',
            'continent': 'AS',
            'coordinates': '139.7791666667, 35.5533333333',
            'elevation_ft': '35'
        },
        {
            'ident': 'ZBAA',
            'name': 'Beijing Capital International Airport',
            'iata_code': 'PEK',
            'icao_code': 'ZBAA',
            'municipality': 'Beijing',
            'iso_country': 'CN',
            'iso_region': 'CN-11',
            'continent': 'AS',
            'coordinates': '116.5844444444, 40.0727777778',
            'elevation_ft': '116'
        },
        {
            'ident': 'YSSY',
            'name': 'Sydney Kingsford Smith International Airport',
            'iata_code': 'SYD',
            'icao_code': 'YSSY',
            'municipality': 'Sydney',
            'iso_country': 'AU',
            'iso_region': 'AU-NSW',
            'continent': 'OC',
            'coordinates': '151.1772222222, -33.9469444444',
            'elevation_ft': '21'
        },
        {
            'ident': 'CYYZ',
            'name': 'Toronto Pearson International Airport',
            'iata_code': 'YYZ',
            'icao_code': 'CYYZ',
            'municipality': 'Toronto',
            'iso_country': 'CA',
            'iso_region': 'CA-ON',
            'continent': 'NA',
            'coordinates': '-79.6305555556, 43.6772222222',
            'elevation_ft': '569'
        },
        {
            'ident': 'CYVR',
            'name': 'Vancouver International Airport',
            'iata_code': 'YVR',
            'icao_code': 'CYVR',
            'municipality': 'Vancouver',
            'iso_country': 'CA',
            'iso_region': 'CA-BC',
            'continent': 'NA',
            'coordinates': '-123.1836111111, 49.1947222222',
            'elevation_ft': '14'
        }
    ]

def get_airport_data():
    """Get airport data with caching"""
    try:
        # Try to fetch from URL first
        return fetch_airport_data()
    except Exception as e:
        print(f"Using sample data due to error: {e}")
        return get_sample_airport_data()

def get_airport_by_code(code):
    """Find airport by IATA code"""
    airports = get_airport_data()
    for airport in airports:
        if airport.get('iata_code', '').upper() == code.upper():
            return airport
    return None

def get_airport_by_city(city):
    """Find airport by city name"""
    airports = get_airport_data()
    for airport in airports:
        if airport.get('municipality', '').lower() == city.lower():
            return airport
    return None

def save_airport_data_to_json(filename='data/airports.json'):
    """Save airport data to a JSON file for offline use"""
    airports = fetch_airport_data()
    
    # Create the data directory if it doesn't exist
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        json.dump(airports, f, indent=2)
    
    return airports

if __name__ == "__main__":
    # Test the functions
    airports = get_airport_data()
    print(f"Loaded {len(airports)} airports")
    
    # Test finding by code
    jfk = get_airport_by_code('JFK')
    if jfk:
        print(f"Found JFK: {jfk['name']} in {jfk['municipality']}")
    
    # Test finding by city
    nyc_airport = get_airport_by_city('New York')
    if nyc_airport:
        print(f"Found airport in New York: {nyc_airport['name']} ({nyc_airport['iata_code']})")
