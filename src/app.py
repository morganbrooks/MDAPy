# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import os

DASH_HOT_RELOAD = os.getenv("DASH_HOT_RELOAD") or False
DASH_DEBUG = os.getenv("DASH_DEBUG") or False

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True, use_pages=True)
app.title = "MDAPy Dashboard"
app.layout = dbc.Container(fluid=True, children=[

    dbc.CardHeader(children=[
        html.A([html.Img(src=app.get_asset_url('img/logo.png'), className="col-sm-1 align-self-center",
               style={'width': "auto", 'height': "90px"})], href='/', style={'width': 'auto'}),
        # <i class="fab fa-bootstrap"></i>
        html.Div(className="col-12 col-xxl-8 align-self-center"),
        html.Div([dbc.Row([
            dbc.Button([html.I(className='fa fa-undo'), " Reset Form"],
                       color="outline-primary", id="data-reset", className="col-sm-5"),
            html.Div(className="col-sm-1"),
            dbc.Button([html.I(className='far fa-question-circle'), " Help"],
                       color="outline-primary", id="data-help", className="col-sm-5", href="help")
        ])], className="col-12 col-xxl-2 align-self-center")],
        className='row dashHeader justify-content-between'),
    
    # Loads the content from the child pages
	dash.page_container,

    html.Br(),
    # dcc.Store stores the intermediate value
    dcc.Store(id='computed-data'),
    dcc.Store(id='computed-data-errors'),
    # dbc.Alert("Hello Bootstrap!", color="success")
],
    className="container-fluid",

)

server = app.server


if __name__ == '__main__':
    app.run_server(debug=DASH_DEBUG, dev_tools_hot_reload=DASH_HOT_RELOAD)
