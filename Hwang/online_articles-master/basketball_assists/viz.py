# ========== (c) JP Hwang 2020-01-27  ==========

import numpy as np

def filt_hexbins(hexbin_stats, min_threshold=0.0):
    """
    Filter hexbin stats to exclude hexbin values below a threshold value (of frequency)

    :param hexbin_stats:
    :param min_threshold:
    :return:
    """
    from copy import deepcopy

    filt_hexbin_stats = deepcopy(hexbin_stats)
    temp_len = len(filt_hexbin_stats['freq_by_hex'])
    filt_array = [i > min_threshold for i in filt_hexbin_stats['freq_by_hex']]
    for k, v in filt_hexbin_stats.items():
        if type(v) != int:
            print(k, len(v), temp_len)
            if len(v) == temp_len:
                print(f'Filtering the {k} array:')
                filt_hexbin_stats[k] = [v[i] for i in range(temp_len) if filt_array[i]]
            else:
                print(f'WEIRD! The {k} array has a wrong length!')
        else:
            print(f'Not filtering {k} as it has an interger value')

    return filt_hexbin_stats


def draw_plotly_court(fig, fig_width=600, margins=10):

    # From: https://community.plot.ly/t/arc-shape-with-path/7205/5
    def ellipse_arc(x_center=0.0, y_center=0.0, a=10.5, b=10.5, start_angle=0.0, end_angle=2 * np.pi, N=200, closed=False):
        t = np.linspace(start_angle, end_angle, N)
        x = x_center + a * np.cos(t)
        y = y_center + b * np.sin(t)
        path = f'M {x[0]}, {y[0]}'
        for k in range(1, len(t)):
            path += f'L{x[k]}, {y[k]}'
        if closed:
            path += ' Z'
        return path

    fig_height = fig_width * (470 + 2 * margins) / (500 + 2 * margins)
    fig.update_layout(width=fig_width, height=fig_height)

    # Set axes ranges
    fig.update_xaxes(range=[-250 - margins, 250 + margins])
    fig.update_yaxes(range=[-52.5 - margins, 417.5 + margins])

    threept_break_y = 89.47765084
    three_line_col = "#777777"
    main_line_col = "#777777"

    fig.update_layout(
        # Line Horizontal
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        shapes=[
            dict(
                type="rect", x0=-250, y0=-52.5, x1=250, y1=417.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="rect", x0=-80, y0=-52.5, x1=80, y1=137.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="rect", x0=-60, y0=-52.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="circle", x0=-60, y0=77.5, x1=60, y1=197.5, xref="x", yref="y",
                line=dict(color=main_line_col, width=1),
                # fillcolor='#dddddd',
                layer='below'
            ),
            dict(
                type="line", x0=-60, y0=137.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=1),
                layer='below'
            ),

            dict(
                type="rect", x0=-2, y0=-7.25, x1=2, y1=-12.5,
                line=dict(color="#ec7607", width=1),
                fillcolor='#ec7607',
            ),
            dict(
                type="circle", x0=-7.5, y0=-7.5, x1=7.5, y1=7.5, xref="x", yref="y",
                line=dict(color="#ec7607", width=1),
            ),
            dict(
                type="line", x0=-30, y0=-12.5, x1=30, y1=-12.5,
                line=dict(color="#ec7607", width=1),
            ),

            dict(type="path",
                 path=ellipse_arc(a=40, b=40, start_angle=0, end_angle=np.pi),
                 line=dict(color=main_line_col, width=1), layer='below'),
            dict(type="path",
                 path=ellipse_arc(a=237.5, b=237.5, start_angle=0.386283101, end_angle=np.pi - 0.386283101),
                 line=dict(color=main_line_col, width=1), layer='below'),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=220, y0=-52.5, x1=220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),

            dict(
                type="line", x0=-250, y0=227.5, x1=-220, y1=227.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=250, y0=227.5, x1=220, y1=227.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=17.5, x1=-80, y1=17.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=27.5, x1=-80, y1=27.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=57.5, x1=-80, y1=57.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=87.5, x1=-80, y1=87.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=17.5, x1=80, y1=17.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=27.5, x1=80, y1=27.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=57.5, x1=80, y1=57.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=87.5, x1=80, y1=87.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),

            dict(type="path",
                 path=ellipse_arc(y_center=417.5, a=60, b=60, start_angle=-0, end_angle=-np.pi),
                 line=dict(color=main_line_col, width=1), layer='below'),

        ]
    )
    return True


