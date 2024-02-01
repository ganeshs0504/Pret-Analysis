# %%
# !pip install altair vega_datasets
# !pip install pandas

# %%
import re
import pandas as pd
import altair as alt

# %%
file = open('free_coffee_chat.txt', encoding = 'UTF-8')
data = file.read()

# %%
data_list = data.split("\n")
print("Total number of chats:", len(data_list))
data_list

# %%
# Removing multi line chats
pattern = re.compile(r'^\d{2}\/\d{2}\/\d{4}')
data_with_removed_multiline = [chat for chat in data_list if pattern.search(chat)]
print("Length of the data list after removing multi line chats:", len(data_with_removed_multiline))
data_with_removed_multiline

# Removing unwanted list like group create messages and encryption info
pattern = re.compile(r'-\s.*:\s')
data_with_chats = [chat for chat in data_with_removed_multiline if pattern.search(chat)]
print("Length of the data list after removing unnecessary lines:", len(data_with_chats))

final_data = data_with_chats

# %%
date_list = [msg.split(',')[0] for msg in final_data]
len(date_list)

# %%
final_data

# %%
pattern = re.compile(r'\d{1,2}:\d{2}\s(am|pm)')
# temp = [pattern.search(chat) for chat in final_data]
# time_list = [time.group() for time in temp]
time_list = [pattern.search(chat).group() for chat in final_data]
len(time_list)

# %%
pattern = re.compile(r'-\s.*:')
name_list = [pattern.search(chat).group()[2:-1] for chat in final_data]
len(name_list)

# %%
pattern = re.compile(r'-\s.*:\s(.*$)')
msg_list = [pattern.search(chat).group(1) for chat in final_data]
len(msg_list)

# %%
df = pd.DataFrame(
    {
        'date': date_list,
        'time': time_list,
        'name': name_list,
        'message': msg_list
    }
)

df.tail(20)

# %%
df['date_time'] = df['date'] + "::" + df['time']
df['date_time'] = pd.to_datetime(df['date_time'], format = '%d/%m/%Y::%I:%M %p')
df['date'] = pd.to_datetime(df['date'], format = '%d/%m/%Y')
# df['time'] = pd.to_datetime(df['time'])

# %%
df

# %%
s = '☕'
s.encode('unicode-escape')

# %%
pattern = re.compile(r'☕|🍹|🍵|getting|got a', re.IGNORECASE)
list_item = [chat for chat in final_data if pattern.search(chat)]
list_item

# %%
pattern = re.compile(r'☕|🍹|getting|got a', re.IGNORECASE)
final_df = df[df['message'].str.contains(pattern)]
final_df.loc[df['name'] == '+44 7944 406269', 'name'] = '.Mags'
# Removing bitch from the dataset
final_df = final_df[final_df['name'] != "+44 7407 395201"]
final_df = final_df.reset_index(drop=True)

# %%
final_df.tail(10)

# %%
# Count of total coffee consumed by each member
total_drinks = alt.Chart(final_df, title='Total drinks consumed by each member').mark_bar().encode(
    x = alt.X('count()').title('Number of Drinks'),
    y = alt.Y('name').title(None),
    tooltip = 'count()'
).properties(
    width=500,
    height=150
)
total_drinks

# %%
weekly_total = alt.Chart(final_df, title='Total number of drinks consumed for each day of week').mark_bar().encode(
    x = alt.X('day(date_time):O').title(None),
    y = alt.Y('count()').title('Number of Drinks'),
    tooltip = 'count()'
).properties(
    width=500
)
weekly_total

# %%
monthly_bar = alt.Chart(final_df, title='Month wise individual consumption').mark_bar().encode(
    x = alt.X('yearmonth(date_time):O').title(None),
    xOffset = 'name:N',
    y = alt.Y('count()').title('Number of Drinks'),
    color = alt.Color('name').title(None),
    tooltip = 'count()'
)
monthly_bar

# %%
monthly_heatmap = alt.Chart(final_df, title=alt.Title('Month wise individual consumption', subtitle='Heatmap representation of the same bar chart above')).mark_rect().encode(
    alt.X('yearmonth(date_time):O').title(None),
    alt.Color('count()', scale=alt.Scale(scheme='lighttealblue')).title('No. of Drinks'),
    alt.Y('name').title(None),
    tooltip = 'count()'
).properties(
    width=500,
    height=150
)
monthly_heatmap

