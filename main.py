# %%
# Loading modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# Loading data from Excel
df = pd.read_excel('data/LV_Datenbank.xlsx', sheet_name='Daten Trägersysteme 2021')

# %%
# Creating a dataframe with all fuel types
df_fuel = pd.DataFrame(pd.unique(df[['stage1_fuel', 'stage2_fuel', 'stage3_fuel', 'stage4_fuel', 'stage5_fuel']].values.ravel('K')), columns=['fuel'])

# Dropping NaN Value
df_fuel = df_fuel.dropna()

# Setting Fuel as index
df_fuel = df_fuel.set_index('fuel')

# %%
# Adding the stoichiometric combustion products per kg fuel

# ['RP-1/LOX', 'Al/AP/HTPB', 'HTPB', 'N2O4/UDMH', 'LH2/LOX', 'Jet A/LOX', 'TH-H8299/Al', 'Hydrazine', 'MMH/MON']
df_fuel['CO2'] = np.array([3.15, 0.385690653, 3.214088774, 1.464583369, 0, 3.15, 0, 0, 0.955238504])
df_fuel['H2O'] = np.array([1.26, 0.277903767, 0.993343379, 1.199053817, 8.936682739, 1.26, 0, 1.124368235, 1.17308007])
df_fuel['N2'] = np.array([0, 0.0140067, 0, 1.398378524, 0, 0, 0, 1.311277585, 2.736174062])
df_fuel['O2'] = np.array([0, 0.23490668, 0, 0, 0, 0, 0, 0, 0])
df_fuel['HCl'] = np.array([0, 0.214130989, 0, 0, 0, 0, 0, 0, 0])
df_fuel['Al2O3'] = np.array([0, 0.358998351, 0, 0, 0, 0, 0, 0, 0])

print(df_fuel)

# %%
# Replacing NaN with 0 within the original dataframe for further calculations
df = df.fillna(0)

# %%
# Creating a dataframe based on the factors of "df_fuel" and the used fuel type from "df"
# Multipling it by the stage mass for every product and every stage
for stage in np.arange(1, 6):
    for product in df_fuel.columns:
        df_temp = []
        for fuel_type in df['stage{0}_fuel'.format(stage)]:
            df_temp.append(df_fuel[product][fuel_type])
        df['stage{0}_{1}'.format(stage, product)] = df['stage{0}_mass_fuel'.format(stage)]*df_temp

df


# %%
# Exporting results

df.to_excel("output.xlsx") 



