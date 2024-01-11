from jinja2 import Environment, FileSystemLoader
import pdfkit
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import base64
from statstics_test import corr_coef
import plotly.graph_objects as go
import markdown


path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


def np_log(row):
    if row == 0:
        return 0
    elif row > 0:
        return np.log(row)
    else:
        return -1 * np.log(row*-1)


def color_row(row):
    if row['Position'] == 'Sell':
        color = 'background-color: red;color:white'
    elif row['Position'] == 'Buy':
        color = 'background-color: green;color:white'
    else:
        color = ''
    return [color] * len(row)


def CreateHtml(strategy):
    env = Environment(loader=FileSystemLoader('.'))
    # Load the template
    template = env.get_template('html/index.html')

    # load excel to html
    df = pd.read_excel("result.xlsx")
    df['SN'] = df.index + 1
    last_column = df.pop(df.columns[-1])  # Remove the last column and store it
    df.insert(0, last_column.name, last_column)
    df['Invest Amount'] = df['Invest Amount'].map('{:,.2f}'.format)
    df['Return Amount'] = df['Return Amount'].map('{:,.2f}'.format)
    df['Return Percent'] = df['Return Percent'].round(2)
    df['Standard Deviation'] = df['Standard Deviation'].round(2)
    df['Beta'] = df['Beta'].round(2)
    df['From Date'] = pd.to_datetime(df['From Date'])
    df['To Date'] = pd.to_datetime(df['To Date'])
    df["Number of Days"] = df["To Date"] - df["From Date"]
    df['Annualized Return'] = (
        (df['Return Percent']/(df['To Date'] - df['From Date']).dt.days) * 365).round(2)
    df = df.sort_values('Return Percent', ascending=False)
    top_5 = (df.sort_values('Return Percent', ascending=False).head(5))[
        "Symbol"].to_list()
    bottom_5 = (df.sort_values('Return Percent', ascending=True).head(5))[
        "Symbol"].to_list()
    top_5_detail = []
    bottom_5_detail = []
    for symbol in top_5:
        try:
            df_head = pd.read_excel(f"result/{symbol}.xlsx")
            # print(df_head)
            df_head['qtd'] = df_head['qtd'].map(
                '{:,.2f}'.format)
            df_head['Invest'] = df_head['Invest'].map(
                '{:,.2f}'.format)
            df_head = df_head.fillna("")
            df_head = df_head.style.apply(color_row, axis=1)
            html_output_head = df_head.to_html(index=False)
            top_5_detail.append({"symbol": symbol, "html": html_output_head})
        except Exception as e:
            print(e)
            pass
    for symbol in bottom_5:
        try:
            df_tail = pd.read_excel(f"result/{symbol}.xlsx")
            df_tail['qtd'] = df_tail['qtd'].map(
                '{:,.2f}'.format)
            df_tail['Invest'] = df_tail['Invest'].map(
                '{:,.2f}'.format)
            df_tail = df_tail.fillna("")
            df_tail = df_tail.style.apply(color_row, axis=1)
            html_output_tail = df_tail.to_html(index=False)
            bottom_5_detail.append(
                {"symbol": symbol, "html": html_output_tail})
        except Exception as e:
            pass
    # print(top_5_detail)

    # relationship betweent return percent and standard deviation
    r_p_log = df['Return Percent'].apply(np_log)
    s_d_log = df['Standard Deviation'].apply(np_log)
    fig = px.line(x=df["Symbol"], y=[r_p_log, s_d_log])
    newnames = {'wide_variable_0': 'Return Percent',
                'wide_variable_1': 'Standard Deviation'}
    fig.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                          legendgroup=newnames[t.name],
                                          hovertemplate=t.hovertemplate.replace(
                                              t.name, newnames[t.name])
                                          )
                       )
    fig.update_layout(
        title='Relationship betweern standard deviation and return percent',
        xaxis_title='Symbol',
        yaxis_title='Value',
        legend_title='Variable Legend'
    )
    image_bytes = pio.to_image(
        fig, format='png',  width=800, height=600, scale=2)
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    chart_html_sd_rp = f'<img src="data:image/png;base64,{image_base64}">'
    # calculating corr and  p
    corr_coeff, p_value = corr_coef(
        df["Return Percent"], df["Standard Deviation"])
    sd_rp_st = f"""
     <h3>Correlation Coefficient: { round(corr_coeff, 2)}</h3>
     <h3>P-value: { round(p_value, 2)}</h3>
     <h3>Implication</h3>
     <p>The correlation coefficient measures the strength and direction of the linear relationship between two variables, ranging from -1 to 1. A correlation coefficient of -0.05 suggests a weak negative correlation, indicating a slight tendency for one variable to decrease as the other variable increases. The p-value assesses the statistical significance of the correlation coefficient. If the p-value is below a predetermined threshold (e.g., 0.05), it indicates a significant correlation, while a higher p-value suggests the correlation could be due to chance. Together, the correlation coefficient and p-value provide insights into the relationship between variables, though other factors should be considered for a comprehensive interpretation.</p>
    """

    # relationship betweent return percent and beta
    r_p_log = df['Return Percent'].apply(np_log)
    b_log = df['Beta'].apply(np_log)
    fig = px.line(x=df["Symbol"], y=[r_p_log, b_log])
    newnames = {'wide_variable_0': 'Return Percent',
                'wide_variable_1': 'Beta'}
    fig.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                          legendgroup=newnames[t.name],
                                          hovertemplate=t.hovertemplate.replace(
                                              t.name, newnames[t.name])
                                          )
                       )
    fig.update_layout(
        title='Relationship betweern beta and return percent',
        xaxis_title='Symbol',
        yaxis_title='Value',
        legend_title='Variable Legend'
    )
    image_bytes = pio.to_image(
        fig, format='png',  width=800, height=600, scale=2)
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    chart_html_b_rp = f'<img src="data:image/png;base64,{image_base64}">'
    # calculating corr and  p
    corr_coeff, p_value = corr_coef(
        df["Return Percent"], df["Beta"])
    sd_rp_b = f"""
     <h3>Correlation Coefficient: { round(corr_coeff, 2)}</h3>
     <h3>P-value: { round(p_value, 2)}</h3>
     <h3>Implication</h3>
     <p>The correlation coefficient and p-value are statistical measures used to assess the relationship between two variables. The correlation coefficient quantifies the strength and direction of the linear relationship between variables, ranging from -1 to 1. A correlation coefficient of 0 indicates no linear relationship, while coefficients closer to -1 or 1 indicate stronger negative or positive correlations, respectively. The p-value indicates the statistical significance of the correlation coefficient. If the p-value is less than a chosen significance level (such as 0.05), it suggests a statistically significant correlation, indicating that the observed relationship is unlikely to have occurred by chance. On the other hand, a p-value greater than the significance level indicates that the observed correlation could plausibly be due to random chance. Thus, the correlation coefficient and p-value together provide insights into the strength and statistical significance of the relationship between variables.</p>
    """

    html_output = df.to_html(index=False)
    try:
        with open(f"content/{strategy}.md", "r") as f:
            md_data = f.read()
        description = markdown.markdown(md_data)
        print(description)
    except Exception as e:
        print(e)
        description = f"""
        <h1><b> We are running {strategy} strategy </b></h1>
        """

    # best case montecarlor
    ms_df = pd.read_excel("msim.xlsx")
    b_case_ms = (ms_df.sort_values('Return Percent', ascending=False).head(5))
    b_case_ms['Invest Amount'] = b_case_ms['Invest Amount'].map(
        '{:,.2f}'.format)
    b_case_ms['Return Amount'] = b_case_ms['Return Amount'].map(
        '{:,.2f}'.format)
    b_case_ms['Return Percent'] = b_case_ms['Return Percent'].round(2)
    b_case_ms = b_case_ms.to_html(index=False)
    # wors case montecarlor
    w_case_ms = (ms_df.sort_values('Return Percent', ascending=True).head(5))
    w_case_ms['Invest Amount'] = w_case_ms['Invest Amount'].map(
        '{:,.2f}'.format)
    w_case_ms['Return Amount'] = w_case_ms['Return Amount'].map(
        '{:,.2f}'.format)
    w_case_ms['Return Percent'] = w_case_ms['Return Percent'].round(2)
    w_case_ms = w_case_ms.to_html(index=False)

    trace = go.Histogram(x=ms_df["Return Percent"])
    layout = go.Layout(title='Histogram', xaxis=dict(
        title='Values'), yaxis=dict(title='Frequency'))
    figure = go.Figure(data=[trace], layout=layout)
    image_bytes = pio.to_image(
        figure, format='png',  width=800, height=600, scale=2)
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    distribution_rp_chart = f'<img src="data:image/png;base64,{image_base64}">'

    # summary
    summary_mcs = ms_df["Return Percent"].describe()
    summary_mcs = summary_mcs.to_frame().to_html()
    # Render the template with data
    total_data = (ms_df["Return Percent"] != 0).sum()
    summary_mcs += f"""
    <br>
    <h1>Probability Of Getting Positive Return: { round((((ms_df["Return Percent"] > 0).sum())/total_data)*100, 2) }%</h1>
    <h1>Probability Of Getting Negative Return: { round((((ms_df["Return Percent"] < 0).sum())/total_data)*100, 2) }%</h1>
    """
    output = template.render(
        name='John Doe',
        description=description,
        result_table=html_output,
        top_five=top_5,
        top_five_detail=top_5_detail,
        bottom_five=bottom_5,
        bottom_five_detail=bottom_5_detail,
        chart_html_sd_rp=chart_html_sd_rp,
        sd_rp_st=sd_rp_st,
        sd_rp_b=sd_rp_b,
        chart_html_b_rp=chart_html_b_rp,
        b_case_ms=b_case_ms,
        w_case_ms=w_case_ms,
        distribution_rp_chart=distribution_rp_chart,
        summary_mcs=summary_mcs
    )

    # pdf = pdfkit.from_string(output, 'output/output.pdf', configuration=config)
    # Print the rendered output
    with open("output/output.html", "w+") as f:
        f.write(output)
    # print(output)
