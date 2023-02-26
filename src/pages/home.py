import dash
import glob
import dash
import json
from dash import dash_table, dcc, html
from dash.exceptions import PreventUpdate
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
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, path='/')


method_description = {
'YSG': """The youngest single grain (YSG) as described in in Dickinson and Gehrels (2009), uses the youngest single detrital zircon grain age and uncertainty measured within the sample as the MDA. If the YSG has a 1σ uncertainty >10 Ma and overlaps with the second-youngest date, then the later is substituted for greater precision. The uncertainty of the youngest grain is used as the uncertainty of the MDA (Dickinson and Gehrels, 2009). Following Sharman et al. (2018), MDAPy takes an array of grain ages and the associated uncertainties, adds 1σ uncertainty to each age measurement, sorts them in ascending order and selects the first grain on the list as the youngest single grain and MDA. When done this way, older, less uncertain grains may be selected over younger more uncertain ones, as the older grain with a smaller added uncertainty could end up being younger once the 1σ uncertainties are added. If values are provided for systematic uncertainties, they are added to the YSG MDA uncertainties.""",
'YDZ': """The youngest detrital zircon (YDZ) (Dickinson and Gehrels, 2009) is based on an algorithm originally developed in Isoplot (a Visual Basic add-in for Microsoft Excel) (Ludwig, 2012). In MDAPy, the YDZ algorithm is written in Python but follows the same methods of Ludwig (2012), where a Monte Carlo simulation is applied on the youngest sub-sample of ages. The simulation is applied as follows: Starts with an array of ages and associated uncertainties for each sample. Ages are then sorted, and a sub-sample of all grains within 5σ of the youngest grain. The simulation runs and each iteration consists of taking the sub-sample of the youngest ages and adjusting them by a random amount of their corresponding uncertainties. From this new random array of ages, the youngest grain is selected. The simulation is repeated 10,000 times and the result is 10,000 of the youngest ages from each simulation. The 10,000 youngest ages are then plotted on a histogram and the mode is selected as the best estimate of the youngest detrital zircon and the MDA of the sample. The upper uncertainty (P97.5) and lower uncertainty (P2.5), which are the ages where only 2.5% of dates are older or younger, define the 2σ uncertainties at 95% confidence. In general, the distribution is asymmetric which results in unequal upper and lower uncertainties. The resulting plots in MDAPy display frequency histograms of the distribution of the 10,000 youngest ages derived from the Monte Carlo simulation for each sample. Due to the nature of this calculation method: systematic uncertainties are not added to the final MDA uncertainties.""",
'YPP': """The youngest graphical peak (YPP) method from Dickinson and Gehrels (2009), is derived from the youngest graphical peak (mode) on an age probability density plot (PDP) which consists of two or more grains that overlap within 2σ uncertainty. There is no uncertainty for MDAs calculated using this method. """,
'YC1s': """The youngest grain cluster at 1σ uncertainty (YC1σ), is calculated using the weighted mean age, weighted by the square of the age uncertainty (Dickinson and Gehrels, 2009). The grain cluster used within the weighted mean age calculation consists of the youngest two or more grains that overlap within 1σ uncertainty. The uncertainty of the YC1σ MDA is calculated as the standard error of the calculated weighted mean age. If values are provided for systematic uncertainties, they are added to the YC1σ MDA uncertainties.""",
'YC2s': """The youngest grain cluster at 2σ uncertainty (YC2σ), is calculated using the weighted mean age, weighted by the square of the age uncertainty (Dickinson and Gehrels, 2009). The grain cluster used within the weighted mean age calculation consists of the youngest three or more grains that overlap within 2σ uncertainty. The uncertainty of the YC2σ MDA is calculated as the standard error of the calculated weighted mean age.""",
'Y3Zo': """The youngest three zircons at 2σ uncertainty (Y3Zo) method calculates an MDA using the weighted mean age of the youngest three zircons that overlap within 2σ uncertainty, weighted by the square of the age uncertainty (Ross et al., 2017). The uncertainty of the Y3Zo MDA is calculated as the standard error of the calculated weighted mean age.""",
'Y3Za': """The youngest three zircons (Y3Za) method calculates an MDA using the weighted mean age of the youngest three zircons, weighted by the square of the age uncertainty (Zhang et al., 2016). The uncertainty of the Y3Za MDA is calculated as the standard error of the calculated weighted mean age.""",
'Tau': """The Tau (𝜏) method calculates an MDA using the weighted mean age, weighted by the square of the age uncertainty, of all dates that fall between the probability minima (troughs) of the youngest peak composed of three or more grains on a probability density plot (Barbeau et al., 2009). The uncertainty of the  𝜏  MDA is calculated as the standard error of the calculated weighted mean age.""",
'YSP': """The youngest statistical population (YSP) method from Coutts et al 2019, calculates an MDA from the weighted mean age, weighted by the square of the age uncertainty, of the youngest two or more grains that produce a MSWD of ~ 1. A MSWD ~1 signals that the dispersion of the age measurements is proportional to the uncertainty of the measurements, and it is reasonable to assume that the grains may be the same true age (Wendt and Carl, 1991). In MDAPy, the sub-sample of grains used in the MDA calculation is selected through a stepwise process. To begin, grains are sorted by age and the MSWD of the two youngest grains is calculated. If the MSWD < 1, more grains are added until the MSWD > 1. The MDA is then calculated from the weighted mean age of this sub-sample of grains. The uncertainty of the MDA is calculated as the standard error of the calculated weighted mean age. """,
'MLA': """The maximum likelihood age (MLA) method developed in Vermeesch (2021), uses a maximum likelihood model that was originally developed for estimating minimum age populations in fission track thermochronology by Galbraith and Laslett (1993). The MDA calculated is the age of the minimum population, based on an error model for analytical uncertainties. The results of the MLA method are visualised on radial plots, which show ages (radial axis) versus error (x-axis) (Galbraith, 1988, 1990), with the angular position of each data point representing the date, and its horizontal distance from the origin representing the precision. Due to the nature of this calculation method: systematic uncertainties are not added to the final MDA uncertainties.  The algorithm used to calculate the MLA MDAs and the associated radial plots was developed by Vermeesch (2021) within an open source software package called IsoplotR (Vermeesch, 2018) ."""
}

