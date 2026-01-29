from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.clock import Clock
from kivy.metrics import dp, sp
import threading
import datetime

# Import your backend modules
from core.connectioin import numberConnection
from core.interval import timeload
from util.translateHost import parse_url


class RocketUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=0, spacing=0, **kwargs)
        
        self.stop_flag = False
        self.attack_thread = None
        
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1)  
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Header with proportional sizing
        header_box = BoxLayout(
            orientation="vertical", 
            size_hint_y=None, 
            height=dp(60),  
            padding=[dp(15), dp(10)]
        )
        with header_box.canvas.before:
            Color(0.15, 0.15, 0.18, 1) 
            self.header_rect = Rectangle(pos=header_box.pos, size=header_box.size)
        header_box.bind(
            pos=lambda instance, value: setattr(self.header_rect, 'pos', value),
            size=lambda instance, value: setattr(self.header_rect, 'size', value)
        )
        
        header = Label(
            text="ROCKET LAUNCHER",
            font_size=sp(24),  
            bold=True,
            color=(1, 1, 1, 1)
        )
        header_box.add_widget(header)
        self.add_widget(header_box)
        
        # Main container with responsive padding
        main_container = BoxLayout(
            orientation="vertical", 
            padding=[dp(15), dp(10)], 
            spacing=dp(10)
        )
        with main_container.canvas.before:
            Color(0.15, 0.15, 0.18, 1)
            self.main_rect = Rectangle(pos=main_container.pos, size=main_container.size)
        main_container.bind(
            pos=lambda instance, value: setattr(self.main_rect, 'pos', value),
            size=lambda instance, value: setattr(self.main_rect, 'size', value)
        )
        
        input_scroll = ScrollView(
            size_hint_y=0.5,
            do_scroll_x=False,
            do_scroll_y=True
        )
        
        input_section = BoxLayout(
            orientation="vertical", 
            size_hint_y=None,
            spacing=dp(8)
        )
        input_section.bind(minimum_height=input_section.setter('height'))
        
        # URL Input
        input_section.add_widget(self.create_label("Target URL"))
        self.url_input = self.create_input("http://example.com/path")
        input_section.add_widget(self.url_input)
        
        # Sleep Time
        input_section.add_widget(self.create_label("Sleep Time (seconds)"))
        self.sleep_input = self.create_input("5", input_filter="int")
        input_section.add_widget(self.sleep_input)
        
        # Number of Threads
        input_section.add_widget(self.create_label("Total Number of Threads"))
        self.count_input = self.create_input("10", input_filter="int")
        input_section.add_widget(self.count_input)
        
        # Threads per Time
        input_section.add_widget(self.create_label("Threads Per Attack"))
        self.tasks_per_sleep_input = self.create_input("1", input_filter="int")
        input_section.add_widget(self.tasks_per_sleep_input)
        
        # Request Delay
        input_section.add_widget(self.create_label("Request Delay (seconds)"))
        self.request_delay_input = self.create_input("0.1")
        input_section.add_widget(self.request_delay_input)
        
        # Method Selection
        input_section.add_widget(self.create_label("HTTP Method"))
        self.method_spinner = self.create_spinner()
        input_section.add_widget(self.method_spinner)
        
        input_scroll.add_widget(input_section)
        main_container.add_widget(input_scroll)
        
        # --- CONTROL BUTTONS ---
        button_layout = BoxLayout(
            size_hint_y=None, 
            height=dp(50), 
            spacing=dp(10), 
            padding=[0, dp(5), 0, dp(5)]
        )
        
        self.start_btn = self.create_button("START", (0.1, 0.5, 0.9, 1))
        self.start_btn.bind(on_press=self.on_start)
        
        self.stop_btn = self.create_button("STOP", (0.3, 0.3, 0.35, 1))
        self.stop_btn.bind(on_press=self.on_stop)
        self.stop_btn.disabled = True
        
        button_layout.add_widget(self.start_btn)
        button_layout.add_widget(self.stop_btn)
        main_container.add_widget(button_layout)
        
        # --- LOG SECTION ---
        log_container = BoxLayout(
            orientation="vertical", 
            size_hint_y=0.35,  # Reduced slightly for better balance
            padding=[0, dp(8), 0, 0], 
            spacing=dp(6)
        )
        
        log_label_header = Label(
            text="MISSION LOG",
            font_size=sp(16),
            bold=True,
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1)
        )
        log_container.add_widget(log_label_header)
        
        # Scrollable log area
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, bar_width=dp(8))
        with scroll.canvas.before:
            Color(0.08, 0.08, 0.1, 1)
            self.scroll_rect = RoundedRectangle(
                pos=scroll.pos, 
                size=scroll.size, 
                radius=[dp(8)]
            )
        scroll.bind(
            pos=lambda instance, value: setattr(self.scroll_rect, 'pos', value),
            size=lambda instance, value: setattr(self.scroll_rect, 'size', value)
        )
        
        # Container for log content
        self.scroll_layout = BoxLayout(
            orientation="vertical", 
            size_hint_y=None, 
            padding=dp(10), 
            spacing=dp(3)
        )
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
        
        self.log_label = Label(
            text="Awaiting launch sequence...",
            size_hint_y=None,
            valign="top",
            halign="left",
            color=(1, 1, 1, 1),
            font_size=sp(12),
            markup=True
        )
        self.log_label.bind(
            texture_size=self.update_label_height, 
            size=self.update_text_size
        )
        self.scroll_layout.add_widget(self.log_label)
        
        scroll.add_widget(self.scroll_layout)
        log_container.add_widget(scroll)
        
        main_container.add_widget(log_container)
        self.add_widget(main_container)
    
    def create_label(self, text):
        """Create a responsive label"""
        return Label(
            text=text,
            font_size=sp(13),
            bold=True,
            size_hint_y=None,
            height=dp(22),
            halign="left",
            color=(1, 1, 1, 1)
        )
    
    def create_input(self, hint, input_filter=None):
        """Create a responsive input field"""
        text_input = TextInput(
            hint_text=hint,
            text=hint,
            multiline=False,
            size_hint_y=None,
            height=dp(38),
            padding=[dp(12), dp(9)],
            font_size=sp(13),
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.1, 0.5, 0.9, 1),
            input_filter=input_filter,
            background_normal='',
            background_active=''
        )
        return text_input
    
    def create_spinner(self):
        """Create a responsive dropdown"""
        spinner = Spinner(
            text="GET",
            values=("GET", "POST"),
            size_hint_y=None,
            height=dp(38),
            background_color=(0.25, 0.25, 0.28, 1),
            color=(1, 1, 1, 1),
            font_size=sp(13),
            background_normal='',
            background_down=''
        )
        return spinner
    
    def create_button(self, text, color):
        """Create a responsive button"""
        button = Button(
            text=text,
            size_hint_y=None,
            height=dp(48),
            font_size=sp(16),
            bold=True,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        with button.canvas.before:
            Color(*color)
            button.bg_rect = RoundedRectangle(
                pos=button.pos,
                size=button.size,
                radius=[dp(10)]
            )
        button.bind(
            pos=lambda instance, value: setattr(instance.bg_rect, 'pos', value),
            size=lambda instance, value: setattr(instance.bg_rect, 'size', value)
        )
        return button
    
    def update_bg(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def update_label_height(self, instance, value):
        instance.height = instance.texture_size[1]
    
    def update_text_size(self, instance, value):
        instance.text_size = (instance.width - dp(15), None)
    
    def on_start(self, instance):
        """Called when the START button is pressed"""
        url = self.url_input.text
        sleep_time = self.sleep_input.text
        n_threads = self.count_input.text
        t_per_time = self.tasks_per_sleep_input.text
        request_delay = self.request_delay_input.text
        method = self.method_spinner.text
        
        if not url:
            self.update_log("ERROR: Target URL is required!")
            return
        
        if not sleep_time or not n_threads or not request_delay:
            self.update_log("ERROR: All fields are required!")
            return
        
        try:
            sleep_time = int(sleep_time)
            n_threads = int(n_threads)
            t_per_time = int(t_per_time)
            request_delay = float(request_delay)
        except ValueError:
            self.update_log("ERROR: Invalid number format!")
            return
        
        try:
            host, port, path = parse_url(url)
            self.update_log(f"Parsed URL - Host: {host}, Port: {port}, Path: {path}")
        except Exception as e:
            self.update_log(f"ERROR: Failed to parse URL - {str(e)}")
            return
        
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.stop_flag = False
        
        self.attack_thread = threading.Thread(
            target=self.run_attack,
            args=(n_threads, sleep_time, t_per_time, host, port, path, request_delay, method),
            daemon=True
        )
        self.attack_thread.start()
        
        self.update_log(f"LAUNCH INITIATED")
        self.update_log(f"Method: {method}, Threads: {n_threads}, Delay: {request_delay}s")
    
    def on_stop(self, instance):
        """Called when the STOP button is pressed"""
        self.stop_flag = True
        self.update_log("ABORT SIGNAL SENT - Stopping attack...")
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
    
    def run_attack(self, number_of_threads, sleep_time, thread_per_time, host, port, path, request_delay, method):
        """Main attack function running in a separate thread"""
        
        if thread_per_time == 0:
            if number_of_threads > 0:
                Clock.schedule_once(
                    lambda dt: self.update_log(f"Launching {number_of_threads} threads..."), 0
                )
                numberConnection(number_of_threads, host, port, path, request_delay, method)
            Clock.schedule_once(
                lambda dt: self.update_log("Attack finished!"), 0
            )
            Clock.schedule_once(lambda dt: self.attack_completed(), 0)
            return
        
        Clock.schedule_once(
            lambda dt: self.update_log("Attack started..."), 0
        )
        
        while number_of_threads > 0:
            if self.stop_flag:
                Clock.schedule_once(
                    lambda dt: self.update_log("Attack stopped by user!"), 0
                )
                Clock.schedule_once(lambda dt: self.attack_completed(), 0)
                return
            
            launch_attack = min(thread_per_time, number_of_threads)
            
            Clock.schedule_once(
                lambda dt, la=launch_attack: self.update_log(f"Launching {la} threads..."), 0
            )
            
            numberConnection(launch_attack, host, port, path, request_delay, method)
            number_of_threads -= launch_attack
            
            if number_of_threads <= 0:
                break
            
            Clock.schedule_once(
                lambda dt, st=sleep_time: self.update_log(f"Sleeping for {st} seconds..."), 0
            )
            
            timeload(sleep_time)
        
        Clock.schedule_once(
            lambda dt: self.update_log("Attack finished!"), 0
        )
        Clock.schedule_once(lambda dt: self.attack_completed(), 0)
    
    def attack_completed(self):
        """Called when attack completes to reset button states"""
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
    
    def update_log(self, message):
        """Update the mission log display"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_label.text += f"\n[{timestamp}] {message}"


class RocketApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.05, 1)
        Window.minimum_width = dp(400)
        Window.minimum_height = dp(600)
        Window.size = (dp(800), dp(900))  
        return RocketUI()


if __name__ == "__main__":
    RocketApp().run()