from flet import *
import flet as ft
from flet import Text, View, Page, AppBar, ElevatedButton, TextField
from flet import RouteChangeEvent, ViewPopEvent, CrossAxisAlignment, MainAxisAlignment
import controls
from datetime import datetime
import psycopg2

mydb = psycopg2.connect(
    host="ep-fancy-firefly-a4lp2wex-pooler.us-east-1.aws.neon.tech",
    user="default",
    password="rCBSUdv3k4MY",
    database="verceldb"
)

cursor = mydb.cursor()

def main(page: Page):

    # // -- Funções  -- //

    page.title = "FinApp"
    page.window_center()
    page.window_height = 700
    page.window_width = 400
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_resizable = False

    data_dia = datetime.now()

    def bt_apagar(e):        
        pass

    def bt_editar(e):        
        pass

    mydt = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Data")),
                 ft.DataColumn(ft.Text("Usuário")),
                 ft.DataColumn(ft.Text("Produto")),
                 ft.DataColumn(ft.Text("Valor")),
                 ft.DataColumn(ft.Text("Categoria")),
                ],
                rows=[],
        data=[
            [data_dia, controls.usuario.value, controls.produto.value, controls.valor_un.value, controls.categoria.value],
        ],
        width=300,
        height=300,
    )


    def load_data_compras():
        cursor.execute("SELECT * FROM compras")
        result = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]

        for row in rows:
            mydt.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row['data'])),
                        ft.DataCell(ft.Text(row['usuario'])),
                        ft.DataCell(ft.Text(row['produto'])),
                        ft.DataCell(ft.Text(row['preço'])),
                        ft.DataCell(ft.Text(row['categoria'])),
                        ft.DataCell(
                            ft.Row([
                               ft.IconButton("Apagar", icon_color="red",
                                           data=row,
                                           on_click=bt_apagar),
                                ft.IconButton("Editar", icon_color="red",
                                           data=row,
                                           on_click=bt_editar),
                            ])
                        )
                    ]
                )
            )
        page.update()

    load_data_compras()

    def load_data_usuarios():
        cursor.execute("SELECT * FROM usuarios")
        result = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]

        for row in rows:
            mydt.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row['usuario'])),
                        ft.DataCell(ft.Text(row['senha'])),
                        ft.DataCell(ft.Text(row['id'])),
                        ft.DataCell(
                            ft.Row([
                               ft.IconButton("Apagar", icon_color="red",
                                           data=row,
                                           on_click=bt_apagar),
                                ft.IconButton("Editar", icon_color="red",
                                           data=row,
                                           on_click=bt_editar),
                            ])
                        )
                    ]
                )
            )
        page.update()
    load_data_usuarios()

    def enviar(e):
        try:
            sql = f"INSERT INTO compras VALUES ('{data_dia}','{controls.usuario.value}','{controls.produto.value}', {controls.valor_un.value}, '{controls.categoria.value}')"
            cursor.execute(sql)
            mydb.commit()
            print(cursor.rowcount, "Compra registrada.")

            mydt.rows.clear()
            load_data_compras()

            controls.produto.value = ''
            controls.valor_un.value = ''
            controls.categoria.value = ''

            page.snack_bar = ft.SnackBar(
                ft.Text("Compra registrada", size=30),
                bgcolor="green"
            )
            page.snack_bar.open = True
            page.update()   
        except Exception as e:
            print(e)
            print("Erro")

        data_dia
        controls.usuario.value
        controls.produto.value
        controls.valor_un.value
        controls.categoria.value
        page.update()

    def cadastrar(e):
        try:
            if(controls.senha.value == controls.conf_senha.value):
                sql = f"INSERT INTO usuarios VALUES ('{controls.usuario.value}','{controls.senha.value}')"
                cursor.execute(sql)
                mydb.commit()
                print(cursor.rowcount, "Usuário cadastrado")

                mydt.rows.clear()
                load_data_compras()

                page.snack_bar = ft.SnackBar(
                    ft.Text("Usuário cadastrado", size=20),
                    bgcolor="green"
                )
                page.snack_bar.open = True
                page.update()
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Senhas não coincidem", size=20),
                    bgcolor="red"
                )
                page.snack_bar.open = True
                page.update()
        except Exception as e:
            print(e)
            print("Erro")

    def verificar_credenciais(usuario, senha):
        try:
            sql = f"SELECT usuario, senha FROM usuarios WHERE usuario = '{controls.usuario.value}' AND senha = '{controls.senha.value}'"
            cursor.execute(sql)
            resultado = cursor.fetchone()

            if resultado is not None:
                page.go('/menu')
                return True
            else:
                print("Credenciais inválidas.")
                return False
        except Exception as e:
            print(e)
            print("Erro na verificação das credenciais.")
            return False

    

    def route_change(e: RouteChangeEvent):
        page.views.clear()

        #Views        
        page.views.append(
            View(
                route='/',
                controls=[
                    AppBar(title=Text("Página Inicial"), bgcolor='green'),
                    Text(value='Dinheiro Contado', size=20),
                    ElevatedButton(text='Fazer Login', on_click=lambda _: page.go('/login')),
                    ElevatedButton(text='Registrar Usuário', on_click=lambda _: page.go('/cadastro'))               
                ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=26
            )
        )

        #Login
        if page.route == '/login':
            page.views.append(
                View(
                    route='/login',
                    controls=[
                    AppBar(title=Text("Página Inicial"), bgcolor='green'),
                    Text(value='Login', size=30),
                    controls.usuario,
                    controls.senha,
                    ElevatedButton(text='Entrar', on_click=lambda _: verificar_credenciais(controls.usuario.value, controls.senha.value)),
                    ElevatedButton(text='Voltar', on_click=lambda _: page.go('/'))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )

            

        #Menu principal
        if page.route == '/menu':
            page.views.append(
                View(
                    route='/menu',
                    controls=[
                    ft.page.AppBar(
                        bgcolor='green',
                        leading=ft.IconButton(ft.icons.ACCOUNT_CIRCLE_OUTLINED),
                        leading_width=40,
                        center_title=False,
                        actions=[
                            ft.IconButton(ft.icons.EDIT_NOTE, on_click=lambda _: page.go('/registro')),
                            ft.IconButton(ft.icons.AUTO_GRAPH_ROUNDED, on_click=lambda _: page.go('/viz')),
                            ft.IconButton(ft.icons.CREDIT_CARD, on_click=lambda _: page.go('/cartao')),
                            ft.IconButton(ft.icons.SETTINGS_OUTLINED, on_click=lambda _: page.go('/config')),
                            ft.IconButton(ft.icons.EXIT_TO_APP_OUTLINED, on_click=lambda _: page.go('/'))            
                            
                        ],
                    )
                ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )
        
        #Cadastro usuário
        if page.route == '/cadastro':
            page.views.append(
                View(
                    route='/login',
                    controls=[
                    AppBar(title=Text("Página Inicial"), bgcolor='green'),
                    Text(value='Login', size=30),
                    controls.usuario,
                    controls.senha,
                    controls.conf_senha,                    
                    ft.ElevatedButton("Enviar", on_click=cadastrar)
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )

            #Menu principal
        if page.route == '/registro':
            page.views.append(
                View(
                    route='/menu',
                    controls=[
                    ft.page.AppBar(
                        bgcolor='green',
                        leading=ft.IconButton(ft.icons.ACCOUNT_CIRCLE_OUTLINED),
                        leading_width=40,
                        center_title=False,
                        actions=[
                            ft.IconButton(ft.icons.EDIT_NOTE, on_click=lambda _: page.go('/registro')),
                            ft.IconButton(ft.icons.AUTO_GRAPH_ROUNDED, on_click=lambda _: page.go('/viz')),
                            ft.IconButton(ft.icons.CREDIT_CARD, on_click=lambda _: page.go('/cartao')),
                            ft.IconButton(ft.icons.SETTINGS_OUTLINED, on_click=lambda _: page.go('/config')),
                            ft.IconButton(ft.icons.EXIT_TO_APP_OUTLINED, on_click=lambda _: page.go('/'))            
                        ],
                    ),
                    controls.produto,
                    controls.valor_un, 
                    controls.categoria,
                    ft.ElevatedButton("Enviar", on_click=enviar)
                    
                ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )

        page.update()

        if page.route == '/':
            page.views.append(
                View(
                    route='/viz',
                    controls=[
                    ft.page.AppBar(
                        bgcolor='green',
                        leading=ft.IconButton(ft.icons.ACCOUNT_CIRCLE_OUTLINED),
                        leading_width=40,
                        center_title=False,
                        actions=[
                            ft.IconButton(ft.icons.EDIT_NOTE, on_click=lambda _: page.go('/registro')),
                            ft.IconButton(ft.icons.AUTO_GRAPH_ROUNDED, on_click=lambda _: page.go('/viz')),
                            ft.IconButton(ft.icons.CREDIT_CARD, on_click=lambda _: page.go('/cartao')),
                            ft.IconButton(ft.icons.SETTINGS_OUTLINED, on_click=lambda _: page.go('/config')),
                            ft.IconButton(ft.icons.EXIT_TO_APP_OUTLINED, on_click=lambda _: page.go('/'))             
                        ],
                    ),
                     mydt


                    
                ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )

        page.update()

    
    def view_pop(e: ViewPopEvent):
        page.views.pop()
        top_View: View = page.views[-1]
        page.go(top_View.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == '__main__':
    ft.app(target=main)