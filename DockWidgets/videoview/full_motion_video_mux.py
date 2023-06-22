import os
import subprocess
from PySide2.QtWidgets import  QDialog, QLineEdit, QPushButton, QFormLayout, QMessageBox, QHBoxLayout, QFileDialog

class Multiplexor(QDialog):
    def __init__(self, parent=None):
        super(Multiplexor, self).__init__(parent)
        
        self.video_line_edit = QLineEdit()
        self.log_line_edit = QLineEdit()
        self.output_dir_line_edit = QLineEdit()
        self.video_button = QPushButton("Select Video")
        self.log_button = QPushButton("Select Log")
        self.output_dir_button = QPushButton("Select Output Directory")
        self.start_button = QPushButton("Start")
        
        layout = QFormLayout()
        layout.addRow("Video File:", QHBoxLayout([self.video_line_edit, self.video_button]))
        layout.addRow("Log File:", QHBoxLayout([self.log_line_edit, self.log_button]))
        layout.addRow("Output Directory:", QHBoxLayout([self.output_dir_line_edit, self.output_dir_button]))
        layout.addRow("", self.start_button)
        
        self.setLayout(layout)
        
        self.video_button.clicked.connect(self.select_video_file)
        self.log_button.clicked.connect(self.select_log_file)
        self.output_dir_button.clicked.connect(self.select_output_dir)
        self.start_button.clicked.connect(self.start_conversion)
        
    def select_video_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Video Files (*.mp4 *.avi)")
        file_dialog.setWindowTitle("Select Video File")
        if file_dialog.exec_():
            video_file_path = file_dialog.selectedFiles()[0]
            self.video_line_edit.setText(video_file_path)
        
    def select_log_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Log Files (*.log)")
        file_dialog.setWindowTitle("Select Log File")
        if file_dialog.exec_():
            log_file_path = file_dialog.selectedFiles()[0]
            self.log_line_edit.setText(log_file_path)
        
    def select_output_dir(self):
        dir_dialog = QFileDialog(self)
        dir_dialog.setFileMode(QFileDialog.Directory)
        dir_dialog.setWindowTitle("Select Output Directory")
        if dir_dialog.exec_():
            output_dir_path = dir_dialog.selectedFiles()[0]
            self.output_dir_line_edit.setText(output_dir_path)
        
    def start_conversion(self):
        video_file = self.video_line_edit.text()
        log_file = self.log_line_edit.text()
        output_dir = self.output_dir_line_edit.text()
        
        if not os.path.isfile(video_file) or not os.path.isfile(log_file):
            QMessageBox.critical(self, "Error", "Invalid file path(s)!")
            return
        
        if not os.path.isdir(output_dir):
            QMessageBox.critical(self, "Error", "Invalid output directory!")
            return
        
        output_file = os.path.join(output_dir, "output.ts")  # Output file path
        
        # Run FFmpeg command to multiplex video and log file
        command = [
            "ffmpeg",
            "-i", video_file,
            "-i", log_file,
            "-c", "copy",
            output_file
        ]
        try:
            subprocess.run(command, check=True)
            QMessageBox.information(self, "Conversion Complete", "Video conversion completed successfully!")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Conversion failed: {e}")
        
        self.close()