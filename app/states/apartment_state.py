import reflex as rx
from typing import Optional, TypedDict
import asyncio
import logging


class ApartmentError(TypedDict):
    field: str
    message: str


class ApartmentState(rx.State):
    name: str = ""
    address: str = ""
    bedrooms: str = ""
    bathrooms: str = ""
    rent: str = ""
    description: str = ""
    is_loading: bool = False
    errors: list[ApartmentError] = []

    @rx.event
    def get_error(self, field: str) -> Optional[str]:
        for error in self.errors:
            if error["field"] == field:
                return error["message"]
        return None

    @rx.var
    def name_error(self) -> Optional[str]:
        return self.get_error("name")

    @rx.var
    def address_error(self) -> Optional[str]:
        return self.get_error("address")

    @rx.var
    def bedrooms_error(self) -> Optional[str]:
        return self.get_error("bedrooms")

    @rx.var
    def bathrooms_error(self) -> Optional[str]:
        return self.get_error("bathrooms")

    @rx.var
    def rent_error(self) -> Optional[str]:
        return self.get_error("rent")

    def _validate_fields(self):
        self.errors = []
        if not self.name:
            self.errors.append({"field": "name", "message": "Name is required."})
        if not self.address:
            self.errors.append({"field": "address", "message": "Address is required."})
        try:
            if self.bedrooms and int(self.bedrooms) <= 0:
                self.errors.append(
                    {"field": "bedrooms", "message": "Must be a positive number."}
                )
        except ValueError as e:
            logging.exception(f"Error: {e}")
            self.errors.append({"field": "bedrooms", "message": "Must be a number."})
        try:
            if self.bathrooms and float(self.bathrooms) <= 0:
                self.errors.append(
                    {"field": "bathrooms", "message": "Must be a positive number."}
                )
        except ValueError as e:
            logging.exception(f"Error: {e}")
            self.errors.append({"field": "bathrooms", "message": "Must be a number."})
        try:
            if self.rent and float(self.rent) <= 0:
                self.errors.append(
                    {"field": "rent", "message": "Must be a positive number."}
                )
        except ValueError as e:
            logging.exception(f"Error: {e}")
            self.errors.append({"field": "rent", "message": "Must be a number."})

    @rx.event
    async def add_apartment(self, form_data: dict):
        self.is_loading = True
        self.errors = []
        self.name = form_data.get("name", "")
        self.address = form_data.get("address", "")
        self.bedrooms = form_data.get("bedrooms", "")
        self.bathrooms = form_data.get("bathrooms", "")
        self.rent = form_data.get("rent", "")
        self.description = form_data.get("description", "")
        yield
        self._validate_fields()
        if self.errors:
            self.is_loading = False
            yield rx.toast.error("Please fix the errors.")
            return
        await asyncio.sleep(1.5)
        self.is_loading = False
        yield rx.toast.success("Apartment added successfully!")