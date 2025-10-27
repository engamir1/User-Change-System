import reflex as rx
from app.login import LoginState


class NavbarState(rx.State):
    is_logged_in: bool = False

    @rx.event
    async def check_login_status(self):
        login_state = await self.get_state(LoginState)
        self.is_logged_in = login_state.email != ""

    @rx.event
    async def logout(self):
        login_state = await self.get_state(LoginState)
        login_state.email = ""
        login_state.password = ""
        login_state.is_loading = False
        self.is_logged_in = False
        return rx.redirect("/")