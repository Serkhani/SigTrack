from fpdf import FPDF, XPos, YPos

class CustomPDF(FPDF):
    
    def __init__(self, author, title):
        super().__init__()
        self.title= title
        self.author = author
        self.set_author(author)
        self.set_title(title)
    
    def header(self):
        self.set_font("Helvetica", 'B', 12)
        self.image("C:\\Users\\USER\\Desktop\\Sigtrack.jpg", x=20, y=10, w=20, keep_aspect_ratio=True)
        self.cell(0, 10, text=self.title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.cell(0, 10, text=f"Author: {self.author}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        self.line(20, self.get_y(), self.w-20, self.get_y())


    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", 'I', 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
