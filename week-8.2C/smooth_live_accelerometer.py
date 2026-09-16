from dash import Dash, dcc, html, Input, Output
import time


def add_smooth_live_graph(
    app,
    graph_id,
    interval_id,
    data_source,
    series_names,
    update_ms=250,
    max_points=200,
    title="Live Data",
    xaxis_title="Time",
    yaxis_title="Value"
):
    traces = [
        {
            "x": [],
            "y": [],
            "mode": "lines",
            "name": series_name
        }
        for series_name in series_names
    ]

    graph = dcc.Graph(
        id=graph_id,
        figure={
            "data": traces,
            "layout": {
                "title": title,
                "xaxis": {"title": xaxis_title},
                "yaxis": {"title": yaxis_title},
                "uirevision": "keep"
            }
        }
    )

    interval = dcc.Interval(
        id=interval_id,
        interval=update_ms,
        n_intervals=0
    )

    @app.callback(
        Output(graph_id, "extendData"),
        Input(interval_id, "n_intervals")
    )
    def update_live_graph(n):
        current_time = time.strftime("%H:%M:%S")

        x_values = [
            [current_time]
            for _ in series_names
        ]

        y_values = [
            [data_source[series_name]]
            for series_name in series_names
        ]

        new_data = {
            "x": x_values,
            "y": y_values
        }

        trace_indices = list(range(len(series_names)))

        return new_data, trace_indices, max_points

    return graph, interval
