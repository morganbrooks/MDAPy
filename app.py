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
              html.Div(children=[dcc.Input(id='age-plot-dimensions', value=30, type='number', className='col-sm-6',  min=5)], style={'width': '100%'}, className="row justify-content-end")]

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
            html.Label('Select Method'),
            dcc.Dropdown(options=[
                {'label': u'YSG: Youngest Single Grain', 'value': 'YSG'},
                {'label': u'YDZ: Youngest Detrital Zircon', 'value': 'YDZ'},
                {'label': u'YPP: Youngest Graphical Peak', 'value': 'YPP'},
                {'label': u'YC1σ (2+): Youngest Grain Cluster at 1σ', 'value': 'YC1Sigma'},
                {'label': u'YC2σ (3+): Youngest Grain Cluster at 2σ', 'value': 'YC2Sigma'},
                {'label': u'Y3Zo: Youngest Three Zircons at 2σ (Y3Zo)', 'value': 'Y3Zo'},
                {'label': u'Y3Za: Youngest Three Zircons (Y3Za)', 'value': 'Y3Za'},
                {'label': u'The Tau Method', 'value': 'TAU'},
                {'label': u'YSP: The Youngest Statistical Population', 'value': 'YSP'},
                {'label': u'The MLA Method', 'value': 'MLA'}], value='MLA', 
                id='method-dropdown'),
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
        ], style={'text-align': 'center'}), json.dumps({}), [html.H5('Data Upload Summary'), html.Br(), html.P('Load or import data to start.', style={'text-align': 'center'})], [html.H5('Select Samples to Plot'), html.Br(), html.P('Load or import data to start.', style={'text-align': 'center'}), html.Div(id='sample_selection')], [html.H5('Age Plotting Dimensions'), html.P('Load or import data to start.', style={'text-align': 'center'}), dcc.Input(id='age-plot-dimensions', value=0, type='number', className='col-sm-6',  min=0,style={'display': 'none'})]


@app.callback(Output('computed-data-errors', 'data'),
              Output('summary-mda-table', 'children'),
              Output('plot-carousel', 'children'),
              Input('computed-data', 'data'),
              Input('method-dropdown', 'value'),
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
              Input('age-plot-dimensions', 'value'),
              Input("mda_all_methods_and_plots", "n_clicks"),
              Input("mda_individual_method_and_plot", "n_clicks"),
              Input("mda_one_method_all_plots", "n_clicks"),
              prevent_initial_call=True)
