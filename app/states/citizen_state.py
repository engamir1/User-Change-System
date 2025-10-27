import reflex as rx
from typing import Optional, TypedDict, ClassVar
import re
import asyncio
import logging


class Citizen(TypedDict):
    national_id: str
    name: str
    building: str
    floor: int
    direction: str
    phone: str
    wish_floor: str
    wish_direction: str


class MatchResult(TypedDict):
    citizen: Citizen
    score: int


class CitizenState(rx.State):
    citizens: list[Citizen] = []
    current_citizen_id: str = ""
    matches: list[MatchResult] = []
    is_searching: bool = False
    search_performed: bool = False
    national_id: str = ""
    name: str = ""
    building: str = ""
    floor: str = ""
    direction: str = ""
    phone: str = ""
    wish_floor: str = ""
    wish_direction: str = ""
    is_loading: bool = False
    is_successful: bool = False
    errors: dict[str, str] = {}
    DIRECTION_OPTIONS: ClassVar[list[str]] = ["بحرى", "قبلى", "شرقى", "غربى"]
    WISH_FLOOR_OPTIONS: ClassVar[list[str]] = ["أعلى", "أسفل", "أى"]
    WISH_DIRECTION_OPTIONS: ClassVar[list[str]] = ["بحرى", "قبلى", "شرقى", "غربى", "أى"]

    @rx.var
    def name_error(self) -> str:
        return self.errors.get("name", "")

    @rx.var
    def national_id_error(self) -> str:
        return self.errors.get("national_id", "")

    @rx.var
    def building_error(self) -> str:
        return self.errors.get("building", "")

    @rx.var
    def floor_error(self) -> str:
        return self.errors.get("floor", "")

    @rx.var
    def direction_error(self) -> str:
        return self.errors.get("direction", "")

    @rx.var
    def phone_error(self) -> str:
        return self.errors.get("phone", "")

    @rx.var
    def wish_floor_error(self) -> str:
        return self.errors.get("wish_floor", "")

    @rx.var
    def wish_direction_error(self) -> str:
        return self.errors.get("wish_direction", "")

    def _validate(self):
        self.errors = {}
        if not self.name:
            self.errors["name"] = "الاسم مطلوب."
        if not self.national_id:
            self.errors["national_id"] = "الرقم القومي مطلوب."
        elif not (self.national_id.isdigit() and len(self.national_id) == 14):
            self.errors["national_id"] = "الرقم القومي يجب أن يتكون من 14 رقمًا."
        if not self.building:
            self.errors["building"] = "رقم العمارة مطلوب."
        if not self.floor:
            self.errors["floor"] = "رقم الدور مطلوب."
        else:
            try:
                int(self.floor)
            except ValueError as e:
                logging.exception(f"Error: {e}")
                self.errors["floor"] = "رقم الدور يجب أن يكون رقمًا صحيحًا."
        if not self.direction:
            self.errors["direction"] = "الاتجاه الحالي مطلوب."
        if not self.wish_floor:
            self.errors["wish_floor"] = "الرجاء تحديد الرغبة في الدور."
        if not self.wish_direction:
            self.errors["wish_direction"] = "الرجاء تحديد الرغبة في الاتجاه."
        if self.phone and (not re.match("^01[0-2,5]\\d{8}$", self.phone)):
            self.errors["phone"] = "صيغة رقم الموبايل غير صحيحة."

    @rx.event
    async def handle_submit(self, form_data: dict):
        self.is_loading = True
        self.is_successful = False
        yield
        self.name = form_data.get("name", "").strip()
        self.national_id = form_data.get("national_id", "").strip()
        self.building = form_data.get("building", "").strip()
        self.floor = form_data.get("floor", "").strip()
        self.direction = form_data.get("direction", "")
        self.phone = form_data.get("phone", "").strip()
        self.wish_floor = form_data.get("wish_floor", "")
        self.wish_direction = form_data.get("wish_direction", "")
        self._validate()
        if self.errors:
            self.is_loading = False
            yield rx.toast.error("الراجاء إصلاح الأخطاء", position="bottom-right")
            return
        await asyncio.sleep(1.5)
        new_citizen: Citizen = {
            "name": self.name,
            "national_id": self.national_id,
            "building": self.building,
            "floor": int(self.floor),
            "direction": self.direction,
            "phone": self.phone,
            "wish_floor": self.wish_floor,
            "wish_direction": self.wish_direction,
        }
        citizen_index = -1
        for i, c in enumerate(self.citizens):
            if c["national_id"] == self.national_id:
                citizen_index = i
                break
        if citizen_index != -1:
            self.citizens[citizen_index] = new_citizen
        else:
            self.citizens.append(new_citizen)
        logging.info(f"Citizen data saved: {new_citizen}")
        logging.info(f"Total citizens: {len(self.citizens)}")
        self.is_loading = False
        self.is_successful = True
        yield rx.toast.success("تم حفظ البيانات بنجاح!", position="bottom-right")

    @rx.event
    async def match_requests(self, national_id: str):
        """Smart matching algorithm that finds compatible exchange partners"""
        self.is_searching = True
        self.search_performed = True
        self.matches = []
        yield
        await asyncio.sleep(1)
        user = None
        for c in self.citizens:
            if c["national_id"] == national_id:
                user = c
                break
        if not user:
            self.is_searching = False
            yield rx.toast.error("لم يتم العثور على المواطن.")
            return
        logging.info(
            f"Searching matches for: {user['name']} (Floor {user['floor']}, wants {user['wish_floor']})"
        )
        potential_matches = []
        for other in self.citizens:
            if other["national_id"] == user["national_id"]:
                continue
            floor_ok = False
            if user["wish_floor"] == "أعلى" and other["floor"] > user["floor"]:
                floor_ok = True
            elif user["wish_floor"] == "أسفل" and other["floor"] < user["floor"]:
                floor_ok = True
            elif user["wish_floor"] == "أى":
                floor_ok = True
            direction_ok = False
            if user["wish_direction"] == "أى":
                direction_ok = True
            elif other["direction"] == user["wish_direction"]:
                direction_ok = True
            reverse_floor_ok = False
            if other["wish_floor"] == "أسفل" and user["floor"] < other["floor"]:
                reverse_floor_ok = True
            elif other["wish_floor"] == "أعلى" and user["floor"] > other["floor"]:
                reverse_floor_ok = True
            elif other["wish_floor"] == "أى":
                reverse_floor_ok = True
            reverse_direction_ok = False
            if other["wish_direction"] == "أى":
                reverse_direction_ok = True
            elif user["direction"] == other["wish_direction"]:
                reverse_direction_ok = True
            logging.info(
                f"Checking {other['name']}: floor_ok={floor_ok}, direction_ok={direction_ok}, reverse_floor_ok={reverse_floor_ok}, reverse_direction_ok={reverse_direction_ok}"
            )
            if floor_ok and direction_ok and reverse_floor_ok and reverse_direction_ok:
                score = 50
                if (
                    user["wish_direction"] == other["direction"]
                    or user["wish_direction"] == "أى"
                    or other["wish_direction"] == "أى"
                ):
                    score += 30
                floor_diff = abs(other["floor"] - user["floor"])
                if floor_diff <= 2:
                    score += 20 - floor_diff * 10
                potential_matches.append(
                    {"citizen": other, "score": min(100, int(score))}
                )
                logging.info(f"✓ Match found: {other['name']} with score {score}%")
        potential_matches.sort(key=lambda x: x["score"], reverse=True)
        self.matches = potential_matches
        self.is_searching = False
        logging.info(f"Found {len(potential_matches)} total matches")
        yield