def plot_shot_hexbins_plotly(
        xlocs, ylocs, freq_by_hex, accs_by_hex,
        marker_cmin=None, marker_cmax=None, colorscale='RdYlBu_r',
        title_txt='', legend_title='Accuracy',
        hexbin_text=[], ticktexts=[], logo_url=None, img_out=None):

    import plotly.graph_objects as go

    if marker_cmin is None:
        marker_cmin = min(accs_by_hex)
    if marker_cmax is None:
        marker_cmax = max(accs_by_hex)

    fig = go.Figure()
    draw_plotly_court(fig, fig_width=600)
    fig.add_trace(go.Scatter(
        x=xlocs, y=ylocs, mode='markers', name='markers',
        text=hexbin_text,
        marker=dict(
            size=freq_by_hex, sizemode='area', sizeref=2. * max(freq_by_hex) / (11. ** 2), sizemin=2.5,
            color=accs_by_hex, colorscale=colorscale,
            colorbar=dict(
                thickness=15,
                x=0.84,
                y=0.87,
                yanchor='middle',
                len=0.2,
                title=dict(
                    text="<B>" + legend_title + "</B>",
                    font=dict(
                        size=11,
                        color='#4d4d4d'
                    ),
                ),
                tickvals=[marker_cmin, (marker_cmin + marker_cmax) / 2, marker_cmax],
                ticktext=ticktexts,
                tickfont=dict(
                    size=11,
                    color='#4d4d4d'
                )
            ),
            cmin=marker_cmin, cmax=marker_cmax,
            line=dict(width=1, color='#333333'), symbol='hexagon',
        ),
        hoverinfo='text'
    ))

    if logo_url is not None:
        title_xloc = 0.19
    else:
        title_xloc = 0.1

    fig.update_layout(
        title=dict(
            text=title_txt,
            y=0.9,
            x=title_xloc,
            xanchor='left',
            yanchor='middle'),
        font=dict(
            family="Arial, Tahoma, Helvetica",
            size=10,
            color="#7f7f7f"
        ),
        annotations=[
            go.layout.Annotation(
                x=0.5,
                y=0.05,
                showarrow=False,
                text="Twitter: @_jphwang",
                xref="paper",
                yref="paper"
            ),
        ],
    )
    if logo_url is not None:
        fig.add_layout_image(
            go.layout.Image(
                source=logo_url,
                xref="x", yref="y", x=-230, y=405, sizex=50, sizey=50,
                xanchor="left", yanchor="top",
                sizing="stretch", opacity=1, layer="above"))

    if img_out is None:
        fig.show(
            config={
                'displayModeBar': False
            }
        )
    else:
        fig.write_image(img_out)

    return fig


def plot_parcat_chart(
        input_df,
        title_txt='Shot flow - 2018/2019 NBA Season (colored: assisted)',
        colorscale=[[0, 'gray'], [1, 'crimson']]):

    import pandas as pd
    import plotly.graph_objects as go
    from copy import deepcopy

    # Create new category boolean to color categories
    input_df = input_df.assign(col_cat=1 - 1 * input_df.assist.isna())

    makes_df = input_df[input_df.shot_made == 1]
    temp_assist_col = deepcopy(makes_df.assist.fillna(''))  # Will not sort with NAs in it
    makes_df.loc[:, 'assist'] = temp_assist_col

    i, r = pd.factorize(makes_df['assist'])
    a = np.argsort(np.bincount(i)[i], kind='mergesort')
    makes_df = makes_df.iloc[a]

    i, r = pd.factorize(makes_df['player'])
    a = np.argsort(np.bincount(i)[i], kind='mergesort')
    a = np.flip(a)
    makes_df = makes_df.iloc[a]

    # Create dimensions
    class_dim = go.parcats.Dimension(values=makes_df.player, categoryorder='array', label=" ")
    zone_dim = go.parcats.Dimension(values=makes_df.shot_zone, categoryorder='category ascending', label=" ")
    assist_dim = go.parcats.Dimension(values=makes_df.assist, categoryorder='array', label=" ")

    # Create parcats trace
    color = makes_df.col_cat

    fig = go.Figure(data=[go.Parcats(dimensions=[class_dim, zone_dim, assist_dim],
                                     line={'color': color, 'colorscale': colorscale},
                                     hoveron='color', hoverinfo='count+probability',
                                     labelfont={'size': 13, 'family': "Arial, Tahoma, Helvetica"},
                                     tickfont={'size': 11, 'family': "Arial, Tahoma, Helvetica"}
                                     )])
    fig.update_layout(
        width=900,
        height=700,
        margin=dict(t=50),
        title=dict(
            text=title_txt,
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='middle'),
        font=dict(
            family="Arial, Tahoma, Helvetica",
            size=11,
            color="#3f3f3f",
        ),
        coloraxis=dict(showscale=False),
        annotations=[
            go.layout.Annotation(
                x=0.5,
                y=0.0,
                showarrow=False,
                xanchor='center',
                yanchor='middle',
                text="Twitter: @_jphwang",
                xref="paper",
                yref="paper"
            ),
            go.layout.Annotation(
                x=0.5,
                y=0.99,
                showarrow=False,
                xanchor='center',
                yanchor='middle',
                text="<B>Left:</B> Shooter, <B>Middle:</B> Shot zone, <B>Right:</B> Assist",
                xref="paper",
                yref="paper"
            ),
        ],
    )
    return fig
