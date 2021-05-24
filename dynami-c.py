import time
import subprocess
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="C4Z")

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        self.create_code_label()
        self.create_code_window()
        self.create_output_label()
        self.create_output_window()

        self.code_buffer = self.code_text.get_buffer()
        self.output_buffer = self.output_text.get_buffer()
        self.code_buffer.connect("notify::cursor-position", self.on_cursor_position_changed)

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        textview = Gtk.TextView()
        scrolledwindow.add(textview)
        return scrolledwindow, textview

    def create_code_window(self):
        self.code_window, self.code_text = self.create_textview()
        self.code_text.set_editable(True)
        self.box.pack_start(self.code_window, True, True, 0)

    def create_output_window(self):
        self.output_window, self.output_text = self.create_textview()
        self.output_text.set_editable(False)
        self.box.pack_start(self.output_window, True, True, 0)
    
    def create_code_label(self):
        self.code_label = Gtk.Label()
        self.code_label.set_text("CODE:")
        self.box.pack_start(self.code_label, False, False, 0)

    def create_output_label(self):
        self.output_label = Gtk.Label()
        self.output_label.set_text("OUTPUT:")
        self.box.pack_start(self.output_label, False, False, 0)


    def get_code(self):
        start_iter = self.code_buffer.get_start_iter()
        end_iter = self.code_buffer.get_end_iter()
        text = self.code_buffer.get_text(start_iter, end_iter, True)
        return text
    
    def on_cursor_position_changed(self, buffer, data=None):
        save_code(self.get_code())
        process = subprocess.Popen(['gcc', '/tmp/program.c', '-o', '/tmp/a.out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.output_label.set_text("ERROR:")
        self.output_buffer.set_text(stderr.decode("utf-8"))
        if not stderr:
            process = subprocess.Popen(['/tmp/a.out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()
            self.output_label.set_text("OUTPUT:")
            self.output_buffer.set_text(output.decode("utf-8"))



def save_code(code):
    code_file = open("/tmp/program.c", "w")
    code_file.write(code)
    code_file.close()


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
