"""
Servicio para obtener puertos/terminales de transporte por modo
"""
import requests
import os

# Claves API
MARINETRAFFIC_API_KEY = os.getenv('MARINETRAFFIC_API_KEY', 'TU_CLAVE_MARINA_AQUI')
AVIATIONSTACK_API_KEY = os.getenv('AVIATIONSTACK_API_KEY', 'TU_CLAVE_AVION_AQUI')

BASE_MARINE = 'https://services.marinetraffic.com/api'
BASE_AVIATION = 'http://api.aviationstack.com/v1'

def get_sea_ports(country=None):
    """
    Obtiene puertos marítimos
    """
    if MARINETRAFFIC_API_KEY == 'TU_CLAVE_MARINA_AQUI':
        # Datos mock
        mock_ports = [
            {'id': 1, 'name': 'Port of Rotterdam', 'country': 'Netherlands'},
            {'id': 2, 'name': 'Port of Shanghai', 'country': 'China'},
            {'id': 3, 'name': 'Port of Singapore', 'country': 'Singapore'},
            {'id': 4, 'name': 'Port of Los Angeles', 'country': 'USA'},
            {'id': 5, 'name': 'Port of Hamburg', 'country': 'Germany'},
            {'id': 6, 'name': 'Port of Buenos Aires', 'country': 'Argentina'},
            {'id': 7, 'name': 'Port of Santos', 'country': 'Brazil'},
        ]
        if country:
            return [p for p in mock_ports if p['country'].lower() == country.lower()]
        return mock_ports

    # API real
    endpoint = f'{BASE_MARINE}/ports/v:1/'
    params = {'key': MARINETRAFFIC_API_KEY, 'protocol': 'json'}
    if country:
        params['country'] = country
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        ports = []
        for port in data.get('ports', []):
            ports.append({
                'id': port.get('port_id'),
                'name': port.get('port_name'),
                'country': port.get('country')
            })
        return ports
    except:
        return []

def get_airports(country=None):
    """
    Obtiene aeropuertos
    """
    if AVIATIONSTACK_API_KEY == 'TU_CLAVE_AVION_AQUI':
        # Datos mock
        mock_airports = [
            {'id': 1, 'name': 'John F. Kennedy International Airport', 'country': 'USA', 'iata': 'JFK'},
            {'id': 2, 'name': 'Heathrow Airport', 'country': 'United Kingdom', 'iata': 'LHR'},
            {'id': 3, 'name': 'Charles de Gaulle Airport', 'country': 'France', 'iata': 'CDG'},
            {'id': 4, 'name': 'Frankfurt Airport', 'country': 'Germany', 'iata': 'FRA'},
            {'id': 5, 'name': 'Narita International Airport', 'country': 'Japan', 'iata': 'NRT'},
            {'id': 6, 'name': 'Ezeiza International Airport', 'country': 'Argentina', 'iata': 'EZE'},
            {'id': 7, 'name': 'Galeão International Airport', 'country': 'Brazil', 'iata': 'GIG'},
        ]
        if country:
            return [a for a in mock_airports if a['country'].lower() == country.lower()]
        return mock_airports

    # API real
    endpoint = f'{BASE_AVIATION}/airports'
    params = {'access_key': AVIATIONSTACK_API_KEY}
    if country:
        params['country'] = country
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        airports = []
        for airport in data.get('data', []):
            airports.append({
                'id': airport.get('id'),
                'name': airport.get('airport_name'),
                'country': airport.get('country_name'),
                'iata': airport.get('iata_code')
            })
        return airports
    except:
        return []

def get_land_terminals(country=None):
    """
    Obtiene terminales terrestres (fronteras o puertos terrestres)
    """
    # Mock data, ya que no hay API estándar
    mock_terminals = [
        {'id': 1, 'name': 'Border Crossing Tijuana', 'country': 'Mexico'},
        {'id': 2, 'name': 'Eurotunnel Terminal', 'country': 'France'},
        {'id': 3, 'name': 'Land Port of Entry Nogales', 'country': 'USA'},
        {'id': 4, 'name': 'Inland Container Depot', 'country': 'India'},
        {'id': 5, 'name': 'Dry Port Buenos Aires', 'country': 'Argentina'},
        {'id': 6, 'name': 'Terminal Terrestre de Santos', 'country': 'Brazil'},
        {'id': 7, 'name': 'Border Station Paso de los Libres', 'country': 'Argentina'},
    ]
    if country:
        return [t for t in mock_terminals if t['country'].lower() == country.lower()]
    return mock_terminals

def get_transport_options(mode, country=None):
    """
    Obtiene opciones de transporte por modo
    """
    if mode == 'sea':
        return get_sea_ports(country)
    elif mode == 'air':
        return get_airports(country)
    elif mode == 'land':
        return get_land_terminals(country)
    return []