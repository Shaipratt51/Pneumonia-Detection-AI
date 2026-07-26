# utils/report.py

from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY


def generate_pdf_report(
    patient_name,
    patient_id,
    age,
    gender,
    hospital,
    doctor,
    prediction,
    confidence,
    normal_probability,
    pneumonia_probability
):
    """
    Generate a modern, hospital-grade AI diagnostic PDF report.

    Parameters
    ----------
    patient_name : str
    patient_id : str
    age : int or str
    gender : str
    hospital : str
    doctor : str
    prediction : str ("NORMAL" or "PNEUMONIA")
    confidence : float (0.0 to 1.0)
    normal_probability : float (0.0 to 1.0)
    pneumonia_probability : float (0.0 to 1.0)

    Returns
    -------
    BytesIO
        PDF buffer ready for download.
    """

    buffer = BytesIO()

    # Page Setup - A4 Portrait with 36pt (0.5 inch) margins
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    page_width = A4[0] - 72  # 595.27 - 72 = 523.27 pt printable width

    # -----------------------------------------------------
    # Design Styles Setup
    # -----------------------------------------------------
    styles = getSampleStyleSheet()

    # Custom Paragraph Styles
    style_header_title = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#FFFFFF')
    )

    style_header_sub = ParagraphStyle(
        'HeaderSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#BFDBFE')
    )

    style_header_right = ParagraphStyle(
        'HeaderRight',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=12,
        alignment=TA_RIGHT,
        textColor=colors.HexColor('#E0F2FE')
    )

    style_section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=6
    )

    style_label = ParagraphStyle(
        'StyleLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#6B7280')
    )

    style_value = ParagraphStyle(
        'StyleValue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#111827')
    )

    style_body = ParagraphStyle(
        'StyleBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#374151')
    )

    style_body_bold = ParagraphStyle(
        'StyleBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#111827')
    )

    elements = []

    # -----------------------------------------------------
    # 1. TOP HEADER BANNER
    # -----------------------------------------------------
    now_str = datetime.now().strftime('%d-%b-%Y %H:%M')
    report_id_str = f"REP-{datetime.now().strftime('%Y%m%d')}-{str(patient_id)[-5:] if patient_id else '89420'}"

    header_left = Paragraph(
        "<b>🩻 PneumoVision AI</b><br/>"
        "<font size=9 color='#BFDBFE'>AI-Powered Chest X-Ray Diagnostic Report</font>",
        style_header_title
    )

    header_right = Paragraph(
        f"<b>REPORT ID:</b> {report_id_str}<br/>"
        f"<b>DATE & TIME:</b> {now_str}<br/>"
        f"<b>AI ENGINE:</b> TensorFlow v2.4",
        style_header_right
    )

    header_table = Table(
        [[header_left, header_right]],
        colWidths=[page_width * 0.62, page_width * 0.38]
    )

    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1E40AF')),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 14))

    # -----------------------------------------------------
    # 2. PATIENT INFORMATION CARD
    # -----------------------------------------------------
    elements.append(Paragraph("👤 PATIENT & DIAGNOSTIC METADATA", style_section_heading))

    p_name = patient_name if patient_name else "Not Specified"
    p_id = patient_id if patient_id else "Not Specified"
    p_age = f"{age} Yrs" if age else "N/A"
    p_gender = gender if gender else "N/A"
    p_hosp = hospital if hospital else "St. Jude Medical Center"
    p_doc = doctor if doctor else "Dr. Sarah Jenkins, MD"

    patient_data = [
        [
            Paragraph("PATIENT NAME", style_label), Paragraph(f"<b>{p_name}</b>", style_value),
            Paragraph("HOSPITAL", style_label), Paragraph(f"<b>{p_hosp}</b>", style_value)
        ],
        [
            Paragraph("PATIENT ID", style_label), Paragraph(f"<b>{p_id}</b>", style_value),
            Paragraph("ATTENDING DOCTOR", style_label), Paragraph(f"<b>{p_doc}</b>", style_value)
        ],
        [
            Paragraph("AGE & GENDER", style_label), Paragraph(f"<b>{p_age} / {p_gender}</b>", style_value),
            Paragraph("ANALYSIS DATE", style_label), Paragraph(f"<b>{now_str}</b>", style_value)
        ]
    ]

    col_w = page_width / 4.0
    patient_table = Table(patient_data, colWidths=[col_w * 0.85, col_w * 1.15, col_w * 0.85, col_w * 1.15])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#F1F5F9')),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(patient_table)
    elements.append(Spacer(1, 14))

    # -----------------------------------------------------
    # 3. CLINICAL SUMMARY BANNER
    # -----------------------------------------------------
    elements.append(Paragraph("🩺 DIAGNOSTIC RESULT SUMMARY", style_section_heading))

    is_pneumonia = (str(prediction).upper() == "PNEUMONIA")

    if is_pneumonia:
        summary_bg = colors.HexColor('#FEF2F2')
        summary_border = colors.HexColor('#EF4444')
        summary_title_color = '#B91C1C'
        summary_sub_color = '#991B1B'
        icon_symbol = "⚠️"
        main_title = "DIAGNOSIS: PNEUMONIA DETECTED"
        main_subtitle = "Deep learning feature extraction identified radiological patterns consistent with pulmonary infection/consolidation."
    else:
        summary_bg = colors.HexColor('#F0FDF4')
        summary_border = colors.HexColor('#22C55E')
        summary_title_color = '#15803D'
        summary_sub_color = '#166534'
        icon_symbol = "✅"
        main_title = "DIAGNOSIS: NORMAL CHEST RADIOGRAPH"
        main_subtitle = "No imaging features suggestive of acute pneumonia or active pulmonary consolidation detected."

    summary_p = Paragraph(
        f"<font size=14 color='{summary_title_color}'><b>{icon_symbol} {main_title}</b></font><br/>"
        f"<font size=9.5 color='{summary_sub_color}'>{main_subtitle}</font>",
        styles['Normal']
    )

    summary_table = Table([[summary_p]], colWidths=[page_width])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), summary_bg),
        ('BOX', (0, 0), (-1, -1), 1.5, summary_border),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 14))

    # -----------------------------------------------------
    # 4. PREDICTION METRIC CARDS (4 Columns)
    # -----------------------------------------------------
    elements.append(Paragraph("📊 QUANTITATIVE MODEL METRICS", style_section_heading))

    conf_pct = f"{confidence * 100:.2f}%" if confidence <= 1.0 else f"{confidence:.2f}%"
    norm_pct = f"{normal_probability * 100:.2f}%" if normal_probability <= 1.0 else f"{normal_probability:.2f}%"
    pneu_pct = f"{pneumonia_probability * 100:.2f}%" if pneumonia_probability <= 1.0 else f"{pneumonia_probability:.2f}%"

    card_style_num = ParagraphStyle(
        'CardNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#111827')
    )

    card_style_lbl = ParagraphStyle(
        'CardLbl',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9,
        textColor=colors.HexColor('#6B7280')
    )

    m1 = [Paragraph("CLASSIFICATION", card_style_lbl), Spacer(1, 4), Paragraph(f"<font color='{summary_title_color}'><b>{prediction.upper()}</b></font>", card_style_num)]
    m2 = [Paragraph("MODEL CONFIDENCE", card_style_lbl), Spacer(1, 4), Paragraph(f"<font color='#2563EB'><b>{conf_pct}</b></font>", card_style_num)]
    m3 = [Paragraph("NORMAL PROBABILITY", card_style_lbl), Spacer(1, 4), Paragraph(f"<font color='#16A34A'><b>{norm_pct}</b></font>", card_style_num)]
    m4 = [Paragraph("PNEUMONIA PROBABILITY", card_style_lbl), Spacer(1, 4), Paragraph(f"<font color='#DC2626'><b>{pneu_pct}</b></font>", card_style_num)]

    m_width = page_width / 4.0
    metrics_table = Table([[m1, m2, m3, m4]], colWidths=[m_width, m_width, m_width, m_width])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    elements.append(metrics_table)
    elements.append(Spacer(1, 14))

    # -----------------------------------------------------
    # 5. RISK ASSESSMENT SPECTRUM BAR
    # -----------------------------------------------------
    elements.append(Paragraph("⚠️ CLINICAL RISK MATRIX ASSESSMENT", style_section_heading))

    p_val = pneumonia_probability if pneumonia_probability <= 1.0 else pneumonia_probability / 100.0

    if p_val >= 0.80:
        active_risk = "CRITICAL"
    elif p_val >= 0.50:
        active_risk = "HIGH"
    elif p_val >= 0.25:
        active_risk = "MODERATE"
    elif p_val >= 0.10:
        active_risk = "LOW"
    else:
        active_risk = "MINIMAL"

    risk_levels = ["MINIMAL", "LOW", "MODERATE", "HIGH", "CRITICAL"]

    risk_cells = []
    for r_level in risk_levels:
        if r_level == active_risk:
            if r_level in ["MINIMAL", "LOW"]:
                cell_bg = colors.HexColor('#22C55E')
            elif r_level == "MODERATE":
                cell_bg = colors.HexColor('#F59E0B')
            else:
                cell_bg = colors.HexColor('#EF4444')
            cell_txt = f"<font size=8.5 color='#FFFFFF'><b>▶ {r_level} ◀</b></font>"
        else:
            cell_bg = colors.HexColor('#F1F5F9')
            cell_txt = f"<font size=8 color='#94A3B8'>{r_level}</font>"

        risk_cells.append(Paragraph(cell_txt, ParagraphStyle('RiskCell', alignment=TA_CENTER)))

    risk_w = page_width / 5.0
    risk_table = Table([risk_cells], colWidths=[risk_w]*5)

    t_style = [
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]

    for idx, r_level in enumerate(risk_levels):
        if r_level == active_risk:
            if r_level in ["MINIMAL", "LOW"]:
                t_style.append(('BACKGROUND', (idx, 0), (idx, 0), colors.HexColor('#22C55E')))
            elif r_level == "MODERATE":
                t_style.append(('BACKGROUND', (idx, 0), (idx, 0), colors.HexColor('#F59E0B')))
            else:
                t_style.append(('BACKGROUND', (idx, 0), (idx, 0), colors.HexColor('#EF4444')))
        else:
            t_style.append(('BACKGROUND', (idx, 0), (idx, 0), colors.HexColor('#F8FAFC')))

    risk_table.setStyle(TableStyle(t_style))
    elements.append(risk_table)
    elements.append(Spacer(1, 14))

    # -----------------------------------------------------
    # 6. AI CLINICAL INTERPRETATION CARD
    # -----------------------------------------------------
    elements.append(Paragraph("🩺 AI CLINICAL INTERPRETATION", style_section_heading))

    if is_pneumonia:
        interp_text = (
            "The neural network detected structural imaging features (airspace opacification, "
            "bronchograms, or focal consolidation) associated with acute pneumonia. "
            "This result should be correlated immediately with clinical symptoms (fever, cough, dyspnea), "
            "auscultation findings, and lab workup by an attending radiologist."
        )
    else:
        interp_text = (
            "The neural network did not detect imaging features suggestive of active pneumonia. "
            "Pulmonary fields demonstrate expected radiolucency without clear consolidation. "
            "Clinical correlation is still recommended if respiratory symptoms persist."
        )

    interp_p = Paragraph(
        f"<font size=9 color='#1E40AF'><b>RADIOLOGICAL FINDINGS & IMPRESSION:</b></font><br/><br/>"
        f"{interp_text}",
        style_body
    )

    interp_table = Table([[interp_p]], colWidths=[page_width])
    interp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('LINEBEFORE', (0, 0), (0, 0), 4, colors.HexColor('#2563EB')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))

    elements.append(interp_table)
    elements.append(Spacer(1, 14))

    # -----------------------------------------------------
    # 7. CLINICAL RECOMMENDATIONS CHECKLIST
    # -----------------------------------------------------
    elements.append(Paragraph("📋 CLINICAL ACTION CHECKLIST & RECOMMENDATIONS", style_section_heading))

    rec_items = []
    if is_pneumonia:
        rec_items.append("✔ <b>Immediate Consultation:</b> Urgent radiologist review and clinical evaluation advised.")
        rec_items.append("✔ <b>Diagnostic Correlation:</b> Correlate with CBC, CRP, blood cultures, and sputum analysis.")
        rec_items.append("✔ <b>Therapeutic Action:</b> Consider appropriate antimicrobial therapy as clinically indicated.")
        rec_items.append("✔ <b>Follow-up Imaging:</b> Schedule follow-up radiograph in 4-6 weeks to assess resolution.")
    else:
        rec_items.append("✔ <b>Radiographic Status:</b> No acute radiographic evidence of pneumonia identified.")
        rec_items.append("✔ <b>Symptom Monitoring:</b> Continue clinical monitoring if patient displays respiratory symptoms.")
        rec_items.append("✔ <b>Clinical History:</b> Correlate findings with patient medical history and physical exam.")
        rec_items.append("✔ <b>Physician Consult:</b> Consult a certified physician if clinical suspicion remains high.")

    rec_html = "<br/>".join([f"<font color='#2563EB'>•</font> {item}" for item in rec_items])
    rec_p = Paragraph(rec_html, style_body)

    rec_table = Table([[rec_p]], colWidths=[page_width])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))

    elements.append(rec_table)
    elements.append(Spacer(1, 14))

    # -----------------------------------------------------
    # 8. AI MODEL TECHNICAL SPECIFICATIONS
    # -----------------------------------------------------
    elements.append(Paragraph("⚙️ AI SYSTEM TECHNICAL SPECIFICATIONS", style_section_heading))

    tech_data = [
        [
            Paragraph("MODEL ARCHITECTURE", style_label), Paragraph("<b>Convolutional Neural Network (CNN)</b>", style_value),
            Paragraph("FRAMEWORK", style_label), Paragraph("<b>TensorFlow / Keras 2.x</b>", style_value)
        ],
        [
            Paragraph("INPUT RESOLUTION", style_label), Paragraph("<b>224 × 224 × 3 (RGB)</b>", style_value),
            Paragraph("CLASSIFICATION", style_label), Paragraph("<b>Binary Softmax Activation</b>", style_value)
        ]
    ]

    tech_table = Table(tech_data, colWidths=[col_w * 0.85, col_w * 1.15, col_w * 0.85, col_w * 1.15])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#F1F5F9')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(tech_table)
    elements.append(Spacer(1, 16))

    # -----------------------------------------------------
    # 9. FOOTER & MEDICAL DISCLAIMER
    # -----------------------------------------------------
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceBefore=0, spaceAfter=8))

    style_footer = ParagraphStyle(
        'StyleFooter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#64748B')
    )

    footer_text = (
        "<b>CONFIDENTIAL MEDICAL REPORT • PNEUMOVISION AI HEALTHCARE TECHNOLOGIES</b><br/>"
        "<b>Medical Disclaimer:</b> This report was generated using an artificial intelligence deep learning algorithm. "
        "It is designed strictly as a clinical decision support tool and MUST NOT be used as a standalone diagnostic device. "
        "Final diagnosis must be rendered by a licensed radiologist or medical professional.<br/>"
        "Copyright © 2026 PneumoVision AI. Built with TensorFlow, Python & ReportLab."
    )

    elements.append(Paragraph(footer_text, style_footer))

    # Build Document
    doc.build(elements)

    buffer.seek(0)
    return buffer