from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.widget import Widget

class RocketUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=0, spacing=0, **kwargs)
        
        # Set background (dark black)
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1)  # Deep black
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # --- HEADER SECTION (Blue) ---
        header_box = BoxLayout(orientation="vertical", size_hint_y=None, height=80, padding=[20, 15])
        with header_box.canvas.before:
            Color(0.1, 0.3, 0.6, 1)  # Deep blue
            self.header_rect = Rectangle(pos=header_box.pos, size=header_box.size)
        header_box.bind(pos=lambda instance, value: setattr(self.header_rect, 'pos', value),
                       size=lambda instance, value: setattr(self.header_rect, 'size', value))
        
        header = Label(
            text="ROCKET LAUNCHER",
            font_size='32sp',
            bold=True,
            color=(1, 1, 1, 1)  # White text
        )
        header_box.add_widget(header)
        self.add_widget(header_box)

        # --- MAIN CONTENT AREA ---
        main_container = BoxLayout(orientation="vertical", padding=25, spacing=15)
        with main_container.canvas.before:
            Color(0.15, 0.15, 0.18, 1)  # Dark gray background
            self.main_rect = Rectangle(pos=main_container.pos, size=main_container.size)
        main_container.bind(pos=lambda instance, value: setattr(self.main_rect, 'pos', value),
                           size=lambda instance, value: setattr(self.main_rect, 'size', value))

        # --- INPUT FIELDS SECTION ---
        input_section = BoxLayout(orientation="vertical", size_hint_y=0.55, spacing=12)
        
        # URL Input
        input_section.add_widget(self.create_label("Target URL"))
        self.url_input = self.create_input("Enter URL")
        input_section.add_widget(self.url_input)

        # Sleep Time
        input_section.add_widget(self.create_label("Sleep Time (seconds)"))
        self.sleep_input = self.create_input("5", input_filter="int")
        input_section.add_widget(self.sleep_input)

        # Number of Tasks
        input_section.add_widget(self.create_label("Total Tasks"))
        self.count_input = self.create_input("10", input_filter="int")
        input_section.add_widget(self.count_input)

        # Tasks per Sleep
        input_section.add_widget(self.create_label("Tasks Per Sleep Cycle"))
        self.tasks_per_sleep_input = self.create_input("1", input_filter="int")
        input_section.add_widget(self.tasks_per_sleep_input)

        # Method Selection
        input_section.add_widget(self.create_label("Execution Method"))
        self.method_spinner = self.create_spinner()
        input_section.add_widget(self.method_spinner)
        
        main_container.add_widget(input_section)

        # --- CONTROL BUTTONS ---
        button_layout = BoxLayout(size_hint_y=None, height=60, spacing=15, padding=[0, 8, 0, 8])
        
        self.start_btn = self.create_button("START", (0.1, 0.5, 0.9, 1))  # Bright blue
        self.start_btn.bind(on_press=self.on_start)
        
        self.stop_btn = self.create_button("STOP", (0.3, 0.3, 0.35, 1))  # Gray
        self.stop_btn.bind(on_press=self.on_stop)
        
        button_layout.add_widget(self.start_btn)
        button_layout.add_widget(self.stop_btn)
        main_container.add_widget(button_layout)

        # --- LOG SECTION (Larger, more space, fully scrollable) ---
        log_container = BoxLayout(orientation="vertical", size_hint_y=0.45, padding=[0, 10, 0, 0], spacing=8)
        
        log_label_header = Label(
            text="MISSION LOG",
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=35,
            color=(1, 1, 1, 1)  # White text
        )
        log_container.add_widget(log_label_header)
        
        # Scrollable log area
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, bar_width=10)
        with scroll.canvas.before:
            Color(0.08, 0.08, 0.1, 1)  # Dark background for log
            self.scroll_rect = RoundedRectangle(pos=scroll.pos, size=scroll.size, radius=[10])
        scroll.bind(pos=lambda instance, value: setattr(self.scroll_rect, 'pos', value),
                   size=lambda instance, value: setattr(self.scroll_rect, 'size', value))
        
        # Container for log content
        self.scroll_layout = BoxLayout(orientation="vertical", size_hint_y=None, padding=15, spacing=5)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))

        self.log_label = Label(
            text="Awaiting launch sequence...",
            size_hint_y=None,
            valign="top",
            halign="left",
            color=(1, 1, 1, 1),  # White text
            font_size='14sp',
            markup=True
        )
        self.log_label.bind(texture_size=self.update_label_height, size=self.update_text_size)
        self.scroll_layout.add_widget(self.log_label)
        
        scroll.add_widget(self.scroll_layout)
        log_container.add_widget(scroll)
        
        main_container.add_widget(log_container)
        self.add_widget(main_container)

    def create_label(self, text):
        """Create a simple white text label"""
        return Label(
            text=text,
            font_size='14sp',
            bold=True,
            size_hint_y=None,
            height=25,
            halign="left",
            color=(1, 1, 1, 1)  # White text
        )

    def create_input(self, hint, input_filter=None):
        """Create a simple gray input field with white text, no borders or shadows"""
        text_input = TextInput(
            hint_text=hint,
            multiline=False,
            size_hint_y=None,
            height=42,
            padding=[15, 11],
            font_size='15sp',
            background_color=(0.25, 0.25, 0.28, 1),  # Simple gray background
            foreground_color=(1, 1, 1, 1),  # White text
            cursor_color=(0.1, 0.5, 0.9, 1),  # Blue cursor
            input_filter=input_filter,
            background_normal='',  # Remove default background
            background_active=''   # Remove default active background
        )
        return text_input

    def create_spinner(self):
        """Create a simple gray dropdown with white text, no borders or shadows"""
        spinner = Spinner(
            text="Computer",
            values=("Hand", "Computer"),
            size_hint_y=None,
            height=42,
            background_color=(0.25, 0.25, 0.28, 1),  # Simple gray background
            color=(1, 1, 1, 1),  # White text
            font_size='15sp',
            background_normal='',
            background_down=''
        )
        return spinner

    def create_button(self, text, color):
        """Create a button with rounded corners"""
        button = Button(
            text=text,
            size_hint_y=None,
            height=55,
            font_size='18sp',
            bold=True,
            background_color=(0, 0, 0, 0),  # Transparent to use canvas
            color=(1, 1, 1, 1)  # White text
        )
        with button.canvas.before:
            Color(*color)
            button.bg_rect = RoundedRectangle(
                pos=button.pos,
                size=button.size,
                radius=[12]
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
        instance.text_size = (instance.width - 20, None)

    # ==========================================
    # BACKEND INTEGRATION POINT #1: START BUTTON
    # ==========================================
    def on_start(self, instance):
        """
        Called when the START button is pressed.
        This is where you initialize and start your backend process.
        """
        # Collect all input data
        data = {
            "url": self.url_input.text,
            "sleep_time": self.sleep_input.text,
            "task_count": self.count_input.text,
            "tasks_per_sleep": self.tasks_per_sleep_input.text,
            "method": self.method_spinner.text
        }
        
        # Validation
        if not self.url_input.text:
            self.update_log("ERROR: Target URL is required!")
            return
        
        if not self.sleep_input.text or not self.count_input.text:
            self.update_log("ERROR: Sleep time and task count are required!")
            return

        # ==========================================
        # 🔹 CALL YOUR BACKEND HERE 🔹
        # ==========================================
        # Option 1: Direct function call (if backend is in same file)
        # self.start_backend_process(data)
        
        # Option 2: Import and call from another module
        # from your_backend import start_tasks
        # start_tasks(data, callback=self.update_log)
        
        # Option 3: Using threading (recommended for long-running tasks)
        # import threading
        # self.backend_thread = threading.Thread(
        #     target=self.run_backend_tasks, 
        #     args=(data,),
        #     daemon=True
        # )
        # self.backend_thread.start()
        
        # Option 4: Using Kivy Clock for periodic tasks
        # from kivy.clock import Clock
        # self.task_event = Clock.schedule_interval(
        #     lambda dt: self.process_task(data), 
        #     int(data['sleep_time'])
        # )
        
        self.update_log(f"LAUNCH INITIATED")
        self.update_log(f"Configuration: {data}")

    # ==========================================
    # BACKEND INTEGRATION POINT #2: STOP BUTTON
    # ==========================================
    def on_stop(self, instance):
        """
        Called when the STOP button is pressed.
        This is where you stop/cancel your backend process.
        """
        # ==========================================
        # 🔹 STOP YOUR BACKEND HERE 🔹
        # ==========================================
        # Option 1: Set a stop flag
        # self.stop_flag = True
        
        # Option 2: Cancel scheduled events
        # if hasattr(self, 'task_event'):
        #     self.task_event.cancel()
        
        # Option 3: Call backend stop function
        # from your_backend import stop_tasks
        # stop_tasks()
        
        # Option 4: Wait for thread to finish (if using threading)
        # if hasattr(self, 'backend_thread') and self.backend_thread.is_alive():
        #     self.stop_flag = True
        #     self.backend_thread.join(timeout=5)
        
        self.update_log("MISSION ABORTED")

    # ==========================================
    # BACKEND INTEGRATION POINT #3: LOG UPDATES
    # ==========================================
    def update_log(self, message):
        """
        Call this method to update the mission log display.
        
        ⚠️ IMPORTANT: If calling from a background thread, use Clock.schedule_once:
        
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: ui_instance.update_log("Message"), 0)
        
        Args:
            message (str): The log message to display
        """
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_label.text += f"\n[{timestamp}] {message}"

    # ==========================================
    # EXAMPLE BACKEND INTEGRATION METHODS
    # ==========================================
    
    def run_backend_tasks(self, data):
        """
        Example method showing how to run backend tasks in a thread.
        Replace this with your actual backend logic.
        """
        from kivy.clock import Clock
        import time
        
        self.stop_flag = False
        task_count = int(data['task_count'])
        sleep_time = int(data['sleep_time'])
        tasks_per_sleep = int(data['tasks_per_sleep'])
        
        for i in range(task_count):
            if self.stop_flag:
                Clock.schedule_once(
                    lambda dt: self.update_log("Tasks stopped by user"), 0
                )
                break
            
            # Your actual task logic here
            # Example: make API call, process data, etc.
            
            Clock.schedule_once(
                lambda dt, num=i+1: self.update_log(f"Task {num}/{task_count} completed"), 0
            )
            
            if (i + 1) % tasks_per_sleep == 0:
                Clock.schedule_once(
                    lambda dt, s=sleep_time: self.update_log(f"Sleeping for {s} seconds..."), 0
                )
                time.sleep(sleep_time)
        
        Clock.schedule_once(
            lambda dt: self.update_log("All tasks completed!"), 0
        )


class RocketApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.05, 1)  # Match background
        Window.size = (1500, 1000)  # Increased height for better log visibility
        return RocketUI()


if __name__ == "__main__":
    RocketApp().run()