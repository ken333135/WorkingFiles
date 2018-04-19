from flask import Flask, render_template

app=Flask(__name__)

@app.route('/plot/')
def plot():
    import pandas
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    df=pandas.DataFrame(columns=["X","Y"])
    df["X"]=[1,2,3,4,5]
    df["Y"]=[53,234,23,55,22]
    p=figure(plot_width=400,plot_height=400,title="ScatterPlot")
    p.circle(df["X"],df["Y"],size=20,color='red')

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]

    script1, div1 = components(p)
    cdn_js=CDN.js_files[0]
    cdn_css=CDN.css_files[0]
    return render_template("plot.html",
    script1=script1,
    div1=div1,
    cdn_css=cdn_css,
    cdn_js=cdn_js )



@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
