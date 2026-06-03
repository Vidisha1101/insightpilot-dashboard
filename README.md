<div align="center">

# 📊 InsightPilot

### An intelligent, interactive data analytics dashboard built with Python & Streamlit

[![Live App](https://img.shields.io/badge/🌐_Live_App-Streamlit-FF4B4B?style=for-the-badge)](https://insightpilot-dashboard.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 🌐 Live Demo

> **👉 [https://insightpilot-dashboard.streamlit.app/](https://insightpilot-dashboard.streamlit.app/)**

---

## 📌 Overview

**InsightPilot** is a no-code, browser-based analytics dashboard that lets you explore, filter, and visualize datasets instantly. Built for data analysts, students, and business teams who need **fast answers from raw data** — no coding required.

Upload a CSV, configure your metrics, and get a live interactive report in seconds.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 **CSV Upload** | Drag & drop any CSV file — smart column detection included |
| 📈 **Interactive Charts** | Bar, line, scatter, histogram powered by Plotly |
| 🔎 **Smart Filters** | Sidebar controls to slice data by column, date range, or category |
| 📊 **KPI Summary** | Auto-calculated mean, sum, count as live stat cards |
| ⬇️ **Export Data** | Download filtered results as CSV with one click |
| ☁️ **Cloud Deployed** | Live on Streamlit Community Cloud — no install needed |

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat) | Core backend logic |
| ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=flat) | Web UI framework |
| ![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white&style=flat) | Data manipulation |
| ![Plotly](https://img.shields.io/badge/-Plotly-3F4F75?logo=plotly&logoColor=white&style=flat) | Interactive visualizations |
| ![NumPy](https://img.shields.io/badge/-NumPy-013243?logo=numpy&logoColor=white&style=flat) | Numerical computations |
| HTML / CSS / JS | Custom styling & UI components |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/insightpilot.git
cd insightpilot

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open your browser at **`http://localhost:8501`**

---

## 📁 Project Structure

```
insightpilot/
├── assets/            # Static files, icons, images
├── components/        # Reusable UI components
├── pages/             # Multi-page app modules
├── app.py             # Main Streamlit entry point
├── utils.py           # Data processing helpers
├── requirements.txt   # Python dependencies
└── README.md
```

---

## 📦 Requirements

```txt
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.15.0
numpy>=1.24.0
```

Install all at once:

```bash
pip install streamlit pandas plotly numpy
```

---

## 🖥️ Usage

1. Open the live app or run it locally
2. **Upload** your CSV file using the file uploader
3. **Select** columns for X and Y axes from the sidebar
4. **Apply filters** to narrow down your dataset
5. **Explore** the auto-generated charts and KPI cards
6. **Download** the filtered data as CSV

---

## 🌍 Deployment

The app is deployed on **Streamlit Community Cloud**. To deploy your own fork:

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set the main file path to `app.py`
5. Click **Deploy** 🚀

---

## 🤝 Contributing

Contributions are welcome!

```bash
# Fork the repo, then:
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature
# Open a Pull Request
```

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 👩‍💻 Author

Made with ❤️ using [Streamlit](https://streamlit.io)

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=flat&logo=github)](https://github.com/YOUR_USERNAME)

---

<div align="center">
  <sub>⭐ Star this repo if you found it useful!</sub>
</div>
