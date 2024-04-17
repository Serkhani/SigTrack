from sigtrack.models.image_models.pdfgen.reportGenModel import ReportGenModel
from sigtrack.views.imageview.report_window_view import ReportWindowView


class ReportGenCon:
    def __init__(self, viewer):
        self.image_viewer = viewer
        self.model = ReportGenModel()
        self.view = ReportWindowView()
        self.view.save_pdf_button.clicked.connect(self.select_save_path)
        # self.view.report_path_button.clicked.connect(self.getImage)
        self.view.save_button.clicked.connect(self.save_pdf)
    
    def select_save_path(self):
        self.model.select_path()
        self.view.save_pdf_path_label.setText(f"Path to Save PDF: {self.model.save_path}")
        
        
    def save_pdf(self):
        self.model.author = self.view.author_input.text()
        self.model.content = self.view.content_input.toPlainText()
        self.model.title = self.view.title_input.text()
        self.model.save_pdf(self.image_viewer)
        self.view.close()