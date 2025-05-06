
# 🧠 KEY_CLUSTER_PROJECT

**KEY_CLUSTER_PROJECT** - is a desktop keyword clustering program with a graphical interface based on **Tkinter**. 
It allows you to load keyword phrases, clean them, analyze them, and automatically combine them into meaningful clusters.

---

## 🚀 Key features

- Load keywords from a file or manually;
- Automatically clean text from noise;
- Build phrase embeddings;
- Clustering using KMeans
- Output results in a convenient format;
- Save clustered phrases to a file;
- Graphical user interface (GUI).

---

## 🗂️ Project structure

```
KEY_CLUSTER_PROJECT/
├── app.py                  # Main startup file
│
├── controller/
│ └── app_controller.py     # GUI and core interaction logic
│
├── core/
│ ├── clusterizer.py        # Phrase clustering
│ ├── data_cleaner.py       # Text cleaning
│ ├── data_loader.py        # Data loading
│ └── result_saver.py       # Result saving
│
├── gui/
│ ├── app_gui.py            # GUI startup
│ ├── base.py               # Base classes
│ ├── gui_style.py          # Interface styling
│
│ ├── main_window/
│ │ ├── gui_main_window.py  # Main window
│ │ ├── top_frame.py
│ │ ├── left_frame.py
│ │ ├── right_frame.py
│ │ └── bottom_frame.py
│
│ ├── process_window/
│ │ ├── gui_process_window.py # Clustering process window
│ │ └── process_frame.py
│
│ └── result_window/
│ ├── gui_result_window.py  # Results window
│ └── result_frame.py
```

---

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/zinaliashenko/key_cluster_project.git
cd key_cluster_project
```

2. Create a virtual environment and activate it (recommended):
```bash
conda env create -f environment.yml
conda activate key_cluster_env
```

3. Download required spaCy model:
```bash
python -m spacy download en_core_web_trf
```

## ▶️ Launching

```bash
python app.py
```

---

## 🛠️ Technologies:

- Python 3.10+
- Tkinter
- scikit-learn
- pandas
- sentence-transformers
- numpy

---

## 📁 Folders `data/` and `results/`

- `data/` - input files with keywords are stored (in .txt or .csv format).
- `results/` - clustering results are automatically saved.

> These folders are added to `.gitignore` and do not get into the repository.

---

## 📬 Contact

**Author:** [zinaliashenko](https://github.com/zinaliashenko)
I'd love to receive feedback, ideas or PR!
