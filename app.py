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
Derecha_1= dbc.Container([
    html.H6("PRECIO UNITARIO COTIZANTE 2", className='mb-4 text-center'),
    dash_table.DataTable(
        id='tabla_valor_2',
        columns=[
            {'name': 'Precio Unitario 2', 'id': 'PRECIO_UNITARIO_2', 'editable': True},  # Modificar el texto del encabezado
        ],
        data=valor_2.to_dict('records'),
        style_table={'overflowX': 'auto'}
    ),
], className='shadow p-3 border rounded')
Derecha_2= dbc.Container([
    html.H6("ITEM COTIZANTE 2", className='mb-4 text-center'),
    dash_table.DataTable(
        id='tabla_item_2',
        columns=[
            {'name':'ITEM_2','id':'ITEM_2','editable':True},
        ],
        data= item_2.to_dict('records'),
        style_table={'overflowX': 'auto'}
    ),
], className='shadow p-3 border rounded')
Izquierda_1= dbc.Container([
    html.H6("ITEM COTIZANTE 1", className='mb-4 text-center'),
    dash_table.DataTable(
        id='tabla_item_1',
        columns=[
            {'name':'ITEM_1','id':'ITEM_1','editable':True},
        ],
        data= item_1.to_dict('records'),
        style_table={'overflowX': 'auto'}
    ),
], className='shadow p-3 border rounded')
Izquierda_2= dbc.Container([
    html.H6("PRECIO UNITARIO COTIZANTE 1", className='mb-4 text-center'),
    dash_table.DataTable(
        id='tabla_valor_1',
        columns=[
            {'name':'PRECIO_UNITARIO_1','id':'PRECIO_UNITARIO_1','editable':True},
        ],
        data= valor_1.to_dict('records'),
        style_table={'overflowX': 'auto'}
    ),
], className='shadow p-3 border rounded')
Derecha= dbc.Container([
    dbc.Row([
        dbc.Col(Derecha_1,md=6,style={'color':'black'}),
        dbc.Col(Derecha_2,md=6,style={'color':'black'})
    ])    
])
Izquierda= dbc.Container([
    dbc.Row([
        dbc.Col(Izquierda_1,md=6,style={'color':'black'}),
        dbc.Col(Izquierda_2,md=6,style={'color':'black'}),
    ])    
])
centro_l= dbc.Container([
   html.H6("VALOR UNITARIO COMPARADO", className='mb-4 text-center'),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='VALOR_MENOR',
                columns=[
                    {'name': 'Valor Menor', 'id': 'VALOR_MENOR', 'editable': False},  # Modificar el texto del encabezado
                ],
                data=max_values.to_dict('records'),
                style_table={'overflowX': 'auto'}
            ),
            md=12
        )
    ], className='shadow p-3 border rounded')
], className='bg-light py-4')

# Dash app initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server
app.layout = layout

@app.callback(
    Output('valor-menor-container', 'children'),
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
        
        return None

@app.callback(
    Output('VALOR_MENOR', 'data'),
    [Input('valor-menor-container', 'children')]
)
def update_comparison_table(_):
    return max_values.to_dict('records')

@app.callback(
    Output('tabla_item_comparado', 'data'),
    [Input('valor-menor-container', 'children')]
)
def update_item_comparison_table(_):
    # Obtener el valor menor comparado
    valor_menor = max_values['VALOR_MENOR'].min()
    
    # Determinar si el valor menor corresponde a item 1 o item 2
    if valor_menor in valor_1['PRECIO_UNITARIO_1'].values:
        item_df = item_1
        valor_key = 'PRECIO_UNITARIO_1'
    else:
        item_df = item_2
        valor_key = 'PRECIO_UNITARIO_2'
    
    # Obtener las palabras a buscar en la columna "ITEM"
    edited_items = item_df[item_df[valor_key] == valor_menor]['ITEM_1' if item_df is item_1 else 'ITEM_2'].tolist()
    
    # Filtrar los datos del CSV por palabras similares al valor menor
    similar_items = []
    for edited_item in edited_items:
        similar_items.extend(get_close_matches(edited_item, data_csv['ITEM'], n=1, cutoff=0.8))
    
    # Filtrar los datos del CSV según las palabras similares
    filtered_data = data_csv[data_csv['ITEM'].isin(similar_items)]
    
    return filtered_data[['ITEM', 'TOTAL']].to_dict('records')

@app.callback(
    Output('tabla_valores_menor', 'data'),
    [Input('valor-menor-container', 'children')]
)
def update_valores_menor_table(_):
    return max_values[['ITEM', 'VALOR_MENOR']].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
