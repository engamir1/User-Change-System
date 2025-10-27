import reflex as rx
from app.states.apartment_state import ApartmentState
from app.components.navbar import navbar


def apartment_form_field(
    label: str,
    name: str,
    placeholder: str,
    on_change_fn,
    error_var: rx.Var[str],
    field_type: str = "text",
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
        rx.cond(
            error_var,
            rx.el.span(
                rx.icon(tag="badge_alert", class_name="w-4 h-4 mr-1"),
                error_var,
                class_name="flex items-center text-sm text-red-500 mt-2",
            ),
            None,
        ),
        class_name="w-full",
    )


def apartments_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h2(
                    "Add Apartment Information",
                    class_name="text-3xl font-bold text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Fill in the details for a new apartment listing.",
                    class_name="text-gray-500 mb-8",
                ),
                rx.el.form(
                    rx.el.div(
                        apartment_form_field(
                            "Apartment Name",
                            "name",
                            "e.g., The Grand Lux",
                            ApartmentState.set_name,
                            ApartmentState.name_error,
                        ),
                        apartment_form_field(
                            "Address",
                            "address",
                            "123 Main St, Anytown, USA",
                            ApartmentState.set_address,
                            ApartmentState.address_error,
                        ),
                        rx.el.div(
                            apartment_form_field(
                                "Bedrooms",
                                "bedrooms",
                                "e.g., 2",
                                ApartmentState.set_bedrooms,
                                ApartmentState.bedrooms_error,
                                field_type="number",
                            ),
                            apartment_form_field(
                                "Bathrooms",
                                "bathrooms",
                                "e.g., 1.5",
                                ApartmentState.set_bathrooms,
                                ApartmentState.bathrooms_error,
                                field_type="number",
                            ),
                            apartment_form_field(
                                "Monthly Rent ($)",
                                "rent",
                                "e.g., 1500",
                                ApartmentState.set_rent,
                                ApartmentState.rent_error,
                                field_type="number",
                            ),
                            class_name="grid md:grid-cols-3 gap-6",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Description",
                                class_name="text-sm font-medium text-gray-700",
                            ),
                            rx.el.textarea(
                                name="description",
                                placeholder="A brief description of the apartment...",
                                on_change=ApartmentState.set_description,
                                class_name="w-full px-4 py-2 mt-1 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-shadow",
                                rows=4,
                            ),
                            class_name="w-full",
                        ),
                        class_name="space-y-6 bg-white p-6 rounded-lg shadow-md border border-gray-200",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.cond(
                                ApartmentState.is_loading,
                                rx.el.div(
                                    rx.spinner(class_name="w-5 h-5"),
                                    class_name="flex justify-center",
                                ),
                                "Add Apartment",
                            ),
                            type="submit",
                            disabled=ApartmentState.is_loading,
                            class_name="w-full md:w-auto px-6 py-3 text-white font-semibold bg-orange-500 rounded-lg shadow-md hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-opacity-75 transition-all duration-200 disabled:bg-orange-300",
                        ),
                        class_name="flex justify-end mt-8",
                    ),
                    on_submit=ApartmentState.add_apartment,
                    reset_on_submit=False,
                    class_name="w-full",
                ),
                class_name="w-full max-w-4xl mx-auto",
            ),
            class_name="relative flex flex-col items-center justify-center min-h-screen py-12 px-4 sm:px-6 lg:px-8 pt-24",
        ),
        class_name="w-full bg-gray-50 font-['Lora']",
    )