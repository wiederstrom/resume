import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from datetime import datetime

# Initialize the Dash app
app = Dash(__name__,
          external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
          use_pages=True,
          suppress_callback_exceptions=True,
          meta_tags=[
              {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=5"}
          ])

# App title
app.title = "Erik Wiederstrom - Data Scientist"

# Navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("Work", href="/experience", active="exact")),
        dbc.NavItem(dbc.NavLink("Education", href="/education", active="exact")),
        dbc.NavItem(dbc.NavLink("Volunteer", href="/volunteer", active="exact")),
        dbc.NavItem(dbc.NavLink("Portfolio", href="/projects", active="exact")),
    ],
    brand="",
    brand_href="/",
    color="dark",
    dark=True,
    fluid=True,
    className="mb-4"
)

# Main app layout
app.layout = dbc.Container([
    navbar,
    dash.page_container,
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.P([
                "Built with ",
                html.A("Dash", href="https://plotly.com/dash/", target="_blank"),
                " & Python • ",
                f"Last updated: {datetime.now().strftime('%B %Y')}"
            ], className="text-center text-muted small")
        ])
    ])
], fluid=True)


server = app.server

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
