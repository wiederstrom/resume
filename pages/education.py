import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import json
from datetime import datetime

# Register the page
dash.register_page(__name__, path='/education', name='Education', title='Education - Erik Wiederstrom')

# Load education data
with open('data/education.json', 'r', encoding='utf-8') as f:
    education_data = json.load(f)

def create_education_cards():
    """Create cards for each education entry"""
    cards = []
    
    for edu in sorted(education_data, key=lambda x: x['end_date'] if x['end_date'] else '9999-12-31', reverse=True):
        # Parse dates
        start_date = datetime.strptime(edu['start_date'], '%Y-%m-%d') if edu['start_date'] else None
        end_date = datetime.strptime(edu['end_date'], '%Y-%m-%d') if edu['end_date'] else None
        
        # Format dates
        start_str = start_date.strftime('%Y') if start_date else 'N/A'
        end_str = end_date.strftime('%Y') if end_date else 'Present'
        
        # Calculate duration if both dates available
        duration = ""
        if start_date and end_date:
            years = (end_date - start_date).days / 365
            duration = f" • {years:.0f} years"
        
        # Create tumbnails
        if edu.get('image_path'):
            image_url = edu['image_path']
            institution_image = html.Img(
                src=image_url,
                style={
                    "maxWidth": "120px",
                    "maxHeight": "120px",
                    "objectFit": "contain"
                },
                className="mb-2"
            )
        else:
            institution_image = html.I(className="fas fa-graduation-cap fa-3x text-muted")

        card = dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H4(f"{edu['degree']} in {edu['field_of_study']}", className="mb-2"),
                        html.H5(edu['institution'], className="text-primary mb-3"),
                        html.P([
                            html.I(className="fas fa-map-marker-alt me-2"),
                            edu['location'],
                            html.Span(" • ", className="mx-2"),
                            html.I(className="fas fa-calendar me-2"),
                            f"{start_str} - {end_str}{duration}"
                        ], className="text-muted mb-3"),
                        html.P(edu['description'], className="mb-3") if edu.get('description') else None,
                        html.Div([
                            html.H6("Key Areas of Study:", className="mb-2"),
                            html.Div([
                                dbc.Badge(area, color="info", className="me-2 mb-2")
                                for area in edu.get('highlights', [])
                            ])
                        ]) if edu.get('highlights') else None
                    ], md=10),
                    dbc.Col([
                        html.Div([
                            institution_image
                        ], className="text-center")
                    ], md=2)
                ])
            ])
        ], className="mb-4")
        
        cards.append(card)
    
    return cards

def create_academic_skills():
    """Create a section highlighting academic skills"""
    skills_categories = [
        {
            "category": "Core Data Science",
            "skills": [
                "Statistical Analysis & Modeling",
                "Machine Learning Algorithms",
                "Deep Learning & Neural Networks",
                "Data Mining & Pattern Recognition",
                "Predictive Analytics"
            ]
        },
        {
            "category": "Programming & Tools",
            "skills": [
                "Python (Pandas, NumPy, Scikit-learn)",
                "R (tidyverse, ggplot2, caret)",
                "SQL & Database Management",
                "Git Version Control",
                "Jupyter Notebooks & RStudio"
            ]
        },
        {
            "category": "Data Visualization",
            "skills": [
                "Matplotlib & Seaborn",
                "Plotly & Bokeh",
                "Tableau & Power BI",
                "D3.js Fundamentals",
                "Statistical Graphics"
            ]
        },
        {
            "category": "Mathematics & Statistics",
            "skills": [
                "Probability Theory",
                "Hypothesis Testing",
                "Regression Analysis",
                "Time Series Analysis",
                "Bayesian Statistics"
            ]
        }
    ]
    
    return skills_categories

# Page layout
layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H1("Education", className="section-header"),
            html.P("My academic background and formal training in data science and related fields.", 
                  className="lead mb-4")
        ])
    ]),
    
    # Education cards
    dbc.Row([
        dbc.Col([
            html.H3("Academic Qualifications", className="mb-4"),
            html.Div(create_education_cards())
        ])
    ]),
    
    # Academic skills section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Academic Skills & Knowledge Areas", className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6(category["category"], className="text-primary mb-3"),
                            html.Ul([
                                html.Li(skill) for skill in category["skills"]
                            ], className="mb-4")
                        ], md=6) 
                        for i, category in enumerate(create_academic_skills())
                        if i % 2 == 0
                    ] + [
                        dbc.Col([
                            html.H6(category["category"], className="text-primary mb-3"),
                            html.Ul([
                                html.Li(skill) for skill in category["skills"]
                            ], className="mb-4")
                        ], md=6)
                        for i, category in enumerate(create_academic_skills())
                        if i % 2 == 1
                    ])
                ])
            ])
        ])
    ], className="mb-4"),
])
