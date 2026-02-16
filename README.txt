 Coin Bias Analysis Project 🪙

 📊 Project Overview
An experimental analysis of coin fairness involving over 3,000 combined tosses. This project automates the processing of raw data from 15 different groups to determine if surface texture (Wooden Table vs. Hard Tiles) influences the probability of landing Heads or Tails.

 🚀 Key Features
Data Aggregation: Automates the extraction and cleaning of inconsistent raw data from multiple Excel sheets (`canvas.py`).
Visualization: Generates professional comparison bar charts to visualize the "Heads Probability" on different surfaces (`visual_canvas.py`).
Simulation: Includes a Pygame script to visually simulate the physics of a coin toss (`toss.py`).

## 📈 Results
The analysis reveals that while modern coins (1B, 5B) are consistent, older coins (1A) show significant bias depending on the surface:
Table: 64% Heads bias.
Tiles: 45% bias (favoring Tails).

 🛠️ Installation
1.  Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the analysis:
    ```bash
    python canvas.py
    ```