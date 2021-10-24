# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import base64
import os
import io

# https://dash-bootstrap-components.opensource.faculty.ai/docs/icons/
# https://bootswatch.com/lumen/
# https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
# https://dash.plotly.com/dash-core-components/radioitems
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button_group/
# https://dash.plotly.com/datatable/editable
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
# https://github.com/facultyai/dash-bootstrap-components
# https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
# https://towardsdatascience.com/create-a-professional-dasbhoard-with-dash-and-css-bootstrap-e1829e238fc5
# https://realpython.com/python-dash/
# https://dash.plotly.com/layout
# https://getbootstrap.com/docs/4.0/layout/grid/
# https://towardsdatascience.com/web-development-with-python-dash-complete-tutorial-6716186e09b3
# https://stackoverflow.com/questions/31575496/prevent-negative-inputs-in-form-input-type-number
# https://stackoverflow.com/questions/7372067/is-there-any-way-to-prevent-input-type-number-getting-negative-values
#
app = dash.Dash(__name__)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
app.title = "MDAPy Dashboard"
app.layout = dbc.Container(fluid=True, children=[

    dbc.CardHeader(children=[
        html.Img(src=app.get_asset_url('img/logo.png'), className="col-sm-1 align-self-center", style={'width': "100px"}),
        html.Div(className="col-sm-9 align-self-center"), # <i class="fab fa-bootstrap"></i>
        html.Div([dbc.Row([
        dbc.Col(children=[html.I(className='fa fa-undo'), " Reset Form"]),
        dbc.Col(children=[html.I(className='far fa-question-circle'), " Help"])
        ])], 
            className="col-sm-2 align-self-center")],
        className='row dashHeader justify-content-between'),

    html.Div(children=[
        html.Div(children=[
            html.B('Input Data'), html.Br(),html.Br(),
            html.Label('Select Dataset'),
            dcc.Dropdown(options=[{'label': u'Pb-U 206/238 & Pb-U 207/235', 'value': 'PbU'}, 
                                  {'label': u'Best Age & SX', 'value': 'BASX'}], value='PbU', id='dataset-dropdown'),
            html.Br(),
            html.Label('Select Sigma (sx)'),
            dcc.RadioItems(options=[{'label': '1 sx', 'value': 'SX1'}, {'label': '2 sx', 'value': 'SX2'}], value='SX1', labelClassName='col-sm-6'),
            html.Br(),
            html.Label('Select Uncertainty Format'),
            dcc.RadioItems(options=[{'label': 'Percent (%)', 'value': 'PER'}, 
                                    {'label': 'Absolute (ABS)', 'value': 'ABS'}],
                                     value='ABS', #labelStyle={'display': 'inline-block'},
                                     labelClassName='col-sm-6'),
            html.Br(),
            html.Div(children=[html.Label('Best Age Cut Off', className='labelCte col-sm-7'), dcc.Input(value=1500, type='number', className='inputNumbers col-sm-2')], className="row input-row"),
            html.Div(children=[html.Label('U238 Decay Constant (10⁻¹⁰)', className='labelCte col-sm-7'), dcc.Input(value=1.55125, type='number', className='inputNumbers col-sm-2')], className="row input-row"),
            html.Div(children=[html.Label('U235 Decay Constant (10⁻¹⁰)', className='labelCte col-sm-7'), dcc.Input(value=9.8485, type='number', className='inputNumbers col-sm-2')], className="row input-row"),
            html.Div(children=[html.Label('U238/U235 Decay Constant', className='labelCte col-sm-7'), dcc.Input(value=133.88, type='number', className='inputNumbers col-sm-2')], className="row input-row"),
            html.Br(),
            html.P('Input 0 if systematic uncertainties not required in final uncertainty calculation'),
            html.Br(),
            html.Div(children=[
            html.Label('Long Term Excess Variance: U-Pb 238/206', className='labelCte col-sm-9'),
            dcc.Input(value=1.2, type='number', className='inputCte col-sm-2',  min=0)
            ], className="row input-row"),
            html.Div(children=[
            html.Label('Long Term Excess Variance: Pb-Pb 207/206', className='labelCte col-sm-9'),
            dcc.Input(value=0.7, type='number', className='inputCte col-sm-2',  min=0)
            ], className="row input-row"),
            
            html.Div(children=[
            html.Label('Sy Calibration Uncertainty U-Pb 238/206', className='labelCte col-sm-9'),
            dcc.Input(value=0.6, type='number', className='inputCte col-sm-2',  min=0)
            ], className="row input-row"),
            
            html.Div(children=[
            html.Label('Sy Calibration Uncertainty Pb-Pb 207/206', className='labelCte col-sm-9'),
            dcc.Input(value=0.6, type='number', className='inputCte col-sm-2',  min=0)
            ], className="row input-row"),
            
            html.Div(children=[
                html.Label('Decay Constant Uncertainty U 238', className='labelCte col-sm-9'),
                dcc.Input(value=0.16, type='number', className='inputCte col-sm-2',  min=0)
            ], className="row input-row"),
            
            html.Div(children=[
            html.Label('Decay Constant Uncertainty U 235', className='labelCte col-sm-9'),
            dcc.Input(value=0.2, type='number', className='inputCte col-sm-2',  min=0)
            ], className="row input-row"),html.Br(),
            
            # html.Div(children=[
            # dbc.Button("Load Data", color="primary", id="data-load", className="mb-3 col-sm-4")
            # ], className="row justify-content-around settings-buttons"),

            dbc.Button("Load Sample Data", color="primary", id="data-load", className="mb-3 col-sm-11"),
            dcc.Upload(dbc.Button("Import Data", color="primary", className="mb-3 col-sm-12"), id="data-upload", className="col-sm-11"),
            dbc.Button("Download Import Template", color="primary", id="btn-download-template", className="mb-3 col-sm-11"),
            dcc.Download(id="download-template")

            

        ], className='col-sm-2 settings-menu'),
        html.Div(2, className='col-sm-9 workbench',id='main-panel'),
    ], className='row justify-content-between'),
    html.Br(),
    dbc.Alert("Hello Bootstrap!", color="success")],
    className="container-fluid",

)


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded),  sheet_name="Data")
    elif 'xlsx' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded),  sheet_name="Data")

    
