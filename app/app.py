import reflex as rx
from app.state import RegistrationState, form_field
from app.login import login
from app.dashboard import dashboard
from app.profile import profile_page
from app.apartments import apartments_page
from app.citizen_registration import citizen_registration_page
from app.match_results import match_results_page
from app.components.navbar import navbar


def registration_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Create an Account",
            class_name="text-2xl font-bold text-gray-900 text-center",
        ),
        rx.el.p(
            "Join us and start your journey.",
            class_name="text-center text-gray-500 mt-2 mb-8",
        ),
        rx.el.form(
            rx.el.div(
                form_field(
                    "Email",
                    "email",
                    "you@example.com",
                    "email",
                    RegistrationState.set_email,
                    RegistrationState.email_error,
                ),
                form_field(
                    "Password",
                    "password",
                    "••••••••",
                    "password",
                    RegistrationState.set_password,
                    RegistrationState.password_error,
                ),
                form_field(
                    "Confirm Password",
                    "confirm_password",
                    "••••••••",
                    "password",
                    RegistrationState.set_confirm_password,
                    RegistrationState.confirm_password_error,
                ),
                form_field(
                    "Mobile Number (Optional)",
                    "mobile_number",
                    "+1234567890",
                    "tel",
                    RegistrationState.set_mobile_number,
                    RegistrationState.mobile_number_error,
                ),
                rx.el.button(
                    rx.cond(
                        RegistrationState.is_loading,
                        rx.el.div(
                            rx.spinner(class_name="w-5 h-5"),
                            class_name="flex justify-center",
                        ),
                        "Create Account",
                    ),
                    type="submit",
                    disabled=RegistrationState.is_loading,
                    class_name="w-full py-3 mt-4 text-white font-semibold bg-orange-500 rounded-lg shadow-md hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-opacity-75 transition-all duration-200 disabled:bg-orange-300",
                ),
                class_name="flex flex-col items-start gap-5",
            ),
            on_submit=RegistrationState.handle_registration,
            reset_on_submit=False,
            class_name="w-full",
        ),
        class_name="w-full max-w-md",
    )


def success_message() -> rx.Component:
    return rx.el.div(
        rx.icon("square_check", class_name="w-16 h-16 text-green-500 mx-auto"),
        rx.el.h2(
            "Registration Successful!",
            class_name="text-2xl font-bold text-gray-900 text-center mt-4",
        ),
        rx.el.p(
            "Welcome aboard! You can now explore all the features.",
            class_name="text-center text-gray-500 mt-2",
        ),
        rx.el.p(
            rx.el.a(
                "Go to Dashboard",
                href="#",
                class_name="text-orange-500 hover:underline",
            ),
            class_name="text-center mt-6 text-sm",
        ),
        class_name="w-full max-w-md p-8",
    )


def index() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        RegistrationState.is_successful,
                        success_message(),
                        registration_form(),
                    ),
                    class_name="w-full max-w-md p-8 bg-white rounded-xl shadow-lg border border-gray-200",
                ),
                rx.el.p(
                    "Already have an account? ",
                    rx.el.a(
                        "Log in",
                        href="/login",
                        class_name="font-semibold text-orange-500 hover:text-orange-600",
                    ),
                    class_name="text-center text-sm text-gray-500 mt-6",
                ),
                class_name="relative flex flex-col items-center justify-center min-h-screen",
            ),
            class_name="w-full bg-gray-50 font-['Lora'] pt-16",
        ),
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)
app.add_page(login, route="/login")
app.add_page(dashboard, route="/dashboard")
app.add_page(profile_page, route="/profile")
app.add_page(apartments_page, route="/apartments")
app.add_page(citizen_registration_page, route="/exchange-request")
app.add_page(match_results_page, route="/match-results")