# import io
# from django.http import FileResponse
# from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions, authentication
# from django.utils.timezone import now
# from django.utils import timezone
# from .models import Dataset
# from .serializers import DatasetSerializer
# from .utils import parse_and_summarize_csv
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# from reportlab.lib.utils import ImageReader
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# import pandas as pd
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response
# from rest_framework import status


# COLUMN_MAP = {
#     "equipment name": "equipment_name",
#     "equip_name": "equipment_name",
#     "equipmentname": "equipment_name",
#     "equipment": "equipment_name",

#     "type": "type",

#     "flow rate": "flowrate",
#     "flowrate": "flowrate",
#     "flow": "flowrate",

#     "pressure": "pressure",
#     "press": "pressure",

#     "temp": "temperature",
#     "temperature": "temperature",
#     "temp.": "temperature",
# }

# def normalize_column_name(col):
#     """
#     Normalize column names to be case-insensitive and typo-tolerant.
#     Example: 'Equipment Name', 'equip_name', or 'EQUIPMENTNAME' 
#     → all map to 'equipment_name'.
#     """
#     key = col.strip().lower().replace("_", " ").replace("-", " ")
#     return COLUMN_MAP.get(key, key)

# # @api_view(["POST"])
# # @permission_classes([AllowAny])
# # def dataset_upload(request):
# #     file = request.FILES.get("file")

# #     if not file:
# #         return Response(
# #             {"detail": "No file uploaded. Use field name 'file' in your request.", "error_code": "file_missing"},
# #             status=status.HTTP_400_BAD_REQUEST,
# #         )

# #     try:
# #         df = pd.read_csv(file)
# #         df.columns = [normalize_column_name(c) for c in df.columns]

# #         required_cols = {"equipment_name", "type", "flowrate", "pressure", "temperature"}
# #         missing = required_cols - set(df.columns)
# #         if missing:
# #             return Response(
# #                 {
# #                     "detail": f"CSV parsing error: missing required column(s): {', '.join(missing)}",
# #                     "error_code": "csv_invalid_structure",
# #                 },
# #                 status=status.HTTP_400_BAD_REQUEST,
# #             )

# #         # Build summary for frontend display
# #         summary = {
# #             "total_equipment": len(df),
# #             "avg_flowrate": round(df["flowrate"].mean(), 2),
# #             "avg_pressure": round(df["pressure"].mean(), 2),
# #             "avg_temperature": round(df["temperature"].mean(), 2),
# #         }

# #         # Save dataset (🔥 owner removed completely)
# #         dataset = Dataset.objects.create(
# #             file_name=file.name,
# #             summary_json={
# #                 "total_equipment": len(df),
# #                 "average_flowrate": round(df["flowrate"].mean(), 2),
# #                 "average_pressure": round(df["pressure"].mean(), 2),
# #                 "average_temperature": round(df["temperature"].mean(), 2),
# #                 "type_distribution": df["type"].value_counts().to_dict(),
# #             },
# #         )

# #         return Response(
# #             {"message": "Dataset uploaded successfully", "summary": summary},
# #             status=status.HTTP_201_CREATED,
# #         )

# #     except Exception as e:
# #         return Response(
# #             {"detail": f"CSV parsing error: {str(e)}", "error_code": "csv_read_error"},
# #             status=status.HTTP_400_BAD_REQUEST,
# #         )

# @api_view(["POST"])
# @permission_classes([AllowAny])
# def dataset_upload(request):
#     file = request.FILES.get("file")

#     if not file:
#         return Response(
#             {
#                 "detail": "No file uploaded. Use field name 'file'.",
#                 "error_code": "file_missing",
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     # ---- Basic validation: must be CSV and not huge ----
#     if not file.name.lower().endswith(".csv"):
#         return Response(
#             {
#                 "detail": "Invalid file type. Please upload a CSV file (*.csv).",
#                 "error_code": "invalid_file_type",
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     max_mb = 10
#     if file.size > max_mb * 1024 * 1024:
#         return Response(
#             {
#                 "detail": f"File too large. Maximum allowed size is {max_mb} MB.",
#                 "error_code": "file_too_large",
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     try:
#         # Read CSV with pandas
#         df = pd.read_csv(file)
#         df.columns = [normalize_column_name(c) for c in df.columns]

#         required_cols = {"equipment_name", "type", "flowrate", "pressure", "temperature"}
#         missing = required_cols - set(df.columns)
#         if missing:
#             return Response(
#                 {
#                     "detail": f"CSV parsing error: missing required column(s): {', '.join(missing)}",
#                     "error_code": "csv_invalid_structure",
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # ---- Build summary JSON once (used for DB + frontend) ----
#         summary_json = {
#             "total_equipment": len(df),
#             "average_flowrate": round(df["flowrate"].mean(), 2),
#             "average_pressure": round(df["pressure"].mean(), 2),
#             "average_temperature": round(df["temperature"].mean(), 2),
#             "type_distribution": df["type"].value_counts().to_dict(),
#         }

