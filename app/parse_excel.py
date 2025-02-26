import pandas as pd
import os
import shutil


def parse_folder(folder_path: str, path_added: str) -> pd.DataFrame:
    """
    This function reads all the excel files in the folder_path in this project files to parse is in "data_from_web" folder and extracts the columns "Date", "Heures" and "Consommation".
    It then moves the files to the path_added folder- "data_added".

    """
    os.makedirs(path_added, exist_ok=True)
    file_path_list = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]
    if file_path_list == []:
        print("⚠️ nothing to parse everything is added")
        return pd.DataFrame()
    print(f"📂 Found {len(file_path_list)} new files. Processing...")

    df_list = []
    for file_name in file_path_list:
        file_path = os.path.join(folder_path, file_name)  # ✅ Correct file path
        df = pd.read_excel(file_path, engine="openpyxl")
        df_selected = df[["Date", "Heures", "Consommation"]]
        df_selected.loc[:, "Date"] = pd.to_datetime(
            df_selected["Date"], format="%d/%m/%Y"
        )
        df_selected.loc[:, "Heures"] = pd.to_datetime(
            df_selected["Heures"], format="%H:%M:%S", errors="coerce"
        ).dt.time
        df_selected.loc[:, "Consommation"] = pd.to_numeric(
            df_selected["Consommation"], errors="coerce"
        )
        df_selected.rename(
            columns={
                "Date": "date",
                "Heures": "heures",
                "Consommation": "consommation",
            },
            inplace=True,
        )
        df_filtered = df_selected.dropna(subset=["consommation"])

        df_list.append(df_filtered)
        new_file_path = os.path.join(path_added, file_name)
        shutil.move(file_path, new_file_path)
        print(f"✅ Moved {file_name} to {new_file_path}")
    if df_list:
        df_all = pd.concat(df_list, ignore_index=True)
        return df_all
    else:
        return pd.DataFrame()


# print(parse_folder(r"data_from_web"))
