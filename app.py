from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.utils
import json
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

class LinuxKPIGenerator:
    def __init__(self):
        self.regions = {
            'North America': {'base': 1000000, 'growth_rate': 0.15},
            'Europe': {'base': 800000, 'growth_rate': 0.18},
            'Asia Pacific': {'base': 600000, 'growth_rate': 0.25},
            'South America': {'base': 200000, 'growth_rate': 0.20},
            'Africa': {'base': 100000, 'growth_rate': 0.30},
            'Middle East': {'base': 150000, 'growth_rate': 0.22}
        }
        
    def generate_data(self):
        """Generate realistic Linux instance data from 2000 to 2025"""
        years = list(range(2000, 2026))
        data = []
        
        for year in years:
            year_data = {'year': year}
            total_instances = 0
            
            for region, config in self.regions.items():
                # Calculate instances with exponential growth and some randomness
                years_from_start = year - 2000
                base_growth = config['base'] * (1 + config['growth_rate']) ** years_from_start
                
                # Add some realistic fluctuations
                fluctuation = random.uniform(0.85, 1.15)
                instances = int(base_growth * fluctuation)
                
                # Add economic crisis impacts (2008, 2020)
                if year == 2008:
                    instances = int(instances * 0.9)
                elif year == 2020:
                    instances = int(instances * 1.1)  # COVID boost for cloud/remote
                
                year_data[region] = instances
                total_instances += instances
            
            year_data['Total'] = total_instances
            data.append(year_data)
        
        return pd.DataFrame(data)

def create_kpi_charts(df):
    """Create various KPI charts using Plotly"""
    charts = {}
    
    # 1. Total Linux Instances Over Time
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df['year'],
        y=df['Total'],
        mode='lines+markers',
        name='Total Linux Instances',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=8)
    ))
    fig1.update_layout(
        title='Global Linux Instances Growth (2000-2025)',
        xaxis_title='Year',
        yaxis_title='Number of Instances',
        template='plotly_white',
        height=400
    )
    charts['total_growth'] = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 2. Regional Distribution Over Time (Stacked Area)
    fig2 = go.Figure()
    regions = [col for col in df.columns if col not in ['year', 'Total']]
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592E83', '#1B998B']
    
    for i, region in enumerate(regions):
        fig2.add_trace(go.Scatter(
            x=df['year'],
            y=df[region],
            mode='lines',
            stackgroup='one',
            name=region,
            fill='tonexty' if i > 0 else 'tozeroy',
            line=dict(color=colors[i % len(colors)])
        ))
    
    fig2.update_layout(
        title='Linux Instances by Region (Stacked)',
        xaxis_title='Year',
        yaxis_title='Number of Instances',
        template='plotly_white',
        height=400
    )
    charts['regional_stacked'] = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 3. Year-over-Year Growth Rate
    df['growth_rate'] = df['Total'].pct_change() * 100
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=df['year'][1:],  # Skip first year (no growth rate)
        y=df['growth_rate'][1:],
        name='YoY Growth Rate',
        marker_color=['red' if x < 0 else 'green' for x in df['growth_rate'][1:]]
    ))
    fig3.update_layout(
        title='Year-over-Year Growth Rate (%)',
        xaxis_title='Year',
        yaxis_title='Growth Rate (%)',
        template='plotly_white',
        height=400
    )
    charts['growth_rate'] = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 4. Regional Market Share (Latest Year)
    latest_year_data = df[df['year'] == 2025].iloc[0]
    regions_data = {region: latest_year_data[region] for region in regions}
    
    fig4 = go.Figure(data=[go.Pie(
        labels=list(regions_data.keys()),
        values=list(regions_data.values()),
        hole=0.3,
        marker_colors=colors
    )])
    fig4.update_layout(
        title='Regional Market Share (2025)',
        template='plotly_white',
        height=400
    )
    charts['market_share'] = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

@app.route('/')
def dashboard():
    """Main dashboard page"""
    generator = LinuxKPIGenerator()
    df = generator.generate_data()
    charts = create_kpi_charts(df)
    
    # Calculate summary KPIs
    latest_data = df[df['year'] == 2025].iloc[0]
    first_data = df[df['year'] == 2000].iloc[0]
    
    kpis = {
        'total_instances_2025': f"{latest_data['Total']:,}",
        'total_growth_25_years': f"{((latest_data['Total'] / first_data['Total'] - 1) * 100):.1f}%",
        'avg_annual_growth': f"{(((latest_data['Total'] / first_data['Total']) ** (1/25) - 1) * 100):.1f}%",
        'fastest_growing_region': max(
            [col for col in df.columns if col not in ['year', 'Total', 'growth_rate']], 
            key=lambda x: latest_data[x] / first_data[x]
        )
    }
    
    return render_template('dashboard.html', charts=charts, kpis=kpis)

@app.route('/api/data')
def get_data():
    """API endpoint to get raw data"""
    generator = LinuxKPIGenerator()
    df = generator.generate_data()
    return jsonify(df.to_dict('records'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12001, debug=False)