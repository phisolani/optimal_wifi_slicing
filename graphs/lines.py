#!/usr/bin/env python
__author__ = "Pedro Heleno Isolani"
__copyright__ = "Copyright 2019, QoS-aware WiFi Slicing"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Pedro Heleno Isolani"
__email__ = "pedro.isolani@uantwerpen.be"
__status__ = "Prototype"

" Python script for making graphs from CSV output"

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def draw_line_graph_with_multiple_y_axis(filename=None, directory=None, title=None,
                                         x_axis=None, y1_axis=None, y2_axis=None,
                                         x_axis_label=None, y1_axis_label=None, y2_axis_label=None,
                                         y1_stdev=None, y2_stdev=None):
    # In case of font problems
    # matplotlib.font_manager._rebuild()
    # or remove ~/.cache/fontconfig/*

    if [filename, title, x_axis, y1_axis, y2_axis] is not None:

        # Applying Seaborn style
        # whitegrid, darkgrid, whitegrid, dark, white, and ticks
        sns.set(style="whitegrid", font='Times New Roman', palette='deep', font_scale=2, color_codes=True, rc=None)

        # Reading data results
        data_dict = read_results(filename=filename,
                                 x_axis=x_axis,
                                 y1_axis=y1_axis, y2_axis=y2_axis,
                                 y1_stdev=y1_stdev, y2_stdev=y2_stdev)

        # Plotting just the first values of the experiment (16, 8)
        fig, host = plt.subplots(figsize=(20, 5), dpi=144)
        # fig.subplots_adjust(right=0.75)

        # Adjust x Axis
        plt.tight_layout()

        par1 = host.twinx()

        # Offset the right spine of par2.  The ticks and label have already been
        # placed on the right by twinx above.
        # Having been created by twinx, par2 has its frame off, so the line of its
        # detached spine is invisible.  First, activate the frame but make the patch
        # and spines invisible.

        # Add linestyle='None' in case of removing the lines
        p1, = host.plot(data_dict['x_axis']['values'], data_dict['y1_axis']['values'], "b-", marker="D", markevery=1,
                        markersize=10, mfc='none', markeredgewidth=2, label=data_dict['y1_axis']['label'])
        p2, = par1.plot(data_dict['x_axis']['values'], data_dict['y2_axis']['values'], "-g", marker="o", markevery=1,
                        markersize=10, mfc='none', markeredgewidth=2, label=data_dict['y2_axis']['label'])

        axis_padding = 0.3  # percentage
        # host.set_xlim(min(data_dict['x_axis']['values']),
        #              max(data_dict['x_axis']['values']))

        host.set_xlim(1,
                      64)

        # plt.xticks(np.arange(min(data_dict['x_axis']['values']), max(data_dict['x_axis']['values'])+1, 1.0))

        host.set_ylim(0,
                      max(data_dict['y1_axis']['values']) +
                      (max(data_dict['y1_axis']['values']) * axis_padding))
        par1.set_ylim(0,
                      max(data_dict['y2_axis']['values']) +
                      (max(data_dict['y2_axis']['values']) * axis_padding))

        host.set_xlabel(x_axis_label)
        host.set_ylabel(y1_axis_label)
        par1.set_ylabel(y2_axis_label)

        # host.yaxis.label.set_color(p1.get_color())
        # par1.yaxis.label.set_color(p2.get_color())

        # tkw = dict(size=4, width=1.5)
        # host.tick_params(axis='y', colors=p1.get_color(), **tkw)
        # par1.tick_params(axis='y', colors=p2.get_color(), **tkw)

        lines = [p1, p2]

        if [y1_stdev, y2_stdev] is not None:
            host.errorbar(data_dict['x_axis']['values'], data_dict['y1_axis']['values'],
                          yerr=data_dict['y1_stdev']['values'], fmt='none', ecolor='b', capthick=3, capsize=5)
            par1.errorbar(data_dict['x_axis']['values'], data_dict['y2_axis']['values'],
                          yerr=data_dict['y2_stdev']['values'], fmt='none', ecolor='g', capthick=3, capsize=5)

        # Title of the graph
        # plt.title(title)
        plt.legend(lines, [l.get_label() for l in lines], loc='upper center', bbox_to_anchor=(0.5, 1.00),
                   ncol=2)  # shadow=True)
        plt.savefig(str(directory) + '/' + str(title) + '.pdf', format="pdf", bbox_inches="tight")
        plt.savefig(str(directory) + '/' + str(title) + '.png', format="png", bbox_inches="tight")
        plt.show()


