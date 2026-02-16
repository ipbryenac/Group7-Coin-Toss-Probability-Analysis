import pandas as pd
import matplotlib.pyplot as plt
import os

def process_all_coins():
    # --- CONFIGURATION ---
    file_name = "cs.xlsx"  # Make sure this matches your file name!
    
    # Based on your file structure:
    # Row 5 (Index 4) has headers like "Number of Flips", "Heads", "Total Heads"
    # Row 6 (Index 5) is where the data starts
    header_row = 4
    data_start_row = 5
    
    # Column Index for "Number of Flips" (Shared by all coins)
    col_n = 25 

    # Define where each coin starts (The 'Heads' column index)
    # The pattern in your file is: Heads, Tails, Total Heads, Total Tails (4 cols per coin)
    coins = {
        "1A":  26,
        "1B":  30,
        "2":   34,
        "5A":  38,
        "5B":  42,
        "10A": 46,
        "10B": 50,
        "20":  54
    }

    print(f"Working Directory: {os.getcwd()}")
    print(f"Reading file: {file_name}...")

    try:
        # Read the file without header first to access by index
        df = pd.read_excel(file_name, header=None)
    except FileNotFoundError:
        print(f"Error: '{file_name}' not found. Please move it to this folder.")
        return

    # Create a sub-folder for organized output (Optional but clean)
    output_folder = "Coin_Results"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    # --- LOOP THROUGH EACH COIN ---
    for coin_name, start_col in coins.items():
        print(f"\nProcessing Coin: {coin_name}...")

        # 1. Extract Data for this specific coin
        # We grab: Number of Flips (Shared), Total Heads (start+2), Total Tails (start+3)
        try:
            # Column Indices
            idx_n = col_n
            idx_acc_h = start_col + 2
            idx_acc_t = start_col + 3
            
            # Extract and Clean
            coin_data = df.iloc[data_start_row:, [idx_n, idx_acc_h, idx_acc_t]].copy()
            coin_data.columns = ['n', 'Acc_Heads', 'Acc_Tails']
            coin_data = coin_data.apply(pd.to_numeric, errors='coerce').dropna()

            if coin_data.empty:
                print(f"  Warning: No data found for {coin_name}. Skipping.")
                continue

            # 2. Save Data to a SEPARATE File (CSV)
            # This makes it "easy to locate" the raw data for just this coin
            csv_filename = os.path.join(output_folder, f"Data_{coin_name}.csv")
            coin_data.to_csv(csv_filename, index=False)
            print(f"  -> Data saved: {csv_filename}")

            # 3. Generate the Graph
            plt.figure(num=f"Coin {coin_name}", figsize=(10, 6))
            
            plt.plot(coin_data['n'], coin_data['Acc_Heads'], 
                     label='Accumulated Heads', color='blue', linewidth=2)
            plt.plot(coin_data['n'], coin_data['Acc_Tails'], 
                     label='Accumulated Tails', color='orange', linewidth=2)

            # Styling
            plt.title(f'Coin {coin_name}: Accumulated Heads vs Tails', fontsize=14)
            plt.xlabel('Number of Flips', fontsize=12)
            plt.ylabel('Accumulated Count', fontsize=12)

            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)

            # 4. Save the Graph Image
            img_filename = os.path.join(output_folder, f"Graph_{coin_name}.png")
            plt.savefig(img_filename)
            print(f"  -> Graph saved: {img_filename}")

            plt.show()
            
            # Close the plot to free memory (remove this line if you want to see them pop up)
            plt.close() 

        except Exception as e:
            print(f"  Error processing {coin_name}: {e}")

    print("\nDone! Check the 'Coin_Results' folder.")

if __name__ == "__main__":
    process_all_coins()