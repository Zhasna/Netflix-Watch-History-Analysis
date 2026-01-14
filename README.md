# Netflix Wrapped – Data Engineering & Analytics Project

An end-to-end data project that analyzes personal Netflix viewing history and presents insights through an interactive Streamlit dashboard, inspired by Netflix Wrapped.
---
## Project Overview

This project demonstrates how raw, real-world data can be transformed into meaningful insights using a structured data pipeline. Starting from Netflix viewing activity data, the project involves data cleaning, enrichment using an external API, exploratory analysis, and an interactive dashboard for visualization.

The goal of this project was to learn and apply core **Data Engineering and Data Analytics concepts** while building a portfolio-worthy application.
---
## Tech Stack

- **Python**
- **Pandas** – data cleaning and analysis  
- **OMDb API** – metadata enrichment (genres, content type, year)  
- **Streamlit** – interactive dashboard  
- **Altair** – styled visualizations  
- **Git & GitHub** – version control  
--- 
## Data Pipeline

1. **Data Collection**  
   - Used Netflix viewing activity CSV downloaded from account settings.

2. **Data Cleaning**  
   - Filtered viewing history to a single profile  
   - Removed irrelevant columns  
   - Parsed datetime fields  
   - Standardized titles and durations  

3. **Data Enrichment**  
   - Integrated the **OMDb API** to fetch:
     - Genre information  
     - Content type (Movie / Series)  
     - Release year  

4. **Exploratory Data Analysis (EDA)**  
   - Time-based viewing patterns  
   - Genre and title preferences  
   - Movie vs Series comparison  
   - Viewing behavior by hour  
   - Binge-watching streak analysis  

5. **Visualization & Dashboard**  
   - Built an interactive Streamlit dashboard  
   - Styled all charts in a Netflix-red theme using Altair  
---
## Key Insights

- Viewing activity shows clear monthly variation, with peak watch time observed in **September**.  
- **Comedy and Crime** are the most frequently watched genres.  
- **TV series dominate viewing time** compared to movies.  
- Viewing activity peaks during the **afternoon hours**.  
- The longest binge-watching streak recorded was **14 consecutive days**.
---
## Streamlit Dashboard

The dashboard displays:
- Total watch time  
- Total titles watched  
- Most-watched genre  
- Longest binge streak  
- Interactive charts for trends and distributions  
---
### What This Project Demonstrates

- Building a structured data pipeline from raw data to insights
- Working with external APIs for data enrichment
- Applying EDA techniques to real user data
- Creating interactive dashboards for storytelling
- Writing clean, maintainable, and modular code