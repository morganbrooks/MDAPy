# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import glob
import dash
import json
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme
from dash.dependencies import Input, Output, State
from MDAPy import MDAPy_Functions as MDAFunc
import plotly.express as px
import pandas as pd
import base64
import os
import numpy as np
import io


plotwidth = 8
plotheight = 5
pd.options.display.float_format = "{:,.2f}".format

carousel = dbc.Carousel(
    items=[{"key": "1", "src": "assets/img/plot_placeholder.svg"}])


def sampleSelector(df):
    checklist_options = [{'label': 'Sample ' + i, 'value': i} for i in df]
    # checklist_options.append({'label': 'All Samples', 'value': json.dumps([i for i in df])})
    selector = dcc.Checklist(id='sample_selection', options=checklist_options, value=[df[0]],
                             labelStyle={'display': 'inline-block', 'margin-bottom': '0.5rem', 'font-size': '1.15rem'}, labelClassName='col-sm-6')
    return selector


dimensions = [html.H5('Age Plotting Dimensions'), html.Br(),
              html.P('For individual MDA plots with all ages plotted, this input controls the maximum age to be plotted to control how many measurements are shown on one plot. Input (Ma) will be added to the oldest age in the age clusters to give a max plotting age.'),
              html.Div(children=[dcc.Input(id='age-plot-dimensions', value=4, type='number', className='col-sm-6',  min=1)], style={'width': '100%'}, className="row justify-content-end")]

summary = html.Div(id='summary-header', children=[
    html.Div(id='summary-data', className="col-sm-3 summary-cards",
             style={'height': '100%'}),
    html.Div(id='sample-selector', className="col-sm-3 summary-cards",
             style={'height': '100%'}),
    html.Div(id='plotting-dimensions',
             className="col-sm-3 summary-cards", style={'height': '100%'}),
], className="row input-row justify-content-between", style={'height': '275px'})


