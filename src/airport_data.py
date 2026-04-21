"""
Havalimanı koordinatları - Demo için temel havalimanları
"""

AIRPORT_DATABASE = {
    'LTFM': {
        'name': 'İstanbul Havalimanı',
        'lat': 41.2753,
        'lon': 28.7519,
        'city': 'İstanbul',
        'country': 'Türkiye'
    },
    'LTAC': {
        'name': 'Esenboğa Havalimanı',
        'lat': 40.1281,
        'lon': 32.9951,
        'city': 'Ankara',
        'country': 'Türkiye'
    },
    'LTAI': {
        'name': 'Antalya Havalimanı',
        'lat': 36.9007,
        'lon': 30.7925,
        'city': 'Antalya',
        'country': 'Türkiye'
    },
    'EGLL': {
        'name': 'London Heathrow',
        'lat': 51.4700,
        'lon': -0.4543,
        'city': 'London',
        'country': 'UK'
    },
    'EDDF': {
        'name': 'Frankfurt Airport',
        'lat': 50.0379,
        'lon': 8.5622,
        'city': 'Frankfurt',
        'country': 'Germany'
    },
    'LFPG': {
        'name': 'Paris Charles de Gaulle',
        'lat': 49.0097,
        'lon': 2.5479,
        'city': 'Paris',
        'country': 'France'
    },
    'OMDB': {
        'name': 'Dubai International',
        'lat': 25.2532,
        'lon': 55.3657,
        'city': 'Dubai',
        'country': 'UAE'
    },
    'OEJN': {
        'name': 'King Abdulaziz Intl',
        'lat': 21.6796,
        'lon': 39.1565,
        'city': 'Jeddah',
        'country': 'Saudi Arabia'
    },
    'KJFK': {
        'name': 'John F Kennedy Intl',
        'lat': 40.6413,
        'lon': -73.7781,
        'city': 'New York',
        'country': 'USA'
    }
}

def get_airport(icao_code):
    """Havalimanı bilgisi getir"""
    return AIRPORT_DATABASE.get(icao_code.upper())