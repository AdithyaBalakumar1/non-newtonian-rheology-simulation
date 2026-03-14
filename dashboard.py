import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

app = Dash(__name__)

gamma = np.logspace(-1,3,200)

app.layout = html.Div([
    
    html.H1("Non-Newtonian Rheology Simulator"),

    html.Label("Consistency Index (K)"),
    dcc.Slider(0.1,2,0.1,value=0.5,id="K"),

    html.Label("Flow Index (n)"),
    dcc.Slider(0.1,1.5,0.05,value=0.7,id="n"),

    dcc.Graph(id="rheology-graph")
])


@app.callback(
    Output("rheology-graph","figure"),
    Input("K","value"),
    Input("n","value")
)

def update_graph(K,n):

    tau = K*gamma**n

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=gamma,
        y=tau,
        mode="lines",
        name="Power Law Fluid"
    ))

    fig.update_layout(
        xaxis_type="log",
        yaxis_type="log",
        xaxis_title="Shear Rate",
        yaxis_title="Shear Stress",
        title="Interactive Rheology Curve"
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
