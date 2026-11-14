import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Smart Warehouse Intelligence", page_icon="📦", layout="wide")

st.title("📦 Inteligentny System Zarządzania Magazynem i Logistyką")
st.markdown("Aplikacja demonstruje wykorzystanie **trzech poziomów analityki danych** w procesach logistycznych.")

# Przykładowe dane symulacyjne dla magazynu
@st.cache_data
def load_data():
    data = pd.DataFrame({
        'ID_Zamowienia': [101, 102, 103, 104, 105],
        'Pracownik': ['Jan Kowalski', 'Anna Nowak', 'Piotr Zieliński', 'Katarzyna Wójcik', 'Michał Lewandowski'],
        'Czas_Pakowania_min': [15, 22, 12, 35, 18],
        'Status': ['Zakończone', 'Zakończone', 'Zakończone', 'Opóźnione', 'W toku'],
        'Błędy': [0, 1, 0, 3, 0]
    })
    return data

df = load_data()

# Zakładki dla poszczególnych analiz
tab1, tab2, tab3 = st.tabs(["📊 1. Analiza Deskryptywna", "🔮 2. Analiza Predykcyjna", "⚙️ 3. Analiza Preskryptywna"])

with tab1:
    st.header("Analiza Deskryptywna (Descriptive Analytics) – *Co się stało?*")
    st.write("Prezentacja danych historycznych dotyczących realizacji zamówień i pracy magazynu.")
    st.dataframe(df)
    st.metric(label="Średni czas pakowania paczki", value=f"{df['Czas_Pakowania_min'].mean():.1f} min")
    st.metric(label="Łączna liczba popełnionych błędów", value=int(df['Błędy'].sum()))

with tab2:
    st.header("Analiza Predykcyjna (Predictive Analytics) – *Co się może wydarzyć?*")
    st.write("Wykrywanie potencjalnych zagrożeń, opóźnień i ryzyka na podstawie bieżących wskaźników.")
    
    # Symulacja predykcji ryzyka
    risk_df = df.copy()
    risk_df['Ryzyko_Opóźnienia'] = risk_df['Czas_Pakowania_min'].apply(lambda x: 'Wysokie 🔴' if x > 20 else 'Niskie 🟢')
    st.dataframe(risk_df[['ID_Zamowienia', 'Pracownik', 'Czas_Pakowania_min', 'Ryzyko_Opóźnienia']])
    st.warning("⚠️ Wykryto wysokie ryzyko opóźnienia w zamówieniu #104 (czas pakowania przekracza normę).")

with tab3:
    st.header("Analiza Preskryptywna (Prescriptive Analytics) – *Co powinniśmy zrobić?*")
    st.write("System rekomendacyjny optymalizujący działania i podpowiadający najlepsze decyzje.")
    
    st.success("✅ **Rekomendacja systemu:**")
    st.markdown("- Aby zoptymalizować czas i uniknąć opóźnień, przydziel najbardziej efektywnego pracownika (**Piotr Zieliński** - średni czas: 12 min) do pilnych zadań pakowania.")
    st.markdown("- Skieruj pracownika **Katarzyna Wójcik** na dodatkowe szkolenie z procedur pakowania w celu redukcji błędów.")
