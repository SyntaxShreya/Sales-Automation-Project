import pandas as pd

def get_analytics(df):
    """Calculates sales summary metrics from a DataFrame."""
    total_revenue = df["total_price"].sum()
    total_orders = len(df)
    average_order = df["total_price"].mean()
    total_quantity = df["qty"].sum()
    
    # top_product is useful for the full dataset
    top_product = None
    if not df.empty and "category" in df.columns:
        top_product = df["category"].value_counts().idxmax()

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_order": average_order,
        "total_quantity": total_quantity,
        "top_product": top_product
    }

if __name__ == "__main__":
    file_path = "DATA/orders.csv"
    df = pd.read_csv(file_path)

    stats = get_analytics(df)

    output_excel = "output/sales_summary.xlsx"

    summary_df = pd.DataFrame({
        "Metric": ["Total Revenue", "Total Orders", "Average Order Value", "Top Product"],
        "Value": [stats["total_revenue"], stats["total_orders"], stats["average_order"], stats["top_product"]]
    })

    summary_df.to_excel(output_excel, index=False)
    print("Excel report saved.")