# %%
weekly_ind = alt.Chart(final_df, title='Weekly individual consumption').mark_bar().encode(
    x = alt.X('day(date_time):O').title(None),
    xOffset = 'name:N',
    y = alt.Y('count()').title('No. of Drinks'),
    color = alt.Color('name').title(None),
    tooltip = 'count()'
)
weekly_ind

# %%
weekly_ind_heatmap = alt.Chart(final_df, title=alt.Title('Weekly individual consumption', subtitle='Heatmap representation of the same bar chart above')).mark_rect().encode(
    alt.X('day(date_time):O').title(None),
    # alt.Y('monthdate(date_time):O'),
    alt.Y('name').title(None),#
    alt.Color('count()', scale=alt.Scale(scheme='yellowgreenblue')),
    tooltip = 'count()'
).properties(
    width=500,
    height=150
)
weekly_ind_heatmap

# %%
time_heatmap = alt.Chart(final_df, title=alt.Title('Beverage consumption time heatmap in a day', subtitle='Heatmap of possible conflicts')).mark_rect().encode(
    alt.X('hours(date_time)').title('Time of Day'),
    # alt.Y('monthdate(date_time):O'),
    alt.Y('name').title(None),#
    alt.Color('count()', scale=alt.Scale(scheme='goldred')),
    tooltip = 'count()'
).properties(
    width=500,
    height=150
)
time_heatmap

# %%
# Chart Website Template
two_charts_template = """
<!DOCTYPE html>
<html>
<head>
  <title>Altair Charts</title>
  <script src="https://cdn.jsdelivr.net/npm/vega@{vega_version}"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-lite@{vegalite_version}"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-embed@{vegaembed_version}"></script>
  <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background-color: #f4f4f4;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .header h1 {{
            color: #333;
            font-size: 2em;
            padding-top: 10px;
        }}
        .header h2 {{
            color: #666;
            font-size: 1.2em;
            margin: 0;
        }}
        .header h3 {{
            color: #888;
            font-size: 1em;
            margin: 0;
        }}
        .header p {{
            color: #888;
            font-size: 1em;
            margin: 0;
        }}
        .chart-container {{
            border: 1px solid #ddd;
            margin-bottom: 20px;
            padding: 10px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body>

    <div class="header">
            <h1>PRET SUBSCRIPTION ANALYSIS (WORKINGGGGGG)</h1>
            <h3>Welcome to my teeny tiny data science project. The data for the below analysis is scraped from the whatsapp group and processed using NLP techniques.</h3>
            <h3>The charts are generated using a tool called Altair (The main motivation behind this project). Feel free to move your mouse over the charts for the actual values.</h3>
    </div>
    <div class="chart-container" id="chart1"></div>
    <div class="chart-container" id="chart7"></div>
    <div class="chart-container" id="chart2"></div>
    <div class="chart-container" id="chart3"></div>
    <div class="chart-container" id="chart4"></div>
    <div class="chart-container" id="chart5"></div>
    <div class="chart-container" id="chart6"></div>

    <div class="header">
        <h2>Updates:</h2>
        <h3>Added template for the webpage so no more fiddling with updating the chart.</h3>
        <h3>The whatsapp text data still needs to be updated to latest value when the chart needs to be updated.</h3>

        <h2>TODO</h2>
        <h3>Schedule a deployment job in GitHub for auto deployment after each commit pushed. (DONE)</h3>
        <h3>ML techniques to predict future scenarios.</h3>
    </div>

<script type="text/javascript">
  vegaEmbed('#chart1', {spec1}).catch(console.error);
  vegaEmbed('#chart2', {spec2}).catch(console.error);
  vegaEmbed('#chart3', {spec3}).catch(console.error);
  vegaEmbed('#chart4', {spec4}).catch(console.error);
  vegaEmbed('#chart5', {spec5}).catch(console.error);
  vegaEmbed('#chart6', {spec6}).catch(console.error);
  vegaEmbed('#chart7', {spec7}).catch(console.error);
</script>
</body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(two_charts_template.format(
        vega_version=alt.VEGA_VERSION,
        vegalite_version=alt.VEGALITE_VERSION,
        vegaembed_version=alt.VEGAEMBED_VERSION,
        spec1=total_drinks.to_json(indent=None),
        spec2=weekly_total.to_json(indent=None),
        spec3=monthly_bar.to_json(indent=None),
        spec4=monthly_heatmap.to_json(indent=None),
        spec5=weekly_ind.to_json(indent=None),
        spec6=weekly_ind_heatmap.to_json(indent=None),
        spec7=time_heatmap.to_json(indent=None)
    ))

# %%
