import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re

def generate_visual_report():
    excel_file = "2BSCS-A _ Tossed Coin Raw Data.xlsx"
    
    print(f"Reading {excel_file}...")
    try:
        all_sheets = pd.read_excel(excel_file, sheet_name=None, header=None)
    except FileNotFoundError:
        print("File not found. Please make sure the Excel file is in this folder.")
        return

    # --- 1. DATA EXTRACTION (Same logic as before) ---
    name_map = { 
        "1A": "1A", "1B": "1B", "1 (New)": "1B", "1 (Old)": "1A", "1 Peso Coin": "1A",
        "2": "2", "2 Peso Coin": "2", "20": "20",
        "5A": "5A", "5B": "5B", "5 (New)": "5B", "New 5 peso coin": "5B", "Old 5 peso coin": "5A",
        "10A": "10A", "10B": "10B", "10A(Peso Coin)": "10A"
    }

    file_configs = {
        1: [("1A", 3, 2), ("2", 6, 5)],
        2: [("1B", 3, 4), ("5A", 11, 12)],
        3: [("1B", 1, 2), ("10A", 9, 10)],
        4: [("5A", 3, 4), ("5B", 8, 9)],
        5: [("1A", 3, 4), ("1B", 9, 10)],
        6: [("5B", 3, 4), ("20", 8, 9)],
        7: [("5A", 4, 5), ("10A", 12, 13)],
        8: [("1A", 3, 4), ("10B", 9, 10)],
        9: [("5B", 3, 4), ("1B", 7, 8), ("20", 11, 12)],
        10: [("5B", 3, 4), ("10B", 8, 9)],
        11: [("1A", 4, 5), ("10B", 10, 11)],
        12: [("5B", 2, 4), ("5A", 8, 10)],
        13: [("1A", 1, 2), ("10A", 5, 6)],
        14: [("1A", 1, 2), ("20", 3, 4)],
        15: [("1B", 1, 2), ("5B", 9, 10)]
    }

    results = []
    
    for i in range(1, 16):
        group_num = i
        surface = "Table (Groups 1-8)" if group_num <= 8 else "Tiles (Groups 9-15)"
        
        target_sheet = None
        for sheet_name in all_sheets.keys():
            if re.search(r'GROUP[\s_-]*' + str(group_num) + r'(?![0-9])', sheet_name, re.IGNORECASE):
                target_sheet = sheet_name
                break
        
        if target_sheet:
            df = all_sheets[target_sheet]
            configs = file_configs.get(group_num, [])
            for coin_label, h_idx, t_idx in configs:
                try:
                    col_h = pd.to_numeric(df.iloc[2:, h_idx], errors='coerce').fillna(0)
                    col_t = pd.to_numeric(df.iloc[2:, t_idx], errors='coerce').fillna(0)
                    
                    if col_h.max() > 10 or col_t.max() > 10:
                        total_h, total_t = col_h.max(), col_t.max()
                    else:
                        total_h, total_t = col_h.sum(), col_t.sum()

                    std_name = name_map.get(coin_label, coin_label)
                    results.append({"Surface": surface, "Coin": std_name, "Heads": total_h, "Tails": total_t})
                except:
                    pass

    # --- 2. CALCULATE PERCENTAGES ---
    df_res = pd.DataFrame(results)
    summary = df_res.groupby(["Surface", "Coin"])[["Heads", "Tails"]].sum().reset_index()
    summary["Total"] = summary["Heads"] + summary["Tails"]
    summary["Heads_Pct"] = (summary["Heads"] / summary["Total"] * 100)

    # --- 3. CREATE THE VISUAL CHART ---
    # Filter for Table vs Tiles
    table_data = summary[summary["Surface"].str.contains("Table")]
    tiles_data = summary[summary["Surface"].str.contains("Tiles")]

    # Get list of unique coins found
    coins = sorted(summary["Coin"].unique())
    
    # Extract values for plotting (aligning by coin name)
    table_vals = []
    tiles_vals = []
    
    for coin in coins:
        # Get Table Value
        val = table_data[table_data["Coin"] == coin]["Heads_Pct"].values
        table_vals.append(val[0] if len(val) > 0 else 0)
        
        # Get Tiles Value
        val = tiles_data[tiles_data["Coin"] == coin]["Heads_Pct"].values
        tiles_vals.append(val[0] if len(val) > 0 else 0)

    # Plotting
    x = np.arange(len(coins))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 7))
    rects1 = ax.bar(x - width/2, table_vals, width, label='Table (Wood)', color='peru')
    rects2 = ax.bar(x + width/2, tiles_vals, width, label='Tiles (Hard)', color='teal')

    # Add theoretical 50% line
    ax.axhline(y=50, color='red', linestyle='--', linewidth=2, label='Theoretical Fair (50%)')

    # Labels and Title
    ax.set_ylabel('Percentage of Heads (%)', fontsize=12)
    ax.set_title('Coin Bias Analysis: Table vs. Tiles (Heads Probability)', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(coins, fontsize=12)
    ax.set_ylim(40, 70) # Zoom in on the 50% mark to see differences clearly
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Add value labels on top of bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f'{height:.1f}%',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9)

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    
    # Save and Show
    img_name = "Visual_Canvass_Chart.png"
    plt.savefig(img_name)
    print(f"Chart saved as {img_name}")
    print("Opening chart...")
    plt.show()

if __name__ == "__main__":
    generate_visual_report()