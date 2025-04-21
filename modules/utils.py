# modules/relatorios/utils.py

import pandas as pd
from fpdf import FPDF
from io import BytesIO

def converter_excel(df):
    """Converte um DataFrame para um arquivo Excel em memória."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Análises')
    return output.getvalue()

def converter_pdf(df):
    """Converte um DataFrame para um arquivo PDF com layout simples."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Relatório de Análises", ln=True, align='C')
    pdf.ln(10)
    for index, row in df.iterrows():
        linha = f"{row['nome_amostra']} | {row['parametro']} | Média: {row['media']}%"
        pdf.cell(200, 6, txt=linha, ln=True)
    return pdf.output(dest='S').encode('latin-1')
