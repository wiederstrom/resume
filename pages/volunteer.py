import dash
from dash import html
import dash_bootstrap_components as dbc
import json
from datetime import datetime

# Register the page
dash.register_page(__name__, path='/volunteer', name='Volunteer Work', title='Volunteer Work - Erik Wiederstrom')

# Load volunteer data
with open('data/volunteer.json', 'r', encoding='utf-8') as f:
    volunteer_data = json.load(f)

def create_volunteer_timeline():
    """Create a timeline of volunteer work"""
    timeline_items = []

    for vol in sorted(volunteer_data, key=lambda x: x['start_date'], reverse=True):
        # Parse dates
        start_date = datetime.strptime(vol['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(vol['end_date'], '%Y-%m-%d') if vol['end_date'] else datetime.now()

        # Calculate duration
        duration = end_date - start_date
        years = duration.days / 365.25

        # Format dates for display
        start_str = start_date.strftime('%B %Y')
        end_str = end_date.strftime('%B %Y') if vol['end_date'] else 'Present'

        # Format duration
        if years >= 1:
            duration_str = f"{years:.0f} years"
        else:
            months = int(duration.days / 30)
            duration_str = f"{months} months" if months > 1 else f"{months} month"

        # Create organization logo/image
        org_logo = None
        if vol.get('image_path'):
            image_url = vol['image_path']
            org_logo = html.Img(
                src=image_url,
                style={
                    "maxWidth": "200px",
                    "maxHeight": "200px",
                    "objectFit": "contain"
                }
            )

        # Build row columns
        row_cols = [
            dbc.Col([
                html.H4(vol['position'], className="mb-1"),
                html.H5([
                    vol['organization'],
                    dbc.Badge("Current", color="success", className="ms-2") if vol['is_current'] else None
                ], className="text-primary mb-2"),
                html.P([
                    html.I(className="fas fa-map-marker-alt me-2"),
                    vol['location'],
                    html.Span(" • ", className="mx-2"),
                    html.I(className="fas fa-calendar me-2"),
                    f"{start_str} - {end_str}",
                    html.Span(" • ", className="mx-2"),
                    html.I(className="fas fa-clock me-2"),
                    duration_str
                ], className="text-muted mb-3"),
                html.P(vol['description'], className="mb-3"),
                html.Div([
                    html.H6("Contributions & Impact:", className="mb-2"),
                    html.Ul([
                        html.Li(highlight)
                        for highlight in vol.get('highlights', [])
                    ])
                ]) if vol.get('highlights') else None
            ], md=10)
        ]

        # Add logo column if logo exists
        if org_logo is not None:
            row_cols.append(
                dbc.Col([
                    org_logo
                ], md=2, className="d-flex align-items-center justify-content-center")
            )

        # Create timeline item
        timeline_item = dbc.Card([
            dbc.CardBody([
                dbc.Row(row_cols, className="align-items-center")
            ])
        ], className="mb-4")

        timeline_items.append(timeline_item)

    return timeline_items

# Page layout
layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H1("Volunteer Work", className="section-header"),
            html.P("My community involvement spans leadership roles in sports organizations, youth safety initiatives, and humanitarian fundraising. These positions have involved project management, budget planning, and cross-sector collaboration while contributing to my local community in Bergen.",
                  className="lead mb-4")
        ])
    ]),

    # Volunteer summary cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(len(volunteer_data), className="text-primary mb-0"),
                    html.P("Volunteer Positions", className="text-muted mb-0")
                ])
            ], className="text-center")
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(len([v for v in volunteer_data if v['is_current']]), className="text-success mb-0"),
                    html.P("Current Positions", className="text-muted mb-0")
                ])
            ], className="text-center")
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(len(set(v['organization'] for v in volunteer_data)), className="text-info mb-0"),
                    html.P("Organizations", className="text-muted mb-0")
                ])
            ], className="text-center")
        ], md=4)
    ], className="mb-5"),

    # Volunteer timeline
    dbc.Row([
        dbc.Col([
            html.H3("Volunteer Timeline", className="mb-4"),
            html.Div(create_volunteer_timeline())
        ])
    ])
])
