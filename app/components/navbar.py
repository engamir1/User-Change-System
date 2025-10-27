import reflex as rx
from app.states.navbar_state import NavbarState


def nav_link(text: str, href: str) -> rx.Component:
    return rx.el.a(
        text,
        href=href,
        class_name="text-sm font-medium text-gray-500 hover:text-gray-900",
    )


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.a(rx.icon("code", class_name="h-8 w-8 text-orange-500"), href="/"),
            rx.el.div(
                rx.cond(
                    NavbarState.is_logged_in,
                    rx.el.div(
                        nav_link("Dashboard", "/dashboard"),
                        nav_link("Profile", "/profile"),
                        nav_link("Apartments", "/apartments"),
                        nav_link("طلب تبديل", "/exchange-request"),
                        nav_link("نتائج المطابقة", "/match-results"),
                        rx.el.button(
                            "Logout",
                            on_click=NavbarState.logout,
                            class_name="ml-4 px-4 py-2 text-sm font-medium text-white bg-orange-500 rounded-md shadow-sm hover:bg-orange-600",
                        ),
                        class_name="flex items-center space-x-4",
                    ),
                    rx.el.div(
                        nav_link("Login", "/login"),
                        rx.el.a(
                            "Sign Up",
                            href="/",
                            class_name="ml-4 px-4 py-2 text-sm font-medium text-white bg-orange-500 rounded-md shadow-sm hover:bg-orange-600",
                        ),
                        class_name="flex items-center",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between w-full max-w-7xl mx-auto",
        ),
        class_name="w-full h-16 flex items-center px-4 sm:px-6 lg:px-8 bg-white border-b border-gray-200 fixed top-0 left-0 right-0 z-50 font-['Lora']",
        on_mount=NavbarState.check_login_status,
    )