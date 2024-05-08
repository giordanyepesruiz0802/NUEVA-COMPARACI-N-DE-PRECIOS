import dash
import dash_bootstrap_components as dbc
from dash import html, dash_table, Input, Output
import pandas as pd
from difflib import get_close_matches

# Sample data
item1 = ["CONCRETO", "ACERO", "MADERA", "VINILO", "PINTURA", "CIELO RASO", "CERAMICA", "MORTERO",
         "CARPINTERIA", "BALDOSA", "MANO DE OBRA", "VIDRIOS"]

item2 = ["CONCRETO", "ACERO", "MADERA", "VINILO", "PINTURA", "CIELO RASO", "CERAMICA", "MORTERO",
         "CARPINTERIA", "BALDOSA", "MANO DE OBRA", "VIDRIOS"]

valor1 = [5000, 3000, 2500, 3600, 4800, 20000, 25000, 8500, 9200, 7000, 1000, 800]

valor2 = [10000, 25000, 11000, 9500, 4700, 2000, 8500, 4250, 2500, 1500, 750, 250]

item_1 = pd.DataFrame({"ITEM_1": item1})
item_2 = pd.DataFrame({"ITEM_2": item2})
valor_1 = pd.DataFrame({"PRECIO_UNITARIO_1": valor1})
valor_2 = pd.DataFrame({"PRECIO_UNITARIO_2": valor2})

max_values = pd.DataFrame({"VALOR_MENOR": [min(v1, v2) for v1, v2 in zip(valor1, valor2)]})
data_csv = pd.read_csv('backend/Lista_oficial_de_precios_unitarios_fijos_de_Obra_P_blica_y_de_consultor_a_-_DEPARTAMENTO_DE_BOYAC__20240505.csv')

# Dash app initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Layout
app.layout = dbc.Container([
    html.H6("VALOR UNITARIO COMPARADO", className='mb-4 text-center'),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='VALOR_MENOR',
                columns=[{'name': 'Valor Menor', 'id': 'VALOR_MENOR', 'editable': False}],
                data=max_values.to_dict('records'),
                style_table={'overflowX': 'auto'}
            ),
            md=12
        )
    ], className='shadow p-3 border rounded'),

    dbc.Row([
        dbc.Col([
            html.H6("PRECIO UNITARIO COTIZANTE 1", className='mb-4 text-center'),
            dash_table.DataTable(
                id='tabla_valor_1',
                columns=[{'name': 'PRECIO_UNITARIO_1', 'id': 'PRECIO_UNITARIO_1', 'editable': True}],
                data=valor_1.to_dict('records'),
                style_table={'overflowX': 'auto'}
            ),
            html.H6("ITEM COTIZANTE 1", className='mb-4 text-center'),
            dash_table.DataTable(
                id='tabla_item_1',
                columns=[{'name': 'ITEM_1', 'id': 'ITEM_1', 'editable': True}],
                data=item_1.to_dict('records'),
                style_table={'overflowX': 'auto'}
            )
        ], md=6, style={'color': 'black'}),
        dbc.Col([
            html.H6("PRECIO UNITARIO COTIZANTE 2", className='mb-4 text-center'),
            dash_table.DataTable(
                id='tabla_valor_2',
                columns=[{'name': 'PRECIO_UNITARIO_2', 'id': 'PRECIO_UNITARIO_2', 'editable': True}],
                data=valor_2.to_dict('records'),
                style_table={'overflowX': 'auto'}
            ),
            html.H6("ITEM COTIZANTE 2", className='mb-4 text-center'),
            dash_table.DataTable(
                id='tabla_item_2',
                columns=[{'name': 'ITEM_2', 'id': 'ITEM_2', 'editable': True}],
                data=item_2.to_dict('records'),
                style_table={'overflowX': 'auto'}
            )
        ], md=6, style={'color': 'black'})
    ]),

    html.H6("ITEM Y VALOR MÁS BAJO", className='mb-4 text-center'),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='tabla_valores_menor',
                columns=[{'name': 'ITEM', 'id': 'ITEM'}, {'name': 'VALOR_MENOR', 'id': 'VALOR_MENOR'}],
                style_table={'overflowX': 'auto'}
            ),
            md=12
        )
    ], className='shadow p-3 border rounded')
], className='bg-light py-4')

# Callbacks
@app.callback(
    [Output('valor-menor-container', 'children'),
     Output('tabla_valores_menor', 'data')],
    [Input('tabla_valor_1', 'data'),
     Input('tabla_valor_2', 'data')]
)
def update_valor_menor(data_valor_1, data_valor_2):
    if data_valor_1 and data_valor_2:
        valor_1_df = pd.DataFrame(data_valor_1)
        valor_2_df = pd.DataFrame(data_valor_2)
        
        # Convertir las columnas a tipo float
        valor_1_df['PRECIO_UNITARIO_1'] = valor_1_df['PRECIO_UNITARIO_1'].astype(float)
        valor_2_df['PRECIO_UNITARIO_2'] = valor_2_df['PRECIO_UNITARIO_2'].astype(float)
        
        # Calcular el valor menor
        max_values['VALOR_MENOR'] = [min(v1, v2) for v1, v2 in zip(valor_1_df['PRECIO_UNITARIO_1'], valor_2_df['PRECIO_UNITARIO_2'])]
        
        return None, max_values[['ITEM', 'VALOR_MENOR']].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