#         # ---- IMPORTANT: reset file pointer so Django can save full file ----
#         file.seek(0)

#         # Save dataset (no owner now, just file + summary)
#         dataset = Dataset.objects.create(
#             file_name=file.name,
#             csv_file=file,
#             summary_json=summary_json,
#         )

#         # What frontend currently expects (avg_ keys)
#         summary_for_frontend = {
#             "total_equipment": summary_json["total_equipment"],
#             "avg_flowrate": summary_json["average_flowrate"],
#             "avg_pressure": summary_json["average_pressure"],
#             "avg_temperature": summary_json["average_temperature"],
#         }

#         return Response(
#             {
#                 "message": "Dataset uploaded successfully",
#                 "summary": summary_for_frontend,
#             },
#             status=status.HTTP_201_CREATED,
#         )

#     except Exception as e:
#         return Response(
#             {"detail": f"CSV parsing error: {str(e)}", "error_code": "csv_read_error"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )

# class LatestSummaryView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def get(self, request):
#         ds = Dataset.objects.order_by('-upload_time').first()
#         if not ds:
#             return Response({"detail": "No dataset available", "error_code": "no_dataset"}, status=status.HTTP_404_NOT_FOUND)
#         return Response(ds.summary_json, status=status.HTTP_200_OK)

# class HistoryView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def get(self, request):
#         qs = Dataset.objects.order_by('-upload_time')[:5]
#         data = []
#         for ds in qs:
#             data.append({
#                 "upload_time": ds.upload_time.isoformat(),
#                 "file_name": ds.file_name,
#                 "summary": ds.summary_json
#             })
#         return Response(data)


# class LatestReportView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         from reportlab.lib import colors
#         from reportlab.lib.pagesizes import letter
#         from reportlab.lib.styles import getSampleStyleSheet
#         from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
#         from reportlab.lib.units import inch
#         from io import BytesIO
#         import matplotlib.pyplot as plt
#         import csv

#         # ✅ 1. Get the latest dataset
#         ds = Dataset.objects.order_by('-upload_time').first()
#         if not ds:
#             return Response(
#                 {"detail": "No dataset available", "error_code": "no_dataset"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         # ✅ 2. Prepare CSV rows (optional if not saved)
#         csv_rows = []
#         if ds.csv_file:
#             ds.csv_file.open("r")
#             reader = csv.reader(ds.csv_file.read().splitlines())
#             csv_rows = list(reader)
#             ds.csv_file.close()

#         # ✅ 3. Initialize PDF document
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter)
#         styles = getSampleStyleSheet()
#         elements = []

#         # ✅ 4. Header
#         title_style = styles["Title"]
#         title_style.textColor = colors.HexColor("#0B5394")
#         elements.append(Paragraph("<b>Chemical Equipment Parameter Visualizer</b>", title_style))
#         elements.append(Spacer(1, 6))
#         elements.append(Paragraph(f"<b>Dataset:</b> {ds.file_name}", styles["Normal"]))

#         # Convert UTC → Local Time for clarity
#         from django.utils.timezone import localtime
#         local_time = localtime(ds.upload_time).strftime('%Y-%m-%d %H:%M:%S')
#         elements.append(Paragraph(f"<b>Uploaded on:</b> {local_time}", styles["Normal"]))
#         elements.append(Spacer(1, 12))

#         # ✅ 5. Summary Section
#         elements.append(Paragraph("<b>Summary Statistics</b>", styles["Heading2"]))
#         summary_data = [["Parameter", "Value"]]
#         for key, value in ds.summary_json.items():
#             if key != "type_distribution":
#                 summary_data.append([key.replace("_", " ").title(), str(value)])

#         table = Table(summary_data, hAlign="LEFT", colWidths=[200, 200])
#         table.setStyle(TableStyle([
#             ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#CFE2F3")),
#             ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
#             ("ALIGN", (0, 0), (-1, -1), "LEFT"),
#             ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
#             ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
#         ]))
#         elements.append(table)
#         elements.append(Spacer(1, 12))

#         # ✅ 6. Add Chart
#         type_dist = ds.summary_json.get("type_distribution", {})
#         if type_dist:
#             fig, ax = plt.subplots(figsize=(4, 3))
#             ax.pie(type_dist.values(), labels=type_dist.keys(), autopct="%1.1f%%")
#             ax.set_title("Equipment Type Distribution")

