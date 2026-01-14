import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="My Netflix Wrapped",
    page_icon="🎬",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/processed/enriched_viewing.csv",
        parse_dates=["start_time"]
    )

data = load_data()

data["duration"] = pd.to_timedelta(data["duration"], errors="coerce")
data["start_time"] = pd.to_datetime(data["start_time"], errors="coerce")

st.title("🎬 My Netflix Wrapped")
st.markdown(
    "An interactive data dashboard built using my personal Netflix viewing history."
)

st.divider()

total_watch_time_hours = data["duration"].sum().total_seconds() / 3600
total_titles = data["title"].nunique()

top_genre = (
    data["genre"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .idxmax()
)

data["watch_date"] = data["start_time"].dt.date
daily_watch = (
    data[["watch_date"]]
    .drop_duplicates()
    .sort_values("watch_date")
)
daily_watch["watch_date"] = pd.to_datetime(daily_watch["watch_date"])
daily_watch["day_diff"] = daily_watch["watch_date"].diff().dt.days
daily_watch["streak_group"] = (daily_watch["day_diff"] != 1).cumsum()
longest_streak = daily_watch.groupby("streak_group").size().max()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Watch Time (hrs)", f"{total_watch_time_hours:.1f}")
col2.metric("Total Titles Watched", total_titles)
col3.metric("Top Genre", top_genre)
col4.metric("Longest Binge Streak (days)", longest_streak)

st.divider()

st.subheader("Watch Time Over Months")

data["month"] = data["start_time"].dt.month
monthly_watch_hours = (
    data.groupby("month")["duration"]
    .sum()
    .dt.total_seconds() / 3600
)

monthly_df = monthly_watch_hours.reset_index()
monthly_df.columns = ["month", "watch_hours"]

chart = (
    alt.Chart(monthly_df)
    .mark_line(point=True, color="#A50A12")
    .encode(
        x=alt.X("month:O", title="Month"),
        y=alt.Y("watch_hours:Q", title="Watch Time (hours)")
    )
    .properties(title="Watch Time Over Months")
)

st.altair_chart(chart, use_container_width=True)

st.subheader("Most Watched Genres")

genre_counts = (
    data["genre"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .reset_index()
)

genre_counts.columns = ["genre", "count"]

Reds = ["#E50914","#B20710","#8B0000","#FF3B3B","#C41E3A","#DC143C","#A40000","#FF6F61","#D72638","#C70039","#900C3F","#AD1457","#F44336"]

pie_chart = (
    alt.Chart(genre_counts)
    .mark_arc(opacity=0.95) 
    .encode(
        theta=alt.Theta("count:Q", sort="-x"),
        color=alt.Color(
            "genre:N",
            scale=alt.Scale(range=Reds),
            legend=alt.Legend(title="Genre")
        ),
        tooltip=[
            alt.Tooltip("genre:N", title="Genre"),
            alt.Tooltip("count:Q", title="Count")
        ]
    )
    .properties(title="Genre Distribution")
)

st.altair_chart(pie_chart, use_container_width=True)


st.subheader("Most Watched Titles")

title_watch_time = (
    data.groupby("title")["duration"]
    .sum()
    .dt.total_seconds() / 3600
)
top_titles = title_watch_time.sort_values(ascending=False).head(5)

top_titles_df = top_titles.reset_index()
top_titles_df.columns = ["title", "watch_hours"]

chart = (
    alt.Chart(top_titles_df)
    .mark_bar(color="#A50A12")
    .encode(
        x=alt.X("title:O", title="Title", sort="-y"),
        y=alt.Y("watch_hours:Q", title="Watch Time (hours)")
    )
    .properties(title="Most Watched Titles")
)

st.altair_chart(chart, use_container_width=True)


st.subheader("Movies vs Series")

content_type = (
    data.groupby("media_type")["duration"]
    .sum()
    .dt.total_seconds() / 3600
)

content_df = content_type.reset_index()
content_df.columns = ["type", "watch_hours"]

chart = (
    alt.Chart(content_df)
    .mark_bar(color="#A50A12")
    .encode(
        x=alt.X("type:O", title="Content Type"),
        y=alt.Y("watch_hours:Q", title="Watch Time (hours)")
    )
    .properties(title="Movies vs Series")
)

st.altair_chart(chart, use_container_width=True)


st.subheader("Watch Time by Hour of Day")

hourly_watch = (
    data.groupby(data["start_time"].dt.hour)["duration"]
    .sum()
    .dt.total_seconds() / 3600
)

hourly_df = hourly_watch.reset_index()
hourly_df.columns = ["hour", "watch_hours"]

chart = (
    alt.Chart(hourly_df)
    .mark_bar(color="#A50A12")
    .encode(
        x=alt.X("hour:O", title="Hour of Day"),
        y=alt.Y("watch_hours:Q", title="Watch Time (hours)")
    )
    .properties(title="Watch Time by Hour")
)

st.altair_chart(chart, use_container_width=True)


st.divider()
st.subheader("Key Insights")

st.markdown(
    f"""
- Viewing activity shows clear monthly variation, with peak watch time observed in **September**.
- **Comedy and Crime** are the most frequently watched genres.
- **TV series dominate viewing time** compared to movies.
- Viewing activity peaks during the **afternoon hours**.
- The longest binge-watching streak recorded was **{longest_streak} consecutive days**.
"""
)