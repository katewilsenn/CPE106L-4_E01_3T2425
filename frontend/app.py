import sys
import os

# Add the parent directory to sys.path so Python can find 'backend'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import flet as ft
import requests

API_BASE = "http://127.0.0.1:8000"

user_logs = {}  # username: list of actions


def main(page: ft.Page):
    page.title = "Eco-Action Tracker"
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 420

    username_field = ft.TextField(label="Username", width=300)
    password_field = ft.TextField(label="Password", password=True, width=300)
    fullname_field = ft.TextField(label="Full Name", width=300)
    feedback_text = ft.Text()

    current_user = {"username": None, "fullname": None}
    action_dropdown = ft.Dropdown(label="Select Eco-Action", width=300)
    history_column = ft.Column()

    def show_signup():
        def register(e):
            uname = username_field.value.strip()
            pwd = password_field.value.strip()
            fname = fullname_field.value.strip()

            if not uname or not pwd or not fname:
                feedback_text.value = "⚠️ All fields are required."
                page.update()
                return

            try:
                resp = requests.post(
                    f"{API_BASE}/signup",
                    json={"username": uname, "password": pwd}
                )
                if resp.status_code == 200:
                    feedback_text.value = f"✅ Registered {fname}. Please log in."
                    username_field.value = ""
                    password_field.value = ""
                    fullname_field.value = ""
                    show_login()
                else:
                    feedback_text.value = resp.json().get("detail", "❌ Signup failed.")
            except Exception as ex:
                feedback_text.value = f"⚠️ Error: {ex}"
            page.update()

        def switch_to_login(e):
            page.clean()
            show_login()

        page.clean()
        page.add(
            ft.Text("Sign Up", size=24, weight="bold"),
            fullname_field,
            username_field,
            password_field,
            ft.ElevatedButton("Sign Up", on_click=register),
            ft.TextButton("Already have an account? Log in", on_click=switch_to_login),
            feedback_text
        )

    def show_login():
        def login(e):
            uname = username_field.value.strip()
            pwd = password_field.value.strip()

            if not uname or not pwd:
                feedback_text.value = "⚠️ All fields are required."
                page.update()
                return

            try:
                resp = requests.post(
                    f"{API_BASE}/login",
                    json={"username": uname, "password": pwd}
                )
                if resp.status_code == 200:
                    current_user["username"] = uname
                    current_user["fullname"] = uname  # optional, replace with real fullname if stored
                    show_action_screen()
                else:
                    feedback_text.value = resp.json().get("detail", "❌ Invalid credentials.")
            except Exception as ex:
                feedback_text.value = f"⚠️ Error: {ex}"
            page.update()

        def switch_to_signup(e):
            page.clean()
            show_signup()

        page.clean()
        page.add(
            ft.Text("Log In", size=24, weight="bold"),
            username_field,
            password_field,
            ft.ElevatedButton("Log In", on_click=login),
            ft.TextButton("Don’t have an account? Sign up", on_click=switch_to_signup),
            feedback_text
        )

    def show_action_screen():
        history_column.controls.clear()

        def load_actions():
            action_dropdown.options.clear()
            try:
                resp = requests.get(f"{API_BASE}/actions")
                if resp.status_code == 200:
                    for action in resp.json():
                        action_dropdown.options.append(
                            ft.dropdown.Option(
                                key=str(action["id"]),
                                text=f'{action["action"]} (+{action["points"]} pts)'
                            )
                        )
                else:
                    feedback_text.value = "❌ Failed to load actions."
            except Exception as e:
                feedback_text.value = f"⚠️ Error: {e}"
            page.update()

        def log_action(e):
            action_id = action_dropdown.value
            if not action_id:
                feedback_text.value = "⚠️ Please select an action."
                page.update()
                return
            try:
                resp = requests.post(
                    f"{API_BASE}/log-action",
                    json={"user": current_user["username"], "action_id": int(action_id)}
                )
                if resp.status_code == 200:
                    message = resp.json().get("message", "Logged.")
                    feedback_text.value = message
                    selected = next(
                        (opt for opt in action_dropdown.options if opt.key == action_id),
                        None
                    )
                    if selected:
                        history_column.controls.append(ft.Text(selected.text))
                else:
                    feedback_text.value = "❌ Failed to log action."
            except Exception as ex:
                feedback_text.value = f"⚠️ Error: {ex}"
            page.update()

        def logout(e):
            current_user["username"] = None
            current_user["fullname"] = None
            feedback_text.value = ""
            show_login()

        page.clean()
        page.add(
            ft.Text(f"Welcome, {current_user['fullname']}", size=22, weight="bold"),
            ft.ElevatedButton("Logout", on_click=logout),
            ft.Text("Available Eco-Actions", size=20, weight="w600"),
            action_dropdown,
            ft.ElevatedButton("Log Action", on_click=log_action),
            feedback_text,
            ft.Text("Your Action History", size=16, weight="bold"),
            history_column
        )
        load_actions()

    show_signup()

ft.app(target=main)
