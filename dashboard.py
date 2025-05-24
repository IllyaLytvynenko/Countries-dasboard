import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Налаштування заголовка та опису
st.title("Порівняльний аналіз ІТ-галузі: Індія, Польща, Ізраїль, Україна")
st.write("Цей дашборд дозволяє аналізувати ключові показники ІТ-галузі в чотирьох країнах.")

# Завантаження даних
uploaded_file = st.file_uploader("Завантажте CSV-файл", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Округлення року до цілого
    df["Year"] = df["Year"].round().astype(int)

    # Фільтри
    countries = df["Country"].unique()
    selected_countries = st.multiselect("Оберіть країни", options=countries, default=countries)
    years = sorted(df["Year"].unique())
    selected_years = st.multiselect("Оберіть роки", options=years, default=[years[0]]) 

    # Фільтрація даних
    filtered_df = df[(df["Country"].isin(selected_countries)) & (df["Year"].isin(selected_years))]

    # Вибір показника для аналізу
    metrics = ["IT_Specialists", "IT_Export_Million_USD", "Startups", "Investments_Million_USD"]
    selected_metric = st.selectbox("Оберіть показник для аналізу", options=metrics)

    # Переклад назв показників для зрозумілості
    metric_names = {
        "IT_Specialists": "Кількість ІТ-спеціалістів",
        "IT_Export_Million_USD": "Експорт ІТ-послуг (млн USD)",
        "Startups": "Кількість стартапів",
        "Investments_Million_USD": "Інвестиції (млн USD)"
    }

    # Візуалізація: вертикальна стовпчаста діаграма з групуванням за роками
    st.subheader(f"Порівняння: {metric_names[selected_metric]} за обрані роки")
    filtered_df["Country_Year"] = filtered_df["Country"] + " (" + filtered_df["Year"].astype(str) + ")"

    # Переконатися, що метрика числова
    filtered_df[selected_metric] = pd.to_numeric(filtered_df[selected_metric], errors="coerce")

    fig = px.bar(
        filtered_df,
        x="Country_Year",
        y=selected_metric,
        color="Country",
        title=f"{metric_names[selected_metric]} за {', '.join(map(str, selected_years))} роки",
        labels={selected_metric: metric_names[selected_metric], "Country_Year": "Країна (Рік)"},
        text=selected_metric
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        barmode="group",
        bargap=0.2,
        bargroupgap=0.1,
        xaxis={'tickangle': 200},
        yaxis_title=metric_names[selected_metric],
    )

    st.plotly_chart(fig)

    # Додаткова візуалізація: кругова діаграма (за один рік, якщо обрано кілька, то для першого)
    if len(selected_years) > 0:
          if len(selected_years) > 0:

            single_year_df = filtered_df[filtered_df["Year"] == selected_years[0]]

            st.subheader(f"Розподіл: {metric_names[selected_metric]} за {selected_years[0]} рік")

            fig_pie = px.pie(single_year_df, names="Country", values=selected_metric,

            title=f"Розподіл {metric_names[selected_metric]} у {selected_years[0]}")
    st.plotly_chart(fig_pie)
        # Додаткова візуалізація: динаміка по роках (лінійний графік)
    st.subheader(f"Динаміка: {metric_names[selected_metric]} у часі")

    line_df = df[df["Country"].isin(selected_countries)]
    line_df = line_df[["Year", "Country", selected_metric]].dropna()
    line_df[selected_metric] = pd.to_numeric(line_df[selected_metric], errors="coerce")

    fig_line = px.line(
        line_df,
        x="Year",
        y=selected_metric,
        color="Country",
        markers=True,
        title=f"Зміна {metric_names[selected_metric]} з часом",
        labels={selected_metric: metric_names[selected_metric], "Year": "Рік"}
    )

    fig_line.update_layout(
        yaxis_title=metric_names[selected_metric],
        xaxis=dict(dtick=1),
        legend_title_text='Країна'
    )

    st.plotly_chart(fig_line)
    # Короткий висновок (для кожного року)
    if not filtered_df.empty:
        st.subheader("Висновки")
        for year in selected_years:
            year_df = filtered_df[filtered_df["Year"] == year]
            if not year_df.empty:
                max_country = year_df.loc[year_df[selected_metric].idxmax()]["Country"]
                max_value = year_df[selected_metric].max()
                st.write(f"Найвищий показник {metric_names[selected_metric]} у {year} році має {max_country}: {max_value}")

else:
    st.write("Будь ласка, завантажте CSV-файл із даними для аналізу.")

# streamlit run
