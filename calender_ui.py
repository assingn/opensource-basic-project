from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 900)  # â ũ�⸦ �� ũ�� ����
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(150, 100, 900, 600))  # ũ�⸦ �� ũ�� ����
        self.calendarWidget.setObjectName("calendarWidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(150, 0, 150, 100))  # ũ�⸦ �� ũ�� ����
        self.graphicsView.setObjectName("graphicsView")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(150, 720, 900, 150))  # ũ�⸦ �� ũ�� ����
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 898, 148))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # Add weather label
        self.weatherLabel = QtWidgets.QLabel(self.centralwidget)
        self.weatherLabel.setGeometry(QtCore.QRect(150, 50, 500, 50))  # ��ġ �� ũ�� ����
        self.weatherLabel.setObjectName("weatherLabel")

        # To-Do List widget
        self.todoListWidget = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.todoListWidget.setGeometry(QtCore.QRect(10, 10, 700, 130))
        self.todoListWidget.setObjectName("todoListWidget")

        # Add item button
        self.addItemButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.addItemButton.setGeometry(QtCore.QRect(720, 10, 150, 30))
        self.addItemButton.setObjectName("addItemButton")
        self.addItemButton.setText("Add Item")

        # Remove item button
        self.removeItemButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.removeItemButton.setGeometry(QtCore.QRect(720, 50, 150, 30))
        self.removeItemButton.setObjectName("removeItemButton")
        self.removeItemButton.setText("Remove Item")

        # To-Do List button
        self.todoListButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.todoListButton.setGeometry(QtCore.QRect(720, 90, 150, 30))
        self.todoListButton.setObjectName("todoListButton")
        self.todoListButton.setText("To-Do List")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)

        # Unchecked To-Do List widget
        self.uncheckedTodoListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.uncheckedTodoListWidget.setGeometry(QtCore.QRect(1100, 100, 250, 600))  # ��ġ �� ũ�� ����
        self.uncheckedTodoListWidget.setObjectName("uncheckedTodoListWidget")

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 21))  # â ũ�⿡ �°� ����
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Initialize To-Do list storage
        self.todo_lists = {}

        # Connect calendar date selection to function
        self.calendarWidget.selectionChanged.connect(self.loadTodoListForSelectedDate)

        # Connect buttons to functions
        self.addItemButton.clicked.connect(self.addItem)
        self.removeItemButton.clicked.connect(self.removeItem)
        self.todoListButton.clicked.connect(self.openTodoListDialog)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def addItem(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Add To-Do Item")
        dialog.resize(300, 200)

        layout = QtWidgets.QVBoxLayout()

        text_label = QtWidgets.QLabel("Enter a new to-do item:")
        layout.addWidget(text_label)
        text_input = QtWidgets.QLineEdit()
        layout.addWidget(text_input)

        time_label = QtWidgets.QLabel("Enter the time:")
        layout.addWidget(time_label)
        time_input = QtWidgets.QTimeEdit()
        time_input.setDisplayFormat("HH:mm")
        layout.addWidget(time_input)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            item_text = text_input.text()
            item_time = time_input.time().toString("HH:mm")
            if item_text:
                item = QtWidgets.QListWidgetItem(f"{item_text} ({item_time})")
                item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.CheckState.Unchecked)
                selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
                if selected_date not in self.todo_lists:
                    self.todo_lists[selected_date] = []
                self.todo_lists[selected_date].append((item_text, item_time, QtCore.Qt.CheckState.Unchecked))
                self.loadTodoListForSelectedDate()  # Update the displayed list

    def removeItem(self):
        selected_items = self.todoListWidget.selectedItems()
        if not selected_items: return
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        if selected_date in self.todo_lists:
            for item in selected_items:
                self.todoListWidget.takeItem(self.todoListWidget.row(item))
                for todo in self.todo_lists[selected_date]:
                    if f"{todo[0]} ({todo[1]})" == item.text():
                        self.todo_lists[selected_date].remove(todo)
                        break
        self.updateUncheckedTodoList()

    def handleItemChanged(self, item):
        font = item.font()
        if item.checkState() == QtCore.Qt.CheckState.Checked:
            font.setStrikeOut(True)
        else:
            font.setStrikeOut(False)
        item.setFont(font)
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        if selected_date in self.todo_lists:
            for i, todo in enumerate(self.todo_lists[selected_date]):
                if f"{todo[0]} ({todo[1]})" == item.text():
                    self.todo_lists[selected_date][i] = (todo[0], todo[1], item.checkState())
        self.updateUncheckedTodoList()

    def loadTodoListForSelectedDate(self):
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        self.todoListWidget.clear()
        if selected_date in self.todo_lists:
            for todo in self.todo_lists[selected_date]:
                item = QtWidgets.QListWidgetItem(f"{todo[0]} ({todo[1]})")
                item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(todo[2])
                self.todoListWidget.addItem(item)
        self.updateUncheckedTodoList()

    def updateUncheckedTodoList(self):
        self.uncheckedTodoListWidget.clear()
        current_month = self.calendarWidget.selectedDate().toString("yyyy-MM")
        for date, todos in self.todo_lists.items():
            if date.startswith(current_month):
                for todo in todos:
                    if todo[2] == QtCore.Qt.CheckState.Unchecked:
                        item = QtWidgets.QListWidgetItem(f"{todo[0]} ({todo[1]}) - {date}")
                        self.uncheckedTodoListWidget.addItem(item)

    def openTodoListDialog(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("To-Do List")
        dialog.resize(400, 300)

        layout = QtWidgets.QVBoxLayout()

        buttons_layout = QtWidgets.QHBoxLayout()
        self.completedTasksButton = QtWidgets.QPushButton("Completed Tasks")
        self.pendingTasksButton = QtWidgets.QPushButton("Pending Tasks")
        buttons_layout.addWidget(self.completedTasksButton)
        buttons_layout.addWidget(self.pendingTasksButton)
        layout.addLayout(buttons_layout)

        self.yearComboBox = QtWidgets.QComboBox()
        self.yearComboBox.addItems([str(year) for year in range(2020, 2031)])
        self.monthComboBox = QtWidgets.QComboBox()
        self.monthComboBox.addItems([str(month).zfill(2) for month in range(1, 13)])
        layout.addWidget(self.yearComboBox)
        layout.addWidget(self.monthComboBox)

        self.todoListTextEdit = QtWidgets.QTextEdit()
        layout.addWidget(self.todoListTextEdit)

        self.completedTasksButton.clicked.connect(self.showCompletedTasks)
        self.pendingTasksButton.clicked.connect(self.showPendingTasks)

        dialog.setLayout(layout)
        dialog.exec()

    def showCompletedTasks(self):
        selected_year = self.yearComboBox.currentText()
        selected_month = self.monthComboBox.currentText()
        self.todoListTextEdit.clear()
        for date, todos in self.todo_lists.items():
            if date.startswith(f"{selected_year}-{selected_month}"):
                for todo in todos:
                    if todo[2] == QtCore.Qt.CheckState.Checked:
                        self.todoListTextEdit.append(f"{todo[0]} ({todo[1]}) - {date}")

    def showPendingTasks(self):
        selected_year = self.yearComboBox.currentText()
        selected_month = self.monthComboBox.currentText()
        self.todoListTextEdit.clear()
        for date, todos in self.todo_lists.items():
            if date.startswith(f"{selected_year}-{selected_month}"):
                for todo in todos:
                    if todo[2] == QtCore.Qt.CheckState.Unchecked:
                        self.todoListTextEdit.append(f"{todo[0]} ({todo[1]}) - {date}")
