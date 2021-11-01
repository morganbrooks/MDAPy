# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import json
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from MDAPy import MDAPy_Functions as MDAFunc
import plotly.express as px
import pandas as pd
import base64
import os
import numpy as np
import io

# https://dash-bootstrap-components.opensource.faculty.ai/docs/icons/
# https://bootswatch.com/lumen/
# https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
# https://dash.plotly.com/dash-core-components/radioitems
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button_group/
# https://dash.plotly.com/datatable/editable
# https://dash.plotly.com/datatable/interactivity
# https://dash.plotly.com/datatable/style
# https://dash.plotly.com/dash-core-components/upload
# https://dash.plotly.com/interactive-graphing
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
# app = dash.Dash(__name__)
# 
# Callbacks
# https://dash.plotly.com/advanced-callbacks
# https://dash.plotly.com/dash-core-components/download
# https://docs.faculty.ai/user-guide/apps/examples/dash_file_upload_download.html
#
# ASSETS
# https://dash.plotly.com/external-resources
# https://dash.plotly.com/dash-enterprise/static-assets
#

def sampleSelector(df):
    checklist_options = [{'label': 'Sample ' + i, 'value': i} for i in df]
    # checklist_options.append({'label': 'All Samples', 'value': json.dumps([i for i in df])})
    selector = dcc.Checklist(options = checklist_options, value = [df[0]],
    labelStyle = {'display': 'inline-block', 'margin-bottom': '0.5rem', 'font-size': '1.15rem'}, labelClassName='col-sm-6')
    return selector


dimensions = [html.H5('Age Plotting Dimensions'), html.Br(), html.P('For individual MDA plots with all ages plotted, this input controls the maximum age to be plotted to control how many measurements are shown on one plot. Input (Ma) will be added to the oldest age in the age clusters to give a max plotting age.')]

summary = html.Div(id='summary-header', children=[
            html.Div(id='summary-data', className="col-sm-3 summary-cards", style={'height': '100%'}),
            html.Div(id='sample-selector',className="col-sm-3 summary-cards", style={'height': '100%'}),
            html.Div(id='plotting-dimensions', className="col-sm-3 summary-cards", style={'height': '100%'}),
            ], className="row input-row justify-content-between", style={'height': '275px'})


methods = html.Div(id='summary-methods', children=[
    dbc.Button([html.I(className='far fa-question-circle'), " Calculate All MDA Methods And Plot"], color="outline-primary", className="col-sm-3 button-method"),
    dbc.Button([html.I(className='far fa-question-circle'), " Calculate Individual MDAs And Plot"], color="outline-primary", className="col-sm-3 button-method"),
    dbc.Button([html.I(className='far fa-question-circle'), " Plot All Samples With One MDA Method"], color="outline-primary", className="col-sm-3 button-method")
            ], className="row input-row justify-content-between")

accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem([html.Div(id='main-panel')], title="Inspect Dataset"),
            dbc.AccordionItem(
                [
                    # html.P("This is the content of the second section"),
                    # dbc.Button("Don't click me!", color="danger"),
                    summary,
                    methods,
                ],
                title="Run Analysis",
            ),
        ],
    ), className='col-sm-9 workbench'
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
app.title = "MDAPy Dashboard"
app.layout = dbc.Container(fluid=True, children=[

    dbc.CardHeader(children=[
        html.A([html.Img(src=app.get_asset_url('img/logo.png'), className="col-sm-1 align-self-center", style={'width': "auto", 'height': "50px"})], href='/', style={'width':'auto'}),
        html.Div(className="col-sm-9 align-self-center"), # <i class="fab fa-bootstrap"></i>
        html.Div([dbc.Row([
        dbc.Button([html.I(className='fa fa-undo'), " Reset Form"], color="outline-primary", id="data-reset", className="col-sm-5"), 
        html.Div(className="col-sm-1"),
        dbc.Button([html.I(className='far fa-question-circle'), " Help"], color="outline-primary", id="data-help", className="col-sm-5")
        ])], className="col-sm-2 align-self-center")],
        className='row dashHeader justify-content-between'),
    
    html.Div(children=[
        html.Div(children=[
            html.B('Input Data'), html.Br(),html.Br(),
            html.Label('Select Dataset'),
            dcc.Dropdown(options=[{'label': u'Pb-U 206/238 & Pb-U 207/235', 'value': '238U/206Pb_&_207Pb/206Pb'}, 
                                  {'label': u'Best Age & SX', 'value': 'Ages'}], value='Ages', id='dataset-dropdown'),
            html.Br(),
            html.Label('Select Sigma (sx)'),
            dcc.RadioItems(options=[{'label': '1 sx', 'value': 1}, {'label': '2 sx', 'value': 2}],
                           id='radio-sigma', value=1, labelClassName='col-sm-6'),
            html.Br(),
            html.Label('Select Uncertainty Format'),
            dcc.RadioItems(options=[{'label': 'Percent (%)', 'value': 'percent'}, 
                                    {'label': 'Absolute (ABS)', 'value': 'absolute'}],
                                     value='percent', id='radio-uncertainty', 
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

            dbc.Button("Load Sample Data", color="primary", id="data-load", className="mb-3 col-sm-11"),
            dcc.Upload(dbc.Button("Import Data", color="primary", className="mb-3 col-sm-12"), id="data-upload", className="col-sm-11"),
            dbc.Button("Download Import Template", color="primary", id="btn-download-template", className="mb-3 col-sm-11"),
            dcc.Download(id="download-template")            

        ], className='col-sm-2 settings-menu'),
        accordion,
    ], className='row justify-content-between'), 
    html.Br(),
    # dcc.Store stores the intermediate value
    dcc.Store(id='computed-data'),
    # dbc.Alert("Hello Bootstrap!", color="success")
    ],
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
        with open('data/temp_data.xlsx', "wb") as fp:
            fp.write(decoded)
        # with pd.ExcelWriter('data/temp_data.xlsx') as writer:  
        #     df_data = pd.read_excel(io.BytesIO(decoded), sheet_name="Data")
        #     df_data = df_data.set_index('Sample_ID')
        #     df_data.to_excel(writer, sheet_name='Data')
        #     df_samples = pd.read_excel(io.BytesIO(decoded), sheet_name="Samples")
        #     sample_list = np.array(df_samples['Sample_ID'])
        #     df_samples = pd.DataFrame(data=sample_list, columns=['Sample_ID'])
        #     df_samples = df_samples.set_index('Sample_ID')
        #     df_samples.to_excel(writer, sheet_name='Samples')
        #
        # return pd.read_excel(io.BytesIO(decoded),  sheet_name="Data")
        return 'data/temp_data.xlsx'

def MDATabLoader(template_path, selection):
    main_df, main_byid_df, samples_df, analyses_df, Data_Type  = MDAFunc.loadDataExcel([template_path], selection)
    tabs = []
    for idx, idx_df in enumerate(samples_df['Sample_ID']):

        temp = analyses_df.loc[analyses_df['Sample_ID'] == idx_df]
        temp = temp.drop('Sample_ID', axis=1)

        tabs.append(
            dcc.Tab(
                label=f"Sample { idx_df }",
                value=f"tab{ idx + 1 }",
                children=[html.Br(),
                            dash_table.DataTable(id='datatable-upload-container',
                                                columns=[{"name": i, "id": i} for i in temp.columns],
                                                data=temp.to_dict('records'),
                                                editable=True, style_cell={'textAlign': 'center'},
                                                page_action="native",
                                                page_size=10)])
        )
    # 
    sa_tables = MDAFunc.check_data_loading(analyses_df, Data_Type)
    sample_selector = sampleSelector(sa_tables['Sample_ID'])
    summary_table = dash_table.DataTable(id='datatable-summary', columns=[{"name": i, "id": i} for i in sa_tables.columns], data=sa_tables.to_dict('records'), page_action="native", page_size=5, style_cell={'textAlign': 'center'})

    df_all_data = {
        'main_df': main_df.to_json(date_format='iso', orient='split'),
        'main_byid_df': main_byid_df.to_json(date_format='iso', orient='split'),
        'samples_df': samples_df.to_json(date_format='iso', orient='split'),
        'analyses_df': analyses_df.to_json(date_format='iso', orient='split'),
        'Data_Type': json.dumps(Data_Type),
        'sample_amounts_table': sa_tables.to_json(date_format='iso', orient='split')

     }

    return dcc.Tabs(id="tab", value="tab1",children=tabs), json.dumps(df_all_data), [html.H5('Data Upload Summary'), html.Br(), summary_table], [html.H5('Select Samples to Plot'), html.Br(), sample_selector], dimensions

# @app.callback(Output('test_output', 'children'),
#               Input('computed-data', 'data'))
# def update_graph(stored_data):
#     if stored_data is not None and len(stored_data) > 2:
#         #
#         loaded_data=json.loads(stored_data)
#         samples_df = pd.read_json(loaded_data.get('samples_df'), orient='split')
#         Data_Type = json.loads(loaded_data.get('Data_Type'))
#         analyses_df = pd.read_json(loaded_data.get('analyses_df'), orient='split')
#         #
#         sample_amounts_table = MDAFunc.check_data_loading(analyses_df, Data_Type)
#         loaded_data['sample_amounts_table'] = sample_amounts_table.to_json(date_format='iso', orient='split')
#     #
#     return html.Div(), json.dumps(loaded_data)


@app.callback(Output('main-panel', 'children'),
              Output('computed-data', 'data'),
              Output('summary-data', 'children'),
              Output('sample-selector', 'children'),
              Output('plotting-dimensions', 'children'),
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
    
    if btn == 'data-load':
        if selection == 'Ages':
            template_path = "data/Data_Upload_Example_Data_Type_Ages.xlsx"
        elif selection == '238U/206Pb_&_207Pb/206Pb':
            template_path = "data/Data_Upload_Example_Data_Type_Ratios.xlsx"

        # df = pd.read_excel(template_filename,  sheet_name="Data")
        
        # table.data =df.to_dict('records')
        # table.columns = [{"name": i, "id": i} for i in df.columns]
        return MDATabLoader(template_path, selection)

        table.data =df.to_dict('records')
        table.columns = [{"name": i, "id": i} for i in df.columns]

    elif btn =='data-upload':
        if contents is not None:
            template_path = parse_contents(contents, filename)
            # table.data = df.to_dict('records')
            # table.columns = [{"name": i, "id": i} for i in df.columns]
            return MDATabLoader(template_path, selection)
    else:     
        return html.Div([
            html.Img(src=app.get_asset_url('img/empty.png'), className="col-sm-1 align-self-center", style={'width': "100%", 'height': "auto"}),
            html.H4("No Data Yet"),
            html.P("Complete the fields and load your data into"),
            html.P("the input form on the left to begin.")
        ], style={'text-align': 'center'}), json.dumps({}), [html.H5('Age Plotting Dimensions'), html.Br(), html.P('Load or import data to start.', style={'text-align': 'center'})], [html.H5('Select Samples to Plot'), html.Br(), html.P('Load or import data to start.', style={'text-align': 'center'})], [html.H5('Age Plotting Dimensions'), html.P('Load or import data to start.', style={'text-align': 'center'})]
        # table = dash_table.DataTable(
        #     id='datatable-upload-container',
        #     columns=([{'id': p, 'name': p} for p in params]),
        #     data=[
        #         dict(Model=i, **{param: 0 for param in params})
        #         for i in range(1, 21)
        #     ],
        #     editable=True,
        #     page_action="native",
        #     page_size= 20
        # )   


@app.callback(
    Output('dataset-dropdown', 'value'), 
    Output('radio-uncertainty', 'value'), 
    Output('radio-sigma', 'value'),
    Input("data-reset", "n_clicks"))
def clear_selection(value):
    return "", "", ""

@app.callback(
    Output("download-template", "data"),
    State('dataset-dropdown', 'value'),
    Input("btn-download-template", "n_clicks"),
    prevent_initial_call=True,
)
def func(selection, download):
    
    if selection == 'Ages':
        template_filename = "data/Data_Upload_Example_Data_Type_Ages.xlsx"
    elif selection == '238U/206Pb_&_207Pb/206Pb':
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