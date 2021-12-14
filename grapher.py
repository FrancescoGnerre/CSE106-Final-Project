import pandas as pd
import matplotlib.pyplot as matPlot


def graph_pie(col, col_label, name):
    # col is the column that we care about
    # col_label is the column label
    # name is the graph name

    matPlot.pie(col, labels=col_label)
    matPlot.title(name)
    matPlot.show()


def graph_bar(col_x, col_y, name, x_label, y_label):
    # col_x is the column that we use for the x
    # col_y is the column that we use for the y
    # name is the graph name
    # x_label is the x axis label
    # y_label is the y axis label

    matPlot.bar(col_x, col_y)
    matPlot.title(name)
    matPlot.xlabel(x_label)
    matPlot.ylabel(y_label)
    matPlot.show()


def graph_line(csv, num_cols, legend_name, name, x_label, y_label):
    # csv is the file
    # num_cols is the number of columns we care about in the y
    # col_x is the column we use for the x
    # name is the graph name
    # legend_name is the legend name
    # x_label is the x-axis label
    # y_label is the y-axis label

    if num_cols == 1:

        matPlot.plot(csv.iloc[:,1:2])
        matPlot.title(name)
        matPlot.xlabel(x_label)
        matPlot.ylabel(y_label)
        matPlot.legend(csv.iloc[:,1:2], title=legend_name)
        matPlot.show()

    elif num_cols == 2:

        matPlot.plot(csv.iloc[:,1:3])
        matPlot.title(name)
        matPlot.xlabel(x_label)
        matPlot.ylabel(y_label)
        matPlot.legend(csv.iloc[:,1:3],title=legend_name)
        matPlot.show()

    elif num_cols == 3:

        matPlot.plot(csv.iloc[:,1:4])
        matPlot.title(name)
        matPlot.xlabel(x_label)
        matPlot.ylabel(y_label)
        matPlot.legend(csv.iloc[:,1:4], title=legend_name)
        matPlot.show()

    elif num_cols == 4:

        matPlot.plot(csv.iloc[:,1:5])
        matPlot.title(name)
        matPlot.xlabel(x_label)
        matPlot.ylabel(y_label)
        matPlot.legend(csv.iloc[:,1:5],title=legend_name)
        matPlot.show()

    elif num_cols == 5:

        matPlot.plot(csv.iloc[:,1:6])
        matPlot.title(name)
        matPlot.xlabel(x_label)
        matPlot.ylabel(y_label)
        matPlot.legend(csv.iloc[:,1:6],title=legend_name)
        matPlot.show()

    elif num_cols == 6:

        matPlot.plot(csv.iloc[:,1:7])
        matPlot.title(name)
        matPlot.xlabel(x_label)
        matPlot.ylabel(y_label)
        matPlot.legend(csv.iloc[:,1:7],title=legend_name)
        matPlot.show()