def pre_calculation(computed_data, method, sample_list, sigma, uncertainty, best_age_cut_off, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, age_addition_set_max_plot, button_method_1, button_method_2, button_method_3):
    
    df_errors = None
    summary_mda_table = html.Div()
    Image_File_Option = 'web'
    plotwidth = 10
    plotheight = 7
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
            if method == 'YSG':
                age_addition_set_max_plot = 30
                text = """The youngest single grain (YSG) as described in in Dickinson and Gehrels (2009), uses the youngest single detrital zircon grain age and uncertainty measured within the sample as the MDA. If the YSG has a 1σ uncertainty >10 Ma and overlaps with the second-youngest date, then the later should be substituted for greater precision. The uncertainty of the youngest grain is used as the uncertainty of the MDA (Dickinson and Gehrels, 2009). Following Sharman et al. (2018), MDAPy takes an array of grain ages and the associated uncertainties, adds 1σ uncertainty to each age measurement, sorts them in ascending order and selects the first grain on the list as the youngest single grain and MDA. This method is contrary to Dickinson and Gehrels (2009), which does not add 1σ to the grain age before sorting and selecting the youngest grain. When done this way, older, less uncertain grains may be selected over younger more uncertain ones, as the older grain with a smaller added uncertainty could end up being younger once the 1σ uncertainties are added. The YSG algorithm outputs a table of calculated YSG MDAs and the corresponding 1σ uncertainty for each sample as well as plots illustrating the grain age measurements with 1σ and 2σ uncertainty bars, sorted from youngest grain age, with the YSG/MDA highlighted in red. The plots give a visual of the distribution of grain age measurements present in the sample, as well as where the YSG fits within this distribution. This visual can assist users in discerning the validity and precision of the YSG method."""
                YSG_MDA, YSG_Table_ = MDAFunc.YSG_outputs(ages, errors, plotwidth, plotheight, sample_list, YSG_MDA, age_addition_set_max_plot, Image_File_Option); YSG_Table_
            elif method == 'YDZ':
                text = """The youngest detrital zircon (YDZ)(Dickinson and Gehrels, 2009) is based on an algorithm originally developed in Isoplot (a Visual Basic add-in for Microsoft Excel) (Ludwig, 2012). In MDAPy, the YDZ algorithm is written in Python but follows the same methods of Ludwig (2012), where a Monte Carlo simulation is applied on the youngest sub-sample of ages. The simulation is applied as follows: Starts with an array of ages and associated uncertainties for each sample Ages are sorted in ascending order, and a sub-sample is selected which consists of all grains within 5σ of the youngest grain. This is considered the youngest sub-sample of ages. The simulation runs and each iteration consists of taking the sub-sample of the youngest ages and adjusting them by a random amount of their corresponding uncertainties. From this new random array of ages, the youngest grain is selected. The simulation is repeated 10,000 times and the result is 10,000 of the youngest ages from each simulation. The 10,000 youngest ages are then plotted on a histogram and the mode is selected as the best estimate of the youngest detrital zircon and the MDA of the sample. The upper uncertainty (P97.5) and lower uncertainty (P2.5), which are the ages where only 2.5% of dates are older or younger, define the 2σ uncertainties at 95% confidence. In general, the distribution is asymmetric which results in unequal upper and lower uncertainties. The resulting plots in MDAPy display frequency histograms of the distribution of the 10,000 youngest ages derived from the Monte Carlo simulation for each sample. The mode (YDZ/MDA) is highlighted in red and the upper and lower uncertainties are highlighted in black dashed lines. Due to the nature of this calculation method: systematic uncertainties are NOT added to the final MDA uncertainties."""
                YDZ_MDAs, YDZ_Table_ = MDAFunc.YDZ_outputs(YDZ_MDA, minAges, mode, ages, errors, sample_list, plotwidth, plotheight, Image_File_Option); YDZ_Table_
            elif method == 'YPP':
                text = """The youngest graphical peak (YPP) method from Dickinson and Gehrels (2009), is derived from the youngest peak (mode) on an age probability density plot (PDP) which consists of two or more grains that overlap within 2σ uncertainty. There is no uncertainty for MDAs calculated using this method. The outputs for the YPP algorithm consist of a table of the calculated YPP MDA values as well as the PDPs for each sample. The MDA values are highlighted, with a red line intersecting the youngest graphical peak (mode) with 2 or more grains that overlap within 2σ uncertainty. The x-axis is set from 0 to MDA + 200 Ma to highlight the youngest peaks within the PDP distribution."""
                YPP_MDAs, YPP_Table_ = MDAFunc.YPP_outputs(ages, errors, sample_list, plotwidth, plotheight, Image_File_Option, sigma=1, min_cluster_size=2, thres=0.01, minDist=1, xdif=0.1); YPP_Table_
            elif method == 'YC1Sigma':
                text = """The youngest grain cluster at 1σ uncertainty (YC1σ), is calculated using the weighted mean age, weighted by the square of the age uncertainty (Dickinson and Gehrels, 2009). The grain cluster used within the weighted mean age calculation consists of the youngest two or more grains that overlap within 1σ uncertainty. The uncertainty of the YC1σ MDA is calculated as the standard error of the calculated weighted mean age. The YC1σ algorithm outputs a summary table and plots of the age measurements. The table lists by sample, the MDA value, 1σ uncertainty, MSWD, and number of grains within the youngest grain cluster that were included in the weighted mean age calculation. The plots display grain ages and the corresponding 1σ and 2σ uncertainty upper and lower limit bars. The ages are sorted in ascending order and include up to 10 Ma above the oldest age within the youngest grain cluster. This restriction allows enough grains to show the grain cluster without showing all the measurements. The red bars illustrate the grains within the youngest grain cluster. The MDA is shown on the plots as a dashed line."""
                YC1s_MDA, YC1s_Table_ = MDAFunc.YC1s_outputs(ages, errors, sample_list, YC1s_MDA, YC1s_cluster_arrays, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option, min_cluster_size=2); YC1s_Table_
            elif method == 'YC2Sigma':
                text = """The youngest grain cluster at 2σ uncertainty (YC2σ), is calculated using the weighted mean age, weighted by the square of the age uncertainty (Dickinson and Gehrels, 2009). The grain cluster used within the weighted mean age calculation consists of the youngest three or more grains that overlap within 2σ uncertainty. The uncertainty of the YC2σ MDA is calculated as the standard error of the calculated weighted mean age. The YC2σ algorithm outputs a summary table and plots of the age measurements. The table lists by sample, the MDA value, 1σ uncertainty, MSWD, and number of grains within the youngest grain cluster that were included in the weighted mean age calculation. The plots display grain ages and the corresponding 1σ and 2σ uncertainty upper and lower limit bars. The ages are sorted ascendingly and include up to 10 Ma above the oldest age within the youngest grain cluster. The red bars illustrate the grains within the youngest grain cluster. The MDA is shown on the plots as a dashed line."""
                age_addition_set_max_plot = 5
                YC2s, YC2s_Table_ = MDAFunc.YC2s_outputs(ages, errors, sample_list, YC2s_MDA, YC2s_cluster_arrays, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option, min_cluster_size=3); YC2s_Table_
            elif method == 'Y3Zo':
                text = """The youngest three zircons at 2σ uncertainty (Y3Zo) method calculates an MDA using the weighted mean age of the youngest three zircons that overlap within 2σ uncertainty, weighted by the square of the age uncertainty (Ross et al., 2017). The grain cluster used within the weighted mean age calculation is determined using the youngest grain cluster algorithm, with only the youngest three zircons selected from the cluster. The uncertainty of the Y3Zo MDA is calculated as the standard error of the calculated weighted mean age. The Y3Zo algorithm outputs a summary table, and plots of the age measurements. The table lists by sample, the MDA value, 1σ uncertainty, and the MSWD. The plots display grain ages and the corresponding 1σ and 2σ uncertainty upper and lower limit bars. The ages are sorted ascendingly and include up to 10 Ma above the oldest age within the youngest three grains that overlap at 2σ uncertainty. The red bars illustrate the youngest three grains within the cluster. The MDA is shown on the plots as a dashed line."""
                age_addition_set_max_plot = 15
                Y3Zo_MDA, Y3Zo_Table_ = MDAFunc.Y3Zo_outputs(ages, errors, sample_list, Y3Zo_MDA, Y3Zo_cluster_arrays, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option, min_cluster_size=3); Y3Zo_Table_
            elif method == 'Y3Za':
                text = """The youngest three zircons (Y3Za) method calculates an MDA using the weighted mean age of the youngest three zircons, weighted by the square of the age uncertainty (Zhang et al., 2016). To select the three youngest zircons, dates are sorted ascendingly by age and the first three are chosen. The uncertainty of the Y3Za MDA is calculated as the standard error of the calculated weighted mean age. The Y3Za algorithm outputs a summary table, and plots of the age measurements. The table lists by sample, the MDA value, 1σ uncertainty, and the MSWD. The plots display grain ages and the corresponding 1σ and 2σ uncertainty upper and lower limit bars. The ages are sorted ascendingly and include up to 10 Ma above the oldest of the youngest three grains. The red bars illustrate the youngest three grains. The MDA is shown on the plots as a dashed line."""
                age_addition_set_max_plot = 10
                Y3Za_MDA, Y3Za_Table_ = MDAFunc.Y3Za_outputs(ages, errors, Y3Za_MDA, Y3Za_cluster_arrays, sample_list, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option); Y3Za_Table_
            elif method == 'TAU':
                text = """The  𝜏  method calculates an MDA using the weighted mean age, weighted by the square of the age uncertainty, of all dates that fall between the probability minima (troughs) of the youngest peak composed of a three or more grains on a PDP (Barbeau et al., 2009). The uncertainty of the  𝜏  MDA is calculated as the standard error of the calculated weighted mean age. The  𝜏  algorithm outputs a summary table as well as a PDP for each sample. The table lists by sample, the MDA value, 1σ uncertainty, MSWD, and the number of grains that fall between the probability minima of the youngest peaks and were therefore used in the weighted mean age calculation. The PDPs highlight the MDA value with an intersecting dotted line as well as the grains that fall between the probability minima of the youngest peak (in red). The x-axis is set from 0 to the MDA value + 200 Ma to highlight the youngest peak within the PDP distribution."""
                Tau_MDA, Tau_Table_ = MDAFunc.Tau_outputs(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off, plotwidth, plotheight, Image_File_Option, min_cluster_size=3, thres=0.01, minDist=1, xdif=1, x1=0, x2=4000)
            elif method == 'YSP':
                text = """The youngest statistical population (YSP) method from Coutts et al 2019, calculates an MDA from the weighted mean age, weighted by the square of the age uncertainty, of the youngest two or more grains that produce a MSWD of ~ 1. A MSWD ~1 signals that the dispersion of the age measurements is proportional to the uncertainty of the measurements, and it is reasonable to assume that the grains may be the same true age (Wendt and Carl, 1991). In MDAPy, the sub-sample of grains used in the MDA calculation is selected through a stepwise process. To begin, grains are sorted by age and the MSWD of the two youngest grains is calculated. If the MSWD < 1, more grains are added until the MSWD > 1. The MDA is then calculated from the weighted mean age of this sub-sample of grains. The uncertainty of the MDA is calculated as the standard error of the calculated weighted mean age. The YSP algorithm outputs a summary table, and plots of the age measurements. The table lists by sample, the MDA value, 1σ uncertainty, MSWD, and the number of grains found within the sub-sample of grains used to calculate the MDA. The plots display grain ages and the corresponding 1σ and 2σ uncertainty upper and lower limit bars. The ages are sorted ascendingly and include up to 10 Ma above the oldest of the sub-sample of grains, which are highlighted in red. The MDA is shown on the plots as a dashed line."""
                age_addition_set_max_plot = 20
                YSP_MDA, YSP_Table_ = MDAFunc.YSP_outputs(ages, errors, sample_list, YSP_MDA, YSP_cluster, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option, min_cluster_size=2, MSWD_threshold=1); YSP_Table_
            elif method == 'MLA':
                text = """This method developed and tested in Vermeesch (2020), uses a maximum likelihood model that was originally developed for fission track thermochronology by Galbraith and Laslett(1993). The approach parameterises the MDA estimation problem with a binary mixture of discrete and continuous distributions. The ‘Maximum Likelihood Age’ (MLA) algorithm converges to a unique MDA value and is a purely statistical approach to MDA estimation. The results of the MLA method are best visualised on radial plots. The radial plot (Galbraith, 1988, 1990) is a graphical device that was specifically designed to display heteroscedastic data, and is constructed as follows. Consider a set of dates {t1, ..., ti, ..., tn} and uncertainties {s[t1], ..., s[ti], ..., s[tn]}. Define zi = z[ti] to be a transformation of ti (e.g., zi = log[ti]), and let s[zi] be its propagated analytical uncertainty (i.e., s[zi] = s[ti]/ti in the case of a logarithmic transformation). Create a scatter plot of (xi, yi) values, where xi = 1/s[zi] and yi = (zi − z◦)/s[zi], where z◦ is some reference value such as the mean. The slope of a line connecting the origin of this scatter plot with any of the (xi, yi)s is proportional to zi and, hence, the date ti. These dates can be more easily visualised by drawing a radial scale at some convenient distance from the origin and annotating it with labelled ticks at the appropriate angles. While the angular position of each data point represents the date, its horizontal distance from the origin is proportional to the precision. Imprecise measurements plot on the left hand side of the radial plot, whereas precise age determinations are found further towards the right. Thus, radial plots allow the observer to assess both the magnitude and the precision of quantitative data in one glance. The radial plot is a graphical method for displaying and comparing observations that have different precision. Invented by Rex Galbraith in 1988 it is commonly used in geochronology but as also a wide range of applications in business analytics or medical research. The observations are standardised and plotted against precision, with the precision defined as the reciprocal of the standard error. The original observations are given by slopes of lines through the origin and can be read using a circular scale. Radial plots provide a visual representation that can help to assess whether the estimates agree with a common value. They can also be used to identify outliers or groups of estimates differing in a systematic way because of some underlying factor or mixture of populations. In experimental sciences it is common to have measurements with different precision. This can arise from natural variations or from the experimental procedure. Geochronological methods such as fission track, 40Ar/39Ar , U-Pb and Optically Stimulated Luminescence (OSL) dating produce age estimates and associated errors for each of several grains. The radial plot can be used to display and compare the age estimates and see how they agree or differ within standard statistical variation. Another application of radial plot is in meta-analysis. Radial plots can be used to compare treatments effects from different clinical studies where the precision of the studies varies. Due to the nature of this calculation method: systematic uncertainties are NOT added to the final MDA uncertainties."""
                MDAFunc.MLA_outputs(sample_list, dataToLoad_MLA); 
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
