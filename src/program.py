

# images processing
import cv2
# matrix processing
import numpy as np
# others
import sys

# GUI
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import SimpleITK as sitk

import logging
import os
import time

date_strftime_format = "%d-%b-%y %H:%M:%S"
message_format = "[%(asctime)s]  %(message)s"
logging.basicConfig(level=logging.INFO, format=message_format, datefmt=date_strftime_format, encoding='utf-8')

keydict = {"0018|1111":"Distance Source to Patient","0018|1147":"Field of View Shape","0018|1149":"Field of View Dimensions","0028|0030":"Pixel Spacing","0028|0106":"Smallest Image Pixel Value","0028|0107":"Largest Image Pixel Value","0028|0A02":"Pixel Spacing Calibration Type","0028|1052":"Rescale Intercept","0028|1053":"Rescale Slope","0028|1054":"Rescale Type","0008|002A":"Acquisition DateTime","0008|0060":"Modality","0008|0070":"Manufacturer","0008|1030":"Study Description","0008|103E":"Series Description","0010|0020":"Patient ID","0010|0040":"Patient's Sex","0010|1010":"Patient's Age","0018|0015":"Body Part Examined","0018|1000":"Device Serial Number","0018|1050":"Spatial Resolution","0018|1164":"Imager Pixel Spacing","0018|5101":"View Position","0020|0060":"Laterality","0028|0004":"Photometric Interpretation","0028|0010":"Rows","0028|0011":"Columns","0028|0034":"Pixel Aspect Ratio"}

class thread(QThread):
    log = pyqtSignal(str)

    def __init__(self, sitk_img, parent=None):
        QThread.__init__(self, parent)
        self.loaded_sitk = sitk_img

    def run(self) -> None:
        time.sleep(.5)
        # try:
        dcm_attr = list(self.loaded_sitk.GetMetaDataKeys())
        
        truth = 0
        false = 0

        for metadata in ["0008|002A","0008|0060","0008|0070","0008|1030","0008|103E","0010|0020","0010|0040","0010|1010","0018|0015","0018|1000","0018|1147","0018|1149","0018|1164","0018|5101","0020|0060","0028|0004","0028|0010","0028|0011","0028|0030","0028|0106","0028|0107"]:
            if metadata in dcm_attr and self.loaded_sitk.GetMetaData(metadata) != "":
                data = self.loaded_sitk.GetMetaData(metadata)
                # self.logTextBox.texteditor.append(metadata+f"({keydict[metadata]}) " + data)
                # logging.info(f"{keydict[metadata]}.....True")
                self.log.emit(f"{keydict[metadata]}.....True_{data}")
                truth += 1
            else:
                # self.logTextBox.texteditor.append(metadata+f"({keydict[metadata]})")
                # logging.info(f"{keydict[metadata]}.....False")
                self.log.emit(f"{keydict[metadata]}.....False")
                # self.logTextBox.texteditor.setHtml("<font color='red' size='6'><red>Hello PyQt5!\nHello</font>")
                false += 1
            time.sleep(.2)

        self.log.emit(f"**Done**_{truth}_{false}")


class QTextEditLogger(logging.Handler):

    def __init__(self, parent):
        super().__init__()
        self.texteditor = QTextEdit(parent)
        self.texteditor.setFixedWidth(400)
        self.texteditor.setReadOnly(True)
        self.texteditor.setPlainText("Welcome to X-ray DICOM Checker!\n")


    def emit(self, record):
        msg = self.format(record)
        self.texteditor.append(msg)
        self.texteditor.ensureCursorVisible()
        self.texteditor.viewport().update()

