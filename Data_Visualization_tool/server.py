from flask import Flask
from flask import render_template, request, url_for
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

describe = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]

null = []

df = 0

theme = ""


@app.route("/")
def home():
    return render_template("gettingdata.html")


@app.route("/", methods=['post'])
def next():
    global df
    global name
    name = request.form["title"]
    data = request.files["data"]
    df = pd.read_csv(data)

    return render_template("details.html", df=df, name=name, describe=describe)


@app.route("/fixvalues")
def fixvalues():
    global df
    nofix = 0
    null = []

    for i in range(df.shape[1]):
        if df.isnull().sum()[i] != 0:
            null.append(i)
            nofix = 1

    return render_template("fixvalues.html", df=df, null=null, nofix=nofix, name=name)


@app.route("/afterfix", methods=['POST'])
def afterfix():
    global df
    cols = request.form['cols']
    meth = request.form['meth']
    if meth == "Drop Column":
        df = df.drop([cols], axis="columns")
    elif meth == "Mean":
        df[cols] = df[cols].fillna(df[cols].mean)
    elif meth == "Std deviation":
        df[cols] = df[cols].fillna(df[cols].std())
    elif meth == "Add upper value":
        df[cols] = df[cols].fillna(method="ffill")
    elif meth == "Add lower value":
        df[cols] = df[cols].fillna(method="bfill")

    nofix = 0
    null = []

    for i in range(df.shape[1]):
        if df.isnull().sum()[i] != 0:
            null.append(i)
            nofix = 1

    return render_template("fixvalues.html", df=df, null=null, nofix=nofix, name=name)


@app.route("/details")
def details():
    return render_template("details.html", df=df, name=name, describe=describe)




@app.route("/visualize")
def visualize():
    return render_template("Visualize.html", name=name, df=df)



@app.route("/yash", methods = ['POST'])
def yash(hs = 0):
    col1 = request.form['col1']
    col2 = request.form['col2']
    palette = request.form['palette']
    plot = request.form['graph']
    if request.form.get('theme') == "dark":
        plt.style.use('dark_background')
        if plot == 'barplot':
            sns_plot = sns.barplot(x=col1, y=col2, data=df, palette=palette)
            sns_plot = sns_plot.get_figure()

        elif plot == 'lineplot':
            sns_plot = sns.lineplot(x=col1, y=col2, data=df, palette=palette)
            sns_plot = sns_plot.get_figure()

        elif plot == 'boxplot':
            sns_plot = sns.boxplot(x=col1, y=col2, data=df, palette=palette)
            sns_plot = sns_plot.get_figure()

        elif plot == 'scatterplot':
            sns_plot = sns.scatterplot(x=col1, y=col2, data=df, palette=palette)
            sns_plot = sns_plot.get_figure()

        elif plot == 'swarmplot':
            sns_plot = sns.swarmplot(x=col1, y=col2, data=df, palette=palette)
            sns_plot = sns_plot.get_figure()

    else:
        if plot == 'barplot':
            sns_plot = sns.barplot(x=col1, y=col2, data=df, palette=palette)
            sns_plot = sns_plot.get_figure()

        elif plot == 'lineplot':
            sns_plot = sns.lineplot(x=col1, y=col2, data=df, palette=palette)
            sns_plot = sns_plot.get_figure()

        elif plot == 'boxplot':
            sns_plot = sns.boxplot(x=col1, y=col2, data=df, palette=palette)
            sns_plot = sns_plot.get_figure()

        elif plot == 'scatterplot':
            sns_plot = sns.scatterplot(x=col1, y=col2, data=df, palette=palette)
            sns_plot = sns_plot.get_figure()

        elif plot == 'swarmplot':
            sns_plot = sns.swarmplot(x=col1, y=col2, data=df, palette=palette)
            sns_plot = sns_plot.get_figure()

    os.remove('static/0.png')
    sns_plot.savefig('static/'+str(hs)+'.png')
    return render_template("Visualize.html", df=df, name=name, image = str(hs)+'.png', col1 = col1, col2 = col2, palette = palette, theme = theme)
# How to show image and save image

if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost", port=5010)
