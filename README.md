# TikTok Integrity & Influence: A Misinformation Dashboard

## Overview

This project investigates the landscape of mis/disinformation* and content integrity on TikTok by analyzing metadata and moderator reports on how content is flagged as "claims" versus "opinions." Using a dataset of over 19,000 TikTok videos, the dashboard visualizes the flow of content verification and examines whether video metadata--specifically duration--correlates with content integrity. The main insight demonstrates that claim-based videos are often shorter and less verified, creating a high-speed environment where malcontent can thrive. By mapping these content journeys, the project aims to identify patterns in how misinformation spreads.

> *mis = unintentional; dis = intentional

## Project Structure

```
├───assets
├───data
│   └───tiktok_dataset.csv
├───notebooks: contains notebook to extract data from kaggle and set up api use. (uploaded)
├───pages: contains all the pages for the dash app
├───results: contains some html visualizations that were generated separately
└───src: the scripts used for the results visualizations,
```

## Data

The analysis uses a pedagogical dataset provided by Ramin Huseyn on [Kaggle](https://www.kaggle.com/datasets/raminhuseyn/dataset-from-tiktok/data). It contains video metadata, verification statuses, and moderator review labels.

* **Source:** `raminhuseyn/dataset-from-tiktok` via Kaggle API.
* **Location:** Data should be stored in the `data/` directory.
* **Format:** Comma separated values.
* **Access:** To refresh/download the data, you must provide a Kaggle API key. Instructions to procure one are provided below. Alternatively, you can download the data directly from Kaggle and move it into the `data/` directory.
* **License:** The creator, Ramin Huseyn, has licensed this dataset under the Public Domain (CC0).

## Environment Setup

You can set up this project using either `uv` (recommended for speed or beginners) or the standard `venv`.

### Option A: Using `uv`

```bash
# Clone the repository
git clone https://github.com/lowellmonis/tiktok-dashboard.git
cd tiktok-dashboard

# Create environment and install dependencies; you should not need to create an environment from scratch
uv sync
```

### Option B: Using `venv`

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# To deactivate
deactivate
```

### Kaggle API Configuration

To pull the data, you need a `.env` file in the root directory:

1. Go to **Kaggle Settings** > **API** > **Create New Token**.
2. Create a file named `.env` and add:
`KAGGLE_API_TOKEN=your_token_here`

## How to Reproduce Results

Follow these steps to go from a fresh clone to a fully interactive dashboard.

### Step 1: Extract the Data (Optional; the dataset is included)

Follow the instructions on the [extraction notebook](notebooks/data_extraction.ipynb) to pull the dataset directly from Kaggle and place it in the `data/` folder.

To open JupyterLab:

```bash
# If using uv
uv run jupyter lab

# If using venv
jupyter lab
```
Once Jupyter Lab opens, navigate to the `notebooks/` folder and open `data_extraction.ipynb`.

* **Expected Outcome:** A file named `tiktok_dataset.csv` will appear in your `data/` directory.

### Step 2: Generate Standalone Visualizations (Recommended to experiment with `uv`; visualizations already exist)

If you want to generate the specific HTML results (Sankey and KDE plots) located in the `results/` folder, run the source scripts from the root:

```bash
# If using uv
uv run src/content_journey_sankey.py
uv run src/duration_content_type_kde.py

# If using venv
python src/content_journey_sankey.py
python src/duration_content_type_kde.py

```

* **Expected Outcome:** New `.html` files will be created in the `results/` directory showing content flows and duration dynamics.

### Step 3: Launch the Dashboard

Run the Dash application locally:

```bash
python app.py

```

* **Expected Outcome:** The terminal will provide a local URL (e.g., `http://127.0.0.1:8050`). Open this in your browser to engage with the dashboard.

> [!TIP]
> You can also view the live deployment [here](https://lowell-monis-tiktok-dashboard.share.connect.posit.cloud).

## Troubleshooting / Known Issues

* **Pathing:** This project uses relative paths (e.g., `../data/`). If you run scripts from *inside* the `src` folder instead of the root, they may fail to find the CSV. Always run from the root.
* **Python Version:** Requires Python 3.9+ due to specific dataframe operations and `kagglehub` requirements. Always use a virtual environment to avoid any errors. If `python` does not work on the terminal, try `python3`.
* **File Signature Error:** If you see `PK` characters when opening the CSV, the file is still zipped. Ensure you have run the extraction logic in `data_extraction.ipynb` which handles `zipfile` unbundling.
* **Memory:** The KDE calculation in `src/` uses `scipy.stats.gaussian_kde`, which can be memory-intensive on very old hardware but should run fine on standard laptops.
* **Naming conventions:** Check the `.gitignore` for what file names you can't use (like `sandbox`). If you really want to use that name, remove it from the `.gitignore` file.
* **Kaggle Auth Fail:** If the download fails, ensure your `.env` file is in the root directory and your `KAGGLE_API_TOKEN` is correct.
* **ModuleNotFoundError:** If a package is missing in Jupyter, ensure you have selected the correct kernel (usually named `.venv` or `python3`) from the top-right corner of the notebook.

## Contributing

Contributions are welcome! To propose changes:

1. Fork the repository.
2. Create a Feature Branch (git checkout -b feature/AmazingFeature).
3. Commit your changes (git commit -m 'Add some AmazingFeature').
4. Push to the branch (git push origin feature/AmazingFeature).
5. Open a Pull Request.

For bugs, please open an Issue with a detailed description and steps to reproduce. Thank you!