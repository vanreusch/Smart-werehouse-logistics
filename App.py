import streamlit as st
import pandas as pd
import numpy as np

# Konfiguracja strony
st.set_page_config(
    page_title="System Analityki Magazynowej - Pakowanie Paczek",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inteligentny System Zarządzania Procesem Pakowania Paczek")
st.markdown("""
Narzędzie analityczne wspomagające zarządzanie magazynem. System zbiera dane o pracy zespołu, 
prognozuje zapotrzebowanie na pracowników i ryzyko opóźnień, a następnie optymalizuje przydział zadań.
""")

# --- INICJALIZACJA DANYCH W PAMIĘCI SESJI ---
if 'pracownicy_df' not in st.session_state:
    st.session_state.pracownicy_df = pd.DataFrame({
        'Pracownik': ['Jan Kowalski', 'Anna Nowak', 'Piotr Zieliński', 'Katarzyna Wójcik', 'Michał Lewandowski'],
        'Zespół': ['Zespół A (Standard)', 'Zespół B (Ekspres)', 'Zespół B (Ekspres)', 'Zespół A (Standard)', 'Zespół C (Gabaryty)'],
        'Spakowane_Paczki': [45, 60, 68, 32, 50],
        'Czas_Pracy_min': [360, 360, 340, 380, 350],
        'Błędy_Pakowania': [1, 0, 0, 4, 2]
    })

# --- SEKCJA KROK 1: WPROWADZANIE DANYCH WEJŚCIOWYCH ---
st.header("🛠️ KROK 1: Dane Wejściowe (Konfiguracja zespołu i celu)")

col_form, col_cel = st.columns([1.2, 1])

with col_form:
    st.subheader("1A. Dodaj pracownika i jego wyniki historyczne")
    with st.form("dodaj_pracownika_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        imie = c1.text_input("Imię i nazwisko pracownika:", placeholder="np. Tomasz Mazur")
        zespol = c2.selectbox("Przypisany zespół:", ["Zespół A (Standard)", "Zespół B (Ekspres)", "Zespół C (Gabaryty)"])
        
        c3, c4, c5 = st.columns(3)
        paczki = c3.number_input("Liczba spakowanych paczek:", min_value=1, max_value=500, value=50)
        czas = c4.number_input("Łączny czas pracy (min):", min_value=10, max_value=1440, value=360)
        bledy = c5.number_input("Liczba błędów / reklamacji:", min_value=0, max_value=100, value=1)
        
        dodaj_btn = st.form_submit_button("➕ Dodaj pracownika do tabeli")
        
        if dodaj_btn:
            if imie.strip() == "":
                st.warning("⚠️ Wpisz imię i nazwisko pracownika!")
            else:
                nowy_wiersz = pd.DataFrame({
                    'Pracownik': [imie.strip()],
                    'Zespół': [zespol],
                    'Spakowane_Paczki': [paczki],
                    'Czas_Pracy_min': [czas],
                    'Błędy_Pakowania': [bledy]
                })
                st.session_state.pracownicy_df = pd.concat([st.session_state.pracownicy_df, nowy_wiersz], ignore_index=True)
                st.success(f"✅ Dodano pracownika: {imie}")

    # Przyciski zarządzania bazą
    b1, b2, b3 = st.columns(3)
    if b1.button("🗑️ Usuń ostatni wiersz"):
        if len(st.session_state.pracownicy_df) > 0:
            st.session_state.pracownicy_df = st.session_state.pracownicy_df.iloc[:-1]
            st.rerun()
    if b2.button("🔄 Przywróć dane przykładowe"):
        del st.session_state.pracownicy_df
        st.rerun()
    if b3.button("🧹 Wyczyść całą tabelę"):
        st.session_state.pracownicy_df = pd.DataFrame(columns=['Pracownik', 'Zespół', 'Spakowane_Paczki', 'Czas_Pracy_min', 'Błędy_Pakowania'])
        st.rerun()

with col_cel:
    st.subheader("1B. Ustaw plan i zapotrzebowanie na kolejną zmianę")
    st.markdown("Wpisz parametry nowego zlecenia, które system ma przeanalizować i rozdzielić:")
    
    planowane_paczki = st.number_input("📦 Liczba wszystkich paczek do spakowania na zmianie:", min_value=10, max_value=10000, value=320, step=10)
    w_tym_pilne = st.slider("🔥 W tym paczki PILNE / VIP (wymagające najwyższej jakości):", min_value=0, max_value=planowane_paczki, value=min(80, planowane_paczki))
    czas_zmiany_h = st.number_input("⏱️ Dostępny czas na realizację zlecenia (w godzinach):", min_value=1.0, max_value=24.0, value=6.0, step=0.5)
    norma_czasu_min = st.slider("🎯 Dopuszczalna norma czasu na 1 paczkę (min):", min_value=2.0, max_value=20.0, value=8.0, step=0.5)

st.divider()

# Sprawdzenie czy w tabeli są jacykolwiek pracownicy
df = st.session_state.pracownicy_df.copy()

if len(df) == 0:
    st.error("⚠️ Tabela pracowników jest pusta! Dodaj przynajmniej jednego pracownika w formularzu powyżej, aby uruchomić analizy.")
    st.stop()

# --- OBLICZENIA BAZOWE DLA WSZYSTKICH ANALIZ ---
df['Średni_Czas_1_Paczki_min'] = (df['Czas_Pracy_min'] / df['Spakowane_Paczki']).round(2)
df['Wydajność_Paczki_na_h'] = (60 / df['Średni_Czas_1_Paczki_min']).round(1)
df['Wskaźnik_Błędów_proc'] = ((df['Błędy_Pakowania'] / df['Spakowane_Paczki']) * 100).round(2)

# Punktacja efektywności (im szybciej i mniej błędów, tym wyższy wynik)
df['Ocena_Efektywności'] = (df['Wydajność_Paczki_na_h'] * 2 - df['Wskaźnik_Błędów_proc'] * 3).round(1)

# --- SEKCJA KROK 2: TRZY POZIOMY ANALITYKI ---
st.header("📈 KROK 2: Wyniki Analiz (Przetwarzanie danych i wnioski)")

tab1, tab2, tab3 = st.tabs([
    "📊 1. Analiza Deskryptywna (Co się stało?)",
    "🔮 2. Analiza Predykcyjna (Co się może wydarzyć?)",
    "⚙️ 3. Analiza Preskryptywna (Co powinniśmy zrobić?)"
])

# ==========================================
# ZAKŁADKA 1: ANALIZA DESKRYPTYWNA
# ==========================================
with tab1:
    st.subheader("📊 Analiza Deskryptywna – Ocena dotychczasowej pracy zespołu")
    
    st.markdown("""
    * **📥 Co jest na WEJŚCIU (Input):** Historyczny rejestr pracy wprowadzony w tabeli (liczba spakowanych paczek, czas pracy w minutach, liczba popełnionych błędów).
    * **📤 Co jest na WYJŚCIU (Output):** Wyliczenie średniego czasu pakowania 1 paczki, tempa pracy (paczki/godz.), wskaźnika błędów oraz ranking wskazujący, **który pracownik i zespół poradził sobie najlepiej**.
    """)
    
    # Główni liderzy
    najlepszy_pracownik_row = df.sort_values(by=['Ocena_Efektywności', 'Wydajność_Paczki_na_h'], ascending=False).iloc[0]
    najgorszy_pracownik_row = df.sort_values(by=['Ocena_Efektywności', 'Wydajność_Paczki_na_h'], ascending=True).iloc[0]
    
    zespoly_summary = df.groupby('Zespół').agg(
        Liczba_Pracowników=('Pracownik', 'count'),
        Razem_Paczek=('Spakowane_Paczki', 'sum'),
        Średni_Czas_min=('Średni_Czas_1_Paczki_min', 'mean'),
        Suma_Błędów=('Błędy_Pakowania', 'sum')
    ).reset_index()
    zespoly_summary['Średni_Czas_min'] = zespoly_summary['Średni_Czas_min'].round(2)
    najlepszy_zespol = zespoly_summary.sort_values(by='Średni_Czas_min').iloc[0]['Zespół']

    # Metryki KPI
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Łącznie spakowanych paczek", f"{df['Spakowane_Paczki'].sum()} szt.")
    k2.metric("Średni czas pakowania 1 paczki", f"{df['Średni_Czas_1_Paczki_min'].mean():.2f} min", 
              delta=f"{norma_czasu_min - df['Średni_Czas_1_Paczki_min'].mean():.2f} min względem normy")
    k3.metric("Najlepszy pracownik", najlepszy_pracownik_row['Pracownik'], f"{najlepszy_pracownik_row['Wydajność_Paczki_na_h']} paczek/h")
    k4.metric("Najbardziej wydajny zespół", najlepszy_zespol)

    st.write("#### 📋 Szczegółowa tabela wyników historycznych (posortowana od najlepszego pracownika):")
    df_sorted = df.sort_values(by='Ocena_Efektywności', ascending=False).reset_index(drop=True)
    st.dataframe(df_sorted, use_container_width=True)

    # Wykresy porównawcze
    w1, w2 = st.columns(2)
    with w1:
        st.write("**Wydajność pracowników (spakowane paczki na godzinę):**")
        st.bar_chart(df.set_index('Pracownik')['Wydajność_Paczki_na_h'])
    with w2:
        st.write("**Podsumowanie wyników według zespołów:**")
        st.dataframe(zespoly_summary, use_container_width=True)

    st.success(f"""
    **📌 Główne wnioski z analizy deskryptywnej:**
    * **Kto poradził sobie najlepiej?** Liderem wydajności i jakości jest **{najlepszy_pracownik_row['Pracownik']}** ({najlepszy_pracownik_row['Zespół']}), który pakuje średnio **{najlepszy_pracownik_row['Wydajność_Paczki_na_h']} paczek na godzinę** (średnio {najlepszy_pracownik_row['Średni_Czas_1_Paczki_min']} min/paczka) przy wskaźniku błędów **{najlepszy_pracownik_row['Wskaźnik_Błędów_proc']}%**.
    * **Kto wymaga uwagi?** Najniższą efektywność odnotowano u pracownika **{najgorszy_pracownik_row['Pracownik']}** ({najgorszy_pracownik_row['Średni_Czas_1_Paczki_min']} min/paczka, błędy: {najgorszy_pracownik_row['Błędy_Pakowania']}).
    """)

# ==========================================
# ZAKŁADKA 2: ANALIZA PREDYKCYJNA
# ==========================================
with tab2:
    st.subheader("🔮 Analiza Predykcyjna – Prognoza realizacji planu i zapotrzebowania na kadrę")
    
    st.markdown("""
    * **📥 Co jest na WEJŚCIU (Input):** Wyliczone tempo pracy zespołu z Analizy 1 oraz nowy cel zlecenia (liczba paczek do spakowania i czas zmiany w godzinach).
    * **📤 Co jest na WYJŚCIU (Output):** Prognoza czasu potrzebnego na realizację zamówienia, **określenie zapotrzebowania na pracowników**, szacowana liczba błędów oraz alerty o ryzyku opóźnienia.
    """)

    # Obliczenia predykcyjne
    obecna_liczba_pracownikow = len(df)
    laczna_wydajnosc_zespolu_na_h = df['Wydajność_Paczki_na_h'].sum()
    srednia_wydajnosc_1_pracownika_na_h = df['Wydajność_Paczki_na_h'].mean()
    
    # Ile paczek obecny zespół jest w stanie spakować w czasie zmiany
    maks_mozliwosci_zespolu = int(laczna_wydajnosc_zespolu_na_h * czas_zmiany_h)
    
    # Ile godzin zajmie spakowanie planowanych paczek obecnemu zespołowi
    prognozowany_czas_h = round(planowane_paczki / laczna_wydajnosc_zespolu_na_h, 2)
    roznica_czasu_h = round(czas_zmiany_h - prognozowany_czas_h, 2)
    
    # Zapotrzebowanie na pracowników, aby wyrobić się dokładnie w czasie zmiany
    wymagana_liczba_pracownikow = int(np.ceil(planowane_paczki / (srednia_wydajnosc_1_pracownika_na_h * czas_zmiany_h)))
    brakujacy_pracownicy = max(0, wymagana_liczba_pracownikow - obecna_liczba_pracownikow)
    
    # Prognoza błędów
    sredni_procent_bledow = df['Błędy_Pakowania'].sum() / df['Spakowane_Paczki'].sum()
    prognozowane_bledy = int(np.round(planowane_paczki * sredni_procent_bledow))

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Możliwości obecnego zespołu", f"{maks_mozliwosci_zespolu} paczek", 
              delta=f"{maks_mozliwosci_zespolu - planowane_paczki} względem planu")
    p2.metric("Prognozowany czas realizacji", f"{prognozowany_czas_h} godz.", 
              delta=f"{roznica_czasu_h} godz. zapasu/opóźnienia")
    p3.metric("Zapotrzebowanie na pracowników", f"{wymagana_liczba_pracownikow} osób", 
              delta=f"Obecnie w bazie: {obecna_liczba_pracownikow}")
    p4.metric("Prognozowana liczba błędów", f"ok. {prognozowane_bledy} szt.")

    # Ocena ryzyka opóźnienia
    if prognozowany_czas_h > czas_zmiany_h:
        opoznienie_min = int((prognozowany_czas_h - czas_zmiany_h) * 60)
        st.error(f"""
        🔴 **WYSOKIE RYZYKO OPÓŹNIENIA!** 
        * Przy obecnym składzie ({obecna_liczba_pracownikow} osób) zespół spakuje maksymalnie **{maks_mozliwosci_zespolu} z {planowane_paczki}** zaplanowanych paczek.
        * Przewidywane opóźnienie wyniesie około **{opoznienie_min} minut** ({prognozowany_czas_h - czas_zmiany_h:.1f} godz. po zakończeniu zmiany).
        * **Prognoza kadrowa:** Aby zrealizować plan na czas, brakuje **{brakujacy_pracownicy} pracowników** o średniej wydajności.
        """)
    else:
        zapas_min = int((czas_zmiany_h - prognozowany_czas_h) * 60)
        st.success(f"""
        🟢 **BRAK RYZYKA OPÓŹNIENIA – PROCES STABILNY!**
        * Obecny zespół ({obecna_liczba_pracownikow} osób) bez problemu zrealizuje cel **{planowane_paczki} paczek** w czasie **{prognozowany_czas_h} godz.**
        * Pozostanie bezpieczny bufor czasowy wynoszący około **{zapas_min} minut**.
        * **Prognoza kadrowa:** Zapotrzebowanie na pracowników wynosi **{wymagana_liczba_pracownikow} osób** (masz wystarczającą kadrę).
        """)

    st.write("#### 🔍 Indywidualna prognoza ryzyka na stanowiskach pracy:")
    pred_table = df[['Pracownik', 'Zespół', 'Średni_Czas_1_Paczki_min', 'Wydajność_Paczki_na_h', 'Wskaźnik_Błędów_proc']].copy()
    pred_table['Prognoza_Czasowa'] = pred_table['Średni_Czas_1_Paczki_min'].apply(
        lambda x: '🔴 Przekracza normę (Wąskie gardło)' if x > norma_czasu_min else '🟢 W normie'
    )
    pred_table['Ryzyko_Reklamacji'] = pred_table['Wskaźnik_Błędów_proc'].apply(
        lambda x: '⚠️ Wysokie ryzyko błędów (>5%)' if x > 5.0 else '✅ Bezpieczny poziom jakości'
    )
    st.dataframe(pred_table, use_container_width=True)

# ==========================================
# ZAKŁADKA 3: ANALIZA PRESKRYPTYWNA
# ==========================================
with tab3:
    st.subheader("⚙️ Analiza Preskryptywna – Optymalny podział zadań i rekomendacje decyzyjne")
    
    st.markdown("""
    * **📥 Co jest na WEJŚCIU (Input):** Wyniki prognozy z Analizy 2 (niedobory kadrowe, wykryte wąskie gardła) oraz pula zamówień podzielona na paczki PILNE (VIP) i Standardowe.
    * **📤 Co jest na WYJŚCIU (Output):** Automatyczny **harmonogram przydziału zadań dla każdego pracownika** (kto ile i jakich paczek ma spakować) oraz lista gotowych decyzji menedżerskich.
    """)

    # Algorytm optymalizacyjny rozdzielający paczki proporcjonalnie do wydajności
    opt_df = df.copy()
    udzial_wydajnosci = opt_df['Wydajność_Paczki_na_h'] / opt_df['Wydajność_Paczki_na_h'].sum()
    opt_df['Przydzielone_Paczki_Razem'] = np.round(udzial_wydajnosci * planowane_paczki).astype(int)
    
    # Korekta zaokrągleń, aby suma zgadzała się co do paczki
    roznica_paczek = planowane_paczki - opt_df['Przydzielone_Paczki_Razem'].sum()
    idx_najlepszy = opt_df['Ocena_Efektywności'].idxmax()
    opt_df.loc[idx_najlepszy, 'Przydzielone_Paczki_Razem'] += roznica_paczek

    # Przydział paczek PILNYCH wyłącznie osobom o najniższym wskaźniku błędów
    opt_df = opt_df.sort_values(by=['Wskaźnik_Błędów_proc', 'Średni_Czas_1_Paczki_min'], ascending=[True, True]).reset_index(drop=True)
    
    pozostale_pilne = w_tym_pilne
    przydzial_pilne = []
    przydzial_standard = []
    rekomendowana_rola = []

    for i, row in opt_df.iterrows():
        limit_pracownika = row['Przydzielone_Paczki_Razem']
        if pozostale_pilne > 0 and row['Wskaźnik_Błędów_proc'] <= 3.0:
            pilne_dla_niego = min(limit_pracownika, pozostale_pilne)
            pozostale_pilne -= pilne_dla_niego
        else:
            pilne_dla_niego = 0
            
        standard_dla_niego = limit_pracownika - pilne_dla_niego
        przydzial_pilne.append(pilne_dla_niego)
        przydzial_standard.append(standard_dla_niego)
        
        if pilne_dla_niego > 0:
            rekomendowana_rola.append("🔥 Obsługa zamówień PILNYCH / VIP (Wysoka jakość)")
        elif row['Wskaźnik_Błędów_proc'] > 5.0:
            rekomendowana_rola.append("🛡️ Paczki proste + nadzór jakościowy (Szkolenie)")
        elif row['Średni_Czas_1_Paczki_min'] > norma_czasu_min:
            rekomendowana_rola.append("🐢 Wsparcie pomocnicze (Odciążenie linii)")
        else:
            rekomendowana_rola.append("📦 Standardowa linia pakowania")

    opt_df['Paczki_PILNE_VIP'] = przydzial_pilne
    opt_df['Paczki_Standardowe'] = przydzial_standard
    opt_df['Szacowany_Czas_Pracy_h'] = (opt_df['Przydzielone_Paczki_Razem'] / opt_df['Wydajność_Paczki_na_h']).round(2)
    opt_df['Rekomendowane_Zadanie'] = rekomendowana_rola

    st.write("#### 📋 Automatyczny plan przydziału zadań na zmianę (Optymalizacja obciążenia):")
    st.dataframe(
        opt_df[['Pracownik', 'Zespół', 'Rekomendowane_Zadanie', 'Przydzielone_Paczki_Razem', 'Paczki_PILNE_VIP', 'Paczki_Standardowe', 'Szacowany_Czas_Pracy_h']],
        use_container_width=True
    )

    st.subheader("🎯 Konkretne decyzje do wdrożenia (Rekomendacje systemu):")
    
    # Rekomendacja 1: Kadry i czas
    if brakujacy_pracownicy > 0:
        st.warning(f"""
        **1. Decyzja kadrowa (Alokacja zasobów):** 
        * Zespół nie wyrobi się w czasie {czas_zmiany_h} godz. **Przesuń {brakujacy_pracownicy} dodatkowych pracowników** z innego działu (np. przyjęcia towaru) do sekcji pakowania lub zaplanuj **{prognozowany_czas_h - czas_zmiany_h:.1f} godz. nadgodzin**.
        """)
    else:
        st.success(f"""
        **1. Decyzja kadrowa (Alokacja zasobów):** 
        * Obecna obsada ({obecna_liczba_pracownikow} osób) jest wystarczająca. Nie ma potrzeby angażowania dodatkowych pracowników.
        """)

    # Rekomendacja 2: Zadania pilne
    liderzy_jakosci = opt_df[opt_df['Paczki_PILNE_VIP'] > 0]['Pracownik'].tolist()
    if len(liderzy_jakosci) > 0:
        st.info(f"""
        **2. Optymalizacja zadań priorytetowych (Kto poradzi sobie najlepiej?):** 
        * Do spakowania **{w_tym_pilne} paczek PILNYCH/VIP** system automatycznie wyznaczył najbardziej bezbłędnych pracowników: **{', '.join(liderzy_jakosci)}**. Pozwoli to uniknąć kosztownych reklamacji u kluczowych klientów.
        """)

    # Rekomendacja 3: Wąskie gardła i szkolenia
    wolni_pracownicy = df[df['Średni_Czas_1_Paczki_min'] > norma_czasu_min]['Pracownik'].tolist()
    bledni_pracownicy = df[df['Wskaźnik_Błędów_proc'] > 5.0]['Pracownik'].tolist()
    
    if wolni_pracownicy or bledni_pracownicy:
        st.error(f"""
        **3. Działania korygujące na stanowiskach:**
        * **Wąskie gardła czasowe:** Pracownicy przekraczający normę ({norma_czasu_min} min/paczka): **{', '.join(wolni_pracownicy) if wolni_pracownicy else 'Brak'}** – system zmniejszył im przydział paczek, aby nie blokowali całej zmiany.
        * **Kontrola jakości:** Pracownicy z wysokim odsetkiem błędów (>5%): **{', '.join(bledni_pracownicy) if bledni_pracownicy else 'Brak'}** – odsunięto ich od paczek VIP i rekomenduje się wdrożenie podwójnej weryfikacji skanerem.
        """)
