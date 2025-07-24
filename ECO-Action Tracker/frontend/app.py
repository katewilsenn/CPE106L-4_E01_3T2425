import sys
import os
import flet as ft
import requests
from datetime import datetime

# Add the parent directory to sys.path so Python can find 'backend'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    leaderboard_column = ft.Column()
    total_points_text = ft.Text("Points: 0", size=14, weight="bold", text_align=ft.TextAlign.END)

    def show_admin_login(e=None):
        def admin_login(e):
            uname = username_field.value.strip()
            pwd = password_field.value.strip()

            try:
                resp = requests.post(
                    f"{API_BASE}/admin/login",
                    json={"username": uname, "password": pwd}
                )
                if resp.status_code == 200:
                    show_admin_panel()
                else:
                    feedback_text.value = resp.json().get("detail", "❌ Invalid admin credentials")
            except Exception as ex:
                feedback_text.value = f"⚠️ Error: {ex}"
            page.update()

        page.clean()
        page.add(
            ft.Text("Admin Login", size=24, weight="bold"),
            username_field,
            password_field,
            ft.ElevatedButton("Log In", on_click=admin_login),
            ft.TextButton("Back to user login", on_click=show_login),
            feedback_text
        )

    def show_admin_panel(e=None):
        timeframe_dropdown = ft.Dropdown(
            label="Reset Timeframe",
            options=[
                ft.dropdown.Option("month"),
                ft.dropdown.Option("year")
            ],
            width=200
        )
        
        users_dropdown = ft.Dropdown(
            label="Select User to Congratulate",
            width=300,
            options=[]
        )
        
        congrats_message = ft.TextField(label="Congrats Message", multiline=True, width=300)
        
        # New fields for adding eco-actions
        new_action_name = ft.TextField(label="New Action Name", width=300)
        new_action_points = ft.TextField(
            label="Points Value", 
            width=300, 
            input_filter=ft.NumbersOnlyInputFilter()
        )
        
        def load_leaderboard_users():
            try:
                resp = requests.get(f"{API_BASE}/leaderboard")
                if resp.status_code == 200:
                    leaderboard_data = resp.json()
                    users_dropdown.options.clear()
                    
                    trophy = ["🥇", "🥈", "🥉"]
                    for rank, user in enumerate(leaderboard_data, start=1):
                        emoji = trophy[rank-1] if rank <= 3 else f"{rank}."
                        users_dropdown.options.append(
                            ft.dropdown.Option(
                                key=user["username"],
                                text=f"{emoji} {user['username']} ({user['points']} pts)"
                            )
                        )
                    page.update()
            except Exception as ex:
                feedback_text.value = f"⚠️ Error loading users: {ex}"
                page.update()
        
        def reset_leaderboard(e):
            if not timeframe_dropdown.value:
                feedback_text.value = "⚠️ Please select a timeframe"
                page.update()
                return
                
            try:
                resp = requests.post(
                    f"{API_BASE}/admin/reset-leaderboard",
                    json={"timeframe": timeframe_dropdown.value}
                )
                feedback_text.value = resp.json().get("message", "✅ Leaderboard reset")
            except Exception as ex:
                feedback_text.value = f"⚠️ Error: {ex}"
            page.update()
        
        def send_congrats(e):
            if not users_dropdown.value:
                feedback_text.value = "⚠️ Please select a user"
                page.update()
                return
                
            if not congrats_message.value:
                feedback_text.value = "⚠️ Please enter a message"
                page.update()
                return
                
            try:
                resp = requests.post(
                    f"{API_BASE}/admin/send-congrats",
                    json={
                        "username": users_dropdown.value,
                        "message": congrats_message.value
                    }
                )
                feedback_text.value = resp.json().get("message", "✅ Message sent")
                congrats_message.value = ""
            except Exception as ex:
                feedback_text.value = f"⚠️ Error: {ex}"
            page.update()
        
        def add_new_action(e):
            if not new_action_name.value or not new_action_points.value:
                feedback_text.value = "⚠️ Please fill all fields"
                page.update()
                return
                
            try:
                resp = requests.post(
                    f"{API_BASE}/admin/add-action",
                    json={
                        "action": new_action_name.value,
                        "points": int(new_action_points.value)
                    }
                )
                if resp.status_code == 200:
                    feedback_text.value = resp.json().get("message", "✅ Action added")
                    new_action_name.value = ""
                    new_action_points.value = ""
                else:
                    feedback_text.value = resp.json().get("detail", "❌ Failed to add action")
            except Exception as ex:
                feedback_text.value = f"⚠️ Error: {ex}"
            page.update()
        
        def logout(e):
            show_login()
        
        # Load users immediately when panel opens
        load_leaderboard_users()
        
        page.clean()
        page.add(
            ft.AppBar(title=ft.Text("Admin Panel", size=22, weight="bold"), 
                     center_title=True,
                     actions=[ft.ElevatedButton("Logout", on_click=logout)]),
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text("Add New Eco-Action", size=20, weight="bold"),
                    new_action_name,
                    new_action_points,
                    ft.ElevatedButton("Add Action", on_click=add_new_action),
                    
                    ft.Divider(height=20),
                    
                    ft.Text("Leaderboard Management", size=20, weight="bold"),
                    timeframe_dropdown,
                    ft.ElevatedButton("Reset Leaderboard", on_click=reset_leaderboard),
                    
                    ft.Divider(height=20),
                    
                    ft.Text("Send Congratulations", size=20, weight="bold"),
                    users_dropdown,
                    congrats_message,
                    ft.ElevatedButton("Send Message", on_click=send_congrats),
                    
                    feedback_text
                ])
            )
        )

    def show_action_screen():
        leaderboard_column.controls.clear()

        history_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            height=200,
            expand = False
        )
        

        def load_points():
            try:
                resp = requests.get(f"{API_BASE}/user-points/{current_user['username']}")
                if resp.status_code == 200:
                    total_points = resp.json().get("points", 0)
                    total_points_text.value = f"Points: {total_points}"
            except:
                total_points_text.value = "Points: 0"
            page.update()

        def load_actions():
            action_dropdown.options.clear()
            try:
                resp = requests.get(f"{API_BASE}/actions")
                if resp.status_code == 200:
                    actions = resp.json()
                    if not isinstance(actions, list):  # Ensure we got an array
                        feedback_text.value = "❌ Invalid actions data."
                        return
                    
                    for action in actions:
                        if not all(k in action for k in ["id", "action", "points"]):
                            continue  # Skip invalid entries
                        
                        action_dropdown.options.append(
                            ft.dropdown.Option(
                                key=str(action["id"]),  # Make sure we're using the ID
                                text=f'{action["action"]} (+{action["points"]} pts)'
                            )
                        )
                    
                    # Select the first action by default if available
                    if action_dropdown.options:
                        action_dropdown.value = action_dropdown.options[0].key
                else:
                    feedback_text.value = "❌ Failed to load actions."
            except Exception as e:
                feedback_text.value = f"⚠️ Error: {e}"
            page.update()

        def load_user_history():
                try:
                    resp = requests.get(f"{API_BASE}/user-history/{current_user['username']}")
                    if resp.status_code == 200:
                        history_data = resp.json()
                        history_column.controls.clear()
                        for action in history_data:
                            history_column.controls.append(
                                ft.Text(
                                    f"{action['action']} (+{action['points']} pts) - {action['timestamp']}",
                                    size=12
                                )
                            )
                        page.update()
                except Exception as e:
                    feedback_text.value = f"⚠️ Error loading history: {str(e)}"
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
                    json={
                        "user": current_user["username"],
                        "action_id": int(action_id)  # Ensure we're sending the action ID
                    }
                )
                if resp.status_code == 200:
                    feedback_text.value = resp.json().get("message", "✅ Action logged")
                    #Refresh points and leaderboard
                    load_points()
                    view_leaderboard(None)
                else:
                    feedback_text.value = resp.json().get("detail", "❌ Failed to log action")
            except Exception as ex:
                feedback_text.value = f"⚠️ Error: {ex}"
            page.update()
                    
                    

        def logout(e):
            current_user["username"] = None
            current_user["fullname"] = None
            feedback_text.value = ""
            show_login()

        def view_leaderboard(e):
            try:
                resp = requests.get(f"{API_BASE}/leaderboard")
                if resp.status_code == 200:
                    leaderboard_data = resp.json()
                    leaderboard_column.controls.clear()
                    leaderboard_column.controls.append(
                        ft.Text("🏆 Eco Champions Leaderboard", size=20, weight="bold", text_align="center")
                    )

                    trophy = ["🥇", "🥈", "🥉"]
                    for rank, entry in enumerate(leaderboard_data, start=1):
                        emoji = trophy[rank - 1] if rank <= 3 else f"{rank}."
                        card = ft.Card(
                            content=ft.Container(
                                content=ft.Row([
                                    ft.Text(emoji, size=20),
                                    ft.Text(entry["username"], size=18, expand=True),
                                    ft.Text(f"{entry['points']} pts", size=16, weight="bold")
                                ]),
                                padding=10
                            ),
                            elevation=3
                        )
                        leaderboard_column.controls.append(card)

                    page.update()
                else:
                    feedback_text.value = "❌ Failed to load leaderboard."
            except Exception as ex:
                feedback_text.value = f"⚠️ Error: {ex}"
            page.update()

        page.clean()
        page.appbar = ft.AppBar(title=ft.Text("🌱 Eco-Action Tracker", size=22, weight="bold"), center_title=True, actions=[total_points_text])
        
        page.add(
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text(f"👋 Welcome, {current_user['fullname']}", size=20, weight="bold"),
                    ft.Row([
                        ft.ElevatedButton("🚪 Logout", on_click=logout),
                        ft.ElevatedButton("📊 View Leaderboard", on_click=view_leaderboard)
                    ], spacing=10),
                    ft.Divider(height=20, thickness=1),
                    ft.Text("🌿 Available Eco-Actions", size=18, weight="w600"),
                    action_dropdown,
                    ft.ElevatedButton("✅ Log Action", on_click=log_action),
                    feedback_text,
                    ft.Divider(height=20, thickness=1),
                    ft.Text("📜 Your Action History", size=16, weight="bold"),
                    history_column,
                    ft.Divider(height=20, thickness=1),
                    leaderboard_column
                ])
            )
        )
        load_actions()
        load_points()
        load_user_history()

    def show_signup(e=None):
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

    def show_login(e=None):
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
                    current_user["fullname"] = uname
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
            ft.TextButton("Don't have an account? Sign up", on_click=switch_to_signup),
            ft.TextButton("Admin Login", on_click=lambda e: show_admin_login()),
            feedback_text
        )

    show_signup()

ft.app(target=main)