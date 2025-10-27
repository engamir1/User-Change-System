import reflex as rx
from app.states.citizen_state import CitizenState
from app.components.navbar import navbar


def form_input_field(
    label: str,
    name: str,
    placeholder: str,
    on_change_fn,
    error_var: rx.Var[str],
    input_type: str = "text",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            htmlFor=name,
            class_name="block text-sm font-medium text-gray-700 text-right",
        ),
        rx.el.input(
            name=name,
            id=name,
            type=input_type,
            placeholder=placeholder,
            on_change=on_change_fn,
            class_name=rx.cond(
                error_var != "",
                "mt-1 block w-full px-3 py-2 bg-white border border-red-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm text-right",
                "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-500 focus:border-orange-500 sm:text-sm text-right",
            ),
        ),
        rx.cond(
            error_var != "",
            rx.el.p(error_var, class_name="mt-2 text-sm text-red-600 text-right"),
            None,
        ),
        class_name="w-full",
    )


def form_select_field(
    label: str,
    name: str,
    placeholder: str,
    options: list[str],
    on_change_fn,
    error_var: rx.Var[str],
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            htmlFor=name,
            class_name="block text-sm font-medium text-gray-700 text-right",
        ),
        rx.el.select(
            rx.el.option(placeholder, value="", disabled=True),
            rx.foreach(options, lambda option: rx.el.option(option, value=option)),
            name=name,
            id=name,
            on_change=on_change_fn,
            class_name=rx.cond(
                error_var != "",
                "mt-1 block w-full pl-3 pr-10 py-2 text-base border-red-300 focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm rounded-md text-right",
                "mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-orange-500 focus:border-orange-500 sm:text-sm rounded-md text-right",
            ),
            default_value="",
        ),
        rx.cond(
            error_var != "",
            rx.el.p(error_var, class_name="mt-2 text-sm text-red-600 text-right"),
            None,
        ),
        class_name="w-full",
    )


def registration_form_content() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            form_input_field(
                "الاسم",
                "name",
                "محمد علي",
                CitizenState.set_name,
                CitizenState.name_error,
            ),
            form_input_field(
                "الرقم القومي",
                "national_id",
                "14 رقم",
                CitizenState.set_national_id,
                CitizenState.national_id_error,
                input_type="number",
            ),
            form_input_field(
                "رقم العمارة",
                "building",
                "مثال: 12",
                CitizenState.set_building,
                CitizenState.building_error,
            ),
            form_input_field(
                "الدور الحالي",
                "floor",
                "مثال: 3",
                CitizenState.set_floor,
                CitizenState.floor_error,
                input_type="number",
            ),
            form_select_field(
                "الاتجاه الحالي",
                "direction",
                "اختر الاتجاه",
                CitizenState.DIRECTION_OPTIONS,
                CitizenState.set_direction,
                CitizenState.direction_error,
            ),
            form_input_field(
                "رقم الموبايل (اختياري)",
                "phone",
                "01xxxxxxxxx",
                CitizenState.set_phone,
                CitizenState.phone_error,
                input_type="tel",
            ),
            form_select_field(
                "الرغبة في الدور",
                "wish_floor",
                "اختر رغبتك",
                CitizenState.WISH_FLOOR_OPTIONS,
                CitizenState.set_wish_floor,
                CitizenState.wish_floor_error,
            ),
            form_select_field(
                "الرغبة في الاتجاه",
                "wish_direction",
                "اختر رغبتك",
                CitizenState.WISH_DIRECTION_OPTIONS,
                CitizenState.set_wish_direction,
                CitizenState.wish_direction_error,
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
        ),
        rx.el.div(
            rx.el.button(
                rx.cond(
                    CitizenState.is_loading,
                    rx.el.div(
                        rx.spinner(class_name="w-5 h-5"),
                        class_name="flex justify-center",
                    ),
                    "حفظ الرغبة",
                ),
                type="submit",
                disabled=CitizenState.is_loading,
                class_name="w-full md:w-auto px-8 py-3 text-white font-semibold bg-orange-500 rounded-lg shadow-md hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-opacity-75 transition-all duration-200 disabled:bg-orange-300",
            ),
            class_name="flex justify-start mt-8",
        ),
        on_submit=CitizenState.handle_submit,
        reset_on_submit=False,
        class_name="w-full mt-8",
    )


def success_view() -> rx.Component:
    return rx.el.div(
        rx.icon("square_check", class_name="w-20 h-20 text-green-500 mx-auto"),
        rx.el.h2(
            "تم التسجيل بنجاح",
            class_name="mt-6 text-3xl font-bold text-gray-900 text-center",
        ),
        rx.el.p(
            "تم حفظ رغبتك في التبديل. سيتم استخدام هذه البيانات لإيجاد أفضل تطابق لك.",
            class_name="mt-2 text-center text-gray-600",
        ),
        rx.el.a(
            "تسجيل طلب آخر",
            href="/exchange-request",
            on_click=lambda: CitizenState.set_is_successful(False),
            class_name="mt-8 inline-block text-orange-500 hover:underline",
        ),
        class_name="text-center p-8",
    )


def citizen_registration_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "تسجيل رغبة تبديل",
                        class_name="text-3xl font-bold text-gray-900 mb-2 text-right",
                    ),
                    rx.el.p(
                        "قم بتعبئة النموذج التالي لتسجيل بيانات شقتك الحالية ورغبتك في التبديل.",
                        class_name="text-gray-500 mb-8 text-right",
                    ),
                    rx.cond(
                        CitizenState.is_successful,
                        success_view(),
                        registration_form_content(),
                    ),
                    class_name="w-full max-w-4xl p-8 bg-white rounded-xl shadow-lg border border-gray-200",
                ),
                class_name="relative flex flex-col items-center justify-center min-h-screen py-12 px-4 sm:px-6 lg:px-8 pt-24",
            ),
            class_name="w-full bg-gray-50 font-['Lora']",
        ),
        class_name="w-full bg-gray-50 font-['Lora']",
        dir="rtl",
    )