methods = html.Div(id='summary-methods', children=[
    dbc.Button(id='mda_all_methods_and_plots', children=["Calculate All MDA Methods And Plot  ", html.I(
        className='fas fa-exclamation-circle')], color="outline-primary", className="col-sm-3 button-method"),
    dbc.Button(id='mda_individual_method_and_plot', children=["Calculate Individual MDAs And Plot  ", html.I(
        className='fas fa-exclamation-circle')], color="outline-primary", className="col-sm-3 button-method"),
    dbc.Button(id='mda_one_method_all_plots', children=["Plot All Samples With One MDA Method  ", html.I(
        className='fas fa-exclamation-circle')], color="outline-primary", className="col-sm-3 button-method")
], className="row input-row justify-content-between")
#
accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem([dcc.Loading(
                id="loading-main-panel",
                type="default",
                children=html.Div(id='main-panel'),
            )],
                title="Inspect Dataset"),
            dbc.AccordionItem(
                [
                    summary,
                    html.Br(),
                    methods,
                    html.Br(),
                    html.Div(children=[
                        html.H4('MDA Method Summary Table', className="col-sm-6"), dbc.Button([html.I(
                            className='fas fa-download'), " Export"], color="outline-primary", className="col-sm-1", disabled=True)
                    ], className="row justify-content-between"),
                    html.P('All errors are quoted in absolute'),
                    html.Hr(),
                    html.Br(),
                    html.Br(),
                    dcc.Loading(
                        id="loading-summary-mda-table",
                        type="default",
                        children=html.Div(id='summary-mda-table'),
                    ),
                    html.Br(),
                    html.Div(children=[
                        html.H4('MDA Method Comparison Plots', className="col-sm-6"), dbc.Button([html.I(
                            className='fas fa-download'), " Export"], color="outline-primary", className="col-sm-1", disabled=True)
                    ], className="row input-row justify-content-between"),
                    html.Hr(),
                    dcc.Loading(
                        id="loading-carousel",
                        type="default",
                        children=html.Div(id="plot-carousel"),
                    ),
                    html.Hr()
                ],
                title="Run Analysis",
            ),
        ],
    ), className='col-sm-9 workbench'
)

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)
app.title = "MDAPy Dashboard"
app.layout = dbc.Container(fluid=True, children=[

    dbc.CardHeader(children=[
        html.A([html.Img(src=app.get_asset_url('img/logo.png'), className="col-sm-1 align-self-center",
               style={'width': "auto", 'height': "50px"})], href='/', style={'width': 'auto'}),
        # <i class="fab fa-bootstrap"></i>
        html.Div(className="col-sm-9 align-self-center"),
        html.Div([dbc.Row([
            dbc.Button([html.I(className='fa fa-undo'), " Reset Form"],
                       color="outline-primary", id="data-reset", className="col-sm-5"),
            html.Div(className="col-sm-1"),
            dbc.Button([html.I(className='far fa-question-circle'), " Help"],
                       color="outline-primary", id="data-help", className="col-sm-5")
        ])], className="col-sm-2 align-self-center")],
        className='row dashHeader justify-content-between'),

    html.Div(children=[
        html.Div(children=[
            html.B('Input Data'), html.Br(), html.Br(),
            html.Label('Select Dataset'),
            dcc.Dropdown(options=[{'label': u'Pb-U 206/238 & Pb-U 207/235', 'value': '238U/206Pb_&_207Pb/206Pb'},
                                  {'label': u'Best Age & SX', 'value': 'Ages'}], value='Ages', id='dataset-dropdown'),
            html.Br(),
            html.Label('Select Sigma (sx)'),
            dcc.RadioItems(options=[{'label': '1 sx', 'value': '1'}, {'label': '2 sx', 'value': '2'}],
                           id='radio_sigma', value='2', labelClassName='col-sm-6'),
            html.Br(),
            html.Label('Select Uncertainty Format'),
            dcc.RadioItems(options=[{'label': 'Percent (%)', 'value': 'percent'},
                                    {'label': 'Absolute (ABS)', 'value': 'absolute'}],
                           value='percent', id='radio_uncertainty',
                           labelClassName='col-sm-6'),
            html.Br(),
            html.Div(children=[html.Label('Best Age Cut Off', className='labelCte col-sm-7'), dcc.Input(
                id='best_age_cut_off', value=1500, type='number', className='inputNumbers col-sm-2')], className="row input-row"),
            html.Div(children=[html.Label('U238 Decay Constant (10⁻¹⁰)', className='labelCte col-sm-7'), dcc.Input(
                id='U238_decay_constant', value=1.55125, type='number', className='inputNumbers col-sm-2')], className="row input-row"),
            html.Div(children=[html.Label('U235 Decay Constant (10⁻¹⁰)', className='labelCte col-sm-7'), dcc.Input(
                id='U235_decay_constant', value=9.8485, type='number', className='inputNumbers col-sm-2')], className="row input-row"),
            html.Div(children=[html.Label('U238/U235 Decay Constant', className='labelCte col-sm-7'), dcc.Input(
                id='U238_U235', value=133.88, type='number', className='inputNumbers col-sm-2')], className="row input-row"),
            html.Br(),
            html.P(
                'Input 0 if systematic uncertainties not required in final uncertainty calculation'),
            html.Br(),
            html.Div(children=[
                html.Label('Long Term Excess Variance: U-Pb 238/206',
                           className='labelCte col-sm-9'),
                dcc.Input(id='excess_variance_206_238', value=1.2,
                          type='number', className='inputCte col-sm-2',  min=0)
            ], className="row input-row"),
            html.Div(children=[
                html.Label('Long Term Excess Variance: Pb-Pb 207/206',
                           className='labelCte col-sm-9'),
                dcc.Input(id='excess_variance_207_206', value=0.7,
                          type='number', className='inputCte col-sm-2',  min=0)
            ], className="row input-row"),

            html.Div(children=[
                html.Label('Sy Calibration Uncertainty U-Pb 238/206',
                           className='labelCte col-sm-9'),
                dcc.Input(id='Sy_calibration_uncertainty_206_238', value=0.6,
                          type='number', className='inputCte col-sm-2',  min=0)
            ], className="row input-row"),

            html.Div(children=[
                html.Label('Sy Calibration Uncertainty Pb-Pb 207/206',
                           className='labelCte col-sm-9'),
                dcc.Input(id='Sy_calibration_uncertainty_207_206', value=0.6,
                          type='number', className='inputCte col-sm-2',  min=0)
            ], className="row input-row"),

            html.Div(children=[
                html.Label('Decay Constant Uncertainty U 238',
                           className='labelCte col-sm-9'),
                dcc.Input(id='decay_constant_uncertainty_U238', value=0.16,
                          type='number', className='inputCte col-sm-2',  min=0)
            ], className="row input-row"),

            html.Div(children=[
                html.Label('Decay Constant Uncertainty U 235',
                           className='labelCte col-sm-9'),
                dcc.Input(id='decay_constant_uncertainty_U235', value=0.2,
                          type='number', className='inputCte col-sm-2',  min=0)
            ], className="row input-row"), html.Br(),

            dbc.Button("Load Sample Data", color="primary",
                       id="data-load", className="mb-3 col-sm-11"),
            dcc.Upload(dbc.Button("Import Data", color="primary", id="upload-button",
                       className="mb-3 col-sm-12"), id="data-upload", className="col-sm-11"),
            dbc.Button("Download Import Template", color="primary",
                       id="btn-download-template", className="mb-3 col-sm-11"),
            dcc.Download(id="download-template")

        ], className='col-sm-2 settings-menu'),
        accordion,
    ], className='row justify-content-between'),
    html.Br(),
    # dcc.Store stores the intermediate value
    dcc.Store(id='computed-data'),
    dcc.Store(id='computed-data-errors'),
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
        return 'data/temp_data.xlsx'


def MDATabLoader(template_path, selection):
    main_df, main_byid_df, samples_df, analyses_df, Data_Type = MDAFunc.loadDataExcel([
                                                                                      template_path], selection)
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
                                               columns=[{"name": i, "id": i, "type": "numeric", 'format': Format(scheme=Scheme.fixed, precision=8)}
                                                        for i in temp.columns],
                                               data=temp.to_dict('records'),
                                               editable=True, style_cell={'textAlign': 'center'},
                                               page_action="native",
                                               page_size=10)])
        )
    #
    sa_tables = MDAFunc.check_data_loading(analyses_df, Data_Type)
    sample_selector = sampleSelector(sa_tables['Sample_ID'])
    summary_table = dash_table.DataTable(id='datatable-summary', columns=[{"name": i, "id": i} for i in sa_tables.columns], data=sa_tables.to_dict(
        'records'), page_action="native", page_size=5, style_cell={'textAlign': 'center'})

    df_all_data = {
        'main_df': main_df.to_json(date_format='iso', orient='split'),
        'main_byid_df': main_byid_df.to_json(date_format='iso', orient='split'),
        'samples_df': samples_df.to_json(date_format='iso', orient='split'),
        'analyses_df': analyses_df.to_json(date_format='iso', orient='split'),
        'Data_Type': json.dumps(Data_Type),
        'sample_amounts_table': sa_tables.to_json(date_format='iso', orient='split')
    }

    return dcc.Tabs(id="tab", value="tab1", children=tabs), json.dumps(df_all_data), [html.H5('Data Upload Summary'), html.Br(), summary_table], [html.H5('Select Samples to Plot'), html.Br(), sample_selector], dimensions


