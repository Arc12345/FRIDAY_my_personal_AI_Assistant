from elevenlabs.conversational_ai.conversation import ClientTools
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import os
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

load_dotenv()


_dataframe_store: dict = {}

def _store_dataframe(key: str, df):
    _dataframe_store[key] = df

def _get_dataframe(key: str):
    return _dataframe_store.get(key)


SKIP_COLS = ['id', 'customer id', 'customerid', 'customer_id', 'index']



def searchWeb(parameters):
    """Search the web using DuckDuckGo."""
    query = parameters.get("query")
    if not query:
        return "Error: No query provided."
    try:
        search = DuckDuckGoSearchRun()
        results = search.run(query)
        return results
    except Exception as e:
        return f"Search failed: {e}"


def save_to_txt(parameters):
    """Save text to a file."""
    filename = parameters.get("filename")
    data = parameters.get("data")
    if not filename or data is None:
        return "Error: 'filename' and 'data' are required."
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(str(data) + "\n")
        return f"Saved to {filename} successfully."
    except Exception as e:
        return f"Failed to save file: {e}"


def create_html_file(parameters):
    """Create an HTML file with given title and content."""
    filename = parameters.get("filename")
    data = parameters.get("data")
    title = parameters.get("title", "Untitled")
    if not filename or data is None:
        return "Error: 'filename' and 'data' are required."
    try:
        formatted_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <div>{data}</div>
