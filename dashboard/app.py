"""
GreenWing Analytics - Ana Dashboard
"""

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime

# Modülleri import et
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_generator import generate_flight_data
from src.airport_data import get_airport

# ═══════════════════════════════════════════════════════════
# VERİYİ YÜKLE
# ═══════════════════════════════════════════════════════════

print("📊 Veri yükleniyor...")
df = generate_flight_data(days=180)
print(f"✅ {len(df)} uçuş kaydı yüklendi")

# ═══════════════════════════════════════════════════════════
# DASH UYGULAMASI
# ═══════════════════════════════════════════════════════════

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    title="GreenWing Analytics"
)

# Renk paleti
COLORS = {
    'bg': '#0a0a1a',
    'card': '#1a1a2e',
    'border': '#2a2a3e',
    'primary': '#00d4aa',
    'warning': '#ff9f43',
    'danger': '#ee5a52',
    'info': '#3498db',
    'text': '#ffffff',
    'text_muted': '#a0a0a0',
}

def create_kpi_card(title, value, icon, color):
    """KPI kartı oluştur"""
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.Span(icon, style={'fontSize': '32px'}),
                html.P(title, className="mb-0 mt-2", style={'color': COLORS['text_muted'], 'fontSize': '12px'}),
                html.H3(value, className="mb-0", style={'color': color, 'fontWeight': 'bold', 'fontSize': '28px'}),
            ], className="text-center")
        ]),
        style={'backgroundColor': COLORS['card'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '10px'}
    )

# ═══════════════════════════════════════════════════════════
# LAYOUT
# ═══════════════════════════════════════════════════════════

app.layout = dbc.Container([
    
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("✈️ GreenWing Analytics", className="mb-0", 
                   style={'color': COLORS['primary'], 'fontWeight': 'bold'}),
            html.P("Fuel Efficiency & Emission Intelligence Platform", 
                   style={'color': COLORS['text_muted'], 'fontSize': '14px'}),
        ], width=8),
        dbc.Col([
            html.Div([
                html.P("📅 Demo Period: Jan - Jun 2025", className="text-end mb-0",
                       style={'color': COLORS['text_muted'], 'fontSize': '12px'}),
                html.P(f"🕒 Last Updated: {datetime.now().strftime('%d %B %Y')}", 
                       className="text-end small", style={'color': COLORS['text_muted'], 'fontSize': '11px'}),
            ])
        ], width=4),
    ], className="mt-3 mb-4"),
    
    # Filters
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("✈️ Aircraft Type", style={'color': COLORS['text_muted'], 'fontSize': '12px'}),
                            dcc.Dropdown(
                                id='aircraft-filter',
                                options=[{'label': '🔹 All Aircraft', 'value': 'ALL'}] + [
                                    {'label': f'✈️ {ac}', 'value': ac} 
                                    for ac in sorted(df['aircraft_type'].unique())
                                ],
                                value='ALL',
                                style={'backgroundColor': COLORS['card'], 'color': '#000', 'borderRadius': '5px'}
                            ),
                        ], width=4),
                        dbc.Col([
                            html.Label("🛫 Route", style={'color': COLORS['text_muted'], 'fontSize': '12px'}),
                            dcc.Dropdown(
                                id='route-filter',
                                options=[{'label': '🌍 All Routes', 'value': 'ALL'}] + [
                                    {'label': f"🛫 {r[0]} → 🛬 {r[1]}", 'value': f"{r[0]}-{r[1]}"}
                                    for r in df[['origin', 'destination']].drop_duplicates().values
                                ],
                                value='ALL',
                                style={'backgroundColor': COLORS['card'], 'color': '#000', 'borderRadius': '5px'}
                            ),
                        ], width=4),
                        dbc.Col([
                            html.Label("📆 Month Range", style={'color': COLORS['text_muted'], 'fontSize': '12px'}),
                            dcc.RangeSlider(
                                id='month-slider',
                                min=1, max=6,
                                step=1,
                                value=[1, 6],
                                marks={i: f'M{i}' for i in range(1, 7)},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ], width=4),
                    ])
                ])
            ], style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '10px'})
        ])
    ], className="mb-4"),
    
    # KPI Cards
    dbc.Row([
        dbc.Col(create_kpi_card("Total Flights", f"{len(df):,}", "✈️", COLORS['info']), width=3),
        dbc.Col(create_kpi_card("Total Fuel", f"{df['fuel_kg'].sum()/1000:,.0f} t", "⛽", COLORS['primary']), width=3),
        dbc.Col(create_kpi_card("Total CO₂", f"{df['co2_kg'].sum()/1000:,.0f} t", "🌍", COLORS['danger']), width=3),
        dbc.Col(create_kpi_card("Avg Efficiency", f"{df['route_efficiency_pct'].mean():.1f}%", "📊", COLORS['warning']), width=3),
    ], className="mb-4"),
    
    # Charts Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📈 Monthly Fuel & CO₂ Trend", style={'color': COLORS['primary']}),
                dbc.CardBody([dcc.Graph(id='trend-chart', config={'displayModeBar': False})])
            ], style={'backgroundColor': COLORS['card'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '10px'})
        ], width=8),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🛩️ Fuel Distribution by Aircraft", style={'color': COLORS['primary']}),
                dbc.CardBody([dcc.Graph(id='ac-distribution', config={'displayModeBar': False})])
            ], style={'backgroundColor': COLORS['card'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '10px'})
        ], width=4),
    ], className="mb-4"),
    
    # Charts Row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📊 Route Efficiency (kg/NM)", style={'color': COLORS['primary']}),
                dbc.CardBody([dcc.Graph(id='route-efficiency', config={'displayModeBar': False})])
            ], style={'backgroundColor': COLORS['card'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '10px'})
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("💰 Savings Opportunities", style={'color': COLORS['primary']}),
                dbc.CardBody([dcc.Graph(id='savings-chart', config={'displayModeBar': False})])
            ], style={'backgroundColor': COLORS['card'], 'border': f'1px solid {COLORS["border"]}', 'borderRadius': '10px'})
        ], width=6),
    ], className="mb-4"),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(style={'borderColor': COLORS['border']}),
            html.P([
                "© 2025 GreenWing Analytics | ",
                html.Span("CORSIA Compliant", style={'color': COLORS['primary']}), " | ",
                "Real-time Fuel Optimization Platform"
            ], className="text-center small", style={'color': COLORS['text_muted']})
        ])
    ]),
    
], fluid=True, style={'backgroundColor': COLORS['bg'], 'padding': '20px', 'minHeight': '100vh'})

