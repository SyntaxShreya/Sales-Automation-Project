import pandas as pd
from fpdf import FPDF
from Analytics import get_analytics

#generating multiple PDFs from Excel based on Category attribute
file_path = "DATA/orders.csv"
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()
grouped = df.groupby("category")

for category, group in grouped:

    # Use Landscape (L) to provide more horizontal space (277mm usable width)
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    pdf.set_font("Arial", size=16)
    pdf.cell(0, 10, txt=f"Category Report: {category}", ln=True, align='C')
    pdf.ln(10)

    #Analytics
    stats = get_analytics(group)

    pdf.set_font("Arial", size=12)
    
    # Configuration for metrics
    metric_config = {
        "total_orders": ("Total Orders", "{}"),
        "total_revenue": ("Total Revenue", "${:.2f}"),
        "average_order": ("Average Order Value", "${:.2f}"),
        "total_quantity": ("Total Quantity Sold", "{}")
    }

    for key, (label, fmt) in metric_config.items():
        value = fmt.format(stats[key])
        pdf.cell(0, 10, txt=f"{label}: {value}", ln=True)

    pdf.ln(10)

    # Dynamic Column Generation
    exclude_cols = ["category"]
    display_cols = [col for col in group.columns if col not in exclude_cols]
    
    # Landscape usable width is roughly 277mm (297mm - 20mm margins)
    usable_width = 277
    col_width = usable_width / len(display_cols)
    columns = [(col, col.replace("_", " ").title(), col_width) for col in display_cols]

    # Table Headers - Bold and smaller font
    pdf.set_font("Arial", 'B', size=10)
    for col_key, col_name, col_width in columns:
        pdf.cell(col_width, 10, col_name, 1, 0, 'C')
    pdf.ln()

    # Table Rows - Even smaller font to prevent overlap
    pdf.set_font("Arial", size=8)
    for _, row in group.iterrows():
        for col_key, col_name, col_width in columns:
            # We use a smaller font and center alignment to reduce overlapping
            # fpdf doesn't auto-wrap in .cell, so we ensure the font is small enough
            text = str(row[col_key])
            pdf.cell(col_width, 8, text, 1, 0, 'C')
        pdf.ln()

    #Save PDF
    pdf.output(f"output/{category}.pdf")

print("PDFs generated.")
