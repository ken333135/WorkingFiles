from flask import Flask, render_template, request
from werkzeug import secure_filename
import pandas
from bokeh.plotting import figure,show,output_file
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.resources import CDN
from bokeh.palettes import d3, Spectral10
from bokeh.transform import factor_cmap

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("Landing.html")

@app.route('/data_upload',methods=['GET','POST'])
def data_upload():
    global file
    if request.method=='POST':
        file=request.files["file"]
        file.save(secure_filename("uploaded_"+file.filename))
        df=pandas.read_csv("uploaded_"+file.filename)
        columns=list(df.columns)
        return render_template('data_upload.html',
                columns=columns)

@app.route('/form2', methods=['GET','POST'])
def form2():
    df=pandas.read_csv("uploaded_"+file.filename)
    result=request.form
    global Continuous
    global Categorical
    Continuous=[]
    Categorical=[]
    for key in result:
        if result[key]=="Continuous":
            Continuous.append(key)
        else:
            Categorical.append(key)
    print(Continuous)
    return render_template('form2.html',
                            Continuous=Continuous,
                            Categorical=Categorical)

@app.route('/plot2', methods=['GET','POST'])
def plot2():
    df=pandas.read_csv("uploaded_"+file.filename)
    if len(request.form)==3:
        def to_color(x):
            factors=list(df[col].unique())
            return d3['Category20'][max(len(factors),3)][factors.index(x)]

        for col in Categorical:
            df[col+'_color']= df[col].apply(to_color)

        df["default_color"]="black"
        #end of data preparation#
        color_columns = []
        for col in df.columns:
            if '_color' in col:
                color_columns.append(col)
        #to define the user defined attributes
        Y=request.form['Y_select']
        X=request.form['X_select']
        title=X + " vs " + Y
        color=str(request.form['Cat_select'])+'_color'
        legend = color[:len(color)-6]
        source=ColumnDataSource(data=df)
        p=figure(plot_width=800,
                plot_height=400,
                title=str(title),
                x_axis_label=str(X),
                y_axis_label=str(Y))
        p.circle(X,Y,size=5,color=color,source=source,legend=legend)
    else:
        groupby1=request.form['grp1_select']
        groupby2=request.form['grp2_select']

        group = df.groupby((groupby1,groupby2))
        grpby_string = groupby1 + '_' + groupby2
        count_string = group.describe().columns[0][0] + '_count'

        source = ColumnDataSource(group)
        index_cmap = factor_cmap(grpby_string, palette=Spectral10, factors=sorted(df[groupby1].unique()), end=1)
        title='Count of '+ groupby1 + " and " + groupby2
        hover=HoverTool(tooltips=[
            ("Count",'@'+count_string),
            ("Group",'@'+grpby_string),
        ])
        p=figure(plot_width=800,
                plot_height=400,
                title=str(title),
                x_range=group,
                tools=[hover])
        p.vbar(x=grpby_string,
               top=count_string,
               width=1,
               source=source,
               line_color="white",
               fill_color=index_cmap)

    p.title.text_font_size = "30px"
    p.yaxis.axis_label_text_font_size= "25px"
    p.xaxis.axis_label_text_font_size= "25px"

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]

    #testing plot 2
    q=figure(plot_width=800,
            plot_height=400,
            title=str('test'),
            x_axis_label=str('testX'),
            y_axis_label=str('testY'))
    q.circle([1,2,3,4,5],[5,4,3,2,1],size=5,color='red')

    script2, div2 = components(q)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]

    return render_template("plot2.html",
    script1=script1,
    div1=div1,
    cdn_css=cdn_css,
    cdn_js=cdn_js,
    Continuous=Continuous,
    Categorical=Categorical,
    script2=script2,
    div2=div2)


@app.route('/plot',methods=['GET','POST'])
def plot():
    df=pandas.read_csv("simulated_data.csv")
    #to prepare color palette for grouping#
    def to_color(x):
        factors=list(df[col].unique())
        return d3['Category20'][max(len(factors),3)][factors.index(x)]

    for col in df.columns:
        if df[col].dtype=="object":
            df[col+'_color']= df[col].apply(to_color)

    df["default_color"]="black"
    #end of data preparation#
    columns=list(df.describe().columns)
    color_columns = []
    for col in df.columns:
        if '_color' in col:
            color_columns.append(col)
    #to define the user defined attributes
    Y=request.form['Col_select']
    X=request.form['Col_select2']
    title=X + " vs " + Y
    color=str(request.form['Col_select3'])

    legend = color[:len(color)-6]
    source=ColumnDataSource(data=df)
    p=figure(plot_width=800,
            plot_height=400,
            title=str(title),
            x_axis_label=str(X),
            y_axis_label=str(Y))
    p.circle(X,Y,size=5,color=color,source=source,legend=legend)
    p.title.text_font_size = "30px"
    p.yaxis.axis_label_text_font_size= "25px"
    p.xaxis.axis_label_text_font_size= "25px"

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]

    return render_template("plot.html",
    script1=script1,
    div1=div1,
    cdn_css=cdn_css,
    cdn_js=cdn_js,
    columns=columns,
    color_columns=color_columns)

@app.route('/form', methods=['GET'])
def my_form():
    df=pandas.read_csv("simulated_data.csv")
    #to prepare color palette for grouping#
    def to_color(x):
        factors=list(df[col].unique())
        return d3['Category20'][max(len(factors),3)][factors.index(x)]

    for col in df.columns:
        if df[col].dtype=="object":
            df[col+'_color']= df[col].apply(to_color)

    df["default_color"]="black"
    #end of data preparation#
    columns=list(df.describe().columns)
    color_columns = []
    for col in df.columns:
        if '_color' in col:
            color_columns.append(col)
    return render_template("myform.html",
    columns=columns,
    color_columns=color_columns)

if __name__=="__main__":
    app.run(debug=True)
