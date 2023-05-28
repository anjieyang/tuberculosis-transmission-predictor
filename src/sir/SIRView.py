import networkx as nx
import pandas as pd
import plotly.graph_objects as go
from dash import dash, dcc, html
from dash.dependencies import Input, Output


class SIRView:
    def __init__(self, file_path):
        self.file_path = file_path

    def show_view(self):
        # Load the Excel file
        xlsx = pd.ExcelFile(self.file_path + 'data.xlsx')

        # Load the first sheet to get the column names
        df = pd.read_excel(xlsx, sheet_name=xlsx.sheet_names[0])

        # Load the fourth sheet of the second Excel file to get the adjacency matrix
        df2 = pd.read_excel(xlsx, sheet_name=xlsx.sheet_names[3])

        # Initialize the Dash app
        app = dash.Dash(__name__)

        # Define the layout of the app
        app.layout = html.Div([
            dcc.Dropdown(
                id='column-dropdown',
                options=[{'label': 'Sum', 'value': 'Sum'}] + [{'label': i, 'value': i} for i in df.columns],
                value=['Sum'],
                multi=True
            ),
            dcc.Checklist(
                id='sheet-checkbox',
                options=[{'label': i, 'value': i} for i in xlsx.sheet_names if i != 'contacts'],
                value=['S', 'I', 'R']
            ),
            dcc.Checklist(
                id='graph-type-checkbox',
                options=[{'label': i, 'value': i} for i in ['Bar', 'Line']],
                value=['Bar', 'Line']
            ),
            dcc.Graph(id='graph'),
            dcc.Graph(id='network-graph')
        ])

        # Define the callback to update the graph when sheets or columns are selected
        @app.callback(
            Output('graph', 'figure'),
            [Input('sheet-checkbox', 'value'),
             Input('column-dropdown', 'value'),
             Input('graph-type-checkbox', 'value')]
        )
        def update_graph(selected_sheets, selected_columns, selected_graph_types):
            # Create the figure
            fig = go.Figure()

            if selected_sheets is None or selected_columns is None or selected_graph_types is None:
                return fig

            # Loop over each selected sheet
            for sheet in selected_sheets:
                # Load the sheet into a data frame
                df = pd.read_excel(xlsx, sheet_name=sheet)

                # Loop over each selected column
                for column in selected_columns:
                    # Check if the special "Sum" option was selected
                    if column == 'Sum':
                        # Calculate the sum across the selected columns for each row
                        df_sum = df.sum(axis=1)

                        if 'Bar' in selected_graph_types:
                            # Add a bar chart of the sum to the figure
                            fig.add_trace(go.Bar(
                                x=df.index,
                                y=df_sum,
                                name=f'{sheet}-Sum'
                            ))

                        if 'Line' in selected_graph_types:
                            # Calculate the difference between consecutive sums
                            df_sum_diff = df_sum.diff()
                            # Add a line chart of the differences to the figure
                            fig.add_trace(go.Scatter(
                                x=df.index,
                                y=df_sum_diff,
                                mode='lines',
                                name=f'{sheet}-Sum change'
                            ))

                    else:
                        if 'Bar' in selected_graph_types:
                            # Add a bar chart of the column to the figure
                            fig.add_trace(go.Bar(
                                x=df.index,
                                y=df[column],
                                name=f'{sheet}-{column}'
                            ))

                        if 'Line' in selected_graph_types:
                            # Calculate the difference between consecutive rows
                            df_diff = df[column].diff()
                            # Add a line chart of the differences to the figure
                            fig.add_trace(go.Scatter(
                                x=df.index,
                                y=df_diff,
                                mode='lines',
                                name=f'{sheet}-{column} change'
                            ))

            return fig

        # Define a new callback to update the network graph
        @app.callback(
            Output('network-graph', 'figure'),
            [Input('column-dropdown', 'value')]
        )
        def update_network_graph(selected_columns):
            # Create the network graph figure
            fig = go.Figure()

            # Create a graph from the DataFrame
            G = nx.from_pandas_adjacency(df2)

            # Compute positions for viz.
            pos = nx.spring_layout(G)

            edge_trace = go.Scatter(
                x=[],
                y=[],
                line=dict(width=0.5, color='#888'),
                hoverinfo='none',
                mode='lines',
                hovertext=[])

            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_trace['x'] += tuple([x0, x1, None])
                edge_trace['y'] += tuple([y0, y1, None])
                contact_rate = df2.loc[edge[0], edge[1]]
                edge_trace['hovertext'] += tuple([f'Contact rate between {edge[0]} and {edge[1]}: {contact_rate}'])

            node_trace = go.Scatter(
                x=[],
                y=[],
                text=[],
                mode='markers+text',
                hoverinfo='text',
                marker=dict(
                    showscale=True,
                    colorscale='YlGnBu',
                    reversescale=True,
                    color=[],
                    size=10,
                    colorbar=dict(
                        thickness=15,
                        title='Node Connections',
                        xanchor='left',
                        titleside='right'
                    ),
                    line=dict(width=2)),
                textposition='top center',
                hovertext=[])

            for node in G.nodes():
                x, y = pos[node]
                degree = len(G[node])  # counting only nodes with non-zero contact rate
                node_trace['x'] += tuple([x])
                node_trace['y'] += tuple([y])
                node_trace['text'] += tuple([node])
                node_trace['marker']['size'] = 15

                if node in selected_columns:
                    node_trace['marker']['color'] += tuple(["#FF0000"])  # Bright red for selected node
                else:
                    node_trace['marker']['color'] += tuple([degree])  # Original color assignment

                node_trace['hovertext'] += tuple([f'Node {node} connects with {degree - 1} nodes'])

            fig.add_trace(edge_trace)
            fig.add_trace(node_trace)

            fig.update_layout(
                title='Network of Contacts',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

            return fig

        app.run_server(debug=False)


# Run the app
if __name__ == '__main__':
    sir_view = SIRView('')
    sir_view.show_view()