class MyApp(QWidget):
    sig = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.item_dict = dict()
        self.missingItem = []

        self.initUI()

    def initUI(self):
        ack_txt = " \n\nDICOM Checker\n\n version: 1.0.0 (update: November 11, 2022)\n\n- This program is used to estimate your DICOM file and give a score based on the most\n  important 21 features in DICOM header. Data type and data range will be considered\n in the test. \n - If a score of dicom file is lower then 90, this DICOM file may cause \n trouble to your research.\n\n This program made by Yonsei Boncentricq Team\n\n\n Funding:\n\n a grant of the Korea Health Technology R&D Project through the Korea Health Industry\n Development Institute (KHIDI), funded by the Ministry of Health & Welfare, \n Republic of Korea (HI22C0452)"
        self.lbl_img = QLabel(ack_txt)
        self.lbl_img.setAlignment(Qt.AlignLeft)

        self.upload_btn = QPushButton("Load a dcm file",self)
        self.upload_btn.clicked.connect(self.btn_fun_FileLoad)

        self.analyze_btn = QPushButton("Analyze",self)
        self.analyze_btn.clicked.connect(self.btn_fun_Analyze)
        self.analyze_btn.setEnabled(False)

        self.logTextBox = QTextEditLogger(self)
        self.logTextBox.setFormatter(logging.Formatter(message_format,"%Y-%m-%d %H:%M:%S"))
        logging.getLogger().addHandler(self.logTextBox)
        logging.getLogger().setLevel(logging.INFO)

        # self.ui.sub_widget = SubWidget()

        vbox = QGridLayout()
        vbox.addWidget(self.lbl_img,0,0)
        vbox.addWidget(self.upload_btn,2,0)
        vbox.addWidget(self.logTextBox.texteditor,0,1,2,1)
        vbox.addWidget(self.analyze_btn,2,1)
        self.setLayout(vbox)


        self.setFixedSize(1000, 600)
        self.setMouseTracking(False)
        self.setWindowTitle('DICOM Checker - Bonecentricq')
        self.move(300, 300)

        self.show()

    # thread log 처리기
    @pyqtSlot(str)
    def appendLog(self, string):
        if "**Done**" not in string:
            if "....True" in string:
                self.item_dict[string.split(".....")[0]] = string.split("True_")[1]
                self.logTextBox.texteditor.append(" - "+string.split("True_")[0]+"True")
                self.logTextBox.texteditor.viewport().update()

            else:
                self.missingItem.append(string.split(".....")[0])
                self.logTextBox.texteditor.append(" - "+string)
                self.logTextBox.texteditor.viewport().update()

        else:
            truth = float(string.split("_")[1])
            false = int(string.split("_")[-1])

            self.show_popup(truth,false)

            # self.logTextBox.texteditor.append(str(truth/21))
            self.logTextBox.texteditor.append(f"\n ** Curation score : {int((truth/21)*100)} / 100")
            self.logTextBox.texteditor.append(f" ** This dicom file has {false} missing values\n")

            self.logTextBox.texteditor.append("\n".join([ " - "+i+": -" for i in self.missingItem])+"\n")
            self.logTextBox.texteditor.viewport().update()
            
            logging.info('Success to analyze dicom metadatas')
            self.logTextBox.texteditor.viewport().update()

            self.upload_btn.setEnabled(True)
            self.analyze_btn.setEnabled(False)

    def show_popup(self,truth,false):
        msg = QMessageBox()
        msg.setWindowTitle("Dicom analysis results")
        msg.setText(f"- Analysis reports\n Curation score : {int((truth/21)*100)} / 100\n This dicom file has {false} missing values")
        msg.setIcon(QMessageBox.Information)
        txt = "* Missing value\n" +"\n".join([ " - "+i+": -" for i in self.missingItem])
        txt += "\n" + "="*20 + "\n"
        txt += "\n".join([f" - {key}:{value}" for key, value in self.item_dict.items()])
        msg.setDetailedText(txt)
        x = msg.exec_() 


    # upload file
    def btn_fun_FileLoad(self):        
        fname=QFileDialog.getOpenFileName(self,filter="Dicom file(*.dcm)")

        logging.info(f'Start to upload a DICOM file : {os.path.basename(fname[0])}')

        try:
            self.imagename = fname[0]
            # self.loaded_image = cv2.imread(self.imagename,0)
            self.loaded_sitk = sitk.ReadImage(self.imagename)
            self.loaded_image = sitk.GetArrayFromImage(self.loaded_sitk)[0]
            # image = (np.clip(self.loaded_image,0,255)).astype(np.uint8)
                
            image = ((self.loaded_image - self.loaded_image.min()) / (self.loaded_image.max() - self.loaded_image.min()) *255).astype(np.uint8)

            qim = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_Indexed8)
            pixmap = QPixmap.fromImage(qim).scaledToWidth(500) 
            self.lbl_img.setPixmap(pixmap)

            logging.info(f'Success to upload a DICOM file : {os.path.basename(fname[0])}')

            self.upload_btn.setEnabled(False)
            self.analyze_btn.setEnabled(True)

        except:
            logging.info(f'Fail to load a DICOM file : {os.path.basename(fname[0])}')
            logging.info(f'Please check your dicom file')


    # Analyzer
    def btn_fun_Analyze(self):        

        logging.info(f'Start to analyze dicom metadatas')
        
        # inactive btn
        self.analyze_btn.setEnabled(False)
        
        # start thread
        self.thread_str = thread(self.loaded_sitk)
        self.thread_str.start()
        self.thread_str.log.connect(self.appendLog)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())