#             chart_buf = BytesIO()
#             plt.savefig(chart_buf, format="png", bbox_inches="tight")
#             plt.close(fig)
#             chart_buf.seek(0)
#             elements.append(Paragraph("<b>Visualizations</b>", styles["Heading2"]))
#             elements.append(Image(chart_buf, width=4 * inch, height=3 * inch))
#             elements.append(Spacer(1, 12))

#         # ✅ 7. Build PDF
#         try:
#             doc.build(elements)
#         except Exception as e:
#             return Response({"detail": f"PDF generation failed: {str(e)}"}, status=500)

#         # ✅ 8. Finalize buffer
#         buffer.seek(0)
#         pdf_data = buffer.getvalue()
#         buffer.close()

#         # ✅ 9. Return proper file response
#         response = FileResponse(
#             io.BytesIO(pdf_data),
#             as_attachment=True,
#             filename=f"{ds.file_name}_styled_report.pdf",
#             content_type="application/pdf"
#         )

#         return response

# api/views.py

from io import BytesIO

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from django.http import FileResponse
from django.utils.timezone import localtime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

from .models import Dataset


# ------------------------------------------------------------
#  Column normalisation helpers (flexible CSV headers)
# ------------------------------------------------------------

COLUMN_MAP = {
    "equipment name": "equipment_name",
    "equip_name": "equipment_name",
    "equipmentname": "equipment_name",
    "equipment": "equipment_name",

    "type": "type",

    "flow rate": "flowrate",
    "flowrate": "flowrate",
    "flow": "flowrate",

    "pressure": "pressure",
    "press": "pressure",

    "temp": "temperature",
    "temperature": "temperature",
    "temp.": "temperature",
}


def normalize_column_name(col: str) -> str:
    """
    Normalize column names to be case-insensitive and typo-tolerant.
    Example: 'Equipment Name', 'equip_name', 'EQUIPMENTNAME'
    -> all map to 'equipment_name'.
    """
    key = col.strip().lower().replace("_", " ").replace("-", " ")
    return COLUMN_MAP.get(key, key)


# ------------------------------------------------------------
#  1) Upload CSV and store dataset
# ------------------------------------------------------------