def draw_stacked_lines_graph(filename=None, directory=None, title=None, fig_size=[10, 3.4]):
    sns.set(style="whitegrid", font='Times New Roman', palette='deep', font_scale=1.5, color_codes=True, rc=None)

    fig, host = plt.subplots(figsize=(fig_size[0], fig_size[1]), dpi=144)

    # TODO: Read from results...
    lista = {}
    lista['index'] = [0, 1, 2, 3]
    lista['basic'] = [0, 1, 2, 3]
    lista['saving'] = [0, 1, 2, 3]
    lista['money_mkt'] = [0, 1, 2, 3]
    lista['credit'] = [0, 1, 2, 3]

    # Adjust x Axis
    plt.tight_layout()

    plt.stackplot(lista['index'],
                  [lista['basic'], lista['saving'],
                   lista['money_mkt'], lista['credit']],
                  labels=['basic', 'saving', 'money_mkt', 'credit'],
                  alpha=0.8)

    host.set_xlabel('Time (sec)')
    host.set_ylabel('Queue Delay (ms)')

    plt.legend(loc='upper center', fontsize='small', ncol=4)
    plt.savefig(str(directory) + '/' + str(title) + '.pdf', format="pdf", bbox_inches="tight")
    plt.savefig(str(directory) + '/' + str(title) + '.png', format="png", bbox_inches="tight")
    plt.show()


