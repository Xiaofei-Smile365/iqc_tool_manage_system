# -*- coding: UTF-8 -*-

"""

@Project Name: IQC_Manage_System
@File Name:    iqc_tool_manage_system

@User:         smile
@Author:       Smile
@Email:        Xiaofei.Smile365@Gmail.com

@Date Time:    2021/4/26 17:13
@IDE:          PyCharm
@Source  : python3 -m pip install *** -i https://pypi.tuna.tsinghua.edu.cn/simple

@程式功能简介：
此程式用于对IQC治具进行统一管理和调配；
1. 建立UI界面
2. 编写相应的功能模块

"""
import datetime
import sys  # 载入必需的模块
import os
import time

from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

import pandas as pd
import numpy as np
import csv


# noinspection PyAttributeOutsideInit
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.screen = QDesktopWidget().screenGeometry()

        self.resize(1024, 600)
        self.setWindowIcon(QIcon('./source_file/platform.ico'))
        self.setWindowTitle("IQC-治具管理平台")

        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background,
                              QBrush(QPixmap('./source_file/background.jpg').scaled(self.width(), self.height())))
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)

        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2, (self.screen.height() - self.size.height()) / 2)

        self.status = self.statusBar()

        self.setFixedSize(1024, 600)

        self.label_set()
        self.layout_set()

        self.qtm_real_time = QtCore.QTimer()
        self.qtm_real_time.timeout.connect(self.real_time)
        self.qtm_real_time.start(1000)

        self.main_frame = QWidget()
        self.main_frame.setLayout(self.layout_v_windows)
        self.setCentralWidget(self.main_frame)

        self.check_database()

        self.status.showMessage("The IQC Tool Manage System Starting", 2000)
        self.label_title.setFocus()

    def label_set(self):
        self.label_title = QLabel()
        self.label_title.setFocus()
        self.label_title.setText("<b>IQC 治具智能管理平台<b>")
        self.label_title.setFont(QFont("SanSerif", 24))
        self.label_title.setStyleSheet("Color: RGB(64, 224, 208)")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setFixedSize(400, 80)
        self.layout_h_label_title = QHBoxLayout()
        self.layout_h_label_title.addWidget(self.label_title)

        self.label_designer = QLabel()
        self.label_designer.setText("Developer:AUO")
        self.label_designer.setFont(QFont("SanSerif", 10))
        self.label_designer.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_designer.setAlignment(Qt.AlignRight)
        self.label_designer.setFixedSize(130, 20)
        self.layout_h_label_designer = QHBoxLayout()
        self.layout_h_label_designer.addWidget(self.label_designer)

        self.label_time = QLabel()
        self.label_time.setText("1997/01/01 00:00:00")
        self.label_time.setFont(QFont("SanSerif", 10))
        self.label_time.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_time.setAlignment(Qt.AlignLeft)
        self.label_time.setFixedSize(150, 20)
        self.layout_h_label_time = QHBoxLayout()
        self.layout_h_label_time.addWidget(self.label_time)

        self.label_search_program = QLabel()
        self.label_search_program.setText("<b>* 查询功能<b>")
        self.label_search_program.setFont(QFont("SanSerif", 12))
        self.label_search_program.setStyleSheet("Color: RGB(64, 224, 208)")
        self.label_search_program.setAlignment(Qt.AlignLeft)
        self.label_search_program.setFixedSize(900, 20)
        self.layout_h_label_search_program = QHBoxLayout()
        self.layout_h_label_search_program.addWidget(self.label_search_program)

        self.label_search_item = QLabel()
        self.label_search_item.setText("查询项目：")
        self.label_search_item.setFont(QFont("SanSerif", 10))
        self.label_search_item.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_search_item.setAlignment(Qt.AlignRight)
        self.label_search_item.setFixedSize(70, 13)
        self.layout_h_label_search_item = QHBoxLayout()
        self.layout_h_label_search_item.addWidget(self.label_search_item)

        self.combox_search_item = QComboBox()
        self.combox_search_item.addItems(['in.csv', 'out.csv', 'delete.csv'])
        self.combox_search_item.setFont(QFont("SanSerif", 10))
        self.combox_search_item.setStyleSheet("Color: RGB(128, 128, 0)")
        self.combox_search_item.setFixedSize(100, 20)
        self.search_file_path = './database/in.csv'
        self.combox_search_item.currentTextChanged[str].connect(self.change_search_item)
        self.layout_h_combox_search_item = QHBoxLayout()
        self.layout_h_combox_search_item.addWidget(self.combox_search_item)

        self.layout_h_search_label_item = QHBoxLayout()
        self.layout_h_search_label_item.addLayout(self.layout_h_label_search_item)
        self.layout_h_search_label_item.addLayout(self.layout_h_combox_search_item)
        self.layout_h_search_label_item.addStretch(1)

        self.label_tool_id = QLabel()
        self.label_tool_id.setText("治具编号：")
        self.label_tool_id.setFont(QFont("SanSerif", 10))
        self.label_tool_id.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_tool_id.setAlignment(Qt.AlignRight)
        self.label_tool_id.setFixedSize(70, 13)
        self.layout_h_label_tool_id = QHBoxLayout()
        self.layout_h_label_tool_id.addWidget(self.label_tool_id)

        self.line_tool_id = QLineEdit()
        self.line_tool_id.setAlignment(Qt.AlignLeft)
        self.line_tool_id.setPlaceholderText("请输入治具编号...")
        self.line_tool_id.setFont(QFont("微软雅黑", 8))
        self.line_tool_id.setFixedSize(120, 18)
        self.layout_h_line_tool_id = QHBoxLayout()
        self.layout_h_line_tool_id.addWidget(self.line_tool_id)

        self.layout_h_tool_id = QHBoxLayout()
        self.layout_h_tool_id.addLayout(self.layout_h_label_tool_id)
        self.layout_h_tool_id.addLayout(self.layout_h_line_tool_id)
        self.layout_h_tool_id.addStretch(1)

        self.label_tool_name = QLabel()
        self.label_tool_name.setText("治具名称：")
        self.label_tool_name.setFont(QFont("SanSerif", 10))
        self.label_tool_name.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_tool_name.setAlignment(Qt.AlignRight)
        self.label_tool_name.setFixedSize(70, 13)
        self.layout_h_label_tool_name = QHBoxLayout()
        self.layout_h_label_tool_name.addWidget(self.label_tool_name)

        self.line_tool_name = QLineEdit()
        self.line_tool_name.setAlignment(Qt.AlignLeft)
        self.line_tool_name.setPlaceholderText("请输入治具名称...")
        self.line_tool_name.setFont(QFont("微软雅黑", 8))
        self.line_tool_name.setFixedSize(120, 18)
        self.layout_h_line_tool_name = QHBoxLayout()
        self.layout_h_line_tool_name.addWidget(self.line_tool_name)

        self.layout_h_tool_name = QHBoxLayout()
        self.layout_h_tool_name.addLayout(self.layout_h_label_tool_name)
        self.layout_h_tool_name.addLayout(self.layout_h_line_tool_name)
        self.layout_h_tool_name.addStretch(1)

        self.button_search = QPushButton()
        self.button_search.setIcon(QIcon("source_file/search_model.png"))
        self.button_search.setText("查询")
        self.button_search.setToolTip("查询范围：治具编号&名称为空时，默认显示所有治具。")
        self.button_search.clicked.connect(self.show_tool)
        self.button_search.setFont(QFont("微软雅黑", 10))
        self.button_search.setFixedSize(150, 30)
        self.layout_button_search = QHBoxLayout()
        self.layout_button_search.addWidget(self.button_search)

        self.button_cancel = QPushButton()
        self.button_cancel.setText("取消")
        self.button_cancel.setToolTip("按钮功能：取消此次查询，并清空已输入关键字。")
        self.button_cancel.clicked.connect(self.cancel_search)
        self.button_cancel.setFont(QFont("微软雅黑", 10))
        self.button_cancel.setFixedSize(100, 30)
        self.layout_button_cancel = QHBoxLayout()
        self.layout_button_cancel.addWidget(self.button_cancel)

        self.label_borrow_program = QLabel()
        self.label_borrow_program.setText("<b>1.借用功能<b>")
        self.label_borrow_program.setFont(QFont("SanSerif", 12))
        self.label_borrow_program.setStyleSheet("Color: RGB(64, 224, 208)")
        self.label_borrow_program.setAlignment(Qt.AlignLeft)
        self.label_borrow_program.setFixedSize(220, 20)
        self.layout_h_label_borrow_program = QHBoxLayout()
        self.layout_h_label_borrow_program.addWidget(self.label_borrow_program)

        self.label_borrow_tool_id = QLabel()
        self.label_borrow_tool_id.setText("治具编号：")
        self.label_borrow_tool_id.setFont(QFont("SanSerif", 10))
        self.label_borrow_tool_id.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_borrow_tool_id.setAlignment(Qt.AlignRight)
        self.label_borrow_tool_id.setFixedSize(100, 13)
        self.layout_h_label_borrow_tool_id = QHBoxLayout()
        self.layout_h_label_borrow_tool_id.addWidget(self.label_borrow_tool_id)

        self.line_borrow_tool_id = QLineEdit()
        self.line_borrow_tool_id.setAlignment(Qt.AlignLeft)
        self.line_borrow_tool_id.setPlaceholderText("请输入治具编号...")
        self.line_borrow_tool_id.setFont(QFont("微软雅黑", 8))
        self.line_borrow_tool_id.setFixedSize(120, 18)
        self.layout_h_line_borrow_tool_id = QHBoxLayout()
        self.layout_h_line_borrow_tool_id.addWidget(self.line_borrow_tool_id)

        self.layout_h_borrow_tool_id = QHBoxLayout()
        self.layout_h_borrow_tool_id.addLayout(self.layout_h_label_borrow_tool_id)
        self.layout_h_borrow_tool_id.addLayout(self.layout_h_line_borrow_tool_id)

        self.label_borrow_person = QLabel()
        self.label_borrow_person.setText("借用人员：")
        self.label_borrow_person.setFont(QFont("SanSerif", 10))
        self.label_borrow_person.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_borrow_person.setAlignment(Qt.AlignRight)
        self.label_borrow_person.setFixedSize(100, 13)
        self.layout_h_label_borrow_person = QHBoxLayout()
        self.layout_h_label_borrow_person.addWidget(self.label_borrow_person)

        self.line_borrow_person = QLineEdit()
        self.line_borrow_person.setAlignment(Qt.AlignLeft)
        self.line_borrow_person.setPlaceholderText("请输入人员工号...")
        self.line_borrow_person.setFont(QFont("微软雅黑", 8))
        self.line_borrow_person.setFixedSize(120, 18)
        self.layout_h_line_borrow_person = QHBoxLayout()
        self.layout_h_line_borrow_person.addWidget(self.line_borrow_person)

        self.layout_h_borrow_person = QHBoxLayout()
        self.layout_h_borrow_person.addLayout(self.layout_h_label_borrow_person)
        self.layout_h_borrow_person.addLayout(self.layout_h_line_borrow_person)

        self.button_borrow = QPushButton()
        self.button_borrow.setText("确认借用")
        self.button_borrow.clicked.connect(self.borrow)
        self.button_borrow.setFont(QFont("微软雅黑", 10))
        self.button_borrow.setFixedSize(80, 30)
        self.layout_button_borrow = QHBoxLayout()
        self.layout_button_borrow.addWidget(self.button_borrow)

        self.button_borrow_cancel = QPushButton()
        self.button_borrow_cancel.setText("取消")
        self.button_borrow_cancel.clicked.connect(self.borrow_cancel)
        self.button_borrow_cancel.setFont(QFont("微软雅黑", 10))
        self.button_borrow_cancel.setFixedSize(60, 30)
        self.layout_button_borrow_cancel = QHBoxLayout()
        self.layout_button_borrow_cancel.addWidget(self.button_borrow_cancel)

        self.layout_h_borrow_cancel = QHBoxLayout()
        # self.layout_h_borrow_cancel.addStretch(1)
        self.layout_h_borrow_cancel.addLayout(self.layout_button_borrow)
        self.layout_h_borrow_cancel.addLayout(self.layout_button_borrow_cancel)
        # self.layout_h_borrow_cancel.addStretch(1)

        self.layout_v_borrow = QVBoxLayout()
        self.layout_v_borrow.addLayout(self.layout_h_label_borrow_program)
        self.layout_v_borrow.addLayout(self.layout_h_borrow_tool_id)
        self.layout_v_borrow.addLayout(self.layout_h_borrow_person)
        self.layout_v_borrow.addLayout(self.layout_h_borrow_cancel)

        self.label_return_program = QLabel()
        self.label_return_program.setText("<b>2.归还功能<b>")
        self.label_return_program.setFont(QFont("SanSerif", 12))
        self.label_return_program.setStyleSheet("Color: RGB(64, 224, 208)")
        self.label_return_program.setAlignment(Qt.AlignLeft)
        self.label_return_program.setFixedSize(220, 20)
        self.layout_h_label_return_program = QHBoxLayout()
        self.layout_h_label_return_program.addWidget(self.label_return_program)

        self.label_return_tool_id = QLabel()
        self.label_return_tool_id.setText("治具编号：")
        self.label_return_tool_id.setFont(QFont("SanSerif", 10))
        self.label_return_tool_id.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_return_tool_id.setAlignment(Qt.AlignRight)
        self.label_return_tool_id.setFixedSize(100, 13)
        self.layout_h_label_return_tool_id = QHBoxLayout()
        self.layout_h_label_return_tool_id.addWidget(self.label_return_tool_id)

        self.line_return_tool_id = QLineEdit()
        self.line_return_tool_id.setAlignment(Qt.AlignLeft)
        self.line_return_tool_id.setPlaceholderText("请输入治具编号...")
        self.line_return_tool_id.setFont(QFont("微软雅黑", 8))
        self.line_return_tool_id.setFixedSize(120, 18)
        self.layout_h_line_return_tool_id = QHBoxLayout()
        self.layout_h_line_return_tool_id.addWidget(self.line_return_tool_id)

        self.layout_h_return_tool_id = QHBoxLayout()
        self.layout_h_return_tool_id.addLayout(self.layout_h_label_return_tool_id)
        self.layout_h_return_tool_id.addLayout(self.layout_h_line_return_tool_id)

        self.label_return_person = QLabel()
        self.label_return_person.setText("归还人员：")
        self.label_return_person.setFont(QFont("SanSerif", 10))
        self.label_return_person.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_return_person.setAlignment(Qt.AlignRight)
        self.label_return_person.setFixedSize(100, 13)
        self.layout_h_label_return_person = QHBoxLayout()
        self.layout_h_label_return_person.addWidget(self.label_return_person)

        self.line_return_person = QLineEdit()
        self.line_return_person.setAlignment(Qt.AlignLeft)
        self.line_return_person.setPlaceholderText("请输入人员工号...")
        self.line_return_person.setFont(QFont("微软雅黑", 8))
        self.line_return_person.setFixedSize(120, 18)
        self.layout_h_line_return_person = QHBoxLayout()
        self.layout_h_line_return_person.addWidget(self.line_return_person)

        self.layout_h_return_person = QHBoxLayout()
        self.layout_h_return_person.addLayout(self.layout_h_label_return_person)
        self.layout_h_return_person.addLayout(self.layout_h_line_return_person)

        self.button_return = QPushButton()
        self.button_return.setText("确认归还")
        self.button_return.clicked.connect(self.is_return)
        self.button_return.setFont(QFont("微软雅黑", 10))
        self.button_return.setFixedSize(80, 30)
        self.layout_button_return = QHBoxLayout()
        self.layout_button_return.addWidget(self.button_return)

        self.button_return_cancel = QPushButton()
        self.button_return_cancel.setText("取消")
        self.button_return_cancel.clicked.connect(self.return_cancel)
        self.button_return_cancel.setFont(QFont("微软雅黑", 10))
        self.button_return_cancel.setFixedSize(60, 30)
        self.layout_button_return_cancel = QHBoxLayout()
        self.layout_button_return_cancel.addWidget(self.button_return_cancel)

        self.layout_h_return_cancel = QHBoxLayout()
        self.layout_h_return_cancel.addLayout(self.layout_button_return)
        self.layout_h_return_cancel.addLayout(self.layout_button_return_cancel)

        self.layout_v_return = QVBoxLayout()
        self.layout_v_return.addLayout(self.layout_h_label_return_program)
        self.layout_v_return.addLayout(self.layout_h_return_tool_id)
        self.layout_v_return.addLayout(self.layout_h_return_person)
        self.layout_v_return.addLayout(self.layout_h_return_cancel)
        
        self.label_add_program = QLabel()
        self.label_add_program.setText("<b>3.添加功能<b>")
        self.label_add_program.setFont(QFont("SanSerif", 12))
        self.label_add_program.setStyleSheet("Color: RGB(64, 224, 208)")
        self.label_add_program.setAlignment(Qt.AlignLeft)
        self.label_add_program.setFixedSize(220, 20)
        self.layout_h_label_add_program = QHBoxLayout()
        self.layout_h_label_add_program.addWidget(self.label_add_program)

        self.label_add_tool_id = QLabel()
        self.label_add_tool_id.setText("治具编号：")
        self.label_add_tool_id.setFont(QFont("SanSerif", 10))
        self.label_add_tool_id.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_add_tool_id.setAlignment(Qt.AlignRight)
        self.label_add_tool_id.setFixedSize(100, 13)
        self.layout_h_label_add_tool_id = QHBoxLayout()
        self.layout_h_label_add_tool_id.addWidget(self.label_add_tool_id)

        self.line_add_tool_id = QLineEdit()
        self.line_add_tool_id.setAlignment(Qt.AlignLeft)
        self.line_add_tool_id.setPlaceholderText("请输入治具编号...")
        self.line_add_tool_id.setFont(QFont("微软雅黑", 8))
        self.line_add_tool_id.setFixedSize(120, 18)
        self.layout_h_line_add_tool_id = QHBoxLayout()
        self.layout_h_line_add_tool_id.addWidget(self.line_add_tool_id)

        self.layout_h_add_tool_id = QHBoxLayout()
        self.layout_h_add_tool_id.addLayout(self.layout_h_label_add_tool_id)
        self.layout_h_add_tool_id.addLayout(self.layout_h_line_add_tool_id)

        self.label_add_tool_name = QLabel()
        self.label_add_tool_name.setText("治具名称：")
        self.label_add_tool_name.setFont(QFont("SanSerif", 10))
        self.label_add_tool_name.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_add_tool_name.setAlignment(Qt.AlignRight)
        self.label_add_tool_name.setFixedSize(100, 13)
        self.layout_h_label_add_tool_name = QHBoxLayout()
        self.layout_h_label_add_tool_name.addWidget(self.label_add_tool_name)

        self.line_add_tool_name = QLineEdit()
        self.line_add_tool_name.setAlignment(Qt.AlignLeft)
        self.line_add_tool_name.setPlaceholderText("请输入治具名称...")
        self.line_add_tool_name.setFont(QFont("微软雅黑", 8))
        self.line_add_tool_name.setFixedSize(120, 18)
        self.layout_h_line_add_tool_name = QHBoxLayout()
        self.layout_h_line_add_tool_name.addWidget(self.line_add_tool_name)

        self.layout_h_add_tool_name = QHBoxLayout()
        self.layout_h_add_tool_name.addLayout(self.layout_h_label_add_tool_name)
        self.layout_h_add_tool_name.addLayout(self.layout_h_line_add_tool_name)

        self.label_add_tool_site = QLabel()
        self.label_add_tool_site.setText("治具位置：")
        self.label_add_tool_site.setFont(QFont("SanSerif", 10))
        self.label_add_tool_site.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_add_tool_site.setAlignment(Qt.AlignRight)
        self.label_add_tool_site.setFixedSize(100, 13)
        self.layout_h_label_add_tool_site = QHBoxLayout()
        self.layout_h_label_add_tool_site.addWidget(self.label_add_tool_site)

        self.line_add_tool_site = QLineEdit()
        self.line_add_tool_site.setAlignment(Qt.AlignLeft)
        self.line_add_tool_site.setPlaceholderText("请输入治具位置...")
        self.line_add_tool_site.setFont(QFont("微软雅黑", 8))
        self.line_add_tool_site.setFixedSize(120, 18)
        self.layout_h_line_add_tool_site = QHBoxLayout()
        self.layout_h_line_add_tool_site.addWidget(self.line_add_tool_site)

        self.layout_h_add_tool_site = QHBoxLayout()
        self.layout_h_add_tool_site.addLayout(self.layout_h_label_add_tool_site)
        self.layout_h_add_tool_site.addLayout(self.layout_h_line_add_tool_site)

        self.button_add = QPushButton()
        self.button_add.setText("确认添加")
        self.button_add.clicked.connect(self.add)
        self.button_add.setFont(QFont("微软雅黑", 10))
        self.button_add.setFixedSize(80, 30)
        self.layout_button_add = QHBoxLayout()
        self.layout_button_add.addWidget(self.button_add)

        self.button_add_cancel = QPushButton()
        self.button_add_cancel.setText("取消")
        self.button_add_cancel.clicked.connect(self.add_cancel)
        self.button_add_cancel.setFont(QFont("微软雅黑", 10))
        self.button_add_cancel.setFixedSize(60, 30)
        self.layout_button_add_cancel = QHBoxLayout()
        self.layout_button_add_cancel.addWidget(self.button_add_cancel)

        self.layout_h_add_cancel = QHBoxLayout()
        self.layout_h_add_cancel.addLayout(self.layout_button_add)
        self.layout_h_add_cancel.addLayout(self.layout_button_add_cancel)

        self.layout_v_add = QVBoxLayout()
        self.layout_v_add.addLayout(self.layout_h_label_add_program)
        self.layout_v_add.addLayout(self.layout_h_add_tool_id)
        self.layout_v_add.addLayout(self.layout_h_add_tool_name)
        self.layout_v_add.addLayout(self.layout_h_add_tool_site)
        self.layout_v_add.addLayout(self.layout_h_add_cancel)

        self.label_delete_program = QLabel()
        self.label_delete_program.setText("<b>4.删除功能<b>")
        self.label_delete_program.setFont(QFont("SanSerif", 12))
        self.label_delete_program.setStyleSheet("Color: RGB(64, 224, 208)")
        self.label_delete_program.setAlignment(Qt.AlignLeft)
        self.label_delete_program.setFixedSize(220, 20)
        self.layout_h_label_delete_program = QHBoxLayout()
        self.layout_h_label_delete_program.addWidget(self.label_delete_program)

        self.label_delete_tool_id = QLabel()
        self.label_delete_tool_id.setText("治具编号：")
        self.label_delete_tool_id.setFont(QFont("SanSerif", 10))
        self.label_delete_tool_id.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_delete_tool_id.setAlignment(Qt.AlignRight)
        self.label_delete_tool_id.setFixedSize(100, 13)
        self.layout_h_label_delete_tool_id = QHBoxLayout()
        self.layout_h_label_delete_tool_id.addWidget(self.label_delete_tool_id)

        self.line_delete_tool_id = QLineEdit()
        self.line_delete_tool_id.setAlignment(Qt.AlignLeft)
        self.line_delete_tool_id.setPlaceholderText("请输入治具编号...")
        self.line_delete_tool_id.setFont(QFont("微软雅黑", 8))
        self.line_delete_tool_id.setFixedSize(120, 18)
        self.layout_h_line_delete_tool_id = QHBoxLayout()
        self.layout_h_line_delete_tool_id.addWidget(self.line_delete_tool_id)

        self.layout_h_delete_tool_id = QHBoxLayout()
        self.layout_h_delete_tool_id.addLayout(self.layout_h_label_delete_tool_id)
        self.layout_h_delete_tool_id.addLayout(self.layout_h_line_delete_tool_id)

        self.label_delete_person = QLabel()
        self.label_delete_person.setText("删除人员：")
        self.label_delete_person.setFont(QFont("SanSerif", 10))
        self.label_delete_person.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_delete_person.setAlignment(Qt.AlignRight)
        self.label_delete_person.setFixedSize(100, 13)
        self.layout_h_label_delete_person = QHBoxLayout()
        self.layout_h_label_delete_person.addWidget(self.label_delete_person)

        self.line_delete_person_id = QLineEdit()
        self.line_delete_person_id.setAlignment(Qt.AlignLeft)
        self.line_delete_person_id.setPlaceholderText("请输入人员工号...")
        self.line_delete_person_id.setFont(QFont("微软雅黑", 8))
        self.line_delete_person_id.setFixedSize(120, 18)
        self.layout_h_line_delete_person_id = QHBoxLayout()
        self.layout_h_line_delete_person_id.addWidget(self.line_delete_person_id)

        self.layout_h_delete_person = QHBoxLayout()
        self.layout_h_delete_person.addLayout(self.layout_h_label_delete_person)
        self.layout_h_delete_person.addLayout(self.layout_h_line_delete_person_id)

        self.label_delete_reason = QLabel()
        self.label_delete_reason.setText("删除原因：")
        self.label_delete_reason.setFont(QFont("SanSerif", 10))
        self.label_delete_reason.setStyleSheet("Color: RGB(128, 128, 0)")
        self.label_delete_reason.setAlignment(Qt.AlignRight)
        self.label_delete_reason.setFixedSize(100, 13)
        self.layout_h_label_delete_reason = QHBoxLayout()
        self.layout_h_label_delete_reason.addWidget(self.label_delete_reason)

        self.line_delete_reason = QLineEdit()
        self.line_delete_reason.setAlignment(Qt.AlignLeft)
        self.line_delete_reason.setPlaceholderText("请输入删除原因...")
        self.line_delete_reason.setFont(QFont("微软雅黑", 8))
        self.line_delete_reason.setFixedSize(120, 18)
        self.layout_h_line_delete_reason = QHBoxLayout()
        self.layout_h_line_delete_reason.addWidget(self.line_delete_reason)

        self.layout_h_delete_reason = QHBoxLayout()
        self.layout_h_delete_reason.addLayout(self.layout_h_label_delete_reason)
        self.layout_h_delete_reason.addLayout(self.layout_h_line_delete_reason)

        self.button_delete = QPushButton()
        self.button_delete.setText("确认删除")
        self.button_delete.clicked.connect(self.delete)
        self.button_delete.setFont(QFont("微软雅黑", 10))
        self.button_delete.setFixedSize(80, 30)
        self.layout_button_delete = QHBoxLayout()
        self.layout_button_delete.addWidget(self.button_delete)

        self.button_delete_cancel = QPushButton()
        self.button_delete_cancel.setText("取消")
        self.button_delete_cancel.clicked.connect(self.delete_cancel)
        self.button_delete_cancel.setFont(QFont("微软雅黑", 10))
        self.button_delete_cancel.setFixedSize(60, 30)
        self.layout_button_delete_cancel = QHBoxLayout()
        self.layout_button_delete_cancel.addWidget(self.button_delete_cancel)

        self.layout_h_delete_cancel = QHBoxLayout()
        self.layout_h_delete_cancel.addLayout(self.layout_button_delete)
        self.layout_h_delete_cancel.addLayout(self.layout_button_delete_cancel)

        self.layout_v_delete = QVBoxLayout()
        self.layout_v_delete.addLayout(self.layout_h_label_delete_program)
        self.layout_v_delete.addLayout(self.layout_h_delete_tool_id)
        self.layout_v_delete.addLayout(self.layout_h_delete_person)
        self.layout_v_delete.addLayout(self.layout_h_delete_reason)
        self.layout_v_delete.addLayout(self.layout_h_delete_cancel)

    def layout_set(self):
        self.layout_h_title = QHBoxLayout()
        self.layout_h_title.addLayout(self.layout_h_label_title)

        self.layout_h_designer_and_time = QHBoxLayout()
        self.layout_h_designer_and_time.addLayout(self.layout_h_label_designer)
        self.layout_h_designer_and_time.addStretch(1)
        self.layout_h_designer_and_time.addLayout(self.layout_h_label_time)

        self.layout_search = QHBoxLayout()
        self.layout_search.addStretch(2)
        self.layout_search.addLayout(self.layout_h_search_label_item)
        self.layout_search.addLayout(self.layout_h_tool_id)
        self.layout_search.addLayout(self.layout_h_tool_name)
        self.layout_search.addStretch(1)
        self.layout_search.addLayout(self.layout_button_search)
        self.layout_search.addLayout(self.layout_button_cancel)
        self.layout_search.addStretch(2)

        self.layout_program_borrow_return = QHBoxLayout()
        self.layout_program_borrow_return.addLayout(self.layout_v_borrow)
        self.layout_program_borrow_return.addLayout(self.layout_v_return)

        self.layout_program_add_delete = QHBoxLayout()
        self.layout_program_add_delete.addLayout(self.layout_v_add)
        self.layout_program_add_delete.addLayout(self.layout_v_delete)

        self.layout_v_windows = QVBoxLayout()

        self.layout_v_windows.addLayout(self.layout_h_title)
        self.layout_v_windows.addLayout(self.layout_h_designer_and_time)
        self.layout_v_windows.addLayout(self.layout_h_label_search_program)
        self.layout_v_windows.addLayout(self.layout_search)
        self.layout_v_windows.addStretch(1)
        self.layout_v_windows.addLayout(self.layout_program_borrow_return)
        self.layout_v_windows.addStretch(1)
        self.layout_v_windows.addLayout(self.layout_program_add_delete)
        self.layout_v_windows.addStretch(1)

    def real_time(self):
        self.real_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.label_time.setText(self.real_time)

    # noinspection PyMethodMayBeStatic
    def check_database(self):
        if not os.path.exists('./database'):
            os.makedirs('./database')

        def file_create(file_path, columns):
            file = open(file_path, 'w', encoding='gbk')
            new_file_columns = columns
            data = pd.DataFrame(columns=new_file_columns, index=None)
            data.to_csv(file_path, index=False)
            file.close()

        if not os.path.exists('./database/in.csv'):
            file_create('./database/in.csv', columns=['id', 'name', 'site', 'into_time', 'into_person'])

        if not os.path.exists('./database/out.csv'):
            file_create('./database/out.csv', columns=['id', 'name', 'site', 'out_time', 'out_person'])

        if not os.path.exists('./database/delete.csv'):
            file_create('./database/delete.csv', columns=['id', 'name', 'site', 'delete_time', 'delete_person', 'delete_reason'])

    def show_tool(self):
        self.tool_information_list = []
        self.get_in_tool_information()
        show_data_child = ShowData(tool_information_list=self.tool_information_list, tool_information_item=self.search_file_path)
        show_data_child.exec()

    def change_search_item(self, i):
        if i == 'out.csv':
            self.search_file_path = './database/out.csv'
        if i == 'delete.csv':
            self.search_file_path = './database/delete.csv'
        if i == 'in.csv':
            self.search_file_path = './database/in.csv'

    def get_in_tool_information(self):
        data_in_tool_information = pd.read_csv(self.search_file_path, encoding='GBK')
        list_in_tool_information = data_in_tool_information.values.tolist()

        if len(self.line_tool_id.text()) == 0 and len(self.line_tool_name.text()) == 0:
            self.tool_information_list = list_in_tool_information

        if len(self.line_tool_id.text()) != 0 and len(self.line_tool_name.text()) == 0:
            for columns in range(0, len(list_in_tool_information)):
                if str(self.line_tool_id.text()) == str(list_in_tool_information[columns][0]):
                    self.tool_information_list.append(list_in_tool_information[columns])

        if len(self.line_tool_id.text()) == 0 and len(self.line_tool_name.text()) != 0:
            for columns in range(0, len(list_in_tool_information)):
                if str(self.line_tool_name.text()) == str(list_in_tool_information[columns][1]):
                    self.tool_information_list.append(list_in_tool_information[columns])

        if len(self.line_tool_id.text()) != 0 and len(self.line_tool_name.text()) != 0:
            for columns in range(0, len(list_in_tool_information)):
                if str(self.line_tool_id.text()) == str(list_in_tool_information[columns][0]) and str(self.line_tool_name.text()) == str(list_in_tool_information[columns][1]):
                    self.tool_information_list.append(list_in_tool_information[columns])

    def cancel_search(self):
        self.line_tool_id.clear()
        self.line_tool_name.clear()

    def borrow(self):
        borrow_tool_information_list = []

        if len(str(self.line_borrow_tool_id.text())) != 0 and len(str(self.line_borrow_person.text())) != 0:
            data_in_tool_information = pd.read_csv('./database/in.csv', encoding='GBK')
            list_in_tool_information = data_in_tool_information.values.tolist()

            for columns in range(0, len(list_in_tool_information)):
                if str(self.line_borrow_tool_id.text()) == str(list_in_tool_information[columns][0]):
                    borrow_tool_information_list.append(list_in_tool_information[columns])

                    borrow_tool_information_list[0][0] = borrow_tool_information_list[0][0]
                    borrow_tool_information_list[0][1] = borrow_tool_information_list[0][1]
                    borrow_tool_information_list[0][2] = borrow_tool_information_list[0][2]
                    borrow_tool_information_list[0][3] = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                    borrow_tool_information_list[0][4] = str(self.line_borrow_person.text())

                    array_borrow_tool_information = np.array(borrow_tool_information_list)
                    df_borrow_tool_information = pd.DataFrame(array_borrow_tool_information)
                    df_borrow_tool_information.to_csv('./database/out.csv', index=False, header=False, mode='a', encoding='gbk')

                    self.delete_data(file_old='./database/in.csv', file_temp='./database/in_temp.csv', delete_row=0, delete_data=str(self.line_borrow_tool_id.text()))

                    QMessageBox.about(self, '提醒', '借出成功！')
                    self.borrow_cancel()
            if len(borrow_tool_information_list) == 0:
                QMessageBox.about(self, '警告', '此治具编号【%s】不存在，请确认！' % str(self.line_borrow_tool_id.text()))

        else:
            QMessageBox.about(self, '警告', '治具编号&借用人员相关信息，禁止为空！')

    def borrow_cancel(self):
        self.line_borrow_tool_id.clear()
        self.line_borrow_person.clear()

    # noinspection PyMethodMayBeStatic
    def delete_data(self, file_old, file_temp, delete_row, delete_data):
        file_old = file_old
        file_temp = file_temp
        delete_row = delete_row
        delete_data = delete_data

        with open(file_old, 'r', newline='', encoding='gbk') as f_old, \
                open(file_temp, 'w', newline='', encoding='gbk') as f_temp:
            f_csv_old = csv.reader(f_old)
            f_csv_temp = csv.writer(f_temp)
            for i, rows in enumerate(f_csv_old):  # 保留header
                if i == 0:
                    f_csv_temp.writerow(rows)
                    break
            for rows in f_csv_old:
                if rows[delete_row] != delete_data:
                    f_csv_temp.writerow(rows)

        os.remove(file_old)
        os.rename(file_temp, file_old)

    def is_return(self):
        return_tool_information_list = []

        if len(str(self.line_return_tool_id.text())) != 0 and len(str(self.line_return_person.text())) != 0:
            data_out_tool_information = pd.read_csv('./database/out.csv', encoding='gbk')
            list_out_tool_information = data_out_tool_information.values.tolist()

            for columns in range(0, len(list_out_tool_information)):
                if str(self.line_return_tool_id.text()) == str(list_out_tool_information[columns][0]):
                    return_tool_information_list.append(list_out_tool_information[columns])

                    return_tool_information_list[0][0] = return_tool_information_list[0][0]
                    return_tool_information_list[0][1] = return_tool_information_list[0][1]
                    return_tool_information_list[0][2] = return_tool_information_list[0][2]
                    return_tool_information_list[0][3] = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                    return_tool_information_list[0][4] = str(self.line_return_person.text())

                    array_return_tool_information = np.array(return_tool_information_list)
                    df_return_tool_information = pd.DataFrame(array_return_tool_information)
                    df_return_tool_information.to_csv('./database/in.csv', index=False, header=False, mode='a', encoding='gbk')

                    self.delete_data(file_old='./database/out.csv', file_temp='./database/out_temp.csv', delete_row=0,
                                     delete_data=str(self.line_return_tool_id.text()))

                    QMessageBox.about(self, '提醒', '归还成功！')
                    self.return_cancel()
            if len(return_tool_information_list) == 0:
                QMessageBox.about(self, '警告', '此治具编号【%s】不存在，请确认！' % str(self.line_return_tool_id.text()))

        else:
            QMessageBox.about(self, '警告', '治具编号&归还人员相关信息，禁止为空！')

    def return_cancel(self):
        self.line_return_tool_id.clear()
        self.line_return_person.clear()

    def add(self):
        add_tool_information_list = []

        if len(str(self.line_add_tool_id.text())) != 0 and str(self.line_add_tool_id.text())[0] != '0' and len(str(self.line_add_tool_name.text())) != 0 and len(str(self.line_add_tool_site.text())) != 0:
            add_tool_information = [str(self.line_add_tool_id.text()), str(self.line_add_tool_name.text()), str(self.line_add_tool_site.text()), str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")), 'admin']
            add_tool_information_list.append(add_tool_information)

            array_add_tool_information = np.array(add_tool_information_list)
            df_add_tool_information = pd.DataFrame(array_add_tool_information)
            df_add_tool_information.to_csv('./database/in.csv', index=False, header=False, mode='a', encoding='gbk')

            QMessageBox.about(self, '提醒', '添加成功！')
            self.add_cancel()
        else:
            QMessageBox.about(self, '警告', '治具编号(首字母禁止为0)、治具名称&治具位置相关信息，禁止为空！')

    def add_cancel(self):
        self.line_add_tool_id.clear()
        self.line_add_tool_name.clear()
        self.line_add_tool_site.clear()

    def delete(self):
        delete_tool_information_list = []

        if len(str(self.line_delete_tool_id.text())) != 0 and len(str(self.line_delete_person_id.text())) != 0 and len(str(self.line_delete_reason.text())) != 0:
            delete_data_in_tool_information = pd.read_csv('./database/in.csv', encoding='GBK')
            delete_list_in_tool_information = delete_data_in_tool_information.values.tolist()

            for columns in range(0, len(delete_list_in_tool_information)):
                if str(self.line_delete_tool_id.text()) == str(delete_list_in_tool_information[columns][0]):
                    delete_tool_information_list.append(delete_list_in_tool_information[columns])

                    delete_tool_information_list[0][0] = delete_tool_information_list[0][0]
                    delete_tool_information_list[0][1] = delete_tool_information_list[0][1]
                    delete_tool_information_list[0][2] = delete_tool_information_list[0][2]
                    delete_tool_information_list[0][3] = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                    delete_tool_information_list[0][4] = str(self.line_delete_person_id.text())
                    delete_tool_information_list[0].append(str(self.line_delete_reason.text()))

                    array_delete_tool_information = np.array(delete_tool_information_list)
                    df_delete_tool_information = pd.DataFrame(array_delete_tool_information)
                    df_delete_tool_information.to_csv('./database/delete.csv', index=False, header=False, mode='a', encoding='gbk')

                    self.delete_data(file_old='./database/in.csv', file_temp='./database/in_temp.csv', delete_row=0, delete_data=str(self.line_delete_tool_id.text()))

                    QMessageBox.about(self, '提醒', '删除成功！')
                    self.delete_cancel()
            if len(delete_tool_information_list) == 0:
                QMessageBox.about(self, '警告', '此治具编号【%s】不存在，请确认！' % str(self.line_delete_tool_id.text()))

        else:
            QMessageBox.about(self, '警告', '治具编号、删除人员&删除原因相关信息，禁止为空！')

    def delete_cancel(self):
        self.line_delete_tool_id.clear()
        self.line_delete_person_id.clear()
        self.line_delete_reason.clear()


class ShowData(QDialog):
    def __init__(self, tool_information_list, tool_information_item):
        super().__init__()
        self.setFocus()
        self.model_list_for_csv = tool_information_list
        self.item = tool_information_item

        self.setFixedSize(600, 320)
        self.setWindowIcon(QIcon("./source_file/search_model.png"))
        self.setWindowTitle("详细治具信息")

        self.set_layout()

    # noinspection PyAttributeOutsideInit
    def set_layout(self):
        self.table_model_list = QTableWidget()
        self.table_model_list.setRowCount(9)
        self.table_model_list.setColumnCount(5)
        self.table_model_list.setFixedSize(580, 300)
        self.table_model_list.setToolTip("此处为治具详细信息列表...")
        self.table_model_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_model_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_model_list.setHorizontalHeaderLabels(["治具编号", '治具名称', '治具位置', '入库时间', '入库人员'])

        self.layout_table_model_list = QHBoxLayout()
        self.layout_table_model_list.addWidget(self.table_model_list)

        self.setLayout(self.layout_table_model_list)

        self.show_table()

    def show_table(self):
        self.table_model_list.setRowCount(len(self.model_list_for_csv))

        if self.item == './database/in.csv':
            self.table_model_list.setColumnCount(5)
            self.table_model_list.setHorizontalHeaderLabels(["治具编号", '治具名称', '治具位置', '入库时间', '操作人员'])
            self.table_model_list.setFixedSize(560, 300)
            self.setFixedSize(580, 320)

        if self.item == './database/out.csv':
            self.table_model_list.setColumnCount(5)
            self.table_model_list.setHorizontalHeaderLabels(["治具编号", '治具名称', '治具位置', '出库时间', '操作人员'])
            self.table_model_list.setFixedSize(560, 300)
            self.setFixedSize(580, 320)

        if self.item == './database/delete.csv':
            self.table_model_list.setColumnCount(6)
            self.table_model_list.setHorizontalHeaderLabels(["治具编号", '治具名称', '治具位置', '删除时间', '删除人员', '删除原因'])
            self.table_model_list.setFixedSize(650, 300)
            self.setFixedSize(670, 320)

        for row in range(0, len(self.model_list_for_csv)):
            for column in range(0, len(self.model_list_for_csv[0])):
                self.table_model_list.setItem(row, column, QTableWidgetItem(str(self.model_list_for_csv[row][column])))
                pass


if __name__ == '__main__':
    app_system = QApplication(sys.argv)
    form_system = MainWindow()
    form_system.show()
    sys.exit(app_system.exec_())

    pass
