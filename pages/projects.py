import dash
from dash import html
import dash_bootstrap_components as dbc
import json

# Register the page
dash.register_page(__name__, path='/projects', name='Projects', title='Projects - Erik Wiederstrom')

# Load projects data
with open('data/projects.json', 'r', encoding='utf-8') as f:
    projects_data = json.load(f)

def create_project_card(project):
    """Create a card for a single project"""
    # Create technology badges
    tech_badges = [
        dbc.Badge(tech, color="secondary", className="me-1 mb-1")
        for tech in project['technologies']
    ]

    # Create action buttons
    buttons = []
    if project['github_url']:
        buttons.append(
            dbc.Button([
                html.I(className="fab fa-github me-1"),
                "Code"
            ], href=project['github_url'], target="_blank", color="dark", outline=True, size="sm")
        )
    if project['demo_url']:
        buttons.append(
            dbc.Button([
                html.I(className="fas fa-external-link-alt me-1"),
                "Live Demo"
            ], href=project['demo_url'], target="_blank", color="primary", size="sm")
        )

    # Featured badge
    featured_badge = dbc.Badge("Featured", color="warning", className="position-absolute top-0 start-0 m-2") if project['is_featured'] else None

    # Create thumbnail image if available
    thumbnail = None
    if project.get('image_path'):
        image_url = project['image_path']
        thumbnail = dbc.CardImg(
            src=image_url,
            top=True,
            style={
                "height": "200px",
                "objectFit": "cover",
                "objectPosition": "top"
            }
        )

    card = dbc.Card([
        featured_badge,
        thumbnail,
        dbc.CardBody([
            html.H5(project['title'], className="card-title d-flex align-items-center"),
            html.P(project['description'], className="card-text mb-3"),
            html.Div([
                html.H6("Technologies:", className="mb-2"),
                html.Div(tech_badges, className="mb-3")
            ]),
            html.Div([
                html.H6("Key Highlights:", className="mb-2"),
                html.Ul([
                    html.Li(highlight) for highlight in project['highlights']
                ], className="small")
            ], className="mb-3"),
            html.Div(buttons, className="d-flex gap-2")
        ])
    ], className="h-100 position-relative")

    return card

def create_technology_summary():
    """Create a summary of technologies used across projects"""
    tech_count = {}
    for project in projects_data:
        for tech in project['technologies']:
            tech_count[tech] = tech_count.get(tech, 0) + 1
    
    # Sort by frequency
    sorted_techs = sorted(tech_count.items(), key=lambda x: x[1], reverse=True)
    
    return [
        dbc.Badge(f"{tech} ({count})", color="info", className="me-2 mb-2")
        for tech, count in sorted_techs
    ]

# Page layout
layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H1("Projects Portfolio", className="section-header"),
            html.P([
                "Welcome to my portfolio of data science and development projects. Each project represents a unique challenge "
                "where I've applied machine learning and data visualization to solve real-world problems. "
                "From deep learning models that classify medical imaging data to interactive dashboards that reveal insights in complex datasets, "
                "these projects demonstrate my ability to transform data into actionable insights and build production-ready applications."
            ], className="lead mb-4")
        ])
    ]),


    # Project summary cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(len(projects_data), className="text-primary mb-0"),
                    html.P("Total Projects", className="text-muted mb-0")
                ])
            ], className="text-center mb-3 mb-md-0")
        ], xs=6, md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(len([p for p in projects_data if p['is_featured']]), className="text-warning mb-0"),
                    html.P("Featured Projects", className="text-muted mb-0")
                ])
            ], className="text-center mb-3 mb-md-0")
        ], xs=6, md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(len(set(tech for project in projects_data for tech in project['technologies'])), className="text-info mb-0"),
                    html.P("Technologies", className="text-muted mb-0")
                ])
            ], className="text-center mb-3 mb-md-0")
        ], xs=6, md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(len([p for p in projects_data if p['demo_url']]), className="text-success mb-0"),
                    html.P("Live Demos", className="text-muted mb-0")
                ])
            ], className="text-center mb-3 mb-md-0")
        ], xs=6, md=3)
    ], className="mb-5"),


    # Projects grid
    dbc.Row([
        dbc.Col([
            create_project_card(project)
        ], xs=12, sm=6, lg=4, className="mb-4")
        for project in sorted(projects_data, key=lambda x: x['sort_order'])
    ]),
])
    