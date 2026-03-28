import os
from kivy.app import App
from core.database import init_db
from ui.screens import get_screen_manager

class SHDAApp(App):
    def build(self):
        init_db()
        return get_screen_manager()

if __name__ == '__main__':
    if 'ANDROID_ARGUMENT' in os.environ:
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.INTERNET, 
            Permission.WRITE_EXTERNAL_STORAGE, 
            Permission.READ_EXTERNAL_STORAGE
        ])
    SHDAApp().run()

