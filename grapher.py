def graph_pie(csv, col):
    # csv is the file
    # col is the column that we care about
    print("will graph a pie chart, eventually")


def graph_bar(csv, col_x, col_y):
    # csv is the file
    # col_x is the column that we use for the x
    # col_y is the column that we use for the y
    print("will graph a bar graph, eventually")


def graph_line(csv, num_cols, *cols, col_x):
    # csv is the file
    # num_cols is the number of columns we care about about in the y
    # *cols is an array of the columns we will use for the y
    # col_x is the column we use for the x
    print("will graph a line graph of %d lines, eventually" % num_cols)