</body>
</html>"""
        with open(filename, "w", encoding="utf-8") as file:
            file.write(formatted_html)
        return f"HTML file '{filename}' created successfully."
    except Exception as e:
        return f"Failed to create HTML file: {e}"


def generate_image(parameters):
    """Generate an image using Pollinations AI (free, no API key needed)."""
    prompt = parameters.get("prompt")
    filename = parameters.get("filename", "generated.png")
    save_dir = parameters.get("save_dir", "generated_images")
    if not prompt:
        return "Error: 'prompt' is required."
    try:
        os.makedirs(save_dir, exist_ok=True)
        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            filename += ".png"
        filepath = os.path.join(save_dir, filename)
        print(f"[DEBUG] Saving to: {filepath}")
        encoded_prompt = requests.utils.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
        print(f"[DEBUG] Fetching from: {image_url}")
        image_response = requests.get(image_url, timeout=60)
        image_response.raise_for_status()
        print(f"[DEBUG] Downloaded {len(image_response.content)} bytes")
        image = Image.open(BytesIO(image_response.content))
        image.save(filepath)
        print(f"[DEBUG] Image saved to: {filepath}")
        return f"Image saved to {filepath}"
    except requests.RequestException as e:
        print(f"[ERROR] Download failed: {e}")
        return f"Failed to download image: {e}"
    except Exception as e:
        print(f"[ERROR] Unexpected: {e}")
        return f"Image generation failed: {e}"




def load_csv(parameters):
    """Load a CSV file and return a preview."""
    filepath = parameters.get("filepath")
    if not filepath:
        return "Error: 'filepath' is required."
    try:
        df = pd.read_csv(filepath)
        _store_dataframe(filepath, df)
        summary = {
            "rows":         int(df.shape[0]),
            "columns":      int(df.shape[1]),
            "column_names": list(df.columns),
            "preview":      df.head(5).to_string(),
        }
        print(f"[DEBUG] Loaded CSV: {filepath} — {df.shape[0]} rows, {df.shape[1]} cols")
        return json.dumps(summary)
    except Exception as e:
        return f"Failed to load CSV: {e}"


def clean_csv(parameters):
    """
    Clean a loaded CSV.
    operations: drop_duplicates | drop_nulls | fill_nulls | fix_dtypes
    """
    filepath   = parameters.get("filepath")
    operations = parameters.get("operations", ["drop_duplicates", "drop_nulls"])
    if not filepath:
        return "Error: 'filepath' is required."
    try:
        df = _get_dataframe(filepath)
        if df is None:
            df = pd.read_csv(filepath)

        report = []

        if "drop_duplicates" in operations:
            before = len(df)
            df = df.drop_duplicates()
            report.append(f"Removed {before - len(df)} duplicate rows.")

        if "drop_nulls" in operations:
            before = len(df)
            df = df.dropna()
            report.append(f"Dropped {before - len(df)} rows with null values.")

        if "fill_nulls" in operations:
            for col in df.select_dtypes(include=np.number).columns:
                df[col] = df[col].fillna(df[col].median())
            for col in df.select_dtypes(include="object").columns:
                df[col] = df[col].fillna("Unknown")
            report.append("Filled nulls with median/Unknown.")

        if "fix_dtypes" in operations:
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass
            report.append("Attempted to fix column data types.")

        _store_dataframe(filepath, df)
        clean_path = filepath.replace(".csv", "_cleaned.csv")
        df.to_csv(clean_path, index=False)
        report.append(f"Cleaned file saved to '{clean_path}'.")

        return " ".join(report)
    except Exception as e:
        return f"Cleaning failed: {e}"


def analyze_csv(parameters):
    """Analyze a loaded CSV and return insights."""
    filepath = parameters.get("filepath")
    if not filepath:
        return "Error: 'filepath' is required."
    try:
        df = _get_dataframe(filepath)
        if df is None:
            df = pd.read_csv(filepath)

        insights = []
        insights.append(f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns.")

  
        nulls = df.isnull().sum()
        null_cols = nulls[nulls > 0]
        if len(null_cols) > 0:
            insights.append(f"Columns with missing values: {dict(null_cols)}.")
        else:
            insights.append("No missing values found.")

        numeric = df.select_dtypes(include=np.number)
        clean_numeric = numeric[[c for c in numeric.columns if c.lower() not in SKIP_COLS]]
        if not clean_numeric.empty:
            insights.append(f"Numeric stats:\n{clean_numeric.describe().to_string()}")
            if len(clean_numeric.columns) > 1:
                corr_vals = clean_numeric.corr().to_numpy().copy()
                np.fill_diagonal(corr_vals, 0)
                max_idx = np.unravel_index(corr_vals.argmax(), corr_vals.shape)
                max_val = corr_vals[max_idx]
                if max_val > 0.5:
                    insights.append(
                        f"Strong correlation ({max_val:.2f}) between "
                        f"'{clean_numeric.columns[max_idx[0]]}' and '{clean_numeric.columns[max_idx[1]]}'."
                    )

        
        for col in df.select_dtypes(include="object").columns[:3]:
            top = df[col].value_counts().head(3).to_dict()
            insights.append(f"Top values in '{col}': {top}.")

        return "\n".join(insights)
    except Exception as e:
        return f"Analysis failed: {e}"


def plot_csv(parameters):
    """
    Generate a chart from CSV data and save it.
    chart_type: bar | line | histogram | scatter | heatmap
    """
    filepath   = parameters.get("filepath")
    chart_type = parameters.get("chart_type", "bar")
    x_col      = parameters.get("x_col")
    y_col      = parameters.get("y_col")
    save_dir   = parameters.get("save_dir", "charts")
    filename   = parameters.get("filename", f"{chart_type}_chart.png")

    if not filepath:
        return "Error: 'filepath' is required."
    try:
        df = _get_dataframe(filepath)
        if df is None:
            df = pd.read_csv(filepath)

        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)

        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor("#050a0f")
        ax.set_facecolor("#0a1520")

        numeric = df.select_dtypes(include=np.number)
        clean_numeric = numeric[[c for c in numeric.columns if c.lower() not in SKIP_COLS]]

        def best_numeric_col():
            """Pick first meaningful numeric column skipping ID columns."""
            for c in numeric.columns:
                if c.lower() not in SKIP_COLS:
                    return c
            return numeric.columns[0]

        def second_numeric_col():
            """Pick second meaningful numeric column skipping ID columns."""
            found = []
            for c in numeric.columns:
                if c.lower() not in SKIP_COLS:
                    found.append(c)
                if len(found) == 2:
                    return found[1]
            return numeric.columns[1] if len(numeric.columns) > 1 else numeric.columns[0]

        if chart_type == "histogram":
            col = x_col or best_numeric_col()
            df[col].hist(ax=ax, bins=20, color="#00cfff", edgecolor="#050a0f")
            ax.set_title(f"Distribution of {col}", color="#00cfff")

        elif chart_type == "bar":
            col_x = x_col or df.select_dtypes(include="object").columns[0]
            col_y = y_col or best_numeric_col()
            df.groupby(col_x)[col_y].sum().plot(kind="bar", ax=ax, color="#ffc400")
            ax.set_title(f"{col_y} by {col_x}", color="#ffc400")

        elif chart_type == "line":
            col_x = x_col or best_numeric_col()
            col_y = y_col or second_numeric_col()
            df.groupby(col_x)[col_y].mean().plot(ax=ax, color="#ff2d2d", linewidth=2)
            ax.set_title(f"Avg {col_y} over {col_x}", color="#ff2d2d")

        elif chart_type == "scatter":
            col_x = x_col or best_numeric_col()
            col_y = y_col or second_numeric_col()
            ax.scatter(df[col_x], df[col_y], color="#00cfff", alpha=0.4, s=15)
            ax.set_xlabel(col_x, color="#c8eaf5")
            ax.set_ylabel(col_y, color="#c8eaf5")
            ax.set_title(f"{col_x} vs {col_y}", color="#00cfff")

        elif chart_type == "heatmap":
            if not clean_numeric.empty:
                sns.heatmap(
                    clean_numeric.corr(), ax=ax, annot=True,
                    fmt=".2f", cmap="Blues", linewidths=0.5
                )
                ax.set_title("Correlation Heatmap", color="#00cfff")

        ax.tick_params(colors="#c8eaf5")
        for spine in ax.spines.values():
            spine.set_edgecolor("#1a3040")

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, facecolor=fig.get_facecolor())
        plt.close()
        print(f"[DEBUG] Chart saved: {save_path}")
        return f"Chart saved to '{save_path}'."
    except Exception as e:
        return f"Plot failed: {e}"



client_tools = ClientTools()


client_tools.register("searchWeb",      searchWeb)
client_tools.register("saveToTxt",      save_to_txt)
client_tools.register("createHtmlFile", create_html_file)
client_tools.register("generateImage",  generate_image)

# Data analytics
client_tools.register("loadCsv",        load_csv)
client_tools.register("cleanCsv",       clean_csv)
client_tools.register("analyzeCsv",     analyze_csv)
client_tools.register("plotCsv",        plot_csv)