def draw_line_graph_with_multiple_y_axis_and_files(filenames=None, title=None, directory=None,
                                                   x_axises=None, y1_axises=None, y2_axises=None, x_axis_label=None,
                                                   y1_axis_label=None, y2_axis_label=None, y1_expected=None, reformulate_xticks=None,
                                                   x_pos=None, x_labels=None, x_axis_limit=None, x_axis_start=None, y1_axis_limit=None, y2_axis_limit=None,
                                                   y1_stdevs=None, y2_stdevs=None, markers=None, fig_size=[10, 3.4],
                                                   log_scale_x=None, log_scale_y=None, annotation_label=None, annotation_xy=None):
    # In case of font problems
    # matplotlib.font_manager._rebuild()

    if [filenames, title, x_axises, y1_axises, y2_axises] is not None:

        # Applying Seaborn style
        # whitegrid, darkgrid, whitegrid, dark, white, and ticks
        sns.set(style="whitegrid", font='Times New Roman', palette='deep', font_scale=1.5, color_codes=True, rc=None)

        #plt.rc('text', usetex=True)
        #plt.rc('font', family='Times New Roman', weight='normal', size=14)
        plt.rcParams['mathtext.fontset'] = 'stix'

        # Reading data results
        data_dict = []

        for i in range(0, len(filenames)):
            if all(param is not None for param in [y1_stdevs, y2_stdevs]):
                data_dict.append(read_results(filename=filenames[i],
                                              x_axis=x_axises[i],
                                              y1_axis=y1_axises[i],
                                              y2_axis=y2_axises[i],
                                              y1_stdev=y1_stdevs[i],
                                              y2_stdev=y2_stdevs[i]))
            else:
                if y1_expected is not None:
                    data_dict.append(read_results(filename=filenames[i],
                                                  x_axis=x_axises[i],
                                                  y1_axis=y1_axises[i],
                                                  y1_expected=y1_expected[i],
                                                  y2_axis=y2_axises[i]))
                else:
                    data_dict.append(read_results(filename=filenames[i],
                                                  x_axis=x_axises[i],
                                                  y1_axis=y1_axises[i],
                                                  y2_axis=y2_axises[i]))

        # Plotting just the first values of the experiment (16, 8)
        fig, host = plt.subplots(figsize=(fig_size[0], fig_size[1]), dpi=144)
        # fig.subplots_adjust(right=0.75)

        # Adjust x Axis
        plt.tight_layout()

        par1 = host.twinx()

        if log_scale_y is not None:
            par1.set_yscale('log')

        if log_scale_x is not None:
            host.set_yscale('log')

        # Offset the right spine of par2.  The ticks and label have already been
        # placed on the right by twinx above.
        # Having been created by twinx, par2 has its frame off, so the line of its
        # detached spine is invisible.  First, activate the frame but make the patch
        # and spines invisible.

        lines = []
        colors = ['darkblue', 'darkviolet', 'mediumblue', 'deeppink', 'dodgerblue', 'magenta']
        for data in data_dict:
            # Add linestyle='None' in case of removing the lines
            # Add mfc='None' in case of no fill for markers
            print(data)

            if markers is None:
                p1, = host.plot(data['x_axis']['values'], data['y1_axis']['values'], colors[0],
                                linewidth=2,
                                label=data['y1_axis']['label'])
                if y1_expected is not None:
                    p3, = host.plot(data['x_axis']['values'], data['y1_expected']['values'], colors[4], linestyle="-.",
                                #linewidth=2,
                                label=r'$\sum_{s\in S^b}{W^s}, \mu^b_{MAX} = 1720$')
                p2, = par1.plot(data['x_axis']['values'], data['y2_axis']['values'], colors[1], linestyle="--",
                                linewidth=2,
                                label=data['y2_axis']['label'])
            else:
                p1, = host.plot(data['x_axis']['values'], data['y1_axis']['values'], colors[0],
                                marker=markers[0], markevery=1, linewidth=2, markersize=8, mfc='none', markeredgewidth=1,
                                label=data['y1_axis']['label'])
                p2, = par1.plot(data['x_axis']['values'], data['y2_axis']['values'], colors[1],
                                marker=markers[0], markevery=1, linewidth=2, markersize=8, markeredgewidth=1,
                                label=data['y2_axis']['label'])

                markers.pop(0)

            colors.pop(0)
            colors.pop(0)

            lines.append(p1)
            if y1_expected is not None:
                lines.append(p3)
            lines.append(p2)

        axis_padding = 0.3  # percentage
        # host.set_xlim(min(data_dict['x_axis']['values']),
        #              max(data_dict['x_axis']['values']))

        if x_axis_limit and x_axis_start:
            host.set_xlim(x_axis_start, x_axis_limit)
        elif x_axis_limit:
            host.set_xlim(1, x_axis_limit)
        else:
            host.set_xlim(1, 64)

        #plt.xticks(np.arange(0, 330, step=30))
        if reformulate_xticks:
            plt.xticks(x_pos, x_labels)

        if annotation_label is not None:
            if annotation_xy is not None:
                par1.annotate(annotation_label,
                              xy=annotation_xy, xycoords='data',
                              xytext=(0.7, 0.95), textcoords='axes fraction',
                              arrowprops=dict(facecolor='black', shrink=0.05),
                              horizontalalignment='right', verticalalignment='top')

        #plt.xticks(np.arange(min(data_dict['x_axis']['values']), max(data_dict['x_axis']['values']), 1.0))

        # host. set_ylim(0,
        #              max(data_dict['y1_axis']['values']) +
        #              (max(data_dict['y1_axis']['values'])*axis_padding))
        # par1.set_ylim(0,
        #              max(data_dict['y2_axis']['values']) +
        #              (max(data_dict['y2_axis']['values']) * axis_padding))

        if y1_axis_limit:
            host.set_ylim(0, y1_axis_limit)

        if y2_axis_limit:
            par1.set_ylim(0, y2_axis_limit)

        host.set_xlabel(x_axis_label)
        host.set_ylabel(y1_axis_label)
        par1.set_ylabel(y2_axis_label)

        # host.yaxis.label.set_color(p1.get_color())
        # par1.yaxis.label.set_color(p2.get_color())

        # tkw = dict(size=4, width=1.5)
        # host.tick_params(axis='y', colors=p1.get_color(), **tkw)
        # par1.tick_params(axis='y', colors=p2.get_color(), **tkw)

        # lines = [p1, p2, p3, p4]

        colors = ['darkblue', 'darkviolet', 'mediumblue', 'deeppink', 'dodgerblue', 'magenta']
        if all(param is not None for param in [y1_stdevs, y2_stdevs]):
            for data in data_dict:
                host.errorbar(data['x_axis']['values'], data['y1_axis']['values'],
                              yerr=data['y1_stdev']['values'], fmt='none', ecolor=colors[0], capthick=3, capsize=1)
                par1.errorbar(data['x_axis']['values'], data['y2_axis']['values'],
                              yerr=data['y2_stdev']['values'], fmt='none', ecolor=colors[1], capthick=3, capsize=1)

                colors.pop(0)
                colors.pop(0)

        # Title of the graph
        # plt.title(title)
        plt.legend(lines, [l.get_label() for l in lines], loc='upper left',
                   ncol=1)  # shadow=True)
        plt.savefig(str(directory) + '/' + str(title) + '.pdf', format="pdf", bbox_inches="tight")
        plt.savefig(str(directory) + '/' + str(title) + '.png', format="png", bbox_inches="tight")
        plt.savefig(str(directory) + '/' + str(title) + '.eps', format="eps", bbox_inches="tight")
        plt.show()


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def read_results(filename, x_axis, y1_axis, y2_axis, y1_expected=None, y1_stdev=None, y2_stdev=None):
    # Common dict structure
    data_dict = {'x_axis': {'label': '', 'values': []},
                 'y1_axis': {'label': '', 'values': []},
                 'y2_axis': {'label': '', 'values': []}
                 }

    if all(param is not None for param in [y1_stdev, y2_stdev]):
        data_dict['y1_stdev'] = {'label': '', 'values': []}
        data_dict['y2_stdev'] = {'label': '', 'values': []}

    if y1_expected is not None:
        data_dict['y1_expected'] = {'label': '', 'values': []}

    # Filename definition
    df = pd.read_csv(filename, sep=',', header=0)

    # Headers definition
    header_names = {'x_axis': x_axis,
                    'y1_axis': y1_axis,
                    'y2_axis': y2_axis
                    }

    if all(param is not None for param in [y1_stdev, y2_stdev]):
        header_names['y1_stdev'] = y1_stdev
        header_names['y2_stdev'] = y2_stdev

    if y1_expected is not None:
        header_names['y1_expected'] = y1_expected

    # Populating with the header fields
    for header_value in df.columns.values:
        for key, value in header_names.items():
            if value in header_value:
                data_dict[key]['label'] = header_value
                data_dict[key]['values'] = []

    # Populating with the values
    for index, row in df.iterrows():
        for key, value in data_dict.items():
            data_dict[key]['values'].append(row[value['label']])

    return data_dict