@app.callback(Output('data-load', 'disabled'),
              Output('upload-button', 'disabled'),
              Output('data-upload', 'disabled'),
              Output("mda_all_methods_and_plots", "disabled"),
              Output("mda_individual_method_and_plot", "disabled"),
              Output("mda_one_method_all_plots", "disabled"),
              Output("btn-download-template", "disabled"),
              Output("data-reset", "disabled"),
              Input('dataset-dropdown', 'value'),
              Input('computed-data', 'data'))
def buttons(selection, summary):

    if (selection == '') or (selection is None):
        B1, B2, B3, B7, B8 = True, True, True, True, True
    else:
        B1, B2, B3, B7, B8 = False, False, False, False, False
    if len(summary) <= 2:
        B4, B5, B6 = True, True, True
    else:
        B4, B5, B6 = False, True, True

    return B1, B2, B3, B4, B5, B6, B7, B8


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
        page_size=20
    )

    btn = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if btn == 'data-load':
        if selection == 'Ages':
            template_path = "data/Data_Upload_Example_Data_Type_Ages.xlsx"
        elif selection == '238U/206Pb_&_207Pb/206Pb':
            template_path = "data/Data_Upload_Example_Data_Type_Ratios.xlsx"

        #
        return MDATabLoader(template_path, selection)

        table.data = df.to_dict('records')
        table.columns = [{"name": i, "id": i} for i in df.columns]

    elif btn == 'data-upload':
        if contents is not None:
            template_path = parse_contents(contents, filename)
            #
            return MDATabLoader(template_path, selection)
    else:
        return html.Div([
            html.Img(src=app.get_asset_url('img/empty.svg'),
                     className="col-sm-1 align-self-center", style={'width': "60%", 'height': "auto"}),
        ], style={'text-align': 'center'}), json.dumps({}), [html.H5('Age Plotting Dimensions'), html.Br(), html.P('Load or import data to start.', style={'text-align': 'center'})], [html.H5('Select Samples to Plot'), html.Br(), html.P('Load or import data to start.', style={'text-align': 'center'}), html.Div(id='sample_selection')], [html.H5('Age Plotting Dimensions'), html.P('Load or import data to start.', style={'text-align': 'center'})]


