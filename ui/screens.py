from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from datetime import datetime

from core.auth import login_user
from core.database import get_connection
from services.firebase_sync import sync_data_background
from services.pdf_generator import generate_donation_report

# Dictionary for multi-language support
LANGUAGES = {
    'EN': {'dash': 'Dashboard', 'mem': 'Members', 'daan': 'Donations', 'seva': 'Seva & Utsav', 'rep': 'Reports'},
    'BN': {'dash': 'ড্যাশবোর্ড', 'mem': 'সদস্যগণ', 'daan': 'দান', 'seva': 'সেবা ও উৎসব', 'rep': 'রিপোর্ট'},
    'HI': {'dash': 'डैशबोर्ड', 'mem': 'सदस्य', 'daan': 'दान', 'seva': 'सेवा और उत्सव', 'rep': 'रिपोर्ट'}
}
CURRENT_LANG = 'EN'

def show_popup(title, message):
    layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
    layout.add_widget(Label(text=message, text_size=(300, None), halign='center'))
    close_btn = Button(text='Close', size_hint_y=0.3, background_color=(0.9, 0.5, 0.1, 1))
    popup = Popup(title=title, content=layout, size_hint=(0.8, 0.4))
    close_btn.bind(on_press=popup.dismiss)
    layout.add_widget(close_btn)
    popup.open()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        layout.add_widget(Label(text="Sanatani Bandhan\nAdmin Portal", font_size=28, halign='center', size_hint_y=0.3))
        self.username = TextInput(hint_text="Username (admin)", multiline=False, size_hint_y=0.15)
        self.password = TextInput(hint_text="Password (admin108)", password=True, multiline=False, size_hint_y=0.15)
        
        login_btn = Button(text="Enter", size_hint_y=0.2, background_color=(0.8, 0.4, 0.1, 1)) # Saffron tone
        login_btn.bind(on_press=self.verify_credentials)
        
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_btn)
        self.add_widget(layout)

    def verify_credentials(self, instance):
        if login_user(self.username.text, self.password.text):
            self.manager.current = 'dashboard'
            sync_data_background()
        else:
            show_popup("Error", "Invalid credentials.")

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header with toggle
        header = BoxLayout(size_hint_y=0.2)
        header.add_widget(Label(text='"Karmanye vadhikaraste..."\nYour right is to perform duty.', halign='center', italic=True))
        
        lang_btn = Button(text="Switch Lang", size_hint_x=0.3, background_color=(0.3, 0.3, 0.3, 1))
        lang_btn.bind(on_press=self.toggle_lang)
        header.add_widget(lang_btn)
        self.layout.add_widget(header)
        
        self.grid = GridLayout(cols=2, spacing=10, size_hint_y=0.6)
        self.build_menu()
        self.layout.add_widget(self.grid)
        
        btn_logout = Button(text="Logout", size_hint_y=0.1, background_color=(0.8, 0.1, 0.1, 1))
        btn_logout.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        self.layout.add_widget(btn_logout)
        self.add_widget(self.layout)

    def build_menu(self):
        self.grid.clear_widgets()
        texts = LANGUAGES[CURRENT_LANG]
        
        btn_members = Button(text=f"👥 {texts['mem']}", background_color=(0.2, 0.5, 0.8, 1))
        btn_members.bind(on_press=lambda x: setattr(self.manager, 'current', 'members'))
        
        btn_donations = Button(text=f"🙏 {texts['daan']}", background_color=(0.8, 0.5, 0.2, 1))
        btn_donations.bind(on_press=lambda x: setattr(self.manager, 'current', 'donations'))
        
        btn_expenses = Button(text=f"🕉️ {texts['seva']}", background_color=(0.6, 0.2, 0.6, 1))
        btn_expenses.bind(on_press=lambda x: setattr(self.manager, 'current', 'expenses'))
        
        btn_reports = Button(text=f"📄 {texts['rep']}", background_color=(0.4, 0.4, 0.4, 1))
        btn_reports.bind(on_press=lambda x: setattr(self.manager, 'current', 'reports'))
        
        self.grid.add_widget(btn_members)
        self.grid.add_widget(btn_donations)
        self.grid.add_widget(btn_expenses)
        self.grid.add_widget(btn_reports)

    def toggle_lang(self, instance):
        global CURRENT_LANG
        langs = ['EN', 'BN', 'HI']
        CURRENT_LANG = langs[(langs.index(CURRENT_LANG) + 1) % 3]
        self.build_menu()

