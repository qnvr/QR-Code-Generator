import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt  # Import Qt from PyQt5.QtCore
from PyQt5.QtGui import QImage, QPixmap, QClipboard
import qrcode
from io import BytesIO

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QR Code Generator | NVR')
        self.setFixedSize(400, 200)  # Set a fixed size for the window
        self.setStyleSheet("background-color: #424242; color: #ffffff;")  # Set background color and text color

        layout = QVBoxLayout(self)

        self.data_input = QLineEdit(self)
        layout.addWidget(QLabel('Enter the data to encode:', self))
        layout.addWidget(self.data_input)

        self.file_name_input = QLineEdit(self)
        layout.addWidget(QLabel('Enter the file name (with extension):', self))
        layout.addWidget(self.file_name_input)

        generate_button = QPushButton('Generate QR Code', self)
        generate_button.clicked.connect(self.generateQRCode)
        generate_button.setStyleSheet("""
            QPushButton {
                background-color: #87CEFA; /* Pastel faded blue background */
                color: #000000; /* Black text color */
                border-radius: 20px; /* Rounded corners */
                padding: 10px 20px; /* Add padding */
            }
        """)
        layout.addWidget(generate_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def generateQRCode(self):
        data = self.data_input.text()
        file_name = self.file_name_input.text()

        if data and file_name:
            try:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10,
                    border=4,
                )
                qr.add_data(data)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                
                # Save the QR code image to BytesIO
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)

                # Convert BytesIO to QPixmap
                pixmap = QPixmap()
                pixmap.loadFromData(buffer.getvalue())

                # Copy the QR code image to clipboard
                clipboard = QApplication.clipboard()
                clipboard.setPixmap(pixmap)

                QMessageBox.information(self, 'Success', f'QR code generated successfully and copied to clipboard.')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'An error occurred: {str(e)}')
        else:
            QMessageBox.warning(self, 'Error', 'Please enter both data and file name.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QRCodeGenerator()
    window.show()
    sys.exit(app.exec_())
