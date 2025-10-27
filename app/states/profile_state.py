import reflex as rx
from typing import Optional, TypedDict
import re
import asyncio


class ProfileError(TypedDict):
    field: str
    message: str


class ProfileState(rx.State):
    full_name: str = ""
    email: str = "user@example.com"
    mobile_number: str = ""
    date_of_birth: str = ""
    address: str = ""
    city: str = ""
    state_province: str = ""
    postal_code: str = ""
    country: str = ""
    bio: str = ""
    avatar_url: str = ""
    is_loading: bool = False
    is_saved: bool = False
    errors: list[ProfileError] = []

    @rx.event
    def get_error(self, field: str) -> Optional[str]:
        for error in self.errors:
            if error["field"] == field:
                return error["message"]
        return None

    @rx.var
    def full_name_error(self) -> Optional[str]:
        return self.get_error("full_name")

    @rx.var
    def email_error(self) -> Optional[str]:
        return self.get_error("email")

    @rx.var
    def mobile_number_error(self) -> Optional[str]:
        return self.get_error("mobile_number")

    def _validate_fields(self):
        self.errors = []
        if not self.full_name:
            self.errors.append(
                {"field": "full_name", "message": "Full name cannot be empty."}
            )
        if self.mobile_number and (
            not re.match("^\\+?1?\\d{9,15}$", self.mobile_number)
        ):
            self.errors.append(
                {"field": "mobile_number", "message": "Invalid phone number format."}
            )

    @rx.event
    async def save_profile(self):
        self.is_loading = True
        self.is_saved = False
        yield
        self._validate_fields()
        if self.errors:
            self.is_loading = False
            yield rx.toast.error("Please fix the errors before saving.")
            return
        await asyncio.sleep(1.5)
        self.is_loading = False
        self.is_saved = True
        yield rx.toast.success("Profile saved successfully!", position="bottom-right")

    @rx.event
    async def load_profile(self):
        self.is_loading = True
        yield
        await asyncio.sleep(1)
        self.full_name = "John Doe"
        self.email = "john.doe@example.com"
        self.mobile_number = "+11234567890"
        self.date_of_birth = "1990-01-01"
        self.address = "123 Main St"
        self.city = "Anytown"
        self.state_province = "CA"
        self.postal_code = "12345"
        self.country = "USA"
        self.bio = "Reflex enthusiast and developer."
        self.avatar_url = (
            f"https://api.dicebear.com/9.x/notionists/svg?seed={self.email}"
        )
        self.is_loading = False