@app.callback(Output('main-panel', 'children'),
              Input('dataset-dropdown', 'value'),
              Input('data-upload', 'contents'),
              State('data-upload', 'filename'),
              Input("data-load", "n_clicks"))
def update_output(selection, contents, filename, clicked):

    params = ['Sample_ID', 'Best_Age', 'Best_Age_sx']
    table = dash_table.DataTable(
        id='datatable-upload-container',
        columns=([{'id': p, 'name': p} for p in params]),
        data=[
            dict(Model=i, **{param: 0 for param in params})
            for i in range(1, 21)
        ],
        editable=True,
        page_action="native",
        page_size= 20
    ) 

    btn = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    print(btn)
    if btn == 'data-load':
        if selection == 'BASX':
            template_filename = "data/Data_Upload_Example_Data_Type_Ages.xlsx"
        elif selection == 'PbU':
            template_filename = "data/Data_Upload_Example_Data_Type_Ratios.xlsx"

        df = pd.read_excel(template_filename,  sheet_name="Data")

        table.data =df.to_dict('records')
        table.columns = [{"name": i, "id": i} for i in df.columns]
    elif btn =='data-upload':
        if contents is not None:
            df = parse_contents(contents, filename)
            table.data =df.to_dict('records')
            table.columns = [{"name": i, "id": i} for i in df.columns]
    else:     
        table = dash_table.DataTable(
            id='datatable-upload-container',
            columns=([{'id': p, 'name': p} for p in params]),
            data=[
                dict(Model=i, **{param: 0 for param in params})
                for i in range(1, 21)
            ],
            editable=True,
            page_action="native",
            page_size= 20
        )   


    #  df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]

    return table


@app.callback(
    Output("download-template", "data"),
    State('dataset-dropdown', 'value'),
    Input("btn-download-template", "n_clicks"),
    prevent_initial_call=True,
)
def func(selection, download):
    
    if selection == 'BASX':
        template_filename = "data/Data_Upload_Example_Data_Type_Ages.xlsx"
    elif selection == 'PbU':
        template_filename = "data/Data_Upload_Example_Data_Type_Ratios.xlsx"

    return dcc.send_file(template_filename)



# @app.callback(
#     Output('main-panel', 'children'),
#     State('dataset-dropdown', 'value'),
#     Input("data-load", "n_clicks"),
#     prevent_initial_call=True,
# )
# def func(selection, n_clicks):

#     btn = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
#     if btn == 'btn-download-template'

#     if selection == 'BASX':
#         template_filename = "data/Data_Upload_Example_Data_Type_Ages.xlsx"
#     elif selection == 'PbU':
#         template_filename = "data/Data_Upload_Example_Data_Type_Ratios.xlsx"

#     df = pd.read_excel(template_filename,  sheet_name="Data")

#     table = dash_table.DataTable(
#         id='datatable-upload-container',
#         columns=[{"name": i, "id": i} for i in df.columns],
#         data=df.to_dict('records'),
#         editable=True,
#         page_action="native",
#         page_size= 20
#     )  

#     return table




server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)

    # table = dash_table.DataTable(
    #     id='table-editing-simple',
    #     columns=[{"name": i, "id": i} for i in df.columns],
    #     data=df.to_dict('records'),
    #     editable=True,
    #     page_action="native",
    #     page_size= 20
    # )