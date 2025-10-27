import reflex as rx
from app.states.citizen_state import CitizenState, MatchResult
from app.components.navbar import navbar


def citizen_selector() -> rx.Component:
    return rx.el.div(
        rx.el.select(
            rx.el.option("اختر مواطن لبدء البحث", value="", disabled=True),
            rx.foreach(
                CitizenState.citizens,
                lambda citizen: rx.el.option(
                    f"{citizen['name']} ({citizen['national_id']})",
                    value=citizen["national_id"],
                ),
            ),
            on_change=CitizenState.set_current_citizen_id,
            class_name="w-full md:w-1/2 p-3 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500",
            default_value="",
        ),
        rx.el.button(
            rx.cond(
                CitizenState.is_searching,
                rx.el.div(
                    rx.spinner(class_name="w-5 h-5 mr-2"),
                    "جاري البحث...",
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.icon(tag="search", class_name="w-5 h-5 mr-2"),
                    "ابحث عن شريك تبديل",
                    class_name="flex items-center",
                ),
            ),
            on_click=lambda: CitizenState.match_requests(
                CitizenState.current_citizen_id
            ),
            disabled=CitizenState.is_searching
            | (CitizenState.current_citizen_id == ""),
            class_name="px-6 py-3 text-white font-semibold bg-orange-500 rounded-lg shadow-md hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-400 disabled:bg-orange-300 disabled:cursor-not-allowed transition-all",
        ),
        class_name="flex flex-col md:flex-row items-center gap-4 w-full",
    )


def match_card(result: MatchResult) -> rx.Component:
    citizen = result["citizen"]
    score = result["score"]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={citizen['name']}",
                    class_name="w-16 h-16 rounded-full border-2 border-white",
                ),
                rx.el.div(
                    rx.el.h3(
                        citizen["name"], class_name="text-lg font-bold text-gray-800"
                    ),
                    rx.el.p(
                        f"عمارة: {citizen['building']}, دور: {citizen['floor']}, اتجاه: {citizen['direction']}",
                        class_name="text-sm text-gray-600",
                    ),
                    rx.el.p(
                        f"رغبة الدور: {citizen['wish_floor']}, رغبة الاتجاه: {citizen['wish_direction']}",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                ),
                class_name="flex items-center gap-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        f"{score}%",
                        class_name="text-xl font-bold",
                        style={
                            "color": rx.cond(
                                score > 80,
                                "#10B981",
                                rx.cond(score > 60, "#F59E0B", "#EF4444"),
                            )
                        },
                    ),
                    rx.el.span("توافق", class_name="text-xs text-gray-500"),
                    class_name="flex flex-col items-center justify-center text-center",
                ),
                class_name="flex items-center justify-center p-2 rounded-full",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(tag="phone", class_name="w-4 h-4 ml-2 text-gray-400"),
                rx.el.a(
                    citizen["phone"],
                    href=f"tel:{citizen['phone']}",
                    class_name="text-orange-600 hover:underline",
                ),
                class_name="flex items-center text-sm",
            ),
            class_name="mt-4 pt-4 border-t border-gray-200",
        ),
        class_name="bg-white p-5 rounded-xl shadow-md border border-gray-200 hover:shadow-lg hover:border-orange-300 transition-all",
    )


def results_display() -> rx.Component:
    return rx.el.div(
        rx.cond(
            CitizenState.is_searching,
            rx.el.div(
                rx.spinner(class_name="w-12 h-12 text-orange-500"),
                rx.el.p(
                    "...جاري البحث عن أفضل التطابقات", class_name="mt-4 text-gray-600"
                ),
                class_name="flex flex-col items-center justify-center p-12 text-center",
            ),
            rx.cond(
                CitizenState.search_performed,
                rx.cond(
                    CitizenState.matches.length() > 0,
                    rx.el.div(
                        rx.foreach(CitizenState.matches, match_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                    rx.el.div(
                        rx.icon(
                            tag="file_search", class_name="w-16 h-16 text-gray-400"
                        ),
                        rx.el.p(
                            "لم يتم العثور على تطابقات.",
                            class_name="mt-4 text-lg font-semibold text-gray-700",
                        ),
                        rx.el.p(
                            "جرب تعديل رغباتك أو تحقق مرة أخرى لاحقًا.",
                            class_name="text-gray-500",
                        ),
                        class_name="text-center p-12 bg-gray-50 rounded-lg",
                    ),
                ),
                rx.el.div(
                    rx.icon(tag="users", class_name="w-16 h-16 text-gray-400"),
                    rx.el.p(
                        "اختر مواطن واضغط على زر البحث للعثور على تطابق.",
                        class_name="mt-4 text-lg font-semibold text-gray-700",
                    ),
                    class_name="text-center p-12 bg-gray-50 rounded-lg",
                ),
            ),
        ),
        class_name="w-full mt-8",
    )


def match_results_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h2(
                    "البحث عن تبادل سكني",
                    class_name="text-3xl font-bold text-gray-900 mb-2 text-right",
                ),
                rx.el.p(
                    "اختر مواطنًا من القائمة للعثور على أفضل شركاء التبادل المحتملين بناءً على رغباتهم.",
                    class_name="text-gray-500 mb-8 text-right",
                ),
                rx.el.div(
                    citizen_selector(),
                    results_display(),
                    class_name="w-full max-w-6xl p-8 bg-white rounded-xl shadow-lg border border-gray-200",
                ),
                class_name="relative flex flex-col items-center min-h-screen py-12 px-4 sm:px-6 lg:px-8 pt-24",
            ),
            class_name="w-full bg-gray-50 font-['Lora']",
        ),
        dir="rtl",
        class_name="font-['Lora']",
    )