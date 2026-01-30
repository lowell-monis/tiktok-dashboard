# TikTok Integrity & Influence: A Misinformation Dashboard

## Overview

This project investigates the landscape of misinformation on TikTok by analyzing how content is flagged as "claims" versus "opinions." Using a dataset of over 19,000 TikTok videos, the dashboard visualizes the flow of content verification and examines whether video metadata—specifically duration—correlates with content integrity. The main insight demonstrates that claim-based videos are often shorter and less verified, creating a high-speed environment where misinformation can thrive.

## Data

The analysis uses a pedagogical dataset provided by [Kaggle](https://www.kaggle.com/datasets/raminhuseyn/dataset-from-tiktok/data). It contains video metadata, verification statuses, and moderator review labels.

* **Source:** `raminhuseyn/dataset-from-tiktok` via Kaggle API.
* **Location:** Data is stored in the `data/` directory (git-ignored to maintain repository light-weightness).
* **Format:** CSV.
* **Access:** To download the data, you must provide a Kaggle API key (see [Environment Setup](https://www.google.com/search?q=%2353-environment-setup)).

## Environment Setup

You can set up this project using either `uv` (recommended for speed) or the standard `venv`.

### Option A: Using `uv`

```bash
# Clone the repository
git clone https://github.com/lowellmonis/tiktok-integrity-analysis.git
cd tiktok-integrity-analysis

# Create environment and install dependencies
uv sync

```

### Option B: Using `venv`

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### Kaggle API Configuration

To pull the data, you need a `.env` file in the root directory:

1. Go to **Kaggle Settings** > **API** > **Create New Token**.
2. Create a file named `.env` and add:
`KAGGLE_API_TOKEN=your_token_here`

## How to Reproduce Results

Follow these steps to go from a fresh clone to a fully interactive dashboard.

### Step 1: Extract the Data

Run the extraction notebook to pull the dataset directly from Kaggle and place it in the `data/` folder.

```bash
jupyter nbconvert --to notebook --execute notebooks/data_extraction.ipynb

```

* **Expected Outcome:** A file named `tiktok_dataset.csv` will appear in your `data/` directory.

### Step 2: Generate Standalone Visualizations

If you want to generate the specific HTML results (Sankey and KDE plots) located in the `results/` folder, run the source scripts from the root:

```bash
python src/generate_sankey.py
python src/generate_kde.py

```

* **Expected Outcome:** New `.html` files will be created in the `results/` directory showing content flows and duration dynamics.

### Step 3: Launch the Dashboard

Run the Dash application locally:

```bash
python app.py

```

* **Expected Outcome:** The terminal will provide a local URL (e.g., `http://127.0.0.1:8050`). Open this in your browser to view the "Content Journey" and "Duration Dynamics" pages.

> [!TIP]
> You can also view the live deployment here: [Link to Posit Cloud/Connect]

## Troubleshooting / Known Issues

* **Pathing:** This project uses relative paths (e.g., `../data/`). If you run scripts from *inside* the `src` folder instead of the root, they may fail to find the CSV. Always run from the root.
* **Python Version:** Requires Python 3.9+ due to specific dataframe operations and `kagglehub` requirements.
* **File Signature Error:** If you see `PK` characters when opening the CSV, the file is still zipped. Ensure you have run the extraction logic in `data_extraction.ipynb` which handles `zipfile` unbundling.
* **Memory:** The KDE calculation in `src/` uses `scipy.stats.gaussian_kde`, which can be memory-intensive on very old hardware but should run fine on standard student laptops.