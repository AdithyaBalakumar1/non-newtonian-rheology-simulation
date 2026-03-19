"""Upgraded interactive Dash dashboard for non-Newtonian rheology."""
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Dash(__name__)

gamma = np.logspace(-1, 3, 300)
GAMMA_MIN = 1e-6

app.layout = html.Div([
    html.H1("Non-Newtonian Rheology Simulator", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.H3("Model Selection"),
            dcc.Dropdown(
                id="model-select",
                options=[
                    {"label": "Power Law", "value": "power_law"},
                    {"label": "Bingham Plastic", "value": "bingham"},
                    {"label": "Herschel-Bulkley", "value": "hb"},
                ],
                value="power_law",
                clearable=False,
            ),

            html.Br(),
            html.H3("Power Law Parameters"),
            html.Label("Consistency Index K"),
            dcc.Slider(0.1, 5.0, 0.1, value=0.5, id="K", tooltip={"placement": "bottom"}),
            html.Label("Flow Index n"),
            dcc.Slider(0.1, 2.0, 0.05, value=0.7, id="n", tooltip={"placement": "bottom"}),

            html.Br(),
            html.H3("Bingham / HB Parameters"),
            html.Label("Yield Stress τ_y (Pa)"),
            dcc.Slider(0.0, 20.0, 0.5, value=2.0, id="tau_y", tooltip={"placement": "bottom"}),
            html.Label("Plastic Viscosity μ_p (Pa·s)"),
            dcc.Slider(0.01, 2.0, 0.05, value=0.3, id="mu_p", tooltip={"placement": "bottom"}),
        ], style={"width": "30%", "display": "inline-block", "verticalAlign": "top", "padding": "20px"}),

        html.Div([
            dcc.Graph(id="rheology-graph"),
            dcc.Graph(id="viscosity-graph"),
        ], style={"width": "68%", "display": "inline-block", "verticalAlign": "top"}),
    ]),
])


@app.callback(
    Output("rheology-graph", "figure"),
    Output("viscosity-graph", "figure"),
    Input("model-select", "value"),
    Input("K", "value"),
    Input("n", "value"),
    Input("tau_y", "value"),
    Input("mu_p", "value"),
)
def update_graphs(model_name, K, n, tau_y, mu_p):
    tau_dict = {}
    mu_dict = {}

    tau_pl = K * gamma ** n
    tau_bp = tau_y + mu_p * gamma
    tau_hb = tau_y + K * gamma ** n

    tau_dict["Power Law"] = tau_pl
    tau_dict["Bingham Plastic"] = tau_bp
    tau_dict["Herschel-Bulkley"] = tau_hb

    gamma_safe = np.maximum(gamma, GAMMA_MIN)
    mu_dict["Power Law"] = tau_pl / gamma_safe
    mu_dict["Bingham Plastic"] = tau_bp / gamma_safe
    mu_dict["Herschel-Bulkley"] = tau_hb / gamma_safe

    fig_r = go.Figure()
    fig_v = go.Figure()

    for name, tau in tau_dict.items():
        visible = True if (
            (model_name == "power_law" and name == "Power Law") or
            (model_name == "bingham" and name == "Bingham Plastic") or
            (model_name == "hb" and name == "Herschel-Bulkley") or
            model_name == "all"
        ) else "legendonly"
        fig_r.add_trace(go.Scatter(x=gamma, y=tau, mode="lines", name=name, visible=visible))
        fig_v.add_trace(go.Scatter(x=gamma_safe, y=mu_dict[name], mode="lines", name=name, visible=visible))

    fig_r.update_layout(
        xaxis_type="log", yaxis_type="log",
        xaxis_title="Shear Rate (s⁻¹)", yaxis_title="Shear Stress (Pa)",
        title="Rheology Curve: Shear Stress vs Shear Rate",
    )
    fig_v.update_layout(
        xaxis_type="log", yaxis_type="log",
        xaxis_title="Shear Rate (s⁻¹)", yaxis_title="Apparent Viscosity (Pa·s)",
        title="Viscosity Curve: Apparent Viscosity vs Shear Rate",
    )
    return fig_r, fig_v


if __name__ == "__main__":
    app.run(debug=True)
