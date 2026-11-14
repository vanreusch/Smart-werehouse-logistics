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
Narzędzie analityczne wspomagające zarządzanie magazynem. Wprowadź dane swojego zespołu oraz cel na zmianę, 
aby otrzymać pełną analizę deskryptywną, predykcyjną i preskryptywną.
""")

# --- INICJALIZACJA PUSTEJ BAZY DANYCH NA STARCIE ---
if 'pracownicy_df' not in st.session_state:
    st.session_state.pracownicy_df = pd.DataFrame(
        columns=['Pracownik', 'Zespół', 'Spakowane_Paczki', 'Czas_Pracy_min', 'Błędy_Pakowania']
    )

# --- SEKCJA KROK 1: WPROWADZANIE DANYCH WEJŚCIOWYCH ---
st.header("📥 KROK 1: Wprowadzanie Danych Wejściowych (Input)")

col_form, col_cel = st.columns([1.2, 1])

with col_form:
    st.subheader("1A. Dodaj pracowników do analizy")
    with st.form("dodaj_pracownika_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        imie = c1.text_input("Imię i nazwisko pracownika:", placeholder="np. Jan Kowalski")
        zespol = c2.text_input("Nazwa zespołu / działu (wpisz własną):", placeholder="np. Zespół A / Zmiana Poranna")
        
        c3, c4, c5 = st.columns(3)
        paczki = c3.number_input("Spakowane paczki (szt.):", min_value=1, max_value=10000, value=50)
        czas = c4.number_input("Czas pracy (min):", min_value=1, max_value=1440, value=360)
        bledy = c5.number_input("Liczba błędów (szt.):", min_value=0, max_value=1000, value=0)
        
        dodaj_btn = st.form_submit_button("➕ Dodaj pracownika do listy")
        
        if dodaj_btn:
            if imie.strip() == "" or zespol.strip() == "":
                st.warning("⚠️ Wpisz zarówno imię pracownika, jak i nazwę zespołu!")
            else:
                nowy_wiersz = pd.DataFrame({
                    'Pracownik': [imie.strip()],
                    'Zespół': [zespol.strip()],
                    'Spakowane_Paczki': [int(paczki)],
                    'Czas_Pracy_min': [int(czas)],
                    'Błędy_Pakowania': [int(bledy)]
                })
                st.session_state.pracownicy_df = pd.concat([st.session_state.pracownicy_df, nowy_wiersz], ignore_index=True)
                st.success(f"✅ Dodano: {imie.strip()} ({zespol.strip()})")
                st.rerun()

    # Usuwanie dowolnie wybranych pracowników z listy
    if len(st.session_state.pracownicy_df) > 0:
        st.markdown("**🗑️ Usuń wybranych pracowników:**")
        u1, u2 = st.columns([2.5, 1])
        opcje_do_usuniecia = [
            f"{idx}: {row['Pracownik']} ({row['Zespół']})" 
            for idx, row in st.session_state.pracownicy_df.iterrows()
        ]
        wybrani_do_usuniecia = u1.multiselect(
            "Wybierz osoby z listy:", 
            options=opcje_do_usuniecia, 
            placeholder="Wybierz kogo chcesz usunąć...",
            label_visibility="collapsed"
        )
        if u2.button("🗑️ Usuń zaznaczonych", use_container_width=True):
            if wybrani_do_usuniecia:
                indeksy = [int(item.split(":")[0]) for item in wybrani_do_usuniecia]
                st.session_state.pracownicy_df = st.session_state.pracownicy_df.drop(index=indeksy).reset_index(drop=True)
                st.rerun()

    # Przyciski pomocnicze (czyszczenie / dane testowe)
    b1, b2 = st.columns(2)
    if b1.button("🧹 Wyczyść całą tabelę", use_container_width=True) and len(st.session_state.pracownicy_df) > 0:
        st.session_state.pracownicy_df = pd.DataFrame(
            columns=['Pracownik', 'Zespół', 'Spakowane_Paczki', 'Czas_Pracy_min', 'Błędy_Pakowania']
        )
        st.rerun()
    if b2.button("⚡ Wczytaj przykładowe dane (test)", use_container_width=True):
        st.session_state.pracownicy_df = pd.DataFrame({
            'Pracownik': ['Anna Nowak', 'Piotr Zieliński', 'Katarzyna Wójcik', 'Michał Lewandowski'],
            'Zespół': ['Zespół Ekspres', 'Zespół Ekspres', 'Zespół Standard', 'Zespół Gabaryty'],
            'Spakowane_Paczki': [60, 68, 35, 50],
            'Czas_Pracy_min': [360, 340, 350, 350],
            'Błędy_Pakowania': [0, 0, 3, 1]
        })
        st.rerun()

with col_cel:
    st.subheader("1B. Określ parametry nowego zlecenia (Cel)")
    planowane_paczki = st.number_input("📦 Liczba paczek do spakowania na nowej zmianie:", min_value=10, max_value=10000, value=300, step=10)
    w_tym_pilne = st.slider("🔥 W tym paczki PILNE / VIP:", min_value=0, max_value=planowane_paczki, value=min(60, planowane_paczki))
    czas_zmiany_h = st.number_input("⏱️ Czas trwania zmiany (w godzinach):", min_value=1.0, max_value=24.0, value=6.0, step=0.5)
    norma_czasu_min = st.slider("🎯 Dopuszczalna norma czasu na 1 paczkę (min):", min_value=2.0, max_value=20.0, value=8.0, step=0.5)

# Podgląd i bezpośrednia edycja wprowadzonych danych wejściowych
if len(st.session_state.pracownicy_df) > 0:
    with st.expander("👁️ Podgląd i edycja danych wejściowych (możesz też poprawiać wartości lub usuwać wiersze bezpośrednio w tabeli)", expanded=True):
        edytowane_df = st.data_editor(
            st.session_state.pracownicy_df,
            num_rows="dynamic",
            use_container_width=True,
            key="edytor_danych"
        )
        if not edytowane_df.equals(st.session_state.pracownicy_df):
            st.session_state.pracownicy_df = edytowane_df.reset_index(drop=True)
            st.rerun()
else:
    st.info("👆 **Tabela wejściowa jest obecnie pusta.** Dodaj pierwszego pracownika i wpisz nazwę jego zespołu w formularzu powyżej (1A), aby wygenerować analizy!")
    st.stop()

st.divider()

# --- OBLICZENIA ANALITYCZNE ---
df = st.session_state.pracownicy_df.copy()
df = df.dropna(subset=['Pracownik', 'Zespół'])
if len(df) == 0:
    st.warning("⚠️ Brak kompletnych wierszy do analizy.")
    st.stop()

df['Spakowane_Paczki'] = pd.to_numeric(df['Spakowane_Paczki'], errors='coerce').fillna(1).clip(lower=1)
df['Czas_Pracy_min'] = pd.to_numeric(df['Czas_Pracy_min'], errors='coerce').fillna(60).clip(lower=1)
df['Błędy_Pakowania'] = pd.to_numeric(df['Błędy_Pakowania'], errors='coerce').fillna(0).clip(lower=0)

df['Średni_Czas_1_Paczki_min'] = (df['Czas_Pracy_min'] / df['Spakowane_Paczki']).round(2)
df['Wydajność_Paczki_na_h'] = (60 / df['Średni_Czas_1_Paczki_min']).round(1)
df['Bezpieczeństwo_Jakości_proc'] = (100 - ((df['Błędy_Pakowania'] / df['Spakowane_Paczki']) * 100)).clip(lower=0).round(2)
df['Wskaźnik_Błędów_proc'] = ((df['Błędy_Pakowania'] / df['Spakowane_Paczki']) * 100).round(2)
df['Indeks_Efektywności_Pkt'] = (df['Wydajność_Paczki_na_h'] * 2 - df['Wskaźnik_Błędów_proc'] * 3).round(1)

# --- SEKCJA KROK 2: WYNIKI ANALIZ (TYLKO DANE WYJŚCIOWE / OUTPUT) ---
st.header("📤 KROK 2: Wyniki Analiz (Dane Wyjściowe / Output)")

tab1, tab2, tab3 = st.tabs([
    "📊 1. Analiza Deskryptywna (Co się stało?)",
    "🔮 2. Analiza Predykcyjna (Co się może wydarzyć?)",
    "⚙️ 3. Analiza Preskryptywna (Co powinniśmy zrobić?)"
])

# ==========================================
# ZAKŁADKA 1: ANALIZA DESKRYPTYWNA
# ==========================================
with tab1:
    st.subheader("📊 Analiza Deskryptywna – Wyliczone wskaźniki wydajności i jakości")
    st.caption("Poniżej prezentowane są wyłącznie wyliczone wskaźniki analityczne (Output) powstałe z przetworzenia danych wejściowych.")
    
    df_ranked = df.sort_values(by=['Indeks_Efektywności_Pkt', 'Wydajność_Paczki_na_h'], ascending=False).reset_index(drop=True)
    df_ranked['Miejsce_w_Rankingu'] = df_ranked.index + 1
    
    najlepszy_pracownik = df_ranked.iloc[0]
    
    zespoly_out = df.groupby('Zespół').agg(
        Liczba_Osób=('Pracownik', 'count'),
        Średnie_Tempo_Paczki_h=('Wydajność_Paczki_na_h', 'mean'),
        Średni_Czas_1_Paczki_min=('Średni_Czas_1_Paczki_min', 'mean'),
        Średni_Wskaźnik_Błędów_proc=('Wskaźnik_Błędów_proc', 'mean')
    ).round(2).reset_index()
    najlepszy_zespol = zespoly_out.sort_values(by='Średni_Czas_1_Paczki_min').iloc[0]['Zespół']

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Średnie tempo zespołu", f"{df['Wydajność_Paczki_na_h'].mean():.1f} paczek/h")
    k2.metric("Średni czas 1 paczki", f"{df['Średni_Czas_1_Paczki_min'].mean():.2f} min", 
              delta=f"{norma_czasu_min - df['Średni_Czas_1_Paczki_min'].mean():.2f} min względem normy")
    k3.metric("Lider wydajności (1. miejsce)", najlepszy_pracownik['Pracownik'], f"{najlepszy_pracownik['Wydajność_Paczki_na_h']} paczek/h")
    k4.metric("Najlepszy zespół", najlepszy_zespol)

    st.write("#### 🏆 Tabela Wyjściowa: Ranking i wyliczone wskaźniki KPI pracowników:")
    output_deskryptywna = df_ranked[[
        'Miejsce_w_Rankingu', 
        'Pracownik', 
        'Zespół', 
        'Średni_Czas_1_Paczki_min', 
        'Wydajność_Paczki_na_h', 
        'Bezpieczeństwo_Jakości_proc',
        'Wskaźnik_Błędów_proc', 
        'Indeks_Efektywności_Pkt'
    ]]
    st.dataframe(output_deskryptywna, use_container_width=True, hide_index=True)

    w1, w2 = st.columns(2)
    with w1:
        st.write("**Wykres wydajności (paczki na godzinę):**")
        st.bar_chart(df_ranked.set_index('Pracownik')['Wydajność_Paczki_na_h'])
    with w2:
        st.write("**Porównanie wpisanych zespołów:**")
        st.dataframe(zespoly_out, use_container_width=True, hide_index=True)

    st.success(f"""
    **📌 Wnioski z Analizy Deskryptywnej:**
    * **Który pracownik poradził sobie najlepiej?** 1. miejsce w rankingu zajmuje **{najlepszy_pracownik['Pracownik']}** ({najlepszy_pracownik['Zespół']}) z tempem **{najlepszy_pracownik['Wydajność_Paczki_na_h']} paczek/h** (1 paczka co {najlepszy_pracownik['Średni_Czas_1_Paczki_min']} min) i bezbłędnością **{najlepszy_pracownik['Bezpieczeństwo_Jakości_proc']}%**.
    * **Który zespół poradził sobie najlepiej?** Najwyższą efektywność osiąga **{najlepszy_zespol}**.
    """)

# ==========================================
# ZAKŁADKA 2: ANALIZA PREDYKCYJNA
# ==========================================
with tab2:
    st.subheader("🔮 Analiza Predykcyjna – Prognoza zapotrzebowania na pracowników i ryzyka opóźnień")
    st.caption("Model predykcyjny zestawia wyliczone tempo zespołu z nowym celem produkcyjnym z Kroku 1B.")

    obecna_liczba_pracownikow = len(df)
    laczna_wydajnosc_zespolu_na_h = df['Wydajność_Paczki_na_h'].sum()
    srednia_wydajnosc_1_osoby = df['Wydajność_Paczki_na_h'].mean()
    
    maks_mozliwosci_zespolu = int(laczna_wydajnosc_zespolu_na_h * czas_zmiany_h)
    prognozowany_czas_h = round(planowane_paczki / laczna_wydajnosc_zespolu_na_h, 2)
    
    wymagana_liczba_pracownikow = int(np.ceil(planowane_paczki / (srednia_wydajnosc_1_osoby * czas_zmiany_h)))
    brakujacy_pracownicy = max(0, wymagana_liczba_pracownikow - obecna_liczba_pracownikow)
    
    sredni_procent_bledow = (df['Wskaźnik_Błędów_proc'].mean()) / 100
    prognozowane_bledy = int(np.round(planowane_paczki * sredni_procent_bledow))

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Prognozowany czas wykonania", f"{prognozowany_czas_h} godz.", 
              delta=f"{czas_zmiany_h - prognozowany_czas_h:.2f} godz. względem zmiany")
    p2.metric("Wymagana liczba pracowników", f"{wymagana_liczba_pracownikow} osób", 
              delta=f"Brakuje: {brakujacy_pracownicy}" if brakujacy_pracownicy > 0 else "Obsada wystarczająca")
    p3.metric("Maks. możliwości obecnej kadry", f"{maks_mozliwosci_zespolu} paczek")
    p4.metric("Prognozowane reklamacje", f"ok. {prognozowane_bledy} szt.")

    if prognozowany_czas_h > czas_zmiany_h:
        opoznienie_min = int((prognozowany_czas_h - czas_zmiany_h) * 60)
        st.error(f"""
        🔴 **PROGNOZA: WYSOKIE RYZYKO OPÓŹNIENIA ZLECENIA!** 
        * Obecny zespół ({obecna_liczba_pracownikow} osób) potrzebuje **{prognozowany_czas_h} godz.**, aby spakować {planowane_paczki} paczek. Przekroczy to czas zmiany o **{opoznienie_min} minut**.
        * **Zapotrzebowanie na pracowników:** Aby wykonać plan w {czas_zmiany_h} godz., potrzebujesz łącznie **{wymagana_liczba_pracownikow} pracowników** (brakuje **{brakujacy_pracownicy} osób**).
        """)
    else:
        zapas_min = int((czas_zmiany_h - prognozowany_czas_h) * 60)
        st.success(f"""
        🟢 **PROGNOZA: ZLECENIE ZOSTANIE WYKONANE PRZED CZASEM!**
        * Zespół uwinie się w **{prognozowany_czas_h} godz.** (zostanie **{zapas_min} minut** zapasu).
        * **Zapotrzebowanie na pracowników:** Wymagane minimum to **{wymagana_liczba_pracownikow} osób** (posiadasz {obecna_liczba_pracownikow}).
        """)

    st.write("#### 🔍 Predykcja wąskich gardeł na poszczególnych stanowiskach:")
    pred_out = df[['Pracownik', 'Zespół', 'Wydajność_Paczki_na_h']].copy()
    pred_out['Szacowany_Udział_w_Planie_szt'] = np.round((df['Wydajność_Paczki_na_h'] / laczna_wydajnosc_zespolu_na_h) * planowane_paczki).astype(int)
    pred_out['Ryzyko_Opóźnienia_Stanowiska'] = df['Średni_Czas_1_Paczki_min'].apply(
        lambda x: '🔴 Wysokie (Przekracza normę czasu)' if x > norma_czasu_min else '🟢 Niskie (W normie)'
    )
    pred_out['Ryzyko_Błędów_Jakościowych'] = df['Wskaźnik_Błędów_proc'].apply(
        lambda x: '⚠️ Wysokie (>5% błędów)' if x > 5.0 else '✅ Niskie'
    )
    st.dataframe(pred_out, use_container_width=True, hide_index=True)

# ==========================================
# ZAKŁADKA 3: ANALIZA PRESKRYPTYWNA
# ==========================================
with tab3:
    st.subheader("⚙️ Analiza Preskryptywna – Optymalizacja przydziału zadań i rekomendacje")
    st.caption("Algorytm automatycznie rozdziela pulę paczek (w tym VIP/Pilne) pomiędzy wprowadzonych pracowników.")

    opt_df = df.copy()
    udzial = opt_df['Wydajność_Paczki_na_h'] / opt_df['Wydajność_Paczki_na_h'].sum()
    opt_df['Optymalny_Przydział_Paczek'] = np.round(udzial * planowane_paczki).astype(int)
    
    roznica = planowane_paczki - opt_df['Optymalny_Przydział_Paczek'].sum()
    idx_max = opt_df['Indeks_Efektywności_Pkt'].idxmax()
    opt_df.loc[idx_max, 'Optymalny_Przydział_Paczek'] += roznica

    opt_df = opt_df.sort_values(by=['Wskaźnik_Błędów_proc', 'Średni_Czas_1_Paczki_min'], ascending=[True, True]).reset_index(drop=True)
    
    pozostale_pilne = w_tym_pilne
    pilne_list, std_list, decyzja_list = [], [], []

    for i, row in opt_df.iterrows():
        limit = row['Optymalny_Przydział_Paczek']
        if pozostale_pilne > 0 and row['Wskaźnik_Błędów_proc'] <= 3.0:
            p_pilne = min(limit, pozostale_pilne)
            pozostale_pilne -= p_pilne
        else:
            p_pilne = 0
            
        p_std = limit - p_pilne
        pilne_list.append(p_pilne)
        std_list.append(p_std)
        
        if p_pilne > 0:
            decyzja_list.append("🔥 Przydzielić paczki PILNE / VIP (Lider jakości)")
        elif row['Wskaźnik_Błędów_proc'] > 5.0:
            decyzja_list.append("🛡️ Tylko paczki standardowe + kontrola skanerem")
        elif row['Średni_Czas_1_Paczki_min'] > norma_czasu_min:
            decyzja_list.append("📉 Zmniejszony limit (Odciążenie wąskiego gardła)")
        else:
            decyzja_list.append("📦 Standardowa obsługa linii pakowania")

    opt_df['W_tym_Paczki_PILNE'] = pilne_list
    opt_df['W_tym_Paczki_Standard'] = std_list
    opt_df['Czas_Realizacji_Przydziału_h'] = (opt_df['Optymalny_Przydział_Paczek'] / opt_df['Wydajność_Paczki_na_h']).round(2)
    opt_df['Rekomendowana_Decyzja'] = decyzja_list

    st.write("#### 📋 Gotowy harmonogram przydziału zadań dla zespołu (Output preskryptywny):")
    presc_out = opt_df[[
        'Pracownik', 
        'Zespół', 
        'Rekomendowana_Decyzja', 
        'Optymalny_Przydział_Paczek', 
        'W_tym_Paczki_PILNE', 
        'W_tym_Paczki_Standard', 
        'Czas_Realizacji_Przydziału_h'
    ]]
    st.dataframe(presc_out, use_container_width=True, hide_index=True)

    st.subheader("🎯 Podsumowanie decyzji menedżerskich do wdrożenia:")
    if brakujacy_pracownicy > 0:
        st.warning(f"**1. Alokacja kadr:** Aby uniknąć opóźnienia, dobierz **{brakujacy_pracownicy} pracowników** z innego działu lub przedłuż zmianę o **{prognozowany_czas_h - czas_zmiany_h:.1f} godz.**")
    else:
        st.success("**1. Alokacja kadr:** Obecna liczba pracowników jest optymalna do wykonania planu na czas.")
        
    liderzy_vip = opt_df[opt_df['W_tym_Paczki_PILNE'] > 0]['Pracownik'].tolist()
    if liderzy_vip:
        st.info(f"**2. Przydział zadań priorytetowych:** Zadania PILNE ({w_tym_pilne} szt.) skierowano do: **{', '.join(liderzy_vip)}**, ponieważ gwarantują najniższe ryzyko pomyłki.")
    else:
        st.warning("**2. Przydział zadań priorytetowych:** Żaden z wpisanych pracowników nie spełnia normy niskiej błędności (<3%) dla paczek VIP! Wdróż podwójną kontrolę jakości.")
