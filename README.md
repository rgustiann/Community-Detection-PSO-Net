# 🧠 Community Detection Using the PSO-Net Algorithm

A Python-based system for detecting communities in a network using the **PSO-Net** algorithm (Particle Swarm Optimization for Community Detection). Equipped with an interactive visual interface powered by **Streamlit** and the ability to save detection results.

---

## ✨ Features

- 🔍 Community detection from network datasets (graph) using the PSO-Net algorithm
- 📊 Interactive graph visualization
- 💾 Save detection results in exportable formats
- 🤝 Open for contributions!

---

## 📂 Dataset Format

Ensure your dataset is in **`.tsv` (Tab Separated Values)** format with the following column structure:
...
```
source<TAB>target
A<TAB>B
B<TAB>C
```
> **Note:** A header row is optional.

---

## 🚀 How to Run

1. **Clone this repository:**

```bash
git clone https://github.com/rgustiann/Community-Detection-PSO-Net.git
cd Community-Detection-PSO-Net
````

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the Streamlit application:**

```bash
streamlit run main.py
```

4. **Upload a .tsv file and start the community detection process.**

---

## 🛠 Technologies Used

* 🐍 Python 3
* 🎈 Streamlit
* 🕸️ NetworkX
* 📊 Matplotlib
* ⚙️ PSO (Particle Swarm Optimization) custom implementation

---

## 📌  Additional Notes
* The dataset must be a .tsv file with source and target columns (header optional).
* Small to medium-sized datasets are recommended for optimal performance.
* Provides interactive network visualization and the ability to save final results.
---

## 💡 Contribution

This project is **open source** and **open for contributions!**

Feel free to fork, submit a pull request, or start a discussion via [Issues](https://github.com/rgustiann/Community-Detection-PSO-Net/issues).

---

