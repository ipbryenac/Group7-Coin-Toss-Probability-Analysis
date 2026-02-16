import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_continuous_graph():
    # --- CONFIGURATION ---
    # Please ensure this matches your file name exactly!
    # If your file is a CSV, change this to "Combined_All_Coin_Data.csv"
    file_name = "Combined_All_Coin_Data.xlsx" 
    
    print(f"Working Directory: {os.getcwd()}")
    
    # 1. Read the File
    # We try reading as Excel first, then CSV if that fails
    try:
        if file_name.endswith('.csv'):
            df = pd.read_csv(file_name)
        else:
            df = pd.read_excel(file_name)
        print(f"Successfully read {file_name}")
    except FileNotFoundError:
        print(f"Error: '{file_name}' not found. Please check the file name and folder.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 2. Extract Data
    # The columns in your file are: 'No. of Flips', 'Total Heads', 'Total Tails'
    try:
        # Ensure data is numeric
        n_flips = pd.to_numeric(df['No. of Flips'], errors='coerce')
        total_heads = pd.to_numeric(df['Total Heads'], errors='coerce')
        total_tails = pd.to_numeric(df['Total Tails'], errors='coerce')
        
        # Drop any empty rows
        df_clean = pd.DataFrame({
            'n': n_flips, 
            'Heads': total_heads, 
            'Tails': total_tails
        }).dropna()
        
    except KeyError as e:
        print(f"Error: Column {e} not found in the file. Please check your column names.")
        print("Expected: 'No. of Flips', 'Total Heads', 'Total Tails'")
        return

    # 3. Generate the Graph
    plt.figure(figsize=(12, 7))
    
    # Plot Accumulated Heads
    plt.plot(df_clean['n'], df_clean['Heads'], 
             label='Accumulated Heads', color='blue', linewidth=2)
    
    # Plot Accumulated Tails
    plt.plot(df_clean['n'], df_clean['Tails'], 
             label='Accumulated Tails', color='orange', linewidth=2)

    # 4. Styling
    plt.title('Continuous Coin Toss: Accumulated Heads vs Tails (1A to 20)', fontsize=14)
    plt.xlabel('Total Number of Flips (Continuous)', fontsize=12)
    plt.ylabel('Accumulated Count', fontsize=12)
    
    # Add a legend
    plt.legend()
    
    # Add a grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 5. Save and Show
    output_file = "Graph_Continuous_Race.png"
    plt.savefig(output_file)
    print(f"Graph saved as: {output_file}")
    
    print("Graph window opened. Close it to finish.")
    plt.show()

if __name__ == "__main__":
    generate_continuous_graph()