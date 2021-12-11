import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="qwe",
                                     user="postgres",
                                     password="qweasd",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.shedule_tab2 = QWidget()
        self.shedule_tab3 = QWidget()
        self.shedule_tab4 = QWidget()
        self.shedule_tab5 = QWidget()
        self.tabs.addTab(self.shedule_tab, "Monday")
        self.tabs.addTab(self.shedule_tab2, "Tuesday")
        self.tabs.addTab(self.shedule_tab3, "Wednesday")
        self.tabs.addTab(self.shedule_tab4, "Thursday")
        self.tabs.addTab(self.shedule_tab5, "Friday")

        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")

        self.svbox = QVBoxLayout()
        self.sxbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.monday_gbox)
        self.shbox1.addWidget(self.tuesday_gbox)

        self._create_monday_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox)


    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(4)
        self.monday_table.setHorizontalHeaderLabels(["subject", "time", "", ""])

        self._update_monday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

    def _create_tuesday_table(self):
        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tuesday_table.setColumnCount(4)
        self.tuesday_table.setHorizontalHeaderLabels(["subject", "time", "", ""])

        self._update_tuesday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.mvbox)

    def _update_tuesday_table(self):
            self.cursor.execute("SELECT * FROM timetable WHERE day = 'Вторник'")
            records = list(self.cursor.fetchall())

            self.tuesday_table.setRowCount(len(records))

            for i, r in enumerate(records):
                r = list(r)
                print(i,r)
                joinButton = QPushButton("Join")
                self.tuesday_table.setItem(i, 0,
                                          QTableWidgetItem(str(r[2])))
                self.tuesday_table.setItem(i, 1,
                                          QTableWidgetItem(str(r[4])))
                self.tuesday_table.setCellWidget(i, 2, joinButton)

                joinButton.clicked.connect(
                    lambda: self._change_day_from_table(i, "tuesday"))
            self.tuesday_table.resizeRowsToContents()

    def _update_monday_table(self):
            self.cursor.execute("SELECT * FROM timetable WHERE day = 'Понедельник'")
            records = list(self.cursor.fetchall())

            self.monday_table.setRowCount(len(records))

            for i, r in enumerate(records):
                r = list(r)
                print(i,r)
                joinButton = QPushButton("Join")
                self.monday_table.setItem(i, 0,
                                          QTableWidgetItem(str(r[2])))
                self.monday_table.setItem(i, 1,
                                          QTableWidgetItem(str(r[4])))
                self.monday_table.setCellWidget(i, 2, joinButton)

                joinButton.clicked.connect(
                    lambda: self._change_day_from_table(i, "monday"))
            self.monday_table.resizeRowsToContents()

    def _change_day_from_table(self, rowNum, day):
        print(rowNum)
        row = list()
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE timetable SET subject=%s,start_time=%s WHERE id=%s", (row[0],row[1],rowNum+1))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _update_shedule(self):
         self._update_monday_table()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
