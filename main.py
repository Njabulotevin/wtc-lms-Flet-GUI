import flet as ft
import subprocess
from flet import ControlEvent


def main(page: ft.Page):
    pending = False
    result = run_command("wtc-lms modules", pending=pending)
    topics = run_command("wtc-lms topics giant-green-cycle", pending=pending)
    page.title = "WTC LMS-GUI"
    welcome_text = ft.Text(value="Welcome To LMS GUI", size=63)
    topic_title = ft.Text(value="Topics")
    lms_buttons = []
    modules_text_list = []
    topics_text_list = [topic_title]


    sub_list = ""
    render_topics = ft.Column(controls=topics_text_list)


    title = ft.Container(
        ft.Row([ft.TextButton(text=f"Modules")]),
        margin=ft.margin.only(bottom=30)
    )
    title.content.controls[0]

    def handle_change_topics(e):
        global active_list
        global sub_list

        print(e.control.key)
        command = e.control.key
        data = e.control.data

        if "topics" in command:
            status = extract_word(data[0], "[", "]")
            clean_title = data[0].replace(extract_word(data[0], "(", ")"), "").replace(status, "")
            title.content.controls = [ft.TextButton(text=f"Modules /", on_click=handle_back), ft.TextButton(text=clean_title)]
        else: 
            title.content.controls = [ft.TextButton(text=f"Modules")]

        active_list = "topics" if "topics" in command else "modules"
        main_render.controls = [
            module_card(module=i[0], command=i[1], handle_click=handle_change_topics)
            for i in clean_results(run_command(data[1], pending),  active_list)
        ]
        page.update()

    for i in clean_results(topics, "topics"):
        topics_text_list.append(ft.TextButton(text=i[0]))
    print("ended")
    pending_page = ft.Row(
        [ft.Text(value="Loading....")],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )


    def handle_back(e):
        new_list = [
            module_card(module=i[0], command=i[1], handle_click=handle_change_topics)
            for i in clean_results(result, "modules")
        ]
        main_render.controls = new_list
        page.update()

    page.padding = 0
    page.scroll = ft.ScrollMode.ADAPTIVE

    main_render = ft.Column(
        [
            module_card(module=i[0], command=i[1], handle_click=handle_change_topics)
            for i in clean_results(result, "modules")
        ],
        spacing=30,
    )

    page.add(
        #    pending_page if pending else actual_page
        ft.Row(
            [
                side_bar(page, title),
                ft.Container(
                    ft.Column(
                        [
                            ft.Container(profile(), margin=ft.margin.only(bottom=80)),
                            title,
                            main_render,
                        ]
                    )
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )


def profile():
    return ft.Column(
        [ft.Text(value="nmkhwanazi023"), ft.Text(value="Student")], spacing=0
    )


def side_bar(page: ft.Page, title: ft.Text):
    logo = ft.Container(
        ft.Image(
            src=f"logo.png",
            width=50,
            height=50,
            fit=ft.ImageFit.CONTAIN,
        ),
        margin=ft.margin.only(bottom=60),
    )
    active = "Modules"
    lms_links = ["Modules", "Reviews", "Tests"]

    def button_color(item):
        return ft.colors.GREY_800 if item == active else None

    def handle_button(e):
        global active
        active = e.control.key
        title.value = e.control.key
        page.update()

    links = ft.Column(
        [
            ft.TextButton(
                text=i,
                icon="settings",
                style=ft.ButtonStyle(
                    bgcolor=button_color(i),
                    color=ft.colors.GREY_50,
                    shape=ft.RoundedRectangleBorder(radius=5),
                ),
                key=i,
                on_click=handle_button,
            )
            for i in lms_links
        ],
        spacing=30,
    )
    return ft.Container(
        ft.Column([logo, links]),
        padding=ft.padding.symmetric(horizontal=20),
        border=ft.border.only(right=ft.border.BorderSide(1, ft.colors.GREY_700)),
        height=600,
    )


def run_command(command, pending):
    pending = True
    results = subprocess.run([command], shell=True, capture_output=True, text=True)
    pending = False
    return results


def clean_results(results, command):
    output = list(results.stdout.split("\n"))[5 if command == "topics" else 3 : -3]
    new_list = []
    clean_list = []
    for i in output:
        if (
            i == ""
            or i
            == f'•You can do the following to view {"problems" if command == "topics" else "topics"}:'
        ):
            pass
        else:
            new_list.append(i)
    for i in range(0, len(new_list) - 1, 2):
        clean_list.append([new_list[i], new_list[i + 1]])
    return clean_list


def module_card(module: str, command: str, handle_click):
    status = extract_word(module, "[", "]")
    clean_module = module.replace(extract_word(module, "(", ")"), " ").replace(
        status, " "
    )
    return ft.Container(
        ft.Row(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Container(
                                    ft.Text(value=clean_module),
                                    margin=ft.margin.only(bottom=10),
                                ),
                                ft.Text(value="Command: ", size=12),
                                ft.Text(value=command),
                            ],
                            spacing=0,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(
                    ft.Text(value=status, size=12),
                    bgcolor=ft.colors.BLUE_500
                    if status == "[In Progress]"
                    else ft.colors.RED_600,
                    padding=ft.padding.all(6),
                    border_radius=30,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        width=600,
        bgcolor=ft.colors.GREY_800,
        padding=ft.padding.all(26),
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=5,
            color=ft.colors.GREY_600,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
        key=command,
        data=[module, command],
        on_click=handle_click,
    )


def extract_word(text, start_letter, end_letter):
    start, end = text.index(start_letter), text.find(end_letter) + 1
    return text[start:end]


ft.app(target=main)
