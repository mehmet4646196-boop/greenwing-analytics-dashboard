"""
Demo havayolu verisi üretici
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_flight_data(start_date='2025-01-01', days=180):
    """
    6 aylık demo uçuş verisi üret
    
    Args:
        start_date: Başlangıç tarihi
        days: Gün sayısı
    
    Returns:
        DataFrame: Uçuş verileri
    """
    
    np.random.seed(42)
    
    # Rota tanımları
    routes = [
        {'origin': 'LTFM', 'dest': 'EGLL', 'dist': 1560, 'ac': 'B738', 'freq': 2},
        {'origin': 'EGLL', 'dest': 'LTFM', 'dist': 1560, 'ac': 'B738', 'freq': 2},
        {'origin': 'LTFM', 'dest': 'EDDF', 'dist': 1000, 'ac': 'B738', 'freq': 3},
        {'origin': 'EDDF', 'dest': 'LTFM', 'dist': 1000, 'ac': 'B738', 'freq': 3},
        {'origin': 'LTFM', 'dest': 'LFPG', 'dist': 1220, 'ac': 'A320', 'freq': 2},
        {'origin': 'LFPG', 'dest': 'LTFM', 'dist': 1220, 'ac': 'A320', 'freq': 2},
        {'origin': 'LTFM', 'dest': 'OMDB', 'dist': 1550, 'ac': 'B77W', 'freq': 1},
        {'origin': 'OMDB', 'dest': 'LTFM', 'dist': 1550, 'ac': 'B77W', 'freq': 1},
        {'origin': 'LTFM', 'dest': 'LTAC', 'dist': 190, 'ac': 'B738', 'freq': 6},
        {'origin': 'LTAC', 'dest': 'LTFM', 'dist': 190, 'ac': 'B738', 'freq': 6},
        {'origin': 'LTFM', 'dest': 'LTAI', 'dist': 300, 'ac': 'A320', 'freq': 4},
        {'origin': 'LTAI', 'dest': 'LTFM', 'dist': 300, 'ac': 'A320', 'freq': 4},
        {'origin': 'LTFM', 'dest': 'OEJN', 'dist': 1380, 'ac': 'B738', 'freq': 1},
        {'origin': 'LTFM', 'dest': 'KJFK', 'dist': 5000, 'ac': 'B77W', 'freq': 1},
    ]
    
    # Yakıt baz değerleri (kg) - distance'a göre
    def calculate_fuel(ac_type, distance):
        if ac_type == 'B738':
            return distance * 5.2  # kg per NM
        elif ac_type == 'A320':
            return distance * 5.8
        else:  # B77W
            return distance * 9.5
    
    flights = []
    start = datetime.strptime(start_date, '%Y-%m-%d')
    
    for day in range(days):
        date = start + timedelta(days=day)
        
        for route in routes:
            for _ in range(route['freq']):
                # Yakıt hesapla
                base_fuel = calculate_fuel(route['ac'], route['dist'])
                
                # Varyasyon ekle (±5%)
                fuel_variation = np.random.normal(1.0, 0.05)
                fuel = base_fuel * fuel_variation
                
                # Mevsimsel etki
                month = date.month
                if month in [12, 1, 2]:  # Kış
                    fuel *= 1.04
                elif month in [6, 7, 8]:  # Yaz
                    fuel *= 0.97
                
                # Rota verimliliği
                route_efficiency = np.random.normal(92, 4)
                
                flights.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'month': date.strftime('%Y-%m'),
                    'week': date.isocalendar()[1],
                    'flight_number': f"{route['ac']}{np.random.randint(100, 999)}",
                    'origin': route['origin'],
                    'destination': route['dest'],
                    'aircraft_type': route['ac'],
                    'distance_nm': route['dist'],
                    'fuel_kg': round(fuel, 0),
                    'co2_kg': round(fuel * 3.16, 0),
                    'route_efficiency_pct': round(route_efficiency, 1),
                    'fuel_per_nm': round(fuel / route['dist'], 2),
                })
    
    df = pd.DataFrame(flights)
    
    # Tasarruf potansiyeli hesapla
    for (origin, dest, ac), group in df.groupby(['origin', 'destination', 'aircraft_type']):
        best_practice = group['fuel_per_nm'].quantile(0.10)
        df.loc[group.index, 'potential_saving_kg'] = (
            (group['fuel_per_nm'] - best_practice) * group['distance_nm']
        ).clip(lower=0)
    
    df['potential_saving_kg'] = df['potential_saving_kg'].fillna(0)
    
    return df