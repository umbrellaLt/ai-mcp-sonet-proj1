# Linux Instances KPI Dashboard

A Python web application that displays interactive KPI graphs showing active Linux instances worldwide from 2000 to 2025.

## Features

- **Interactive Charts**: Built with Plotly for dynamic data visualization
- **Multiple KPIs**: 
  - Total Linux instances growth over time
  - Regional distribution (stacked area chart)
  - Year-over-year growth rates
  - Regional market share (pie chart)
- **Responsive Design**: Bootstrap-based UI that works on all devices
- **RESTful API**: JSON endpoint for raw data access

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Visualization**: Plotly.js for interactive charts
- **Frontend**: Bootstrap 5 for responsive UI
- **Data Processing**: Pandas and NumPy for data manipulation

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access the dashboard at: http://localhost:12001

## API Endpoints

- `GET /` - Main dashboard with interactive charts
- `GET /api/data` - JSON data endpoint

## Data Model

The application generates realistic synthetic data representing Linux server adoption across six regions:
- North America
- Europe  
- Asia Pacific
- South America
- Africa
- Middle East

Data includes realistic growth patterns, economic impact events (2008 financial crisis, 2020 COVID boost), and regional variations in adoption rates.

## Charts Available

1. **Total Growth**: Line chart showing global Linux instances from 2000-2025
2. **Regional Distribution**: Stacked area chart showing regional breakdown over time
3. **Growth Rate**: Bar chart displaying year-over-year percentage growth
4. **Market Share**: Pie chart showing regional distribution for 2025

## Configuration

The application runs on port 12001 by default and is configured to:
- Accept connections from any host (0.0.0.0)
- Enable CORS for cross-origin requests
- Support iframe embedding

## Live Demo

The application is designed to be deployed and accessed via web browser for interactive data exploration.

## Future Enhancements

- Real-time data integration
- Additional chart types (heatmaps, treemaps)
- Export functionality (PDF, PNG, CSV)
- User authentication and personalized dashboards
- Historical data comparison tools