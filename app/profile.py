import reflex as rx
from app.states.profile_state import ProfileState


def profile_input(
    label: str,
    name: str,
    value: rx.Var[str],
    on_change_fn,
    error_var: rx.Var[str],
    input_type: str = "text",
    placeholder: str = "",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700"),
        rx.el.input(
            name=name,
            default_value=value,
            type=input_type,
            on_change=on_change_fn,
            placeholder=placeholder,
            class_name=rx.cond(
                error_var,
                "mt-1 block w-full px-3 py-2 bg-white border border-red-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm",
                "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-500 focus:border-orange-500 sm:text-sm",
            ),
        ),
        rx.cond(
            error_var, rx.el.p(error_var, class_name="mt-2 text-sm text-red-600"), None
        ),
        class_name="w-full",
    )


def profile_section(title: str, *children) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-semibold text-gray-900 mb-4"),
        rx.el.div(*children, class_name="grid grid-cols-1 md:grid-cols-2 gap-6"),
        class_name="bg-white p-6 rounded-lg shadow-md border border-gray-200",
    )


from app.components.navbar import navbar


def profile_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "My Profile", class_name="text-3xl font-bold text-gray-900 mb-2"
                ),
                rx.el.p(
                    "Manage your personal information and settings.",
                    class_name="text-gray-500 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.image(
                            src=rx.cond(
                                ProfileState.avatar_url,
                                ProfileState.avatar_url,
                                "/placeholder.svg",
                            ),
                            class_name="h-24 w-24 rounded-full object-cover border-4 border-white shadow-sm",
                        ),
                        rx.el.button(
                            "Change Picture",
                            class_name="ml-4 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50",
                        ),
                        class_name="flex items-center mb-8",
                    ),
                    rx.el.div(
                        profile_section(
                            "Personal Information",
                            profile_input(
                                "Full Name",
                                "full_name",
                                ProfileState.full_name,
                                ProfileState.set_full_name,
                                ProfileState.full_name_error,
                                placeholder="Your full name",
                            ),
                            profile_input(
                                "Date of Birth",
                                "date_of_birth",
                                ProfileState.date_of_birth,
                                ProfileState.set_date_of_birth,
                                None,
                                input_type="date",
                            ),
                        ),
                        profile_section(
                            "Contact Details",
                            profile_input(
                                "Email Address",
                                "email",
                                ProfileState.email,
                                ProfileState.set_email,
                                ProfileState.email_error,
                                input_type="email",
                                placeholder="you@example.com",
                            ),
                            profile_input(
                                "Mobile Number",
                                "mobile_number",
                                ProfileState.mobile_number,
                                ProfileState.set_mobile_number,
                                ProfileState.mobile_number_error,
                                input_type="tel",
                                placeholder="+1234567890",
                            ),
                        ),
                        profile_section(
                            "Address",
                            profile_input(
                                "Street Address",
                                "address",
                                ProfileState.address,
                                ProfileState.set_address,
                                None,
                                placeholder="123 Main St",
                            ),
                            profile_input(
                                "City",
                                "city",
                                ProfileState.city,
                                ProfileState.set_city,
                                None,
                                placeholder="Anytown",
                            ),
                            profile_input(
                                "State / Province",
                                "state_province",
                                ProfileState.state_province,
                                ProfileState.set_state_province,
                                None,
                                placeholder="CA",
                            ),
                            profile_input(
                                "Postal Code",
                                "postal_code",
                                ProfileState.postal_code,
                                ProfileState.set_postal_code,
                                None,
                                placeholder="12345",
                            ),
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "About Me",
                                class_name="text-lg font-semibold text-gray-900 mb-4",
                            ),
                            rx.el.textarea(
                                default_value=ProfileState.bio,
                                on_change=ProfileState.set_bio,
                                placeholder="Tell us a little about yourself...",
                                class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-500 focus:border-orange-500 sm:text-sm",
                                rows=4,
                            ),
                            class_name="bg-white p-6 rounded-lg shadow-md border border-gray-200",
                        ),
                        class_name="space-y-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.cond(
                                ProfileState.is_loading,
                                rx.el.div(
                                    rx.spinner(class_name="w-5 h-5"),
                                    class_name="flex justify-center",
                                ),
                                "Save Changes",
                            ),
                            on_click=ProfileState.save_profile,
                            disabled=ProfileState.is_loading,
                            class_name="w-full md:w-auto px-6 py-3 text-white font-semibold bg-orange-500 rounded-lg shadow-md hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-opacity-75 transition-all duration-200 disabled:bg-orange-300",
                        ),
                        class_name="flex justify-end mt-8",
                    ),
                ),
                class_name="w-full max-w-4xl mx-auto",
            ),
            class_name="relative flex flex-col items-center justify-center min-h-screen py-12 px-4 sm:px-6 lg:px-8 pt-24",
        ),
        class_name="w-full bg-gray-50 font-['Lora']",
        on_mount=ProfileState.load_profile,
    )