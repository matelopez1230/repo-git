"""
Servicio para integrar con la API de VesselFinder/MarineTraffic
"""
import requests
import os
from datetime import datetime

# Clave API - Debes obtenerla registrándote en https://www.marinetraffic.com/en/ais-api
API_KEY = os.getenv('MARINETRAFFIC_API_KEY', 'TU_CLAVE_API_AQUI')  # Reemplaza con tu clave real

BASE_URL = 'https://services.marinetraffic.com/api'

def get_ports(country=None):
    """
    Obtiene lista de puertos, opcionalmente filtrados por país
    """
    if API_KEY == 'TU_CLAVE_API_AQUI':
        # Datos mock si no hay clave API
        mock_ports = [
            {'id': 1, 'name': 'Port of Rotterdam', 'country': 'Netherlands', 'latitude': 51.9167, 'longitude': 4.4833},
            {'id': 2, 'name': 'Port of Shanghai', 'country': 'China', 'latitude': 31.2304, 'longitude': 121.4737},
            {'id': 3, 'name': 'Port of Singapore', 'country': 'Singapore', 'latitude': 1.3521, 'longitude': 103.8198},
            {'id': 4, 'name': 'Port of Los Angeles', 'country': 'USA', 'latitude': 33.7380, 'longitude': -118.2620},
            {'id': 5, 'name': 'Port of Hamburg', 'country': 'Germany', 'latitude': 53.5511, 'longitude': 9.9937}
        ]
        if country:
            return [p for p in mock_ports if p['country'].lower() == country.lower()]
        return mock_ports
    
    endpoint = f'{BASE_URL}/ports/v:1/'
    params = {
        'key': API_KEY,
        'protocol': 'json'
    }
    if country:
        params['country'] = country

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        # Procesar datos - la API retorna una lista de puertos
        ports = []
        for port in data.get('ports', []):
            ports.append({
                'id': port.get('port_id'),
                'name': port.get('port_name'),
                'country': port.get('country'),
                'latitude': port.get('latitude'),
                'longitude': port.get('longitude')
            })
        return ports
    except requests.RequestException as e:
        print(f"Error al obtener puertos: {e}")
        return []

def get_vessel_positions(mmsi=None, imo=None):
    """
    Obtiene posiciones de barcos
    """
    endpoint = f'{BASE_URL}/exportvessel/v:5/'
    params = {
        'key': API_KEY,
        'protocol': 'json',
        'msgtype': 'simple'  # Para posiciones simples
    }
    if mmsi:
        params['mmsi'] = mmsi
    if imo:
        params['imo'] = imo

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error al obtener posiciones: {e}")
        return []

def get_vessel_details(imo):
    """
    Obtiene detalles de un barco por IMO
    """
    endpoint = f'{BASE_URL}/vesseldetails/v:1/'
    params = {
        'key': API_KEY,
        'protocol': 'json',
        'imo': imo
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        vessel = data.get('vessel', [{}])[0] if data.get('vessel') else {}
        return {
            'name': vessel.get('name'),
            'type': vessel.get('type_name'),  # e.g., Container Ship
            'flag': vessel.get('flag'),
            'year_built': vessel.get('year_built'),
            'dwt': vessel.get('dwt'),  # Deadweight tonnage
            'length': vessel.get('length'),
            'width': vessel.get('width')
        }
    except requests.RequestException as e:
        print(f"Error al obtener detalles del barco: {e}")
        return {}

def validate_route(origin_port, destination_port, departure_date, arrival_date):
    """
    Valida si una ruta es posible basado en barcos disponibles
    """
    # Esto es simplificado - en realidad, buscar barcos que naveguen esa ruta
    # Por ahora, solo verificar fechas
    try:
        dep_date = datetime.fromisoformat(departure_date)
        arr_date = datetime.fromisoformat(arrival_date)
        if arr_date > dep_date:
            return True
        return False
    except ValueError:
        return False

# Funciones helper para tipos de contenedores y productos
CONTAINER_TYPES = [
    '20ft Standard',
    '40ft Standard',
    '40ft High Cube',
    '20ft Refrigerated',
    '40ft Refrigerated',
    'Open Top',
    'Flat Rack',
    'Tank Container'
]

PRODUCT_TYPES = [
    'Electronics',
    'Food & Beverages',
    'Chemicals',
    'Machinery',
    'Textiles',
    'Automotive Parts',
    'Pharmaceuticals',
    'Agricultural Products',
    'Construction Materials',
    'Other'
]

def get_container_types():
    return CONTAINER_TYPES

def get_product_types():
    return PRODUCT_TYPES