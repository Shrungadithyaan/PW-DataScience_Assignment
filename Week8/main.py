import pandas as pd
from bokeh.plotting import figure, show
from bokeh.sampledata.stocks import GOOG
from flask import Flask, render_template
from bokeh.embed import components
from bokeh.resources import CDN

app = Flask(__name__)

@app.route('/')
def plot_bokeh():
            

    df = pd.DataFrame(GOOG).tail(50)
    df["date"] = pd.to_datetime(df["date"])
    
    inc = df.close > df.open
    dec = df.open > df.close
    w = 16*60*60*1000 # milliseconds

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, width=1000, height=400,
               title="Google Candlestick Plot", background_fill_color="#efefef")
    p.xaxis.major_label_orientation = 0.8 # radians

    p.segment(df.date, df.high, df.date, df.low, color="black")

    p.vbar(df.date[dec], w, df.open[dec], df.close[dec], color="#eb3c40")
    p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="green",
           line_color="green", line_width=2)
    
    script, div = components(p)
    cdn_js = CDN.js_files[0]

    return render_template('index.html',cdn_js=cdn_js,script=script,div=div)

if __name__ == "__main__":
    app.run(port=5008,debug=True)