@api_view(["POST"])
@permission_classes([AllowAny])
def dataset_upload(request):
    """
    Upload a CSV file, validate it, compute summary and
    store dataset (anonymous – no user ownership now).
    """
    file = request.FILES.get("file")

    # 1) Check file presence
    if not file:
        return Response(
            {
                "detail": "No file uploaded. Use field name 'file'.",
                "error_code": "file_missing",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 2) Basic validation: only CSV
    if not file.name.lower().endswith(".csv"):
        return Response(
            {
                "detail": "Invalid file type. Please upload a CSV file (*.csv).",
                "error_code": "invalid_file_type",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 3) Limit file size (10 MB)
    max_mb = 10
    if file.size > max_mb * 1024 * 1024:
        return Response(
            {
                "detail": f"File too large. Maximum allowed size is {max_mb} MB.",
                "error_code": "file_too_large",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # 4) Read CSV
        df = pd.read_csv(file)
        df.columns = [normalize_column_name(c) for c in df.columns]

        # 5) Check required columns
        required_cols = {"equipment_name", "type", "flowrate", "pressure", "temperature"}
        missing = required_cols - set(df.columns)
        if missing:
            return Response(
                {
                    "detail": f"CSV parsing error: missing required column(s): {', '.join(missing)}",
                    "error_code": "csv_invalid_structure",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 6) Build summary JSON (for DB + API)
        summary_json = {
            "total_equipment": len(df),
            "average_flowrate": round(df["flowrate"].mean(), 2),
            "average_pressure": round(df["pressure"].mean(), 2),
            "average_temperature": round(df["temperature"].mean(), 2),
            "type_distribution": df["type"].value_counts().to_dict(),
        }

        # 7) Reset file pointer so FileField saves full file
        file.seek(0)

        # 8) Store Dataset (anonymous – no owner)
        Dataset.objects.create(
            file_name=file.name,
            csv_file=file,
            summary_json=summary_json,
        )

        # 9) Response format expected by frontend Upload page
        summary_for_frontend = {
            "total_equipment": summary_json["total_equipment"],
            "avg_flowrate": summary_json["average_flowrate"],
            "avg_pressure": summary_json["average_pressure"],
            "avg_temperature": summary_json["average_temperature"],
        }

        return Response(
            {
                "message": "Dataset uploaded successfully",
                "summary": summary_for_frontend,
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response(
            {
                "detail": f"CSV parsing error: {str(e)}",
                "error_code": "csv_read_error",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# ------------------------------------------------------------
#  2) Latest summary (used by /summary page)
# ------------------------------------------------------------

class LatestSummaryView(APIView):
    """
    Return summary_json of the latest uploaded dataset.
    Anonymous – no user filtering.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ds = Dataset.objects.order_by("-upload_time").first()
        if not ds:
            return Response(
                {"detail": "No dataset available", "error_code": "no_dataset"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(ds.summary_json, status=status.HTTP_200_OK)


# ------------------------------------------------------------
#  3) History – last 5 uploads
# ------------------------------------------------------------

class HistoryView(APIView):
    """
    Return last 5 uploaded datasets (global, not per user).
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = Dataset.objects.order_by("-upload_time")[:5]
        data = []
        for ds in qs:
            data.append(
                {
                    "upload_time": ds.upload_time.isoformat(),
                    "file_name": ds.file_name,
                    "summary": ds.summary_json,
                }
            )
        return Response(data, status=status.HTTP_200_OK)


# ------------------------------------------------------------
#  4) PDF report for latest dataset
# ------------------------------------------------------------

class LatestReportView(APIView):
    """
    Generate a PDF report for the latest dataset:
    - Header
    - Summary table
    - Pie chart for type distribution
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # 1) Get latest dataset
        ds = Dataset.objects.order_by("-upload_time").first()
        if not ds:
            return Response(
                {"detail": "No dataset available", "error_code": "no_dataset"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 2) Prepare PDF document
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # ---- Header ----
        title_style = styles["Title"]
        title_style.textColor = colors.HexColor("#0B5394")

        elements.append(
            Paragraph("<b>Chemical Equipment Parameter Visualizer</b>", title_style)
        )
        elements.append(Spacer(1, 6))
        elements.append(
            Paragraph(f"<b>Dataset:</b> {ds.file_name}", styles["Normal"])
        )

        local_time_str = localtime(ds.upload_time).strftime("%Y-%m-%d %H:%M:%S")
        elements.append(
            Paragraph(f"<b>Uploaded on:</b> {local_time_str}", styles["Normal"])
        )
        elements.append(Spacer(1, 12))

        # ---- Summary table ----
        elements.append(Paragraph("<b>Summary Statistics</b>", styles["Heading2"]))

        summary_data = [["Parameter", "Value"]]
        for key, value in ds.summary_json.items():
            if key == "type_distribution":
                continue
            label = key.replace("_", " ").title()
            summary_data.append([label, str(value)])

        table = Table(summary_data, hAlign="LEFT", colWidths=[220, 220])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#CFE2F3")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ]
            )
        )
        elements.append(table)
        elements.append(Spacer(1, 12))

        # ---- Chart: type distribution ----
        type_dist = ds.summary_json.get("type_distribution", {})
        if type_dist:
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.pie(
                type_dist.values(),
                labels=type_dist.keys(),
                autopct="%1.1f%%",
            )
            ax.set_title("Equipment Type Distribution")

            chart_buf = BytesIO()
            plt.savefig(chart_buf, format="png", bbox_inches="tight")
            plt.close(fig)
            chart_buf.seek(0)

            elements.append(Paragraph("<b>Visualizations</b>", styles["Heading2"]))
            elements.append(Image(chart_buf, width=4 * 72, height=3 * 72))  # 72 dpi
            elements.append(Spacer(1, 12))
                    # ---- Data Preview (first 30 rows) ----
            # ------------------------------------------------------------
#  Add First 30 CSV Rows (always on Page 2)
# ------------------------------------------------------------
            from reportlab.platypus import PageBreak

            # Add a page break so the table ALWAYS starts on a new page
            elements.append(PageBreak())

            elements.append(Paragraph("<b>Data Preview (first 30 rows)</b>", styles["Heading2"]))
            elements.append(Spacer(1, 6))

            csv_rows = []
            if ds.csv_file:
                import csv
                ds.csv_file.open("r")
                reader = csv.reader(ds.csv_file.read().splitlines())
                csv_rows = list(reader)
                ds.csv_file.close()

            # Show the first 30 rows (header + rows)
            max_rows = min(30, len(csv_rows))
            table_data = csv_rows[:max_rows]

            data_table = Table(
                table_data,
                repeatRows=1,  # repeat header if page splits
                colWidths=[120, 120, 80, 80, 100],  # adjust widths if required
            )

            data_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#CFE2F3")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ]))

            elements.append(data_table)
            elements.append(Spacer(1, 12))



        # 3) Build PDF
        try:
            doc.build(elements)
        except Exception as e:
            return Response(
                {"detail": f"PDF generation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # 4) Return PDF file
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f"{ds.file_name}_styled_report.pdf",
            content_type="application/pdf",
        )