method_title = {
    'YSG': 'Youngest Single Grain', 'YDZ': 'Youngest Detrital Zircon', 'YPP': 'YPP: Youngest Graphical Peak',
    'YC1s': 'YC1σ (2+): Youngest Grain Cluster at 1σ', 'YC2s': 'YC2σ (3+): Youngest Grain Cluster at 2σ',
    'Y3Zo': 'Y3Zo: Youngest Three Zircons at 2σ (Y3Zo)', 'Y3Za': 'Y3Za: Youngest Three Zircons (Y3Za)',
    'Tau': 'Tau: Tau Method', 'YSP': 'YSP: Youngest Statistical Population', 'MLA': 'MLA: Maximum Likelihood Age',
    }

plotwidth = 8
plotheight = 5
pd.options.display.float_format = "{:,.2f}".format

carousel = dbc.Carousel(id="CarouselPlot", 
    items=[{"key": "1", "src": "assets/img/plot_placeholder.svg"}])

def sampleSelector(df):
    checklist_options = [{'label': '' + i, 'value': i} for i in df]
    # checklist_options.append({'label': 'All Samples', 'value': json.dumps([i for i in df])})
    selector = dcc.Checklist(id='sample_selection', options=checklist_options, value=[df[0]],
                             labelStyle={'display': 'inline-block', 'margin-bottom': '0.5rem', 'font-size': '1.15rem'}, labelClassName='col-sm-6')
    return selector

dimensions = [html.H5('Age Plotting Dimensions'),
              html.Div(children=[html.P('For individual MDA plots with all ages plotted, this input controls the maximum age to be plotted to control how many measurements are shown on one plot. Input (Ma) will be added to the oldest age in the age clusters to give a max plotting age.'),
                                 dcc.Input(id='age-plot-dimensions', value=30, type='number', required=True, className='col-12',  min=5)], style={'width': '100%'}, className="row justify-content-end"),]

summary = html.Div(id='summary-header', children=[
    html.Div(id='summary-data', className="col-xs-12 col-sm-3 summary-cards",
             style={'height': '100%'}),
    html.Div(id='sample-selector', className="col-xs-12 col-sm-3 summary-cards",
             style={'height': '100%'}),
    html.Div(id='plotting-dimensions',
             className="col-xs-12 col-sm-3 summary-cards", style={'height': '100%'}),
], className="row input-row justify-content-between", style={'height': '275px'})

