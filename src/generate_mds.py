import calendar
import pandas as pd
import numpy as np

OUTPUT_DIR = './data/md/'
YEAR = 2024

def build_monthly_page_content(month):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    cal = calendar.Calendar(firstweekday=0)
    
    content_page = f'[🏠 Home](../../index.md)\n'
    content_page += f'# {calendar.month_name[month]} {YEAR}\n\n'
    content_page += '|' + '|'.join(days) + '|' + '\n'
    content_page += '|' + '|'.join([':-:' for _ in range(len(days))]) + '|' + '\n'

    for days in cal.monthdatescalendar(YEAR, month):
        content_page += '|'
        for d in days:
            month_str = calendar.month_name[d.month].lower()
            content_page += f'[{d.day}](./{month_str}_{d.day}.md)|'
        content_page += '\n'
    return content_page

def build_daily_page_content(
        month, day,
        painting_name, painting_author, painting_wiki, painting_genre,
        song_title, song_artist, song_writers, song_released,
        unesco_site_name, unesco_site_country, unesco_site_description,
        color_name, color_link, color_hex,
        plant_name,
        discovery,
        philosophical_concept_name, philosophical_concept_url,
        saying_text, saying_explanation,
        international_day):
    page_content = f'''
[🏠 Home](../../index.md)\n
# {month} {day}\n
## 🧑‍🎨 Painting of the day\n
<img width=\"600\" src=\"../img/{painting_name}\">\n
[{painting_author}]({painting_wiki}) ({painting_genre})\n
<button class="btn btn-success"
onclick=" window.open(\'https://lens.google.com/uploadbyurl?url=https://iretes.github.io/one-a-day/data/img/{painting_name}\',\'_blank\')">
Search with Google Lens
</button>\n
## 🎼 Song of the day\n
> *{song_title}*\nby {song_artist}\n
<br />Written by {song_writers}.\n
Released in {song_released}.\n
<button class="btn btn-success"
onclick=" window.open(\'http://www.youtube.com/search?q={song_title.replace("'", " ")} by {song_artist.replace("'", " ")}\',\'_blank\')">
Search on YouTube
</button>\n
## 🏛️ UNESCO heritage site of the day\n
> *{unesco_site_name}*, {unesco_site_country}\n
{unesco_site_description}\n
<button class="btn btn-success"
onclick=" window.open(\'http://www.google.com/search?q={unesco_site_name.replace("'", " ")}\',\'_blank\')">
Search on Google
</button>\n
## 🗺️ Place of the day\n
<iframe
src="https://www.mapcrunch.com"
name="mapcrunch"
width="500"
height="500"
allowTransparency="true"
scrolling="no"
frameborder="0"\n>
</iframe>
## 🎨 Color of the day\n
> *[{color_name}]({color_link})*\n
<div style="color:{color_hex}; font-size: 100px;">&#9632;</div>\n
## 🌿 Plant of the day\n
> *{plant_name}*\n
<button class="btn btn-success"
onclick=" window.open(\'http://www.google.com/search?q={plant_name.replace("'", " ")}\',\'_blank\')">
Search on Google
</button>\n
## 🧑‍🔬 Scientific discovery of the day\n
> *{discovery}*\n
<button class="btn btn-success"
onclick=" window.open(\'http://www.google.com/search?q={discovery.replace("'", " ")}\',\'_blank\')">
Search on Google
</button>\n
## 💭 Philosophical concept of the day\n
> *[{philosophical_concept_name}]({philosophical_concept_url})*\n
## 🗣️ Saying of the day\n
> *{saying_text}*\n
{saying_explanation}\n'''
    if international_day is not np.nan:
        page_content += f'''
## 🏳️‍🌈 International day\n
{international_day}.'''
    return page_content

# Generate monthly pages
for month in range(1, 13):
    content_page = build_monthly_page_content(month)
    with open(f'{OUTPUT_DIR}{calendar.month_name[month].lower()}.md', 'w') as f:
        f.write(content_page)
# Generate daily pages
data_df = pd.read_csv('./data/data.csv', index_col='date', parse_dates=True)
for index, row in data_df.iterrows():
    page_content = build_daily_page_content(
        month=calendar.month_name[index.month],
        day=index.day,
        painting_name = row['painting_name'],
        painting_author = row['painting_author'],
        painting_wiki = row['painting_wiki'],
        painting_genre = row['painting_genre'].replace(",", ", "),
        song_title = row["song_title"],
        song_artist = row["song_artist"],
        song_writers = row["song_writers"],
        song_released = row["song_released"],
        unesco_site_name = row['UNESCO_site_name'],
        unesco_site_country = row['UNESCO_site_country'],
        unesco_site_description = row['UNESCO_site_description'],
        color_name = row["color_name"],
        color_link = row["color_link"],
        color_hex = row["color_hex"],
        plant_name = row["plant_name"],
        discovery = row["discovery"],
        philosophical_concept_name=row["philosophical_concept_name"],
        philosophical_concept_url=row["philosophical_concept_url"],
        saying_text = row["saying_text"],
        saying_explanation = row["saying_explanation"],
        international_day = row["international_day"]
    )
    with open(f'{OUTPUT_DIR}{calendar.month_name[index.month].lower()}_{index.day}.md', 'w') as f:
        f.write(page_content)