# ═══════════════════════════════════════════════════════════
# CALLBACKS
# ═══════════════════════════════════════════════════════════

@app.callback(
    [Output('trend-chart', 'figure'),
     Output('ac-distribution', 'figure'),
     Output('route-efficiency', 'figure'),
     Output('savings-chart', 'figure')],
    [Input('aircraft-filter', 'value'),
     Input('route-filter', 'value'),
     Input('month-slider', 'value')]
)
def update_charts(aircraft_type, route, month_range):
    """Tüm grafikleri güncelle"""
    
    # Veriyi filtrele
    filtered_df = df.copy()
    
    # Month filter
    month_min, month_max = month_range
    month_num = filtered_df['month'].str.split('-').str[1].astype(int)
    filtered_df = filtered_df[month_num.between(month_min, month_max)]
    
    # Aircraft filter
    if aircraft_type != 'ALL':
        filtered_df = filtered_df[filtered_df['aircraft_type'] == aircraft_type]
    
    # Route filter
    if route != 'ALL':
        origin, dest = route.split('-')
        filtered_df = filtered_df[(filtered_df['origin'] == origin) & (filtered_df['destination'] == dest)]
    
    # 1. Trend Chart
    monthly = filtered_df.groupby('month').agg({
        'fuel_kg': 'sum',
        'co2_kg': 'sum'
    }).reset_index()
    
    trend_fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    trend_fig.add_trace(
        go.Bar(x=monthly['month'], y=monthly['fuel_kg']/1000, 
               name='⛽ Fuel (tons)', marker_color=COLORS['info'], text=monthly['fuel_kg']/1000,
               textposition='auto'),
        secondary_y=False
    )
    
    trend_fig.add_trace(
        go.Scatter(x=monthly['month'], y=monthly['co2_kg']/1000, 
                   name='🌍 CO₂ (tons)', line=dict(color=COLORS['danger'], width=3),
                   mode='lines+markers', marker=dict(size=8)),
        secondary_y=True
    )
    
    trend_fig.update_layout(
        plot_bgcolor=COLORS['card'],
        paper_bgcolor=COLORS['card'],
        font_color=COLORS['text'],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=40, b=40),
        height=350,
        hovermode='x unified'
    )
    trend_fig.update_yaxes(title_text="⛽ Fuel (tons)", secondary_y=False, gridcolor=COLORS['border'], color=COLORS['text'])
    trend_fig.update_yaxes(title_text="🌍 CO₂ (tons)", secondary_y=True, gridcolor=COLORS['border'], color=COLORS['text'])
    
    # 2. Aircraft Distribution
    ac_data = filtered_df.groupby('aircraft_type')['fuel_kg'].sum().reset_index()
    
    ac_fig = go.Figure(data=[go.Pie(
        labels=ac_data['aircraft_type'],
        values=ac_data['fuel_kg'],
        hole=0.4,
        marker_colors=[COLORS['primary'], COLORS['info'], COLORS['warning']],
        textinfo='label+percent',
        textfont=dict(size=12, color=COLORS['text']),
        hovertemplate="<b>%{label}</b><br>Fuel: %{value:,.0f} kg<br>Share: %{percent}<extra></extra>"
    )])
    
    ac_fig.update_layout(
        plot_bgcolor=COLORS['card'],
        paper_bgcolor=COLORS['card'],
        font_color=COLORS['text'],
        margin=dict(l=20, r=20, t=40, b=20),
        height=350,
        showlegend=False,
    )
    
    # 3. Route Efficiency
    route_data = filtered_df.groupby(['origin', 'destination']).agg({
        'fuel_per_nm': 'mean',
        'distance_nm': 'first'
    }).reset_index()
    route_data['route'] = route_data['origin'] + ' → ' + route_data['destination']
    route_data = route_data.sort_values('fuel_per_nm', ascending=True)
    
    route_fig = go.Figure()
    
    colors_bar = [
        COLORS['primary'] if x < 9 else COLORS['warning'] if x < 11 else COLORS['danger']
        for x in route_data['fuel_per_nm']
    ]
    
    route_fig.add_trace(go.Bar(
        y=route_data['route'],
        x=route_data['fuel_per_nm'],
        orientation='h',
        marker_color=colors_bar,
        text=route_data['fuel_per_nm'].round(1),
        textposition='outside',
        textfont=dict(color=COLORS['text']),
        hovertemplate="<b>%{y}</b><br>Fuel/NM: %{x:.1f} kg<extra></extra>"
    ))
    
    route_fig.add_vline(x=9.5, line_dash="dash", line_color=COLORS['warning'], line_width=2,
                        annotation_text="🎯 Industry Avg: 9.5", annotation_font_color=COLORS['warning'])
    
    route_fig.update_layout(
        plot_bgcolor=COLORS['card'],
        paper_bgcolor=COLORS['card'],
        font_color=COLORS['text'],
        margin=dict(l=100, r=60, t=40, b=40),
        xaxis_title="Fuel Consumption (kg/NM)",
        xaxis=dict(gridcolor=COLORS['border'], title_font=dict(color=COLORS['text'])),
        yaxis=dict(gridcolor=COLORS['border'], title_font=dict(color=COLORS['text'])),
        height=400,
    )
    
    # 4. Savings Chart
    savings = filtered_df.groupby(['origin', 'destination']).agg({
        'potential_saving_kg': 'sum'
    }).reset_index()
    savings['route'] = savings['origin'] + ' → ' + savings['destination']
    savings['saving_usd'] = savings['potential_saving_kg'] * 0.85
    savings['saving_co2'] = savings['potential_saving_kg'] * 3.16 / 1000
    savings = savings.sort_values('saving_usd', ascending=True).tail(10)
    
    savings_fig = go.Figure()
    
    savings_fig.add_trace(go.Bar(
        y=savings['route'],
        x=savings['saving_usd'],
        orientation='h',
        marker_color=COLORS['primary'],
        text=savings['saving_usd'].apply(lambda x: f"${x:,.0f}"),
        textposition='outside',
        textfont=dict(color=COLORS['text']),
        hovertemplate="<b>%{y}</b><br>💵 Savings: $%{x:,.0f}<br>🌍 CO₂ Reduction: %{customdata:,.0f} tons<extra></extra>",
        customdata=savings['saving_co2']
    ))
    
    savings_fig.update_layout(
        plot_bgcolor=COLORS['card'],
        paper_bgcolor=COLORS['card'],
        font_color=COLORS['text'],
        margin=dict(l=100, r=80, t=40, b=40),
        xaxis_title="💵 Potential Savings (USD)",
        xaxis=dict(gridcolor=COLORS['border'], title_font=dict(color=COLORS['text'])),
        yaxis=dict(gridcolor=COLORS['border'], title_font=dict(color=COLORS['text'])),
        height=400,
    )
    
    return trend_fig, ac_fig, route_fig, savings_fig

# ═══════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  🚀 GreenWing Analytics Dashboard")
    print("  📍 http://localhost:8050")
    print("  ⌨️  Press CTRL+C to stop")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=8050)