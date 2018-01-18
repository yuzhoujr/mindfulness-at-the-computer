import os
import logging
import mc.model
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mc import model, mc_global
import mc.gui.breathing_dlg

NEXT_STR = "Next >>"


class IntroDlg(QtWidgets.QDialog):
    close_signal = QtCore.pyqtSignal(bool)
    # -the boolean indicates whether or not we want the breathing dialog to open

    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 550, 450)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)
        self.wizard_qsw_w3 = QtWidgets.QStackedWidget()
        vbox_l2.addWidget(self.wizard_qsw_w3)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        hbox_l3.addStretch(1)
        self.prev_qpb = QtWidgets.QPushButton("<< Prev")
        hbox_l3.addWidget(self.prev_qpb, stretch=1)
        self.prev_qpb.clicked.connect(self.on_prev_clicked)
        self.next_qpb = QtWidgets.QPushButton(NEXT_STR)
        hbox_l3.addWidget(self.next_qpb, stretch=1)
        hbox_l3.addStretch(1)
        self.next_qpb.clicked.connect(self.on_next_clicked)
        """
        self.close_qpb = QtWidgets.QPushButton("Close")
        hbox_l3.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_clicked)
        """

        self.info = InformationPage()
        self.wizard_qsw_w3.addWidget(self.info)

        self.initial_setup = BreathingInitSetupPage()
        self.wizard_qsw_w3.addWidget(self.initial_setup)

        self.breathing_dialog_coming = BreathingDialogComing()
        self.wizard_qsw_w3.addWidget(self.breathing_dialog_coming)

        """
        self.wizard_qll = QtWidgets.QLabel(self.tr("3. Please choose your initial settings"))
        vbox_l2.addWidget(self.wizard_qll)
        self.setting_example_interval_qsb = QtWidgets.QSpinBox()
        vbox_l2.addWidget(self.setting_example_interval_qsb)
        self.setting_example_audio_qcb = QtWidgets.QCheckBox("Audio active")
        vbox_l2.addWidget(self.setting_example_audio_qcb)

        vbox_l2.addSpacing(40)

        self.close_qpb = QtWidgets.QPushButton("Close")
        vbox_l2.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_clicked)
        """

        self.update_gui()

        # self.setup_rest_action_list()
        self.show()

    def on_close_clicked(self):
        self.close_signal.emit(False)
        self.close()

    def on_next_clicked(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        if current_index_int >= self.wizard_qsw_w3.count() - 1:
            self.close_signal.emit(True)
            self.close()
        logging.debug("current_index_int = " + str(current_index_int))
        self.wizard_qsw_w3.setCurrentIndex(current_index_int + 1)
        self.update_gui()

    def on_prev_clicked(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        if current_index_int <= 0:
            return
        logging.debug("current_index_int = " + str(current_index_int))
        self.wizard_qsw_w3.setCurrentIndex(current_index_int - 1)
        self.update_gui()

    def update_gui(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        self.prev_qpb.setDisabled(current_index_int == 0)

        if current_index_int == self.wizard_qsw_w3.count() - 1:
            self.next_qpb.setText("Finish")  # "open breathing dialog"
        else:
            self.next_qpb.setText(NEXT_STR)


class InformationPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.title_qll = QtWidgets.QLabel("Introduction")
        self.title_qll.setFont(mc.mc_global.get_font_large())
        vbox_l2.addWidget(self.title_qll)

        vbox_l2.addStretch(1)

        self.text_qll = QtWidgets.QLabel('''
Welcome! Please take a few moments to set read about and up the application. Or you can skip and return to this wizard later by going to "help" -> "setup wizard"
''')
        self.text_qll.setWordWrap(True)
        vbox_l2.addWidget(self.text_qll)

        vbox_l2.addStretch(1)


class BreathingDialogComing(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.title_qll = QtWidgets.QLabel("Breathing Dialog")
        self.title_qll.setFont(mc.mc_global.get_font_large())
        vbox_l2.addWidget(self.title_qll)

        vbox_l2.addStretch(1)

        self.text_qll = QtWidgets.QLabel('''
When you click on finish a breathing dialog will be shown. You can use it by ______ or using the keyboard
''')
        self.text_qll.setWordWrap(True)
        vbox_l2.addWidget(self.text_qll)

        vbox_l2.addStretch(1)


class BreathingInitSetupPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.title_qll = QtWidgets.QLabel("Initial setup (breathing)")
        self.title_qll.setFont(mc.mc_global.get_font_large())
        vbox_l2.addWidget(self.title_qll)

        vbox_l2.addStretch(1)

        self.text_qll = QtWidgets.QLabel("Please select the intial setup parameters for the breathing. (Or use the default values)")
        self.text_qll.setWordWrap(True)
        vbox_l2.addWidget(self.text_qll)

        vbox_l2.addStretch(1)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        hbox_l3.addWidget(QtWidgets.QLabel("Time between breathing notifications"))
        self.time_btw_notifications_qsb = QtWidgets.QSpinBox()
        hbox_l3.addWidget(self.time_btw_notifications_qsb)
        self.time_btw_notifications_qsb.valueChanged.connect(self.on_time_btw_notifications_valuechanged)

        vbox_l2.addStretch(1)

        """
        self.play_audio_qcb = QtWidgets.QCheckBox("Play Audio")
        vbox_l2.addWidget(self.play_audio_qcb)
        self.play_audio_qcb.toggled.connect(self.on_play_audio_toggled)
        """

    def on_time_btw_notifications_valuechanged(self, i_new_value: int):
        logging.debug("on_time_btw_notifications_valuechanged, i_new_value = " + str(i_new_value))
        mc.model.SettingsM.update_breathing_reminder_interval(i_new_value)

    def on_play_audio_toggled(self, i_checked: bool):
        mc.model.SettingsM.update_breathing_dialog_audio_active(i_checked)
        if not mc.model.SettingsM.get().breathing_reminder_audio_path_str:
            mc.model.SettingsM.update_breathing_reminder_audio_path("small_bell_long[cc0].wav")

