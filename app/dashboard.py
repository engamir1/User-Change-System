import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.navbar import navbar


def dashboard() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Welcome to your Dashboard",
                        class_name="text-2xl font-bold text-gray-900 text-center",
                    ),
                    rx.el.p(
                        "This is a simple dashboard page.",
                        class_name="text-center text-gray-500 mt-2 mb-8",
                    ),
                    rx.el.a(
                        "Go to Profile",
                        href="/profile",
                        class_name="mt-4 inline-block text-orange-500 hover:underline",
                    ),
                    class_name="w-full max-w-md p-8 bg-white rounded-xl shadow-lg border border-gray-200 text-center",
                ),
                class_name="relative flex flex-col items-center justify-center min-h-screen",
            ),
            class_name="w-full bg-gray-50 font-['Lora'] pt-16",
        ),
    )