class MemberScreen(Screen):
    def __init__(self, **kwargs):
        super(MemberScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.m_name = TextInput(hint_text="Devotee/Member Name", multiline=False, size_hint_y=0.15)
        self.m_phone = TextInput(hint_text="Phone Number", multiline=False, input_type='number', size_hint_y=0.15)
        
        btn_save = Button(text="Add Member", size_hint_y=0.15, background_color=(0.1, 0.7, 0.1, 1))
        btn_save.bind(on_press=self.save)
        
        btn_back = Button(text="Back", size_hint_y=0.15)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        
        layout.add_widget(Label(text="Add Community Member", size_hint_y=0.1))
        layout.add_widget(self.m_name)
        layout.add_widget(self.m_phone)
        layout.add_widget(btn_save)
        layout.add_widget(Label(size_hint_y=0.3))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def save(self, instance):
        if self.m_name.text:
            conn = get_connection()
            conn.execute("INSERT INTO members (name, phone, join_date) VALUES (?, ?, ?)", 
                           (self.m_name.text, self.m_phone.text, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            show_popup("Success", "Member Added.")
            self.m_name.text = ""
            self.m_phone.text = ""

class DonationScreen(Screen):
    def __init__(self, **kwargs):
        super(DonationScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.d_name = TextInput(hint_text="Donor Name", multiline=False, size_hint_y=0.15)
        self.d_amount = TextInput(hint_text="Amount (Daan)", multiline=False, input_type='number', size_hint_y=0.15)
        
        btn_save = Button(text="Record Daan", size_hint_y=0.15, background_color=(0.8, 0.5, 0.2, 1))
        btn_save.bind(on_press=self.save)
        
        btn_back = Button(text="Back", size_hint_y=0.15)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        
        layout.add_widget(Label(text="Record New Donation", size_hint_y=0.1))
        layout.add_widget(self.d_name)
        layout.add_widget(self.d_amount)
        layout.add_widget(btn_save)
        layout.add_widget(Label(size_hint_y=0.3))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def save(self, instance):
        if self.d_name.text and self.d_amount.text:
            conn = get_connection()
            conn.execute("INSERT INTO donations (member_name, amount, date) VALUES (?, ?, ?)", 
                           (self.d_name.text, float(self.d_amount.text), datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            show_popup("Success", "Daan Recorded.")
            self.d_name.text = ""
            self.d_amount.text = ""

class ExpenseScreen(Screen):
    def __init__(self, **kwargs):
        super(ExpenseScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.e_cat = Spinner(text='Category', values=('Social Work', 'Festivals'), size_hint_y=0.15)
        self.e_name = TextInput(hint_text="Event/Item Name", multiline=False, size_hint_y=0.15)
        self.e_amount = TextInput(hint_text="Amount Spent", multiline=False, input_type='number', size_hint_y=0.15)
        
        btn_save = Button(text="Save Expense", size_hint_y=0.15, background_color=(0.6, 0.2, 0.6, 1))
        btn_save.bind(on_press=self.save)
        
        btn_back = Button(text="Back", size_hint_y=0.15)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        
        layout.add_widget(Label(text="Record Seva / Utsav Expense", size_hint_y=0.1))
        layout.add_widget(self.e_cat)
        layout.add_widget(self.e_name)
        layout.add_widget(self.e_amount)
        layout.add_widget(btn_save)
        layout.add_widget(Label(size_hint_y=0.1))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def save(self, instance):
        if self.e_name.text and self.e_amount.text and self.e_cat.text != 'Category':
            conn = get_connection()
            conn.execute("INSERT INTO expenses (category, name, total_amount, date) VALUES (?, ?, ?, ?)", 
                           (self.e_cat.text, self.e_name.text, float(self.e_amount.text), datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            show_popup("Success", "Expense Recorded.")
            self.e_name.text = ""
            self.e_amount.text = ""

class ReportScreen(Screen):
    def __init__(self, **kwargs):
        super(ReportScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        btn_daan = Button(text="Generate Donation PDF", size_hint_y=0.2, background_color=(0.2, 0.6, 0.8, 1))
        btn_daan.bind(on_press=self.gen_daan)
        
        btn_back = Button(text="Back", size_hint_y=0.2)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        
        layout.add_widget(Label(text="Generate Official Reports", size_hint_y=0.2))
        layout.add_widget(btn_daan)
        layout.add_widget(Label(size_hint_y=0.4))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def gen_daan(self, instance):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM donations")
        data = cursor.fetchall()
        conn.close()
        
        if data:
            path = generate_donation_report(data)
            show_popup("Success", f"PDF Saved to:\n{path}")
        else:
            show_popup("Empty", "No donations found to report.")

def get_screen_manager():
    sm = ScreenManager()
    sm.add_widget(LoginScreen(name='login'))
    sm.add_widget(DashboardScreen(name='dashboard'))
    sm.add_widget(MemberScreen(name='members'))
    sm.add_widget(DonationScreen(name='donations'))
    sm.add_widget(ExpenseScreen(name='expenses'))
    sm.add_widget(ReportScreen(name='reports'))
    return sm
