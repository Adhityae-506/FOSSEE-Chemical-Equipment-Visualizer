import sys
import json

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QTextEdit,
    QTabWidget,
    QFormLayout,
)
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import api_client


class MplCanvas(FigureCanvas):
    """Simple Matplotlib canvas for embedding charts in PyQt."""

    def __init__(self, width=4, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer (Desktop)")
        self.resize(1100, 700)

        self.current_csv_path = None

        
        root = QWidget()
        root_layout = QVBoxLayout(root)

        
        self.tabs = QTabWidget()
        root_layout.addWidget(self.tabs)

        
        self._build_upload_tab()
        self._build_history_tab()
        self._build_report_tab()

        self.setCentralWidget(root)

        
        self.refresh_summary()
        self.refresh_history()

  
    def _build_upload_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        
        upload_row = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("font-weight: 500;")

        btn_browse = QPushButton("Choose CSV")
        btn_browse.clicked.connect(self.choose_file)

        btn_upload = QPushButton("Upload to Server")
        btn_upload.clicked.connect(self.upload_file)

        upload_row.addWidget(self.file_label, stretch=1)
        upload_row.addWidget(btn_browse)
        upload_row.addWidget(btn_upload)

        layout.addLayout(upload_row)

        self.upload_status_label = QLabel("")
        layout.addWidget(self.upload_status_label)

        
        summary_group = QWidget()
        form = QFormLayout(summary_group)

        self.lbl_total = QLabel("-")
        self.lbl_flow = QLabel("-")
        self.lbl_pressure = QLabel("-")
        self.lbl_temp = QLabel("-")

        form.addRow("Total Equipment:", self.lbl_total)
        form.addRow("Average Flowrate:", self.lbl_flow)
        form.addRow("Average Pressure:", self.lbl_pressure)
        form.addRow("Average Temperature:", self.lbl_temp)

        layout.addWidget(summary_group)

        
        charts_row = QHBoxLayout()

        self.bar_canvas = MplCanvas()
        self.pie_canvas = MplCanvas()

        charts_row.addWidget(self.bar_canvas, stretch=1)
        charts_row.addWidget(self.pie_canvas, stretch=1)

        layout.addLayout(charts_row)

        layout.addStretch(1)
        self.tabs.addTab(tab, "Upload & Summary")

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Equipment CSV",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )
        if path:
            self.current_csv_path = path
            self.file_label.setText(path)
            self.upload_status_label.setText("")
        else:
            self.current_csv_path = None
            self.file_label.setText("No file selected")

    def upload_file(self):
        if not self.current_csv_path:
            QMessageBox.warning(self, "No file", "Please choose a CSV file first.")
            return

        self.upload_status_label.setText("Uploading...")
        QApplication.processEvents()

        try:
            data = api_client.upload_csv(self.current_csv_path)
        except api_client.ApiError as e:
            self.upload_status_label.setText("")
            QMessageBox.critical(self, "Upload failed", str(e))
            return

        self.upload_status_label.setText("Upload successful ✅")

        
        self.refresh_summary()
        self.refresh_history()

    def refresh_summary(self):
        try:
            summary = api_client.get_latest_summary()
        except api_client.ApiError as e:
            
            self.lbl_total.setText("-")
            self.lbl_flow.setText("-")
            self.lbl_pressure.setText("-")
            self.lbl_temp.setText("-")

            self.bar_canvas.ax.clear()
            self.bar_canvas.draw()
            self.pie_canvas.ax.clear()
            self.pie_canvas.draw()

            
            if "no dataset" not in str(e).lower():
                QMessageBox.warning(self, "Summary", f"Unable to fetch summary:\n{e}")
            return

        
        self.lbl_total.setText(str(summary.get("total_equipment", "-")))
        self.lbl_flow.setText(str(summary.get("average_flowrate", "-")))
        self.lbl_pressure.setText(str(summary.get("average_pressure", "-")))
        self.lbl_temp.setText(str(summary.get("average_temperature", "-")))

        
        self._update_bar_chart(summary)
        self._update_pie_chart(summary)

    def _update_bar_chart(self, summary):
        self.bar_canvas.ax.clear()

        vals = [
            summary.get("average_flowrate", 0),
            summary.get("average_pressure", 0),
            summary.get("average_temperature", 0),
        ]
        labels = ["Flowrate", "Pressure", "Temperature"]

        self.bar_canvas.ax.bar(labels, vals)
        self.bar_canvas.ax.set_title("Average Parameter Values")
        self.bar_canvas.ax.set_ylabel("Value")

        self.bar_canvas.fig.tight_layout()
        self.bar_canvas.draw()

    def _update_pie_chart(self, summary):
        self.pie_canvas.ax.clear()

        dist = summary.get("type_distribution") or {}
        if not dist:
            self.pie_canvas.ax.set_title("No type distribution data")
            self.pie_canvas.draw()
            return

        labels = list(dist.keys())
        vals = list(dist.values())

        self.pie_canvas.ax.pie(vals, labels=labels, autopct="%1.1f%%")
        self.pie_canvas.ax.set_title("Equipment Type Distribution")

        self.pie_canvas.fig.tight_layout()
        self.pie_canvas.draw()

    
    def _build_history_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        layout.addWidget(QLabel("Last 5 uploads (raw JSON view):"))
        layout.addWidget(self.history_text)

        btn_refresh = QPushButton("Refresh History")
        btn_refresh.clicked.connect(self.refresh_history)
        layout.addWidget(btn_refresh, alignment=Qt.AlignRight)

        self.tabs.addTab(tab, "History")

    def refresh_history(self):
        try:
            items = api_client.get_history()
        except api_client.ApiError as e:
            self.history_text.setPlainText(f"Unable to fetch history:\n{e}")
            return

        
        self.history_text.clear()
        for item in items:
            self.history_text.append(f"File: {item.get('file_name')}")
            self.history_text.append(f"Uploaded: {item.get('upload_time')}")
            self.history_text.append(
                json.dumps(item.get("summary", {}), indent=2)
            )
            self.history_text.append("\n" + "-" * 60 + "\n")

    
    def _build_report_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        info = QLabel(
            "Click the button below to download the latest equipment summary\n"
            "report as a PDF generated by the Django backend."
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        btn_download = QPushButton("Download Latest Report (PDF)")
        btn_download.clicked.connect(self.download_report_clicked)
        layout.addWidget(btn_download)

        self.report_status = QLabel("")
        layout.addWidget(self.report_status)

        layout.addStretch(1)

        self.tabs.addTab(tab, "Report")

    def download_report_clicked(self):
        
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report PDF",
            "latest_equipment_report.pdf",
            "PDF Files (*.pdf);;All Files (*)",
        )
        if not path:
            return

        self.report_status.setText("Downloading report...")
        QApplication.processEvents()

        try:
            saved = api_client.download_report(path)
        except api_client.ApiError as e:
            self.report_status.setText("")
            QMessageBox.critical(self, "Download failed", str(e))
            return

        self.report_status.setText(f"Report saved to: {saved}")
        QMessageBox.information(
            self,
            "Download complete",
            f"Report successfully saved to:\n{saved}",
        )


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
