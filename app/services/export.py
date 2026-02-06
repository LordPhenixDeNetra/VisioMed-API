from typing import List, Any
from io import BytesIO
from datetime import datetime
import pandas as pd
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class ExportService:
    def generate_excel(self, data: List[dict], sheet_name: str = "Data") -> BytesIO:
        """
        Generate Excel file from list of dicts.
        """
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        output.seek(0)
        return output

    def generate_pdf_report(self, title: str, data: List[List[Any]], headers: List[str]) -> BytesIO:
        """
        Generate a simple PDF report with a table.
        """
        output = BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        elements.append(Paragraph(title, styles['Title']))
        elements.append(Paragraph(f"Généré le: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        elements.append(Paragraph("<br/><br/>", styles['Normal']))
        
        # Table Data
        table_data = [headers] + data
        
        # Create Table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(table)
        doc.build(elements)
        output.seek(0)
        return output

export_service = ExportService()
