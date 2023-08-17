import yaml
from yaml.loader import SafeLoader
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title='Data Analysis',layout='wide')

with open('auth.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status == False:
    st.error('Access denied')
if authentication_status == None:
    st.warning('Please enter your username and password')
if authentication_status:
    authenticator.logout('Logout', 'main')
    if username == 'bses':
        st.write(f'Welcome *{name}*,')
        
    df = pd.read_csv('cleandata.csv')

    df.rename(columns = {'Sources':'Source'}, inplace = True)
    source_grp = pd.DataFrame(df.groupby(['Source']).size())
    source_grp.columns = ['No. of Reports']
    df['Date of Incident'] = pd.to_datetime(df['Date of Incident'],errors='coerce')
    time_source = df[['Date of Incident','Source']]
    time_source.dropna(inplace = True)  
    time_source['Date of Incident'] = time_source['Date of Incident'].dt.year
    ts = time_source.groupby(['Date of Incident', 'Source']).size().unstack(fill_value=0)
    ts = ts.loc[:,(ts[ts.columns].sum() > 19).values]
    type_grp = pd.DataFrame(df.groupby(['Type of Attack']).size())
    type_grp.reset_index(inplace=True)
    type_grp.columns = ['Type of Attack','No. of cases']
    attemp_grp = pd.DataFrame(df.groupby(['Attempted or Raped']).size())
    attemp_grp.reset_index(inplace = True)
    attemp_grp.columns = ['Attempted or Raped','No. of cases']
    col1,col2 = st.columns(2)
    fig_pie = px.pie(type_grp, values = 'No. of cases', names='Type of Attack',
                     title = '<span style="color:yellow">Pie chart showing Types of Attack</span>',width= 500,color_discrete_sequence=px.colors.qualitative.Bold)
    fig_pie.update_traces(textposition = "outside", hoverinfo = 'value' )
    fig_pie2 = px.pie(attemp_grp, values = 'No. of cases', names='Attempted or Raped',
                     title = '<span style="color:yellow">Pie chart showing category of attack</span>',width= 500,color_discrete_sequence=px.colors.qualitative.Bold)
    fig_pie2.update_traces(textposition = "outside", hoverinfo = 'value' )
    col1.plotly_chart(fig_pie)
    col2.plotly_chart(fig_pie2)
    st.write('''
    ### Sources

    Among various sources, we can first analyze the trend and pattern in which sources were highly active in covering the topic as well as which sources were more engaged over time.
    ''')
    
    fig = px.bar(source_grp, y = 'No. of Reports',
                color = 'No. of Reports', color_continuous_scale=px.colors.sequential.Sunsetdark,width=1000)
    fig.update_traces(width = 0.7)
    fig.update_layout(title_text="<span style='color:yellow'>Bar plot of Stories by Sources</span>")
    expander_1 = st.expander('Analysis -- Sources and Stories')
    expander_1.plotly_chart(fig)
    col1,col2 = expander_1.columns([0.38,0.62])
    col1.markdown('<p style = "color:Yellow"><b>Dataframe</b></p>',unsafe_allow_html=True)
    col1.dataframe(source_grp,width=380,height=420)
    col2.markdown('''
<p style = 'color:Yellow'><b>Analysis</b></p>
<p>The graph above clearly illustrates the primary data sources for reports on sexual violence in Nepal over time. Unquestionably, Nepal Police stands out as the most prominent contributor, providing a significantly higher number of reports compared to other sources.</p>
<p>Interestingly, INSECOnline, a human rights-focused news portal in Nepal, also holds a notable number of records related to rape incidents. 
On the other hand, while Nepal Monitor has a respectable collection of records in general, it falls short of its potential in addressing this critical issue. Given its role as a monitoring website dedicated to incidents in Nepal, one would expect it to lead the way in reporting such sensitive incidents.Among all the top news sources in Nepal, only three—'The Himalayan Times,' 'Ratopati,' and 'Online 
Khabar'—demonstrate a strong commitment to covering stories of sexual incidents in the country.</p>
<p> In summary, Nepal Police rightfully takes the lead in covering stories related to sexual violence in Nepal, while specialized sources like 'INSECOnline' and 'Nepal Monitor' are significantly ahead in reporting various incidents. This divergence might be attributed to the fact that general news sources have
a broader focus on all aspects of national events, whereas targeted news sources concentrate solely on human rights and incidents in Nepal.</p>
''',unsafe_allow_html=True)

    fig2 = px.line(ts, title = 'Line plot of Sources by time', color = 'Source', markers = True,width=850) #text="value")
    fig2.update_layout(xaxis = dict(showline=False,showgrid=False),xaxis_range = (2013,2022))
    fig2.update_traces(visible = 'legendonly')
    expander_2 = st.expander('Analysis -- Sources over Time')
    expander_2.markdown('<p style = "color:yellow">Click on legend to show the lines.</p>',unsafe_allow_html=True)
    expander_2.plotly_chart(fig2)