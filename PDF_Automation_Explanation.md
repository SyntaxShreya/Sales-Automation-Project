# PDF_Automation.py - Line-by-Line Explanation

This document provides a thorough explanation of every line in `PDF_Automation.py` to help you understand how it generates PDF reports from your data.

---

### 1. Imports
```python
import pandas as pd
```
* **What it does:** Imports the `pandas` library, which is the industry standard for handling data in Python.
* **Why:** We use it to read the CSV file, group the data, and perform calculations. We rename it to `pd` to make it shorter and easier to type.

```python
from fpdf import FPDF
```
* **What it does:** Imports the `FPDF` class from the `fpdf` library.
* **Why:** This is the tool we use to actually create and format the PDF documents (adding pages, text, and tables).

```python
from Analytics import get_analytics
```
* **What it does:** Imports a custom function called `get_analytics` from your other file, `Analytics.py`.
* **Why:** Instead of rewriting the math logic here, we reuse the code you've already written elsewhere.

---

### 2. Loading the Data
```python
#generating multiple PDFs from Excel based on Category attribute
```
* **What it does:** This is a **comment**. It doesn't run; it's just a note for you or other developers explaining what this section does.

```python
file_path = "DATA/orders.csv"
```
* **What it does:** Creates a variable named `file_path` that stores the location of your data file.

```python
df = pd.read_csv(file_path)
```
* **What it does:** Tells pandas to read the CSV file and store it in a **DataFrame** (think of it like a digital Excel spreadsheet) called `df`.

```python
df.columns = df.columns.str.strip()
```
* **What it does:** Cleans up the column names by removing any accidental spaces at the beginning or end (e.g., `" category "` becomes `"category"`).

```python
grouped = df.groupby("category")
```
* **What it does:** Organizes the data into groups based on the "category" column. If you have "Electronics" and "Furniture," it separates them so we can make a report for each.

---

### 3. The Main Loop (Processing Each Category)
```python
for category, group in grouped:
```
* **What it does:** Starts a **loop**. It says: "For every unique category found, call the name `category` and the data for that specific category `group`."

```python
    # Use Landscape (L) to provide more horizontal space (277mm usable width)
    pdf = FPDF(orientation='L', unit='mm', format='A4')
```
* **What it does:** Initializes a new PDF object.
    * `orientation='L'`: Landscape mode (sideways), which is better for wide tables.
    * `unit='mm'`: We will measure things in millimeters.
    * `format='A4'`: The standard paper size.

```python
    pdf.add_page()
```
* **What it does:** Creates the first blank page in the PDF.

```python
    pdf.set_font("Arial", size=16)
```
* **What it does:** Sets the "active" font to Arial, size 16. Anything we write next will use this style.

```python
    pdf.cell(0, 10, txt=f"Category Report: {category}", ln=True, align='C')
```
* **What it does:** Creates a text box (cell).
    * `0`: Makes the box span the full width of the page.
    * `10`: The height of the box.
    * `txt=f"..."`: The text to display, including the current category name.
    * `ln=True`: Tells the "cursor" to move to the next line after drawing this.
    * `align='C'`: Centers the text.

```python
    pdf.ln(10)
```
* **What it does:** Adds a vertical space of 10mm (like pressing "Enter" a few times).

---

### 4. Adding Analytics Metrics
```python
    #Analytics
    stats = get_analytics(group)
```
* **What it does:** Runs the function we imported earlier. It looks at the current `group` (e.g., all Electronics) and returns a dictionary of calculated numbers (Total Revenue, etc.).

```python
    pdf.set_font("Arial", size=12)
```
* **What it does:** Shrinks the font size to 12 for the summary section.

```python
    # Configuration for metrics
    metric_config = {
        "total_orders": ("Total Orders", "{}"),
        "total_revenue": ("Total Revenue", "${:.2f}"),
        "average_order": ("Average Order Value", "${:.2f}"),
        "total_quantity": ("Total Quantity Sold", "{}")
    }
```
* **What it does:** This is a "lookup table." It tells the script:
    * The **Key** in our `stats` dictionary (e.g., `"total_revenue"`).
    * The **Label** to show in the PDF (e.g., `"Total Revenue"`).
    * The **Format** (e.g., `"${:.2f}"` means "Add a $ sign and show 2 decimal places").

```python
    for key, (label, fmt) in metric_config.items():
```
* **What it does:** Loops through that lookup table we just made.

```python
        value = fmt.format(stats[key])
```
* **What it does:** Takes the raw number from `stats` and formats it (e.g., `1234.5` becomes `"$1234.50"`).

```python
        pdf.cell(0, 10, txt=f"{label}: {value}", ln=True)
```
* **What it does:** Prints that metric line into the PDF and moves to the next line.

```python
    pdf.ln(10)
```
* **What it does:** Adds another 10mm space before the table starts.

---

### 5. Creating the Data Table
```python
    # Dynamic Column Generation
    exclude_cols = ["category"]
```
* **What it does:** We don't want to repeat the "Category" name in every row of the table (since the whole report is about that category), so we list it here to exclude it.

```python
    display_cols = [col for col in group.columns if col not in exclude_cols]
```
* **What it does:** Creates a list of all columns we *actually* want to show in the table.

```python
    # Landscape usable width is roughly 277mm (297mm - 20mm margins)
    usable_width = 277
```
* **What it does:** Defines how much horizontal space we have to work with on the page.

```python
    col_width = usable_width / len(display_cols)
```
* **What it does:** Calculates how wide each column should be so they all fit perfectly across the page.

```python
    columns = [(col, col.replace("_", " ").title(), col_width) for col in display_cols]
```
* **What it does:** Prepares the column headers. It changes names like `"order_id"` to `"Order Id"` so they look professional.

```python
    # Table Headers - Bold and smaller font
    pdf.set_font("Arial", 'B', size=10)
```
* **What it does:** Sets the font to Bold (`'B'`) and size 10 for the header row.

```python
    for col_key, col_name, col_width in columns:
        pdf.cell(col_width, 10, col_name, 1, 0, 'C')
```
* **What it does:** Draws each header box.
    * `1`: Adds a border around the cell.
    * `0`: Tells the PDF *not* to move to the next line yet (so the next header is drawn to the right).

```python
    pdf.ln()
```
* **What it does:** Now that all headers are drawn, move to the next line for the data.

```python
    # Table Rows - Even smaller font to prevent overlap
    pdf.set_font("Arial", size=8)
```
* **What it does:** Makes the text even smaller (size 8) so the data rows don't get messy or overlap.

```python
    for _, row in group.iterrows():
```
* **What it does:** Loops through every single row of data for this category.

```python
        for col_key, col_name, col_width in columns:
            text = str(row[col_key])
            pdf.cell(col_width, 8, text, 1, 0, 'C')
```
* **What it does:** For every column in that row, it gets the data, converts it to text, and draws a bordered box.

```python
        pdf.ln()
```
* **What it does:** Moves to the next line after finishing a full row of data.

---

### 6. Saving the Result
```python
    #Save PDF
    pdf.output(f"output/{category}.pdf")
```
* **What it does:** This is the most important part! It saves all that formatting as a file in the `output` folder, named after the category (e.g., `Electronics.pdf`).

```python
print("PDFs generated.")
```
* **What it does:** Displays a message in your terminal so you know the script finished successfully.
