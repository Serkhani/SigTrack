from PySide2.QtWidgets import QFileDialog, QWidget, QMessageBox
from sigtrack.models.image_models.pdfgen.custompdf import CustomPDF
from PIL import ImageQt

class ReportGenModel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.save_path = None
        self.author = None
        self.title = None
        self.content = None

    # def getImage(self):
    #     path = QFileDialog.getOpenFileName(
    #         self,
    #         caption="Select image(s)",
    #         dir="C:\\Users\\LENOVO\\Desktop",
    #         filter="Image (*.jpg)",
    #     )
    #     if path[0]:
    #         self.image_path.setText(path[0])

    def select_path(self):
        path = QFileDialog.getSaveFileName(self, 'Save PDF', '', 'PDF files (*.pdf)')
        if path[0]:
            self.save_path = (path[0])


    def save_pdf(self, image_viewer):
        if self.save_path:
            pdf = CustomPDF(self.author, self.title)
            pdf.set_margin(20)
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save Image",
                f'edit_{image_viewer.imgPath.split("/")[-1]}',
                "Images (*.png *.xpm *.bmp)",
            )
            if file_name:
                if not file_name.endswith('.jpg'): 
                    image = ImageQt.fromqpixmap(image_viewer.grab())
                    image.save(file_name)
                    width = 0.7 * pdf.w
                    pdf.image(file_name, x=0.15*width+10, y=pdf.get_y()+10, w=width, keep_aspect_ratio=True)
                else:
                    QMessageBox.warning(self, "Error", "Saving as .jpg is not allowed.", QMessageBox.Ok)
                    return
                    
            pdf.set_y(pdf.get_y() + 100)
            # Content
            pdf.multi_cell(0, 10, text=self.content)

            pdf.output(self.save_path)
            return 
    
    # def get_image(self):
        # path = QFileDialog.getOpenFileName(
        #     self.view,
        #     caption="Select image(s)",
        #     dir="C:\\Users\\LENOVO\\Desktop",
        #     filter="Image (*.jpg)",
        # )
        # if path[0]:
        #     self.view.report_img_path.setText(path[0])
        #     self.model.image_path = path[0]
        # pass

    # def select_path(self):
    #     path = QFileDialog.getSaveFileName(self.view, 'Save PDF', '', 'PDF files (*.pdf)')
    #     if path[0]:
    #         self.view.path_input.setText(path[0])
    #         self.model.path = path[0]
    
    
#     def save_pdf(self):
#         path = self.view.path_input.text()
#         author = self.view.author_input.text()
#         title = self.view.title_input.text()
#         content = self.view.content_input.toPlainText()
#         image = self.view.report_img_path.text()

#         # pdf = CustomPDF(author, title)
#         # pdf.set_margin(20)
#         # pdf.add_page()
#         # pdf.set_font("Helvetica", size=12)
#         # if image:
#         #     width = 0.7 * pdf.w
#         #     pdf.image(image, x=0.15*width+10, y=pdf.get_y()+10, w=width, keep_aspect_ratio=True)
#         # pdf.set_y(pdf.get_y() + 100)
#         # pdf.multi_cell(0, 10, text=content)
#         # pdf.output(path)
#         # self.close()
#         # path = self.path_input.text()
#         path = "C:\\Users\\USER\\Desktop\\out.pdf"
#         # author = self.author_input.text()
#         author = "serkhani"
#         # title = self.title_input.text()
#         title = "The Quest"
#         # content = self.content_input.toPlainText()
#         content = """What is Lorem Ipsum?
# Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

# Why do we use it?
# It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).


# Where does it come from?
# Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.

# The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham."
# """
#         # image = self.report_img_path.text()
#         image = "C:\\Users\\USER\\Documents\\Image Support Type\\20230414_115705147.jpg"

#         pdf = CustomPDF(author, title)
#         pdf.set_margin(20)
#         pdf.add_page()
#         pdf.set_font("Helvetica", size=12)
#         if image:
#             width = 0.7 * pdf.w
#             pdf.image(image, x=0.15*width+10, y=pdf.get_y()+10, w=width, keep_aspect_ratio=True)
#         pdf.set_y(pdf.get_y() + 100)
#         # Content
#         pdf.multi_cell(0, 10, text=content)

#         pdf.output(path)
#         self.close()
