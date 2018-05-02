import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import plotly
import pandas as pd
import datasource
from datetime import datetime as _datetime
from plotly.graph_objs import Scatter

df = datasource.data_from_backend()
app = dash.Dash()

app.layout = html.Div([
    html.H1('Side Effective: Side Task Tracker'),
    dt.DataTable(
        rows=df.to_dict('records'),
        columns=df.columns,
        row_selectable=True,
        filterable=True,
        sortable=True,
        editable=True,
        resizable=True,
        enable_drag_and_drop=True,
        selected_row_indices=[],
        id='table'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(id='graph'),
], className="container")

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@app.callback(
    Output('table', 'rows'),
    [Input('table', 'row_update')],
    [State('table', 'rows')])
def update_record(row_update, rows):
    if row_update:
        from_row, to_row, updated_dict = row_update[0][
            'from_row'], row_update[0]['to_row'], row_update[0]['updated']
        for i in range(from_row, to_row + 1):
            for k, v in updated_dict.items():
                datasource.update(i, k, v)
        if to_row == df.shape[0] - 1:
            dff = datasource.data_from_backend()  # should be updated receiving from backend
            dff.loc[from_row:to_row+1] = dff[from_row:to_row +
                                             1].assign(**updated_dict)
            return dff.append(dict(), ignore_index=True).to_dict('records')
    return rows


@app.callback(
    Output('graph', 'figure'),
    [Input('table', 'rows'),
     Input('table', 'selected_row_indices')])
def redraw_graph_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=3, cols=1,
        subplot_titles=('When', 'Who', 'What',),
        shared_xaxes=False)
    marker = {'color': ['#0074D9']*len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace(
        Scatter(
            name='When',
            x=dff['When'],
            y=dff['How long(hours)'],
            mode='lines+marker',
            marker=marker), 1, 1)
    fig.append_trace({
        'name': 'Who',
        'x': dff['Who'],
        'y': dff['How long(hours)'],
        'type': 'bar',
        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'name': 'What',
        'x': dff['What'],
        'y': dff['How long(hours)'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)
    fig['layout']['showlegend'] = True
    return fig


@app.callback(
    Output('table', 'selected_row_indices'),
    [Input('graph', 'clickData')],
    [State('table', 'selected_row_indices')])
def select_row_indices_on_table(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


if __name__ == '__main__':
    app.run_server(debug=True, port=80)
