import pandas as pd
import altair as alt
import datapane as dp

df = pd.read_csv('https://query1.finance.yahoo.com/v7/finance/download/GOOG?period2=1585222905&interval=1mo&events=history')

chart = alt.Chart(df).encode(
    x='Date:T',
    y='Open'
).mark_line().interactive()

r = dp.Report(dp.Table(df), dp.Plot(chart))
r.save(path='index.html', open=True)