methods = html.Div(id='summary-methods', children=[
    dbc.Button(id='mda_all_methods_and_plots', children=["Calculate All MDA Methods And Plot  "], color="outline-primary", className="col-sm-3 button-method"),
    dbc.Button(id='mda_individual_method_and_plot', children=["Calculate One MDA Method And Plot  "], color="outline-primary", className="col-sm-3 button-method"),
    dbc.Button(id='mda_one_method_all_plots', children=["Plot All Samples With One MDA Method  "], color="outline-primary", className="col-sm-3 button-method")
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
                    dcc.Loading(
                        id="loading-summary-mda-text",
                        type="default",
                        children=[html.H4(id='summary-mda-title'), html.Div(id='summary-mda-text'), html.Br()],
                    ),
                    html.Hr(),
                    html.Div(children=[
                        html.H4('Calculated MDAs & Uncertainties', className="col-12 col-md-6"),
                        html.P('All uncertainties are quoted in absolute values'),
                        dcc.Dropdown(options=[
                            {'label': u'Export as CSV', 'value': 'csv'},
                            {'label': u'Export as XLSX', 'value': 'xlsx'},
                            ], placeholder="Select a format to export", value='csv', id='tabletype-dropdown'),
                    ], className="row justify-content-between"),
                    html.Hr(),
                    dcc.Loading(
                        id="loading-summary-mda-table",
                        type="default",
                        children=[html.Br(), html.Div(id='summary-mda-table')],
                    ),
                    html.Br(),
                    html.Div(children=[
                        html.H4('MDA Plots', className="col-sm-6"),
                        html.Div(children=[dcc.Dropdown(options=[
                            {'label': u'EPS', 'value': '.eps'},
                            {'label': u'JPEG', 'value': '.jpeg'},
                            {'label': u'PDF', 'value': '.pdf'},
                            {'label': u'PNG', 'value': '.png'},
                            {'label': u'SVG', 'value': '.svg'},
                            {'label': u'TIFF', 'value': '.tiff'}
                            ], placeholder="Select a plot format", value='.tiff', id='filetype-dropdown'),
                        dbc.Button([html.I(className='fas fa-download'), " Export"], color="outline-primary", id="btn-download-plot", disabled=True, className="col-sm-2"),
                        dcc.Download(id="download-plot")], className="col-sm-1", style= {'display': "contents"}),
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
    ), className='col-12 col-lg-9 workbench'
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
                label=f"{ idx_df }",
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
    select_all = dcc.Checklist(id="sample_all", options=[{"label": "Select all Samples", "value": "All"}], value=[], labelStyle={"display": "inline-block"},)
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

    return dcc.Tabs(id="tab", value="tab1", children=tabs), json.dumps(df_all_data), [html.H5('Data Upload Summary'), html.Br(), summary_table], [html.H5('Select Samples to Plot'), html.Br(), select_all, html.Hr(), sample_selector], dimensions


@callback(Output('data-load', 'disabled'),
              Output('upload-button', 'disabled'),
              Output('data-upload', 'disabled'),
              Output("mda_all_methods_and_plots", "disabled"),
              Output("mda_individual_method_and_plot", "disabled"),
              Output("mda_one_method_all_plots", "disabled"),
              Output("btn-download-template", "disabled"),
              Output("data-reset", "disabled"),
              Input('dataset-dropdown', 'value'),
              Input('method-dropdown', 'value'),
              Input('computed-data', 'data'),
              Input('sample_selection', 'value'))
def buttons(selection, method, summary, sample_selection):
    """
        This method handle the state of eight buttons that should be enabled/disabled based on
        conditions that allow the calculations to be executed appropriately.
    """
    if (((selection == '') or (selection is None)) and ((method == '') or (method is None))):
        Button_1, Button_2, Button_3, Button_7, Button_8 = True, True, True, True, True
    else:
        Button_1, Button_2, Button_3, Button_7, Button_8 = False, False, False, False, False
    if len(summary) <= 2 or len(sample_selection)==0:
        Button_4, Button_5, Button_6 = True, True, True
    else:
        if (method is None):
            Button_4, Button_5, Button_6 = False, True, True
        elif (method == 'All'):
            Button_4, Button_5, Button_6 = False, True, False
        else:
            Button_4, Button_5, Button_6 = False, False, False
    
    return Button_1, Button_2, Button_3, Button_4, Button_5, Button_6, Button_7, Button_8


@callback(Output('main-panel', 'children'),
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
            html.Img(src='/assets/img/empty.svg',
                     className="col-sm-1 align-self-center", style={'width': "60%", 'height': "auto"}),
        ], style={'text-align': 'center'}), json.dumps({}), [html.H5('Data Upload Summary'), html.Br(), html.P('Load or import data to start.', style={'text-align': 'center'})], [html.H5('Select Samples to Plot'), html.Br(), html.P('Load or import data to start.', style={'text-align': 'center'}), html.Div(id='sample_selection')], [html.H5('Age Plotting Dimensions'), html.P('Load or import data to start.', style={'text-align': 'center'}), dcc.Input(id='age-plot-dimensions', value=0, type='number', className='col-sm-6',  min=0,style={'display': 'none'})]


@callback(
    Output("download-plot", "data"),
    Output('btn-download-plot', 'disabled'),
    Output('filetype-dropdown', 'disabled'),
    Input("btn-download-plot", "n_clicks"),
    Input("CarouselPlot", "active_index"),
    Input("filetype-dropdown", "value"),
    Input("CarouselPlot", "items"),
    prevent_initial_call=True,
)
def download_plot(clicked, idx, file_format, items):

    triggered = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered == "btn-download-plot":
        if idx is None:
            idx = 0
        file = items[idx]['src']
        o = dcc.send_file(os.getcwd() + file[0:].replace('.svg', file_format)), False, False
    else:
        if 'plot_placeholder' not in items[0]['src']:
            if file_format is None:
                o = None, True, False
            else:
                o = None, False, False
        else:
            o = None, True, True
    return o


@callback(
    Output('computed-data-errors', 'data'),
    Output('summary-mda-title', 'children'),
    Output('summary-mda-text', 'children'),
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
    Input('tabletype-dropdown', 'value'),

    State('computed-data-errors', 'data'),
    State('summary-mda-title', 'children'),
    State('summary-mda-text', 'children'),
    State('summary-mda-table', 'children'),
    State('plot-carousel', 'children'),

    prevent_initial_call=True)
def pre_calculation(computed_data, method, sample_list, sigma, uncertainty,
                    best_age_cut_off, U238_decay_constant, U235_decay_constant, U238_U235,
                    excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238,
                    Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238,
                    decay_constant_uncertainty_U235, age_addition_set_max_plot,
                    button_method_1, button_method_2, button_method_3, tabletype,
                    state_computed_data_errors, state_summary_mda_title, state_summary_mda_text,
                    state_summary_mda_table, state_plot_carousel):
    df_errors = None
    summary_mda_table = html.Div()
    Image_File_Option = 'web'
    method_title_text = ''
    plotwidth = 10
    plotheight = 7
    method_text = None
    dashtable = None
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

            U238_decay_constant, U235_decay_constant, U238_U235, YSG_MDA, YC1s_MDA, YC1s_cluster_arrays, YC2s_MDA, YC2s_cluster_arrays, YDZ_MDA, minAges, mode, Y3Zo_MDA, Y3Zo_cluster_arrays, Y3Za_MDA, Y3Za_cluster_arrays, Tau_MDA, Tau_Grains, PDP_age, PDP, ages_errors1s_filtered, YSP_MDA, YSP_cluster, YPP_MDA, MLA_MDA = MDAFunc.MDA_Calculator(
                ages, errors, sample_list, dataToLoad_MLA, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off)
                
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

        if triggered == 'mda_all_methods_and_plots':
            folder_path = '/assets/plots/All_MDA_Methods_Plots/'
            
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
                                             style_table={'overflowX': 'auto'}, export_format=tabletype)

            files = glob.glob("assets/plots/All_MDA_Methods_Plots/*")
            for f in files:
                os.remove(f)

            MDAfig, MDA_plot_final = MDAFunc.Plot_MDA(MDAs_1s_table, all_MDA_data, sample_list, YSG_MDA, YC1s_MDA, YC2s_MDA,
                                                      YDZ_MDA, Y3Zo_MDA, Y3Za_MDA, Tau_MDA, YSP_MDA, YPP_MDA, MLA_MDA, Image_File_Option, plotwidth, plotheight)
            files = [file for file in os.listdir(
                os.getcwd() + folder_path) if file.endswith(".svg")]

            carousel2 = dbc.Carousel(id="CarouselPlot", items=[{"key": str(pos+1), "src": folder_path+img} for pos, img in enumerate(files)],
                                     controls=True, indicators=True, variant="dark")

            return df_errors, method_title_text, method_text, mda_table, carousel2
        elif triggered == 'mda_individual_method_and_plot':
            folder_path = 'assets/plots/Individual_MDA_Plots/'
            files = glob.glob(folder_path+"*")
            for f in files:
                os.remove(f)
            
            method_text = method_description[method]
            method_title_text = method_title[method]

            if method == 'YSG':
                YSG_MDA, method_table = MDAFunc.YSG_outputs(ages, errors, plotwidth, plotheight, sample_list, YSG_MDA, age_addition_set_max_plot, Image_File_Option)
            elif method == 'YDZ':
                YDZfig, YDZ_MDAs, method_table = MDAFunc.YDZ_outputs(ages, errors, sample_list, plotwidth, plotheight, Image_File_Option,iterations=10000, bins=25)
            elif method == 'YPP':
                YPP_MDAs, method_table = MDAFunc.YPP_outputs(ages, errors, sample_list, plotwidth, plotheight, Image_File_Option, sigma=1, min_cluster_size=2, thres=0.01, minDist=1, xdif=0.1)
            elif method == 'YC1s':
                YC1s_MDA, method_table = MDAFunc.YC1s_outputs(ages, errors, sample_list, YC1s_MDA, YC1s_cluster_arrays, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option, min_cluster_size=2)
            elif method == 'YC2s':
                YC2s, method_table = MDAFunc.YC2s_outputs(ages, errors, sample_list, YC2s_MDA, YC2s_cluster_arrays, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option, min_cluster_size=3)
            elif method == 'Y3Zo':
                Y3Zo_MDA, method_table = MDAFunc.Y3Zo_outputs(ages, errors, sample_list, Y3Zo_MDA, Y3Zo_cluster_arrays, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option, min_cluster_size=3)
            elif method == 'Y3Za':
                Y3Za_MDA, method_table = MDAFunc.Y3Za_outputs(ages, errors, Y3Za_MDA, Y3Za_cluster_arrays, sample_list, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option)
            elif method == 'Tau':
                Tau_MDA, method_table = MDAFunc.Tau_outputs(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off, plotwidth, plotheight, Image_File_Option, min_cluster_size=3, thres=0.01, minDist=1, xdif=1, x1=0, x2=4000)
            elif method == 'YSP':
                YSP_MDA, method_table = MDAFunc.YSP_outputs(Data_Type, ages, errors, sample_list, YSP_MDA, YSP_cluster, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option, min_cluster_size=2, MSWD_threshold=1)
            elif method == 'MLA':
                folder_path = 'assets/plots/IsoplotR/'
                files_web = glob.glob(folder_path + "*.svg") + glob.glob(folder_path + "*.png")
                for f in files_web:
                    os.remove(f)
                method_table = MDAFunc.MLA_outputs(sample_list, dataToLoad_MLA, True)
            
            dashtable = dash_table.DataTable(id='datatable-mda', export_format=tabletype,
                                             columns=[{"name": i, "id": i, "type": "numeric", 'format': Format(
                                                 scheme=Scheme.fixed, precision=2)} for i in method_table.columns],
                                             data=method_table.to_dict('records'), page_action="native", page_size=5,
                                             style_cell={'textAlign': 'center'}, style_table={'overflowX': 'auto'})

            files = [file for file in os.listdir(os.getcwd() + "/" + folder_path) if file.endswith(".svg")]
            carousel2 = dbc.Carousel(id="CarouselPlot", items=[{"key": str(pos+1), "src": folder_path+img} for pos, img in enumerate(files)], controls=True, indicators=True, variant="dark")

            return errors, method_title_text, method_text, dashtable, carousel2
        elif triggered == 'mda_one_method_all_plots':
            folder_path = 'assets/plots/Stratigraphic_Plots/'
            files = glob.glob(folder_path+"*")
            for f in files:
                os.remove(f)
            if method != 'All':
                method_text = method_description[method]
                method_title_text = method_title[method]

            MDAFunc.MDA_Strat_Plot(YSG_MDA, YC1s_MDA, YC2s_MDA, YDZ_MDA, Y3Zo_MDA, Y3Za_MDA, Tau_MDA, YSP_MDA, YPP_MDA, MLA_MDA, ages, errors, sample_list, Image_File_Option, plotwidth, plotheight, method)

            files = [file for file in os.listdir(os.getcwd() + "/" + folder_path) if file.endswith(".svg")]
            carousel2 = dbc.Carousel(id="CarouselPlot", items=[{"key": str(pos+1), "src": folder_path+img} for pos, img in enumerate(files)], controls=True, indicators=True, variant="dark")
            return df_errors, method_title_text, method_text, None, carousel2
    if triggered == "tabletype-dropdown":
      return state_computed_data_errors, state_summary_mda_title, state_summary_mda_text, state_summary_mda_table, state_plot_carousel
    else:
      return df_errors, method_title_text, method_text, summary_mda_table, carousel


@callback(
    Output('best_age_cut_off', 'value'),
    Output('U238_decay_constant', 'value'),
    Output('U235_decay_constant', 'value'),
    Output('U238_U235', 'value'),
    Output('excess_variance_206_238', 'value'),
    Output('excess_variance_207_206', 'value'),
    Output('Sy_calibration_uncertainty_206_238', 'value'),
    Output('Sy_calibration_uncertainty_207_206', 'value'),
    Output('decay_constant_uncertainty_U238', 'value'),
    Output('decay_constant_uncertainty_U235', 'value'),
    Input("data-reset", "n_clicks"))
def reset_numerics(clicks):
    """
        This function handle the reset of the numeric inputs that we have in the left bar.
        Currently, the reset button is only enable after a dataset type is selected.
        The clicks input doesn't have its value used, but it is responsible for triggering the event.
    """
    return 1500, 1.55125, 9.8485, 137.818, 1.2, 0.7, 0.6, 0.1, 0.16, 0.2


@callback(
    Output('dataset-dropdown', 'value'),
    Output('method-dropdown', 'value'),
    Output('radio_uncertainty', 'value'),
    Output('radio_sigma', 'value'),
    Input("data-reset", "n_clicks"))
def clear_selection(clicks):
    if clicks is not None:
        return None, None, None, None
    else:
        return None, None, "percent", 2


@callback(
    Output("download-template", "data"),
    State('dataset-dropdown', 'value'),
    Input("btn-download-template", "n_clicks"),
    prevent_initial_call=True,
)
def func(selection, download):

    if selection == 'Ages':
        template_filename = "data/Data_Upload_Example_Template_Ages.xlsx"
    elif selection == '238U/206Pb_&_207Pb/206Pb':
        template_filename = "data/Data_Upload_Example_Template_Ratios.xlsx"

    return dcc.send_file(template_filename)

@callback(
    Output("sample_selection", "value"),
    [Input("sample_all", "value")],
    [State("sample_selection", "options")],
)
def select_all_none(all_selected, options):
    all_or_none = []
    all_or_none = [option["value"] for option in options if all_selected]
    return all_or_none










######################################################################################################


layout = html.Div(children=[
        html.Div(children=[
            html.B('Input Data'), html.Br(), html.Br(),
            html.Label('Select Dataset Type'),
            dcc.Dropdown(options=[{'label': u'U-Pb 238/206 & Pb-Pb 207/206', 'value': '238U/206Pb_&_207Pb/206Pb'},
                                  {'label': u'Best Age & σx', 'value': 'Ages'}], value='Ages', id='dataset-dropdown'),
            html.Br(),
            html.Label('Select MDA Calculation Method'),
            dcc.Dropdown(options=[
                {'label': u'YSG: Youngest Single Grain', 'value': 'YSG'},
                {'label': u'YDZ: Youngest Detrital Zircon', 'value': 'YDZ'},
                {'label': u'YPP: Youngest Graphical Peak', 'value': 'YPP'},
                {'label': u'YC1σ (2+): Youngest Grain Cluster at 1σ', 'value': 'YC1s'},
                {'label': u'YC2σ (3+): Youngest Grain Cluster at 2σ', 'value': 'YC2s'},
                {'label': u'Y3Zo: Youngest Three Zircons at 2σ (Y3Zo)', 'value': 'Y3Zo'},
                {'label': u'Y3Za: Youngest Three Zircons (Y3Za)', 'value': 'Y3Za'},
                {'label': u'Tau: Tau Method', 'value': 'Tau'},
                {'label': u'YSP: Youngest Statistical Population', 'value': 'YSP'},
                {'label': u'MLA: Maximum Likelihood Age', 'value': 'MLA'},
                {'label': u'All Methods', 'value': 'All'}], id = 'method-dropdown', value=None),
            html.Br(),
            html.Label('Sigma (σx) in Dataset (default is 1σx)'),
            dcc.RadioItems(options=[{'label': '1 σx', 'value': 1},
                                    {'label': '2 σx', 'value': 2}],
                           value=2, id='radio_sigma', labelClassName='col-sm-6'),
            html.Br(),
            html.Label('Uncertainty Format in Dataset'),
            dcc.RadioItems(options=[{'label': 'Percent (%)', 'value': 'percent'},
                                    {'label': 'Absolute (ABS)', 'value': 'absolute'}],
                           value='percent', id='radio_uncertainty',
                           labelClassName='col-sm-6'),
            html.Br(),
            html.Div(children=[
                html.Label('Best Age Cut Off', className='labelCte col-sm-7'),
                dcc.Input(id='best_age_cut_off', value=1500, min=0, required=True,
                          type='number', className='inputNumbers col-sm-2')],
                className="row input-row"),
            html.Div(children=[
                html.Label('U238 Decay Constant (10⁻¹⁰)', className='labelCte col-sm-7'),
                dcc.Input(id='U238_decay_constant', value=1.55125, min=0, required=True,
                          type='number', className='inputNumbers col-sm-2')],
                className="row input-row"),
            html.Div(children=[
                html.Label('U235 Decay Constant (10⁻¹⁰)', className='labelCte col-sm-7'),
                dcc.Input(id='U235_decay_constant', value=9.8485, min=0, required=True,
                          type='number', className='inputNumbers col-sm-2')],
                className="row input-row"),
            html.Div(children=[
                html.Label('U238/U235', className='labelCte col-sm-7'),
                dcc.Input(id='U238_U235', value=137.818, min=0, required=True,
                          type='number', className='inputNumbers col-sm-2')],
                className="row input-row"),

            html.Br(),
            html.B('Systematic Uncertainties (%)'),
            html.P('Input 0 if not required in final MDA uncertainty calculation. Only applies to: YC1σ,YC2σ,YSG,Y3Za,Y3Zo,YSP,Tau'),
            
            html.Div(children=[
                html.Label('Long Term Excess Variance: U-Pb 238/206',
                           className='labelCte col-sm-9'),
                dcc.Input(id='excess_variance_206_238', value=1.2,
                          min=0, required=True, type='number',
                          className='inputCte col-sm-2')
            ], className="row input-row"),
            html.Div(children=[
                html.Label('Long Term Excess Variance: Pb-Pb 207/206',
                           className='labelCte col-sm-9'),
                dcc.Input(id='excess_variance_207_206', value=0.7,
                          min=0, required=True, type='number',
                          className='inputCte col-sm-2')
            ], className="row input-row"),

            html.Div(children=[
                html.Label('Sy Calibration Uncertainty U-Pb 238/206',
                           className='labelCte col-sm-9'),
                dcc.Input(id='Sy_calibration_uncertainty_206_238', value=0.6,
                          min=0, required=True, type='number',
                          className='inputCte col-sm-2')
            ], className="row input-row"),

            html.Div(children=[
                html.Label('Sy Calibration Uncertainty Pb-Pb 207/206',
                           className='labelCte col-sm-9'),
                dcc.Input(id='Sy_calibration_uncertainty_207_206', value=0.1,
                          min=0, required=True, type='number',
                          className='inputCte col-sm-2')
            ], className="row input-row"),

            html.Div(children=[
                html.Label('Decay Constant Uncertainty U 238',
                           className='labelCte col-sm-9'),
                dcc.Input(id='decay_constant_uncertainty_U238', value=0.16,
                          min=0, required=True, type='number',
                          className='inputCte col-sm-2')
            ], className="row input-row"),

            html.Div(children=[
                html.Label('Decay Constant Uncertainty U 235',
                           className='labelCte col-sm-9'),
                dcc.Input(id='decay_constant_uncertainty_U235', value=0.2,
                          min=0, required=True, type='number',
                          className='inputCte col-sm-2')
            ], className="row input-row"), html.Br(),

            dbc.Button("Load Sample Data", color="primary",
                       id="data-load", className="mb-3 col-sm-11"),
            dcc.Upload(dbc.Button("Import Data", color="primary", id="upload-button",
                       className="mb-3 col-sm-12"), id="data-upload", className="col-sm-11"),
            dbc.Button("Download Import Template", color="primary",
                       id="btn-download-template", className="mb-3 col-sm-11"),
            dcc.Download(id="download-template")

        ], className='col-12 col-lg-3 settings-menu'),
        accordion,
    ], className='row justify-content-between')
