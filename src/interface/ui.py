from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import threading
import time
import requests
from datetime import datetime
from urllib.parse import urlparse
import queue

class StressTestGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10
        
        # Set window properties
        Window.size = (800, 700)
        Window.clearcolor = (0.12, 0.12, 0.15, 1)
        
        # Attack state variables
        self.is_running = False
        self.stop_flag = False
        self.threads = []
        self.request_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.log_queue = queue.Queue()
        
        # Build UI
        self.build_ui()
        
        # Schedule log updates
        Clock.schedule_interval(self.update_logs, 0.1)
        
        # Show warning on startup
        Clock.schedule_once(lambda dt: self.show_warning(), 0.5)
    
    def build_ui(self):
        # Title Section
        title_box = BoxLayout(size_hint=(1, 0.08), padding=[5, 5])
        with title_box.canvas.before:
            Color(0.2, 0.25, 0.3, 1)
            self.title_rect = Rectangle(pos=title_box.pos, size=title_box.size)
        title_box.bind(pos=self.update_rect, size=self.update_rect)
        
        title = Label(
            text='[b]Network Stress Testing Tool[/b]\n[size=12sp]Educational Use Only - Thesis Project[/size]',
            markup=True,
            font_size='22sp',
            color=(1, 1, 1, 1)
        )
        title_box.add_widget(title)
        self.add_widget(title_box)
        
        # Warning Label
        warning = Label(
            text='⚠️ For authorized testing and educational purposes only ⚠️',
            size_hint=(1, 0.05),
            font_size='14sp',
            color=(1, 0.3, 0.3, 1),
            bold=True
        )
        self.add_widget(warning)
        
        # Input Section
        input_section = GridLayout(
            cols=2,
            size_hint=(1, 0.25),
            spacing=8,
            padding=10
        )
        
        with input_section.canvas.before:
            Color(0.15, 0.15, 0.18, 1)
            self.input_rect = Rectangle(pos=input_section.pos, size=input_section.size)
        input_section.bind(pos=self.update_input_rect, size=self.update_input_rect)
        
        # URL Input
        input_section.add_widget(self.create_label('Target URL:'))
        self.url_input = TextInput(
            hint_text='https://example.com',
            multiline=False,
            font_size='14sp',
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1),
            padding=[10, 10]
        )
        input_section.add_widget(self.url_input)
        
        # Number of Threads
        input_section.add_widget(self.create_label('Number of Threads:'))
        self.threads_input = TextInput(
            text='10',
            multiline=False,
            input_filter='int',
            font_size='14sp',
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1),
            padding=[10, 10]
        )
        input_section.add_widget(self.threads_input)
        
        # Attack Duration
        input_section.add_widget(self.create_label('Attack Duration (seconds):'))
        self.duration_input = TextInput(
            text='5.0',
            multiline=False,
            input_filter='float',
            font_size='14sp',
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1),
            padding=[10, 10]
        )
        input_section.add_widget(self.duration_input)
        
        # Attacks Per Second
        input_section.add_widget(self.create_label('Attacks Per Second:'))
        self.attacks_per_sec_input = TextInput(
            text='100',
            multiline=False,
            input_filter='int',
            font_size='14sp',
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1),
            padding=[10, 10]
        )
        input_section.add_widget(self.attacks_per_sec_input)
        
        # Request Delay
        input_section.add_widget(self.create_label('Request Delay (seconds):'))
        self.delay_input = TextInput(
            text='0.01',
            multiline=False,
            input_filter='float',
            font_size='14sp',
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1),
            padding=[10, 10]
        )
        input_section.add_widget(self.delay_input)
        
        self.add_widget(input_section)
        
        # Control Buttons
        button_box = BoxLayout(size_hint=(1, 0.08), spacing=10, padding=10)
        
        self.start_btn = Button(
            text='Start Attack',
            font_size='16sp',
            bold=True,
            background_color=(0.2, 0.7, 0.3, 1),
            background_normal=''
        )
        self.start_btn.bind(on_press=self.confirm_start)
        button_box.add_widget(self.start_btn)
        
        self.stop_btn = Button(
            text='Stop Attack',
            font_size='16sp',
            bold=True,
            background_color=(0.8, 0.2, 0.2, 1),
            background_normal='',
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_attack)
        button_box.add_widget(self.stop_btn)
        
        self.clear_btn = Button(
            text='Clear Logs',
            font_size='16sp',
            background_color=(0.4, 0.4, 0.5, 1),
            background_normal=''
        )
        self.clear_btn.bind(on_press=self.clear_logs)
        button_box.add_widget(self.clear_btn)
        
        self.add_widget(button_box)
        
        # Status Section
        status_box = BoxLayout(orientation='vertical', size_hint=(1, 0.15), padding=10, spacing=5)
        
        with status_box.canvas.before:
            Color(0.15, 0.15, 0.18, 1)
            self.status_rect = Rectangle(pos=status_box.pos, size=status_box.size)
        status_box.bind(pos=self.update_status_rect, size=self.update_status_rect)
        
        self.status_label = Label(
            text='Status: Idle',
            font_size='16sp',
            color=(0.3, 0.7, 1, 1),
            bold=True,
            size_hint=(1, 0.3)
        )
        status_box.add_widget(self.status_label)
        
        stats_grid = GridLayout(cols=3, size_hint=(1, 0.4), spacing=5)
        
        self.requests_label = Label(text='Requests: 0', font_size='14sp', color=(1, 1, 1, 1))
        self.success_label = Label(text='Success: 0', font_size='14sp', color=(0.3, 1, 0.3, 1))
        self.failure_label = Label(text='Failed: 0', font_size='14sp', color=(1, 0.3, 0.3, 1))
        
        stats_grid.add_widget(self.requests_label)
        stats_grid.add_widget(self.success_label)
        stats_grid.add_widget(self.failure_label)
        
        status_box.add_widget(stats_grid)
        
        self.progress_bar = ProgressBar(max=100, size_hint=(1, 0.3))
        status_box.add_widget(self.progress_bar)
        
        self.add_widget(status_box)
        
        # Log Section
        log_label = Label(
            text='Activity Log:',
            size_hint=(1, 0.04),
            font_size='14sp',
            color=(1, 1, 1, 1),
            bold=True
        )
        self.add_widget(log_label)
        
        scroll = ScrollView(size_hint=(1, 0.4))
        self.log_display = Label(
            text='',
            size_hint_y=None,
            font_size='12sp',
            color=(0.8, 0.8, 0.8, 1),
            markup=True,
            halign='left',
            valign='top'
        )
        self.log_display.bind(texture_size=self.log_display.setter('size'))
        self.log_display.bind(size=self.update_log_text_size)
        scroll.add_widget(self.log_display)
        self.add_widget(scroll)
    
    def update_rect(self, instance, value):
        self.title_rect.pos = instance.pos
        self.title_rect.size = instance.size
    
    def update_input_rect(self, instance, value):
        self.input_rect.pos = instance.pos
        self.input_rect.size = instance.size
    
    def update_status_rect(self, instance, value):
        self.status_rect.pos = instance.pos
        self.status_rect.size = instance.size
    
    def update_log_text_size(self, instance, value):
        instance.text_size = (instance.width - 20, None)
    
    def create_label(self, text):
        return Label(
            text=text,
            font_size='14sp',
            color=(1, 1, 1, 1),
            halign='right',
            size_hint_x=0.4
        )
    
    def show_warning(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(
            text='⚠️ WARNING ⚠️\n\nThis tool is for AUTHORIZED TESTING ONLY.\n\n'
                 'Unauthorized use against systems you do not own\n'
                 'or have explicit permission to test is ILLEGAL.\n\n'
                 'Use responsibly and ethically.',
            font_size='14sp',
            halign='center'
        ))
        
        btn = Button(text='I Understand', size_hint=(1, 0.2))
        content.add_widget(btn)
        
        popup = Popup(
            title='Legal Warning',
            content=content,
            size_hint=(0.6, 0.5),
            auto_dismiss=False
        )
        btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def confirm_start(self, instance):
        if not self.validate_inputs():
            return
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(
            text=f'Start stress test on:\n{self.url_input.text}\n\nAre you authorized to test this target?',
            font_size='14sp',
            halign='center'
        ))
        
        btn_box = BoxLayout(size_hint=(1, 0.3), spacing=10)
        yes_btn = Button(text='Yes, Start', background_color=(0.2, 0.7, 0.3, 1))
        no_btn = Button(text='Cancel', background_color=(0.8, 0.2, 0.2, 1))
        
        btn_box.add_widget(yes_btn)
        btn_box.add_widget(no_btn)
        content.add_widget(btn_box)
        
        popup = Popup(
            title='Confirm Attack',
            content=content,
            size_hint=(0.6, 0.4),
            auto_dismiss=False
        )
        
        yes_btn.bind(on_press=lambda x: (popup.dismiss(), self.start_attack(None)))
        no_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def validate_inputs(self):
        # Validate URL
        url = self.url_input.text.strip()
        if not url:
            self.show_error('Please enter a target URL')
            return False
        
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValueError()
        except:
            self.show_error('Invalid URL format')
            return False
        
        # Validate numeric inputs
        try:
            threads = int(self.threads_input.text)
            if threads <= 0 or threads > 1000:
                raise ValueError()
        except:
            self.show_error('Threads must be between 1 and 1000')
            return False
        
        try:
            duration = float(self.duration_input.text)
            if duration <= 0:
                raise ValueError()
        except:
            self.show_error('Duration must be greater than 0')
            return False
        
        try:
            attacks = int(self.attacks_per_sec_input.text)
            if attacks <= 0:
                raise ValueError()
        except:
            self.show_error('Attacks per second must be greater than 0')
            return False
        
        try:
            delay = float(self.delay_input.text)
            if delay < 0:
                raise ValueError()
        except:
            self.show_error('Request delay must be 0 or greater')
            return False
        
        return True
    
    def show_error(self, message):
        popup = Popup(
            title='Validation Error',
            content=Label(text=message),
            size_hint=(0.5, 0.3)
        )
        popup.open()
    
    def start_attack(self, instance):
        self.is_running = True
        self.stop_flag = False
        self.request_count = 0
        self.success_count = 0
        self.failure_count = 0
        
        # Update UI
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.url_input.disabled = True
        self.threads_input.disabled = True
        self.duration_input.disabled = True
        self.attacks_per_sec_input.disabled = True
        self.delay_input.disabled = True
        
        self.status_label.text = 'Status: Running'
        self.status_label.color = (0.3, 1, 0.3, 1)
        
        self.log_message('[b][color=00ff00]Attack started[/color][/b]')
        
        # Get parameters
        url = self.url_input.text.strip()
        num_threads = int(self.threads_input.text)
        duration = float(self.duration_input.text)
        attacks_per_sec = int(self.attacks_per_sec_input.text)
        delay = float(self.delay_input.text)
        
        # Start attack threads
        self.threads = []
        for i in range(num_threads):
            thread = threading.Thread(
                target=self.attack_worker,
                args=(url, duration, attacks_per_sec, delay, i+1)
            )
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
        
        # Start progress tracker
        Clock.schedule_once(lambda dt: self.track_progress(duration), 0)
    
    def attack_worker(self, url, duration, attacks_per_sec, delay, thread_id):
        start_time = time.time()
        request_interval = 1.0 / attacks_per_sec if attacks_per_sec > 0 else 0
        
        while time.time() - start_time < duration and not self.stop_flag:
            try:
                response = requests.get(url, timeout=5)
                self.request_count += 1
                
                if response.status_code == 200:
                    self.success_count += 1
                else:
                    self.failure_count += 1
                    
            except Exception as e:
                self.request_count += 1
                self.failure_count += 1
            
            time.sleep(max(delay, request_interval))
        
        self.log_message(f'Thread {thread_id} completed')
    
    def track_progress(self, duration):
        if not self.is_running:
            return
        
        start_time = time.time()
        
        def update_progress(dt):
            elapsed = time.time() - start_time
            progress = min((elapsed / duration) * 100, 100)
            self.progress_bar.value = progress
            
            if elapsed >= duration or self.stop_flag:
                self.finish_attack()
            elif self.is_running:
                Clock.schedule_once(update_progress, 0.1)
        
        Clock.schedule_once(update_progress, 0.1)
    
    def stop_attack(self, instance):
        self.stop_flag = True
        self.log_message('[b][color=ff6600]Stopping attack...[/color][/b]')
        self.status_label.text = 'Status: Stopping...'
        self.status_label.color = (1, 0.6, 0, 1)
    
    def finish_attack(self):
        self.is_running = False
        self.stop_flag = True
        
        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=1)
        
        # Update UI
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.url_input.disabled = False
        self.threads_input.disabled = False
        self.duration_input.disabled = False
        self.attacks_per_sec_input.disabled = False
        self.delay_input.disabled = False
        
        self.status_label.text = 'Status: Completed'
        self.status_label.color = (0.3, 0.7, 1, 1)
        self.progress_bar.value = 100
        
        self.log_message('[b][color=00ffff]Attack completed[/color][/b]')
        self.log_message(f'Total Requests: {self.request_count}, Success: {self.success_count}, Failed: {self.failure_count}')
    
    def update_logs(self, dt):
        # Update statistics
        self.requests_label.text = f'Requests: {self.request_count}'
        self.success_label.text = f'Success: {self.success_count}'
        self.failure_label.text = f'Failed: {self.failure_count}'
        
        # Update log display
        while not self.log_queue.empty():
            try:
                message = self.log_queue.get_nowait()
                current_text = self.log_display.text
                self.log_display.text = message + '\n' + current_text
            except:
                pass
    
    def log_message(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f'[{timestamp}] {message}'
        self.log_queue.put(log_entry)
    
    def clear_logs(self, instance):
        self.log_display.text = ''
        self.log_message('[color=ffff00]Logs cleared[/color]')


class StressTestApp(App):
    def build(self):
        self.title = 'Network Stress Testing Tool'
        return StressTestGUI()


if __name__ == '__main__':
    StressTestApp().run()