@app.callback(Output('computed-data-errors', 'data'),
              Output('summary-mda-table', 'children'),
              Output('plot-carousel', 'children'),
              Input('computed-data', 'data'),
              Input('sample_selection', 'value'),
              Input('radio_sigma', 'value'),
              Input('radio_uncertainty', 'value'),
              Input('best_age_cut_off', 'value'),
              Input('U238_decay_constant', 'value'),
              Input('U235_decay_constant', 'value'),
              Input('U238_U235', 'value'),
              Input('excess_variance_206_238', 'value'),
              Input('excess_variance_207_206', 'value'),
              Input('Sy_calibration_uncertainty_206_238', 'value'),
              Input('Sy_calibration_uncertainty_207_206', 'value'),
              Input('decay_constant_uncertainty_U238', 'value'),
              Input('decay_constant_uncertainty_U235', 'value'),
              Input("mda_all_methods_and_plots", "n_clicks"),
              Input("mda_individual_method_and_plot", "n_clicks"),
              Input("mda_one_method_all_plots", "n_clicks"),
              prevent_initial_call=True)
def pre_calculation(computed_data, sample_list, sigma, uncertainty, best_age_cut_off, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, button_method_1, button_method_2, button_method_3):

    df_errors = None
    summary_mda_table = html.Div()
    triggered = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    buttons = ['mda_all_methods_and_plots',
               'mda_individual_method_and_plot', 'mda_one_method_all_plots']

    if triggered in buttons:
        if sample_list is not None:
            loaded_data = json.loads(computed_data)
            main_byid_df = pd.read_json(loaded_data.get(
                'main_byid_df'), orient='split').applymap(np.array)
            Data_Type = json.loads(loaded_data.get('Data_Type'))

            U238_decay_constant = U238_decay_constant*(10**-10)
            U235_decay_constant = U235_decay_constant*(10**-10)

            ages, errors, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, numGrains, labels, sample_list, best_age_cut_off, dataToLoad_MLA, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235 = MDAFunc.sampleToData(
                sample_list, main_byid_df, sigma, Data_Type, uncertainty, best_age_cut_off, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235)

        if triggered == 'mda_all_methods_and_plots':
            folder_path = '/assets/plots/All_MDA_Methods_Plots/'
            U238_decay_constant, U235_decay_constant, U238_U235, YSG_MDA, YC1s_MDA, YC1s_cluster_arrays, YC2s_MDA, YC2s_cluster_arrays, YDZ_MDA, minAges, mode, Y3Zo_MDA, Y3Zo_cluster_arrays, Y3Za_MDA, Y3Za_cluster_arrays, Tau_MDA, Tau_Grains, PDP_age, PDP, plot_max, ages_errors1s_filtered, tauMethod_WM, tauMethod_WM_err2s, YSP_MDA, YSP_cluster, YPP_MDA, MLA_MDA = MDAFunc.MDA_Calculator(
                ages, errors, sample_list, dataToLoad_MLA, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off)

            MDAs_1s_table, excel_MDA_data, all_MDA_data = MDAFunc.output_tables(
                sample_list, YSG_MDA, YC1s_MDA, YC2s_MDA, YDZ_MDA, Y3Zo_MDA, Y3Za_MDA, Tau_MDA, YSP_MDA, YPP_MDA, MLA_MDA)

            df_errors = {
                'ages': ages,
                'errors': errors,
                'eight_six_ratios': eight_six_ratios,
                'eight_six_error': eight_six_error,
                'seven_six_ratios': seven_six_ratios,
                'seven_six_error': seven_six_error,
                'numGrains': json.dumps(numGrains),
                'labels': json.dumps(labels),
                'sample_list': json.dumps(sample_list),
                'best_age_cut_off': json.dumps(best_age_cut_off),
                'dataToLoad_MLA': json.dumps(dataToLoad_MLA),
                'MDAs_1s_table': MDAs_1s_table.to_json(date_format='iso', orient='split'),
                # 'excel_MDA_data': excel_MDA_data.to_json(date_format='iso', orient='split'),
                'all_MDA_data': all_MDA_data.to_json(date_format='iso', orient='split'),
                'U238_decay_constant': json.dumps(U238_decay_constant),
                'U235_decay_constant': json.dumps(U235_decay_constant),
                'U238_U235': json.dumps(U238_U235),
                'excess_variance_206_238': json.dumps(excess_variance_206_238),
                'excess_variance_207_206': json.dumps(excess_variance_207_206),
                'Sy_calibration_uncertainty_206_238': json.dumps(Sy_calibration_uncertainty_206_238),
                'Sy_calibration_uncertainty_207_206': json.dumps(Sy_calibration_uncertainty_207_206),
                'decay_constant_uncertainty_U238': json.dumps(decay_constant_uncertainty_U238),
                'decay_constant_uncertainty_U235': json.dumps(decay_constant_uncertainty_U235)
            }

            mda_table = dash_table.DataTable(id='datatable-mda', columns=[{"name": i, "id": i, "type": "numeric",
                                                                           'format': Format(scheme=Scheme.fixed, precision=2)} for i in MDAs_1s_table.columns],
                                             data=MDAs_1s_table.to_dict('records'), page_action="native", page_size=5, style_cell={'textAlign': 'center'},
                                             style_table={'overflowX': 'auto'})  # , export_format="csv"

            # eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff34
            Image_File_Option = 'web'
            import glob
            import os

            files = glob.glob("assets/plots/All_MDA_Methods_Plots/*")
            for f in files:
                os.remove(f)

            MDAfig, MDA_plot_final = MDAFunc.Plot_MDA(MDAs_1s_table, all_MDA_data, sample_list, YSG_MDA, YC1s_MDA, YC2s_MDA,
                                                      YDZ_MDA, Y3Zo_MDA, Y3Za_MDA, Tau_MDA, YSP_MDA, YPP_MDA, MLA_MDA, Image_File_Option, plotwidth, plotheight)
            files = [file for file in os.listdir(
                os.getcwd() + folder_path) if file.endswith(".svg")]

            carousel2 = dbc.Carousel(items=[{"key": str(pos+1), "src": folder_path+img} for pos, img in enumerate(files)],
                                     controls=True, indicators=True, variant="dark")

            return df_errors, mda_table, carousel2
        elif triggered == 'mda_individual_method_and_plot':
            pass
        elif triggered == 'mda_one_method_all_plots':
            pass

    return df_errors, summary_mda_table, carousel


@app.callback(
    Output('dataset-dropdown', 'value'),
    Output('radio_uncertainty', 'value'),
    Output('radio_sigma', 'value'),
    Input("data-reset", "n_clicks"))
def clear_selection(clicks):
    if clicks is not None:
        return "", "", ""
    else:
        return "", "percent", "2"


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


server = app.server


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)
