import flet as ft
import sqlite3


def main(page: ft.Page):
    page.title = "Flet App sqlite3"
    page.theme_mode = "dark"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_height = 500
    page.window_width = 400
    page.window_resizable = False

    def register(e):
        db = sqlite3.connect('data.db')

        cur = db.cursor()
        # cur.execute('DROP TABLE IF EXISTS users')
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            login TEXT NOT NULL,
            pass TEXT NOT NULL)
            ''')
        cur.execute(f"INSERT INTO users VALUES (NULL, '{user_login.value}', '{user_pass.value}')")
        db.commit()
        db.close()

        user_login.value = ''
        user_pass.value = ''
        btn_reg.text = 'Added'
        page.update()

    def validate(e):
        if all([user_login.value, user_pass.value]):
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True

        page.update()

    def auth_user(e):
        db = sqlite3.connect('data.db')

        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE login = '{user_login.value}' AND pass = '{user_pass.value}'")
        if cur.fetchone() != None:
            user_login.value = ''
            user_pass.value = ''
            btn_auth.text = 'Authorized'

            if len(page.navigation_bar.destinations) == 2:
                page.navigation_bar.destinations.append(
                    ft.NavigationDestination(icon=ft.icons.PERSON, label='Personal Area',
                                             selected_icon=ft.icons.BOOKMARK))
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text('Not Authorized'))
            page.snack_bar.open = True
            page.update()

        db.commit()
        db.close()

    user_login = ft.TextField(label='Login', color='green', width=200, on_change=validate)
    user_pass = ft.TextField(label='Password', password=True, color='green', width=200, on_change=validate)
    btn_reg = ft.OutlinedButton(text='Add', on_click=register, width=200, disabled=True)
    btn_auth = ft.OutlinedButton(text='Auth', on_click=auth_user, width=200, disabled=True)

    # user Cabinet

    users_list = ft.ListView(spacing=10, padding=20)

    # user Cabinet end

    panel_reg = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Registration'),
                    user_login,
                    user_pass,
                    btn_reg
                ]
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    panel_auth = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Authorization'),
                    user_login,
                    user_pass,
                    btn_auth
                ]
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    panel_cabinet = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Personal Area'),
                    users_list

                ]
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    def navigate(e):
        page.clean()
        if page.navigation_bar.selected_index == 0:
            page.add(panel_reg)
        elif page.navigation_bar.selected_index == 1:
            page.add(panel_auth)
        elif page.navigation_bar.selected_index == 2:
            users_list.controls.clear()

            db = sqlite3.connect('data.db')

            cur = db.cursor()
            cur.execute(f"SELECT * FROM users")
            res = cur.fetchall()
            if res != None:
                for user in res:
                    users_list.controls.append(ft.Row([
                        ft.Text(user[1]),
                        ft.Icon(ft.icons.VERIFIED_USER_OUTLINED)
                    ]))
            db.commit()
            db.close()
            page.add(panel_cabinet)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label='Registration'),
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER_OUTLINED, label='Authorization')
        ], on_change=navigate
    )

    page.add(panel_reg)


ft.app(target=main)
