import reflex as rx
from typing import Optional
import re


class LoginState(rx.State):
    email: str = ""
    password: str = ""
    email_error: Optional[str] = None
    password_error: Optional[str] = None
    is_loading: bool = False

    def _validate_email(self) -> None:
        self.email_error = None
        if not self.email:
            self.email_error = "Email cannot be empty."
        elif not re.match("[^@]+@[^@]+\\.[^@]+", self.email):
            self.email_error = "Invalid email format."

    def _validate_password(self) -> None:
        self.password_error = None
        if not self.password:
            self.password_error = "Password cannot be empty."

    @rx.event
    async def handle_login(self, form_data: dict):
        self.is_loading = True
        self.email = form_data.get("email", "").strip()
        self.password = form_data.get("password", "")
        self._validate_email()
        self._validate_password()
        if self.email_error or self.password_error:
            self.is_loading = False
            return
        import asyncio

        await asyncio.sleep(1.5)
        self.is_loading = False
        yield rx.redirect("/dashboard")


def error_message(message: rx.Var[str]) -> rx.Component:
    return rx.el.div(
        rx.cond(
            message,
            rx.el.span(
                rx.icon(tag="badge_alert", class_name="w-4 h-4 mr-1"),
                message,
                class_name="flex items-center text-sm text-red-500 mt-2",
            ),
            None,
        )
    )


def login_form_field(
    label: str,
    name: str,
    placeholder: str,
    field_type: str,
    on_change_fn,
    error_var: rx.Var[str],
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700"),
        rx.el.input(
            name=name,
            placeholder=placeholder,
            type=field_type,
            on_change=on_change_fn,
            class_name=rx.cond(
                error_var,
                "w-full px-4 py-2 mt-1 bg-white border border-red-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-shadow",
                "w-full px-4 py-2 mt-1 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-shadow",
            ),
        ),
        error_message(error_var),
        class_name="w-full",
    )


def login_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Welcome Back", class_name="text-2xl font-bold text-gray-900 text-center"
        ),
        rx.el.p(
            "Log in to continue your journey.",
            class_name="text-center text-gray-500 mt-2 mb-8",
        ),
        rx.el.form(
            rx.el.div(
                login_form_field(
                    "Email",
                    "email",
                    "you@example.com",
                    "email",
                    LoginState.set_email,
                    LoginState.email_error,
                ),
                login_form_field(
                    "Password",
                    "password",
                    "••••••••",
                    "password",
                    LoginState.set_password,
                    LoginState.password_error,
                ),
                rx.el.button(
                    rx.cond(
                        LoginState.is_loading,
                        rx.el.div(
                            rx.spinner(class_name="w-5 h-5"),
                            class_name="flex justify-center",
                        ),
                        "Log In",
                    ),
                    type="submit",
                    disabled=LoginState.is_loading,
                    class_name="w-full py-3 mt-4 text-white font-semibold bg-orange-500 rounded-lg shadow-md hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-opacity-75 transition-all duration-200 disabled:bg-orange-300",
                ),
                class_name="flex flex-col items-start gap-5",
            ),
            on_submit=LoginState.handle_login,
            reset_on_submit=False,
            class_name="w-full",
        ),
        class_name="w-full max-w-md",
    )


def login() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("code", class_name="h-8 w-8 text-orange-500"),
                    href="/",
                    class_name="absolute top-8 left-8",
                ),
                rx.el.div(
                    login_form(),
                    class_name="w-full max-w-md p-8 bg-white rounded-xl shadow-lg border border-gray-200",
                ),
                rx.el.p(
                    "Don't have an account? ",
                    rx.el.a(
                        "Sign up",
                        href="/",
                        class_name="font-semibold text-orange-500 hover:text-orange-600",
                    ),
                    class_name="text-center text-sm text-gray-500 mt-6",
                ),
                class_name="relative flex flex-col items-center justify-center min-h-screen",
            ),
            class_name="w-full bg-gray-50 font-['Lora']",
        ),
        class_name="font-['Lora']",
    )