import pandas as pd
import matplotlib.pyplot as plt


DEFAULT_COLORS = ['#0472c2', '#1ec5d6', '#fcd251', '#c36c6c', '#eac1c1', '#c5c5c5']

font = {'family' : 'Verdana',
        'weight' : 'normal',
        'size'   : 18}
plt.rc('font', **font)


def bin_long_tail(brand_summary, count_threshold, column):
    df_ = brand_summary.copy()
    above_threshold = df_[df_[column] >= count_threshold]
    below_threshold = df_[df_[column] < count_threshold]
    binned = pd.concat([
            above_threshold[['Brand', column]],
            pd.DataFrame(
                [['Other', int(below_threshold[column].sum())]],
                columns=['Brand', column]
                )
        ])
    return binned

def create_pie_chart(brand_summary, count_threshold = 3, column='Total Votes'):
    votes_binned = bin_long_tail(brand_summary, count_threshold, column)
    n = len(votes_binned)

    fig, ax = plt.subplots()
    ax.pie(
        votes_binned[column],
        labels=votes_binned['Brand'],
        colors=DEFAULT_COLORS[0:n],
        startangle=90,
        labeldistance=1.2,
        pctdistance=0.7,
        wedgeprops = {"edgecolor":"k",'linewidth': 2, 'linestyle': 'solid', 'antialiased': True}
        )
    ax.axis('equal')
    plt.title(column, pad=40)
    plt.show()

def create_bar_chart(brand_summary, count_threshold = 3, column='Total Votes'):
    votes_binned = bin_long_tail(brand_summary, count_threshold, column)
    n = len(votes_binned)

    fig, ax = plt.subplots()
    ax.barh(
        votes_binned['Brand'],
        votes_binned[column],
        color=DEFAULT_COLORS[0:n],
        )
    ax.invert_yaxis()
    plt.title(column, pad=40)
    plt.show()
