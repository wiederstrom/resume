import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import json
from datetime import datetime

# Register the page
dash.register_page(__name__, path='/experience', name='Experience', title='Experience - Erik Wiederstrom')

# Load experience data
with open('data/experience.json', 'r', encoding='utf-8') as f:
    experience_data = json.load(f)

def create_experience_timeline():
    """Create a timeline of work experience"""
    timeline_items = []
    
    for exp in sorted(experience_data, key=lambda x: x['start_date'], reverse=True):
        # Parse dates
        start_date = datetime.strptime(exp['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(exp['end_date'], '%Y-%m-%d') if exp['end_date'] else datetime.now()
        
        # Calculate duration
        duration = end_date - start_date
        years = duration.days / 365.25
        
        # Format dates for display
        start_str = start_date.strftime('%B %Y')
        end_str = end_date.strftime('%B %Y') if exp['end_date'] else 'Present'
        
        # Create company logo/image
        company_logo = None
        if exp.get('image_path'):
            image_url = exp['image_path']
            company_logo = html.Img(
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
                html.H4(exp['position'], className="mb-1"),
                html.H5([
                    exp['company'],
                    dbc.Badge("Current", color="success", className="ms-2") if exp['is_current'] else None
                ], className="text-primary mb-2"),
                html.P([
                    html.I(className="fas fa-map-marker-alt me-2"),
                    exp['location'],
                    html.Span(" • ", className="mx-2"),
                    html.I(className="fas fa-calendar me-2"),
                    f"{start_str} - {end_str}",
                    html.Span(" • ", className="mx-2"),
                    html.I(className="fas fa-clock me-2"),
                    f"{years:.0f} years"
                ], className="text-muted mb-3"),
                html.P(exp['description'], className="mb-3"),
                html.Div([
                    html.H6("Key Responsibilities & Achievements:", className="mb-2"),
                    html.Ul([
                        html.Li(highlight)
                        for highlight in exp.get('highlights', [])
                    ])
                ]) if exp.get('highlights') else None
            ], md=10)
        ]

        # Add logo column if logo exists
        if company_logo is not None:
            row_cols.append(
                dbc.Col([
                    company_logo
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

def create_experience_summary():
    """Create summary statistics of experience"""
    current_positions = 0
    companies = set()

    for exp in experience_data:
        if exp['is_current']:
            current_positions += 1

        companies.add(exp['company'])

    return {
        'current_positions': current_positions,
        'companies': len(companies),
        'total_positions': len(experience_data)
    }

# Page layout
layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H1("Professional Experience", className="section-header"),
            html.P("My professional journey and key contributions across different organizations.", 
                  className="lead mb-4")
        ])
    ]),
    
    # Experience summary cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("10+", className="text-primary mb-0"),
                    html.P("Years Relevant Experience", className="text-muted mb-0")
                ])
            ], className="text-center")
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(create_experience_summary()['current_positions'], className="text-success mb-0"),
                    html.P("Current Positions", className="text-muted mb-0")
                ])
            ], className="text-center")
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(create_experience_summary()['companies'], className="text-info mb-0"),
                    html.P("Companies", className="text-muted mb-0")
                ])
            ], className="text-center")
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(create_experience_summary()['total_positions'], className="text-warning mb-0"),
                    html.P("Total Positions", className="text-muted mb-0")
                ])
            ], className="text-center")
        ], md=3)
    ], className="mb-5"),
    
    # Experience timeline
    dbc.Row([
        dbc.Col([
            html.H3("Career Timeline", className="mb-4"),
            html.Div(create_experience_timeline())
        ])
    ]),
    
    # Skills developed section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Key Skills Developed", className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("Leadership & Management", className="text-primary"),
                            html.Ul([
                                html.Li("Strategic planning and execution"),
                                html.Li("Team coordination and project management"),
                                html.Li("Stakeholder communication"),
                                html.Li("Budget planning and resource allocation")
                            ])
                        ], md=6),
                        dbc.Col([
                            html.H6("Data & Analytics", className="text-primary"),
                            html.Ul([
                                html.Li("Data-driven decision making"),
                                html.Li("Performance metrics analysis"),
                                html.Li("Process optimization"),
                                html.Li("Reporting and visualization")
                            ])
                        ], md=6)
                    ])
                ])
            ])
        ])
    ], className="mt-4")
])
