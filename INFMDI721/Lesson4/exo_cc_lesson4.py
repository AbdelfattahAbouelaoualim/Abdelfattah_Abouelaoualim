import requests
import pandas as pd
import re

URL = 'https://www.open-medicaments.fr/api/v1/medicaments?limit=100&query=paracetamol'

try:
    page = requests.get(URL)
    data = page.json()
except:
    raise Exception('Requests failed!')
df = pd.DataFrame(data)
df = df['denomination'].str.split(',', expand=True)
df = df.rename(index=str, columns={0: "Nom", 1: "Type"})
df1 = df["Nom"].str.extract(r'([\D]*)(\d+)(.*)')
df2 = df["Type"].str.strip().str.split(" ").str.get(0)
df1 = df1.rename(index=str, columns={0: "Nom", 1: "Dosage", 2: "Unité"})
df1["Type"] = df2
print(df1)
