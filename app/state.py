import reflex as rx
import re
from typing import TypedDict, Optional


class FieldError(TypedDict):
    field: str
    message: str


class RegistrationState(rx.State):
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    mobile_number: str = ""
    errors: list[FieldError] = []
    is_loading: bool = False
    is_successful: bool = False

    @rx.var
    def email_error(self) -> Optional[str]:
        for error in self.errors:
            if error["field"] == "email":
                return error["message"]
        return None

    @rx.var
    def password_error(self) -> Optional[str]:
        for error in self.errors:
            if error["field"] == "password":
                return error["message"]
        return None

    @rx.var
    def confirm_password_error(self) -> Optional[str]:
        for error in self.errors:
            if error["field"] == "confirm_password":
                return error["message"]
        return None

    @rx.var
    def mobile_number_error(self) -> Optional[str]:
        for error in self.errors:
            if error["field"] == "mobile_number":
                return error["message"]
        return None

    def _validate_email(self) -> None:
        if not self.email:
            self.errors.append({"field": "email", "message": "Email cannot be empty."})
        elif not re.match("[^@]+@[^@]+\\.[^@]+", self.email):
            self.errors.append({"field": "email", "message": "Invalid email format."})

    def _validate_password(self) -> None:
        if not self.password:
            self.errors.append(
                {"field": "password", "message": "Password cannot be empty."}
            )
        elif len(self.password) < 8:
            self.errors.append(
                {
                    "field": "password",
                    "message": "Password must be at least 8 characters.",
                }
            )
        elif not re.search("[A-Z]", self.password):
            self.errors.append(
                {"field": "password", "message": "Password needs an uppercase letter."}
            )
        elif not re.search("[a-z]", self.password):
            self.errors.append(
                {"field": "password", "message": "Password needs a lowercase letter."}
            )
        elif not re.search("\\d", self.password):
            self.errors.append(
                {"field": "password", "message": "Password needs a number."}
            )

    def _validate_confirm_password(self) -> None:
        if self.password != self.confirm_password:
            self.errors.append(
                {"field": "confirm_password", "message": "Passwords do not match."}
            )

    def _validate_mobile_number(self) -> None:
        if self.mobile_number and (
            not re.match("^\\+?1?\\d{9,15}$", self.mobile_number)
        ):
            self.errors.append(
                {"field": "mobile_number", "message": "Invalid phone number format."}
            )

    @rx.event
    async def handle_registration(self, form_data: dict):
        self.is_loading = True
        self.is_successful = False
        self.errors = []
        self.email = form_data.get("email", "").strip()
        self.password = form_data.get("password", "")
        self.confirm_password = form_data.get("confirm_password", "")
        self.mobile_number = form_data.get("mobile_number", "").strip()
        self._validate_email()
        self._validate_password()
        self._validate_confirm_password()
        self._validate_mobile_number()
        if self.errors:
            self.is_loading = False
            return
        import asyncio

        await asyncio.sleep(1.5)
        self.is_loading = False
        self.is_successful = True
        yield rx.toast.success(
            "Registration successful! Welcome.", position="bottom-right"
        )


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


def form_field(
    label: str,
    name: str,
    placeholder: str,
    field_type: str,
    state_var: rx.Var[str],
    error_var: rx.Var[str],
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700"),
        rx.el.input(
            name=name,
            placeholder=placeholder,
            type=field_type,
            on_change=state_var,
            class_name=rx.cond(
                error_var,
                "w-full px-4 py-2 mt-1 bg-white border border-red-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-shadow",
                "w-full px-4 py-2 mt-1 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-shadow",
            ),
        ),
        error_message(error_var),
        class_name="w-full",
    )