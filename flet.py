import flet as ft


def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    def open_sub(e):
        ft.app(target=sub)

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
                ft.IconButton(ft.icons.ADD_REACTION, on_click=open_sub),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


def sub(page: ft.Page):
    page.title = "Sub window"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)
    txt_value = ft.TextField(value="Yipp", text_align=ft.TextAlign.LEFT, width=5000)

    def yippee(e):
        txt_number.value = str(int(txt_number.value) + 1)
        txt_value.value = str(txt_value.value) + "e"
        page.update()

    def pie(f):
        txt_number.value = 0
        txt_value.value = str(txt_value.value).replace("e", "")
        page.update()

    page.add(
        ft.Column(
            [
                ft.IconButton(ft.icons.ADD, on_click=yippee),
                txt_number,
                txt_value,
                ft.IconButton(ft.icons.REMOVE, on_click=pie),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


ft.app(target=main)
