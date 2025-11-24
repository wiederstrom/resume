import dash
from dash import html
import dash_bootstrap_components as dbc
import json

# Register the page
dash.register_page(__name__, path='/', name='Home', title='Erik Wiederstrøm - Data Scientist')

# Load data
def load_data():
    with open('data/personal_info.json', 'r', encoding='utf-8') as f:
        personal_info = json.load(f)
    with open('data/skills.json', 'r', encoding='utf-8') as f:
        skills = json.load(f)
    with open('data/projects.json', 'r', encoding='utf-8') as f:
        projects = json.load(f)
    with open('data/experience.json', 'r', encoding='utf-8') as f:
        experience = json.load(f)
    with open('data/volunteer.json', 'r', encoding='utf-8') as f:
        volunteer = json.load(f)
    return personal_info, skills, projects, experience, volunteer

personal_info, skills, projects, experience, volunteer = load_data()

# Helper functions
def create_technical_skills_display():
    """Create an organized display of technical skills from skills.json"""
    category_sections = []

    # Iterate through skills categories from skills.json
    for category in skills:
        cat_name = category['category']
        cat_skills = category['skills']

        if cat_skills:
            # Create skill badges with proficiency indicator
            skill_badges = []
            for skill in cat_skills:
                # Color based on proficiency
                if skill['proficiency'] >= 4:
                    color = "success"
                elif skill['proficiency'] >= 3:
                    color = "primary"
                else:
                    color = "secondary"

                skill_badges.append(
                    dbc.Badge(
                        skill['name'],
                        color=color, className="me-2 mb-2", style={"fontSize": "0.9rem"}
                    )
                )

            category_sections.append(
                html.Div([
                    html.H6(cat_name, className="mb-2 mt-3"),
                    html.Div(skill_badges)
                ])
            )

    return category_sections


def create_current_position_cards():
    """Create cards for current positions (work and volunteer)"""
    current_positions = []

    # Get current work positions
    for exp in experience:
        if exp['is_current']:
            current_positions.append({
                'title': exp['company'],
                'position': exp['position'],
                'location': exp['location'],
                'description': exp['description'],
                'image_path': exp.get('image_path'),
                'type': 'Work'
            })

    # Get current volunteer positions
    for vol in volunteer:
        if vol['is_current']:
            current_positions.append({
                'title': vol['organization'],
                'position': vol['position'],
                'location': vol['location'],
                'description': vol['description'],
                'image_path': vol.get('image_path'),
                'type': 'Volunteer'
            })

    # Create cards
    position_cards = []
    for pos in current_positions:
        # Create logo if available
        logo = None
        if pos.get('image_path'):
            image_url = pos['image_path']
            logo = html.Img(
                src=image_url,
                style={
                    "maxWidth": "100px",
                    "maxHeight": "100px",
                    "objectFit": "contain"
                }
            )

        # Build row columns
        row_cols = [
            dbc.Col([
                dbc.Badge(pos['type'], color="success" if pos['type'] == 'Work' else "info", className="mb-2"),
                html.H5(pos['position'], className="mb-1"),
                html.H6(pos['title'], className="text-primary mb-2"),
                html.P([
                    html.I(className="fas fa-map-marker-alt me-2"),
                    pos['location']
                ], className="text-muted mb-2"),
                html.P(pos['description'], className="mb-0")
            ], md=10)
        ]

        # Add logo column
        if logo is not None:
            row_cols.append(
                dbc.Col([
                    logo
                ], md=2, className="d-flex align-items-center justify-content-center")
            )

        card = dbc.Card([
            dbc.CardBody([
                dbc.Row(row_cols, className="align-items-center")
            ])
        ], className="mb-3")

        position_cards.append(card)

    return position_cards

# Page layout
layout = html.Div([
    # Hero Section
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.H1(personal_info['full_name'], className="display-4 fw-bold mb-3"),
                        html.H3(personal_info['title'], className="mb-4 fw-light"),
                        html.P(personal_info['summary'], className="lead mb-4"),
                        dbc.ButtonGroup([
                            dbc.Button([
                                html.I(className="fab fa-linkedin me-2"),
                                "LinkedIn"
                            ], href=personal_info['linkedin'], target="_blank", color="light", outline=True),
                            dbc.Button([
                                html.I(className="fab fa-github me-2"),
                                "GitHub"
                            ], href=personal_info['github'], target="_blank", color="light", outline=True),
                            dbc.Button([
                                html.I(className="fas fa-envelope me-2"),
                                "Contact"
                            ], href=f"mailto:{personal_info['email']}", color="light")
                        ], className="d-flex flex-column flex-md-row gap-2")
                    ], xs=12, md=8, className="mb-4 mb-md-0"),
                    dbc.Col([
                        html.Div([
                            html.Img(
                                src="/assets/profile.jpg",
                                className="img-fluid rounded-circle",
                                style={"maxWidth": "400px"}
                            )
                        ], className="text-center")
                    ], xs=12, md=4)
                ])
            ], className="hero-section text-white p-5 rounded mb-5")
        ])
    ]),
    
    # Skills and Projects Row
    dbc.Row([
        # Technical Skills from Data Science Education
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Technical Skills", className="mb-0")
                ]),
                dbc.CardBody([
                    html.Div(create_technical_skills_display())
                ])
            ], className="mb-3 mb-md-0")
        ], xs=12, md=6),

        # Featured Projects
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Featured Projects", className="mb-0")
                ]),
                dbc.CardBody([
                    html.Div([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6(project['title'], className="card-title mb-2"),
                                html.P(project['description'][:100] + "...", className="card-text small mb-2"),
                                html.Div([
                                    dbc.Badge(tech, color="secondary", className="me-1 mb-1")
                                    for tech in project['technologies'][:3]
                                ], className="mb-2"),
                                html.Div([
                                    dbc.Button([
                                        html.I(className="fab fa-github me-1"),
                                        "Code"
                                    ], href=project['github_url'], target="_blank", color="dark", outline=True, size="sm", className="me-2")
                                    if project.get('github_url') else None,
                                    dbc.Button([
                                        html.I(className="fas fa-external-link-alt me-1"),
                                        "Demo"
                                    ], href=project['demo_url'], target="_blank", color="primary", size="sm")
                                    if project.get('demo_url') else None
                                ], className="d-flex gap-1 flex-wrap")
                            ])
                        ], className="mb-2")
                        for project in [p for p in projects if p['is_featured']][:3]
                    ]),
                    html.Div([
                        dbc.Button("View All Projects", href="/projects", color="primary", size="sm", className="w-100 w-md-auto")
                    ], className="text-center mt-3")
                ])
            ])
        ], xs=12, md=6)
    ], className="mb-5"),
    
    # Current Positions
    dbc.Row([
        dbc.Col([
            html.H3("Current Positions", className="section-header mb-4"),
            html.Div(create_current_position_cards())
        ])
    ])
])
