import os
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)

# Load the manual from MANUAL.md
# The file is located in the root of the project, two levels up from this file
MANUAL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'MDAPy_User_Manual.md')

try:
    with open(MANUAL_PATH, 'r', encoding='utf-8') as f:
        manual_content = f.read()
except FileNotFoundError:
    manual_content = "# Manual Not Found\n\nThe user manual could not be located. Please refer to the [GitHub repository](https://github.com/morganbrooks/MDAPy) for documentation."

layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Markdown(
                            children=manual_content,
                            style={
                                'fontFamily': 'inherit',
                                'fontSize': '0.9rem',
                                'lineHeight': '1.7',
                            }
                        )
                    ),
                    className='settings-menu',
                    style={'marginTop': '20px', 'marginBottom': '40px'}
                ),
                width=10,
                className='offset-1'
            )
        )
    ]
)
