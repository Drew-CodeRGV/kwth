from flask import Flask, render_template, jsonify, request
import requests
import json
import random
import os
from dotenv import load_dotenv
from airport_data import get_airport_data, get_airport_by_code, get_airport_by_city

load_dotenv()

app = Flask(__name__)

# Configuration
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY', '')
WIKIPEDIA_API_BASE = 'https://en.wikipedia.org/api/rest_v1/page/summary/'

def get_airport_images(airport_name, city_name):
    """Fetch airport images from Pixabay"""
    if not PIXABAY_API_KEY:
        # Return placeholder images if no API key
        return {
            'terminal': 'https://via.placeholder.com/600x400/333/fff?text=Airport+Terminal',
            'overhead': 'https://via.placeholder.com/600x400/333/fff?text=Overhead+View',
            'entrance': 'https://via.placeholder.com/600x400/333/fff?text=Airport+Entrance'
        }
    
    queries = [
        f"{airport_name} airport terminal",
        f"{city_name} airport overhead view",
        f"{airport_name} airport entrance"
    ]
    
    images = {}
    types = ['terminal', 'overhead', 'entrance']
    
    for i, query in enumerate(queries):
        try:
            url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo&per_page=5"
            response = requests.get(url)
            data = response.json()
            
            if 'hits' in data and len(data['hits']) > 0:
                images[types[i]] = data['hits'][0]['webformatURL']
            else:
                images[types[i]] = f'https://via.placeholder.com/600x400/333/fff?text={types[i].title()}'
        except Exception as e:
            print(f"Error fetching {types[i]} image: {e}")
            images[types[i]] = f'https://via.placeholder.com/600x400/333/fff?text={types[i].title()}'
    
    return images

def get_city_facts(city_name, country):
    """Fetch city facts from Wikipedia"""
    try:
        url = f"{WIKIPEDIA_API_BASE}{city_name.replace(' ', '_')}"
        response = requests.get(url)
        data = response.json()
        
        # Extract key facts from Wikipedia summary
        description = data.get('extract', '')
        
        # Create simple facts from the description
        sentences = description.split('.')[:5]
        facts = [sentence.strip() + '.' for sentence in sentences if sentence.strip()]
        
        # Add some generic facts if not enough found
        while len(facts) < 3:
            facts.append(f"{city_name} is located in {country}")
            facts.append(f"This is a major city in {country}")
            facts.append(f"{city_name} has significant cultural importance")
            facts = facts[:3]
            break
        
        return facts[:3]
    except Exception as e:
        print(f"Error fetching city facts: {e}")
        return [
            f"{city_name} is a major city in {country}",
            f"The airport serves the {city_name} metropolitan area",
            f"{city_name} has significant air traffic connections"
        ]

def get_code_meanings():
    """Generate airport code meanings with some real ones and some fake options"""
    real_meanings = {
        'JFK': 'John F. Kennedy International',
        'LAX': 'Los Angeles International (X for international)',
        'ORD': "O'Hare International (named after Edward O'Hare)",
        'LGA': 'LaGuardia (named after Fiorello La Guardia)',
        'DFW': 'Dallas/Fort Worth International',
        'ATL': 'Atlanta International',
        'PHX': 'Phoenix Sky Harbor',
        'DEN': 'Denver International',
        'FLL': 'Fort Lauderdale-Hollywood International',
        'MCO': 'Orlando International (McCoy Air Force Base)',
        'BOS': 'Boston Logan International',
        'IAH': 'Houston Intercontinental (Humble Airport originally)',
        'BWI': 'Baltimore/Washington International',
        'PHL': 'Philadelphia International',
        'YYZ': 'Toronto Pearson (Y prefix for Canadian airports)',
        'YVR': 'Vancouver International'
    }
    
    fake_meanings = [
        'International Aviation Terminal',
        'Regional Airport Authority',
        'Air Transportation Hub',
        'Central Flight Operations',
        'Metropolitan Aviation Center',
        'International Departure Point',
        'Sky Harbor Interface',
        'Aviation Service Complex',
        'Flight Connection Center',
        'Passenger Terminal Gateway',
        'Air Travel Facility',
        'Commercial Aviation Port'
    ]
    
    return real_meanings, fake_meanings

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "Airport Code Game",
        "short_name": "Airport Game",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#000000",
        "theme_color": "#007AFF",
        "icons": [
            {
                "src": "static/icon.png",
                "sizes": "192x192",
                "type": "image/png"
            }
        ]
    })

@app.route('/get_airport', methods=['GET'])
def get_random_airport():
    """Get a random airport for the game"""
    game_mode = request.args.get('mode', 'guess_code')
    airports = get_airport_data()
    
    # Filter airports with IATA codes only
    iata_airports = [a for a in airports if a.get('iata_code')]
    
    if not iata_airports:
        return jsonify({'error': 'No airports available'}), 500
    
    airport = random.choice(iata_airports)
    
    # Get airport images
    airport_name = airport.get('name', '')
    city_name = airport.get('municipality', '')
    images = get_airport_images(airport_name, city_name)
    
    # Get city facts for hints
    country = airport.get('iso_country', '')
    city_facts = get_city_facts(city_name, country)
    
    # Get code meanings
    real_meanings, fake_meanings = get_code_meanings()
    code = airport.get('iata_code', '')
    
    # Create meaning options (1 real, 3 fake)
    meaning_options = []
    if code in real_meanings:
        meaning_options.append(real_meanings[code])
    else:
        meaning_options.append(f"{airport_name}")
    
    # Add 3 random fake meanings
    available_fakes = [f for f in fake_meanings if f not in meaning_options]
    meaning_options.extend(random.sample(available_fakes, 3))
    random.shuffle(meaning_options)
    
    # Prepare response
    response = {
        'code': code,
        'name': airport_name,
        'city': city_name,
        'country': country,
        'images': images,
        'city_facts': city_facts,
        'meaning_options': meaning_options,
        'correct_meaning': meaning_options[0] if code not in real_meanings else real_meanings[code]
    }
    
    return jsonify(response)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    """Check if the user's answer is correct"""
    data = request.json
    game_mode = data.get('mode')
    user_answer = data.get('answer', '').strip().upper()
    correct = data.get('correct', '').strip().upper()
    
    is_correct = user_answer == correct
    
    return jsonify({
        'correct': is_correct,
        'user_answer': user_answer,
        'correct_answer': correct
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
