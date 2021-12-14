import pandas as pd
import matplotlib.pyplot as matPlot

def graph_pie(csv, col, col_label, name, legend_name):
    # csv is the file
    # col is the column that we care about
    # col_label is the column label
    # name is the graph name
    # legend_name is the legend name

    matPlot.pie(col, labels=col_label)
    matPlot.legend(title=legend_name)
    matPlot.title(name)
    matPlot.show()


def graph_bar(csv, col_x, col_y, name, legend_name, x_label, y_label):
    # csv is the file
    # col_x is the column that we use for the x
    # col_y is the column that we use for the y
    # name is the graph name
    # legend_name is the legend name
    # x_label is the x axis label
    # y_label is the y axis label

    matPlot.bar(col_x, col_y)
    matPlot.title(name)
    matPlot.xlabel(x_label)
    matPlot.ylabel(y_label)
    matPlot.legend(title=legend_name)
    matPlot.show()


def graph_line(csv, num_cols, *cols, col_x):
    # csv is the file
    # num_cols is the number of columns we care about about in the y
    # *cols is an array of the columns we will use for the y
    # col_x is the column we use for the x
    print("will graph a line graph of %d lines, eventually" % num_cols)
