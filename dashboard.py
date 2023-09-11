import yaml
from yaml.loader import SafeLoader
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title='Data Analysis',layout='wide')

with open('auth.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],    #kaile samma logout nagarne
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
    st.write(f'Welcome *{name}*,')
    st.markdown('<hr>',unsafe_allow_html=True)    
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

    p_age = pd.read_csv('P_age.csv')
    p_age.drop('P ',axis = 1, inplace=True)
    p_age.dropna(inplace=True)
    p_age['Age'] = p_age['Age'].astype('int')
    p_age['norm_1'] = (p_age['Age']//10)*10 
    p_age['norm_1'] = p_age['norm_1'].astype('int')
    p_age['norm_2'] = p_age['norm_1'] + 9
    p_age['norm_1'] = p_age['norm_1'].astype('str')
    p_age['norm_2'] = p_age['norm_2'].astype('str')
    p_age['norm_age'] = p_age['norm_1'] + ' - ' + p_age['norm_2']
    p_age.drop(['norm_1','norm_2'],axis = 1,inplace=True)

    age_p = pd.DataFrame(p_age.groupby('norm_age').size())
    age_p.columns = ['Total number']    
    age_p.reset_index(inplace=True)
    
    v_age = pd.read_csv('V_age.csv')
    v_age.drop('V',axis = 1, inplace=True)
    v_age.dropna(inplace=True)
    v_age['Age'] = v_age['Age'].astype('int')
    v_age['norm_1'] = (v_age['Age']//10)*10 
    v_age['norm_1'] = v_age['norm_1'].astype('int')
    v_age['norm_2'] = v_age['norm_1'] + 9
    v_age['norm_1'] = v_age['norm_1'].astype('str')
    v_age['norm_2'] = v_age['norm_2'].astype('str')
    v_age['norm_age'] = v_age['norm_1'] + ' - ' + v_age['norm_2']
    v_age.drop(['norm_1','norm_2'],axis = 1,inplace=True)   
    age_v = pd.DataFrame(v_age.groupby('norm_age').size())
    age_v.columns = ['Total number']
    age_v.reset_index(inplace=True)
    
    Time = pd.read_csv('Time.csv')
    Time.dropna(inplace=True)
    Time_1 = pd.read_csv("Time.csv", usecols = ['Time'])
    time_v = pd.DataFrame(Time_1.groupby('Time').size())
    time_v.columns = ['Total number']
    time_v.reset_index(inplace=True)
    time_v['etime'] = (time_v['Time'] + 1) % 24
    time_v['Time'] = time_v['Time'].astype('str') + ":00"
    time_v['etime'] = time_v['etime'].astype('str') +    ":00"
    time_v['norm_time'] = time_v['Time'] + " - " + time_v['etime']
    time_v.drop(['Time','etime'],axis = 1,inplace=True)

    Caste = pd.read_csv('Caste_Data.csv')
    Caste.dropna(inplace=True)
    Caste_1 = pd.read_csv("Caste_Data.csv", usecols = ['Ethnicity code'])
    Caste_v =  pd.DataFrame(Caste_1.groupby('Ethnicity code').size())
    Caste_v.columns = ['Total number']
    Caste_v.reset_index(inplace=True)

    caste_code = pd.read_csv('Caste_code.csv')

    dis = pd.read_csv('District.csv')
    dis.iloc[59,1] = 83.3789
    map = px.scatter_geo(dis, lat='Latitude', lon='Longitude',width = 500, opacity = 0.3,template='plotly_dark',
                     hover_name='Districts',color='Number', size='Number',
                     title='<span style="color:blue">Incidents in Nepal</span>', color_continuous_scale=px.colors.sequential.Sunsetdark)
    map.update_layout(geo = dict(scope = 'asia',resolution = 50,lataxis_range =[25,32],lonaxis_range = [78,90]),margin={"r":0,"t":25,"l":0,"b":0})
    col1,col2 = st.columns(2)
    col1.plotly_chart(map)
    col2.markdown('''
<p style = 'color:#EA7371'><b>Abstract</b></p>
<p>This report offers a comprehensive visual analysis of sexual-related cases in Nepal, shedding light on the nature, location, timing, and sources of these incidents. Through meticulously crafted pie charts and scatter plots, we examine various facets of these cases, aiming to provide a deeper understanding of this critical issue.
The report delves into the types of sexual attacks that have occurred, categorizing them to reveal patterns and trends. By mapping the geographical distribution of these events, we uncover insights into where they have taken place, offering valuable information for policymakers, law enforcement, and advocacy groups.
In addition, we dissect the times at which they occurred. This temporal analysis can help stakeholders allocate resources more effectively and implement preventive measures during high-risk periods.
Furthermore, the report investigates the sources of data on sexual-related cases, including news outlets and other organizations that collect and store this information.<br> Overall, this report serves as a visual resource to facilitate a data-driven approach to addressing sexual-related cases in Nepal.</p>
''',unsafe_allow_html=True)
    fig_pie = px.pie(type_grp, values = 'No. of cases', names='Type of Attack',
                     title = '<span style="color:#EA7371">Pie chart showing attack categories.</span>',width= 500,color_discrete_sequence=px.colors.qualitative.Bold)
    fig_pie.update_traces(textposition = "outside", hoverinfo = 'value' )
    fig_pie2 = px.pie(attemp_grp, values = 'No. of cases', names='Attempted or Raped',
                     title = '<span style="color:#EA7371">Pie chart showing the types of attack.</span>',width= 500,color_discrete_sequence=px.colors.qualitative.Bold)
    fig_pie2.update_traces(textposition = "outside", hoverinfo = 'value' )
    fig_pie3 = px.pie(age_p, values = 'Total number', names='norm_age',
                     title = '<span style="color:#EA7371">Pie chart showing perputator age groups.</span>',width= 500,color_discrete_sequence=px.colors.qualitative.Bold)
    fig_pie3.update_traces(textposition = "outside", hoverinfo = 'value')
    fig_pie3.update_layout(legend_title = 'Age groups')
    fig_pie4 = px.pie(age_v, values = 'Total number', names='norm_age',
                     title = '<span style="color:#EA7371">Pie chart showing victim age groups.</span>',width= 500,color_discrete_sequence=px.colors.qualitative.Bold)
    fig_pie4.update_traces(textposition = "outside", hoverinfo = 'value' )
    fig_pie4.update_layout(legend_title = 'Age groups',)
    fig_pie5 = px.pie(time_v, values = 'Total number', names='norm_time',
                     title = '<span style="color:#EA7371">Pie chart showing the time of attack.</span>',width=500,color_discrete_sequence=px.colors.qualitative.Bold)
    fig_pie5.update_traces(textposition = "outside", hoverinfo = 'value' )
    fig_pie5.update_layout(margin={"r":120,"t":80,"l":72,"b":120})
    fig_pie6 = px.pie(Caste_v, values = 'Total number', names='Ethnicity code',
                     title = '<span style="color:#EA7371">Pie chart showing ethnicity of perpetrator.</span>',width= 500,color_discrete_sequence=px.colors.qualitative.Bold)
    fig_pie6.update_traces(textposition = "outside", hoverinfo = 'value' )

    col1.plotly_chart(fig_pie)
    col2.plotly_chart(fig_pie2)
    col1.plotly_chart(fig_pie3)
    col2.plotly_chart(fig_pie4)
    col1.plotly_chart(fig_pie5)
    col2.plotly_chart(fig_pie6)
    expan = st.expander('Ethnicity codes')
    expan.dataframe(caste_code,width=550)
    st.markdown('''
    ### <span style = 'color:#EA7371'>Sources</span>

    Among various sources, we can first analyze the trend and pattern in which sources were highly active in covering the topic as well as which sources were more engaged over time.
    ''',unsafe_allow_html=True)
    
    fig_bar = px.bar(source_grp, y = 'No. of Reports',
                color = 'No. of Reports', color_continuous_scale=px.colors.sequential.Sunsetdark,width=1000)
    fig_bar.update_traces(width = 0.7)
    fig_bar.update_layout(title_text="<span style='color:#EA7371'>Bar plot of Stories by Sources</span>")
    expander_1 = st.expander('Analysis -- Sources and Stories')
    expander_1.plotly_chart(fig_bar)
    col1,col2 = expander_1.columns([0.38,0.62])
    col1.markdown('<p style = "color:#EA7371"><b>Dataframe</b></p>',unsafe_allow_html=True)
    col1.dataframe(source_grp,width=380,height=420)
    col2.markdown('''
<p style = 'color:#EA7371'><b>Analysis</b></p>
<p>The graph above clearly illustrates the primary data sources for reports on sexual violence in Nepal over time. Unquestionably, Nepal Police stands out as the most prominent contributor, providing a significantly higher number of reports compared to other sources.</p>
<p>Interestingly, INSECOnline, a human rights-focused news portal in Nepal, also holds a notable number of records related to rape incidents. 
On the other hand, while Nepal Monitor has a respectable collection of records in general, it falls short of its potential in addressing this critical issue. Given its role as a monitoring website dedicated to incidents in Nepal, one would expect it to lead the way in reporting such sensitive incidents.Among all the top news sources in Nepal, only three—'The Himalayan Times,' 'Ratopati,' and 'Online 
Khabar'—demonstrate a strong commitment to covering stories of sexual incidents in the country.</p>
<p> In summary, Nepal Police rightfully takes the lead in covering stories related to sexual violence in Nepal, while specialized sources like 'INSECOnline' and 'Nepal Monitor' are significantly ahead in reporting various incidents. This divergence might be attributed to the fact that general news sources have
a broader focus on all aspects of national events, whereas targeted news sources concentrate solely on human rights and incidents in Nepal.</p>
''',unsafe_allow_html=True)

    fig_line = px.line(ts, title = 'Line plot of Sources by time', color = 'Source', markers = True,width=850) #text="value")
    fig_line.update_layout(xaxis = dict(showline=False,showgrid=False),xaxis_range = (2013,2022))
    expander_2 = st.expander('Analysis -- Sources over Time')
    expander_2.markdown('<p style = "color:#EA7371">Click on legend to show the lines.</p>',unsafe_allow_html=True)
    expander_2.plotly_chart(fig_line)
    expander_2.markdown('''
<p style = 'color:#EA7371'><b>Analysis</b></p>
<p>The line plot represents the coverage of news sources related to sexual assaults over a span of ten years, from 2013 to 2022, with time (years) on the x-axis and the number of records covered by various news sources on the y-axis. The plot provides valuable insights into the trends and patterns in media reporting on sexual assault incidents in Nepal.</p>
<p>At the outset, it is evident that the data reveals distinct trends for different news sources. The Nepal Police exhibits a notable peak in coverage in the year 2020, suggesting that this was a year when sexual assault incidents were prominently covered and reported by this source. However, this peak is followed by a consistent decrease in coverage in the subsequent years, indicating a potential decline in the frequency of reported incidents or a shift in the focus of the Nepal Police's reporting.</p>
<p>Another significant contributor to the coverage of sexual assault incidents is INSECOnline. The data highlights a rising trend in coverage from the base year of 2013, reaching its peak around 2021. This indicates that INSECOnline's reporting gained momentum over the years, culminating in a substantial amount of coverage in 2021. However, a slight decrease in coverage is observed in the following year (2022), suggesting a potential change in reporting strategies or a fluctuation in the incidence of sexual assault cases.</p>
<p>In contrast, Nepal Monitor starts off with relatively passive coverage until 2019. However, the data illustrates an upward trend in coverage from 2019 onwards. This upward trajectory indicates an increased emphasis on reporting sexual assault incidents by Nepal Monitor in recent years, possibly due to shifting societal awareness or changes in their reporting methodologies.</p>
<p>The analysis also identifies other news sources that appear to maintain a more consistent or passive level of coverage throughout the ten-year period. These sources might indicate a stable approach to reporting sexual assault incidents or might reflect the lack of significant changes in their reporting strategies over the years.</p>
<p>Overall, the line plot demonstrates the dynamic nature of media reporting on sexual assault incidents in Nepal. Peaks and troughs in coverage from different news sources reflect shifts in priorities, societal awareness, and reporting methodologies. The analysis highlights the importance of considering multiple news sources to gain a comprehensive understanding of trends in sexual assault reporting and to identify potential changes in the prevalence of such incidents over time. Further exploration of contextual factors and correlations with real-world events could provide deeper insights into the patterns observed in the line plot.</p>
''',unsafe_allow_html=True)
    
    st.markdown('''
    ### <span style = 'color:#EA7371'>Consequences of the attack</span>

    Among all the districts, we can analyze the trend and pattern which districts were highly prone to which consequences.
    ''',unsafe_allow_html=True)
    district_grp = pd.DataFrame(df.groupby(['Districts']).size())
    district_grp.columns = ['No. of Incidents']
    cons_grp = pd.DataFrame(df.groupby(['Districts','Consequences of the attack']).size().unstack(fill_value=0))
    fig = px.bar(cons_grp, title = 'Bar plot of occurence of consequences',
             color = 'Consequences of the attack', color_discrete_sequence=['Black','Blue','Green',px.colors.qualitative.T10[5],'Red'],width=1000)
    fig.update_traces(width = 0.7)
    fig.update_layout(title_text="<span style='color:#EA7371'>Bar plot of Consequences of attack</span>")
    expander_1 = st.expander('Analysis -- Occurence of Consequences')
    expander_1.plotly_chart(fig)
    col1,col2 = expander_1.columns([0.38,0.62])
    col1.markdown('<p style = "color:#EA7371"><b>Dataframe</b></p>',unsafe_allow_html=True)
    col1.dataframe(district_grp,width=380,height=420)
    col2.markdown('''
<p style = 'color:#EA7371'><b>Analysis</b></p>
<p>From the bar graph above representing the consequences,we observe that the highest rate of occurrence is attributed to "physical injury".
   This indicates that survivors most commonly experience physical harm as a consequence of the crime,underlining the immediate and tangible 
   impact on their well-being.In Kathmandu,the prevalence of consequences resulting from the data set is highest, with a notable emphasis on "Physical Injury"(almost no other consequences).</p>
<p> As of the current data, the districts of Manang and Rukum exhibit the lowest incidence of consequences arising from rape compared to the others.</p>
<p>Survivors often experience significant psychological and emotional trauma. Common psychological consequences include mental illness,anxiety, depression, post-traumatic stress disorder (PTSD),
    feelings of shame, guilt, fear, and self-blame. The emotional impact can be long-lasting and may require therapy and counseling for healing.And for this,Morang stands out as a district warranting attention.
     Similarly , we can observe other consequences in districts from the graph.</p>                               
''',unsafe_allow_html=True)
    df['Date of Incident'] = pd.to_datetime(df['Date of Incident'])
    time_source = df[['Date of Incident','Districts']]
    time_source.dropna(inplace = True)  
    time_source['Date of Incident'] = time_source['Date of Incident'].dt.year
    ts = time_source.groupby(['Date of Incident', 'Districts']).size().unstack(fill_value=0)
    ts = ts.loc[:,(ts[ts.columns].sum() > 70).values]
    fig_lin = px.line(ts, title = 'Line plot of Districts by time', color = 'Districts', markers = True,width=850) #text="value")
    fig_lin.update_layout(xaxis = dict(showline=False,showgrid=False),xaxis_range = (2013,2022))
    expander_2 = st.expander('Analysis -- Districts over Time')
   # expander_2.markdown('<p style = "color:yellow">Click on legend to show the lines.</p>',unsafe_allow_html=True)
   # expander_2.plotly_chart(fig_lin)
   # col1,col2 = expander_1.columns([0.38,0.62])
   # col1.markdown('<p style = "color:Yellow"><b>Dataframe</b></p>',unsafe_allow_html=True)
    #col1.dataframe(district_grp,width=380,height=420)
    fig_line = px.line(ts, title = 'Line plot of Districts by time', color = 'Districts', markers = True,width=850) #text="value")
    fig_line.update_layout(xaxis = dict(showline=False,showgrid=False),xaxis_range = (2013,2022))
    expander_2 = st.expander('Analysis -- Districts over Time')
    expander_2.markdown('<p style = "color:#EA7371">Click on legend to show the lines.</p>',unsafe_allow_html=True)
    expander_2.plotly_chart(fig_line)
    expander_2.markdown('''
<p style = 'color:#EA7371'><b>Analysis</b></p>
<p>The line plot represents the distribution of incidents across different districts over time.It shows how the frequency of incidents has evolved over time.It allows us to identify periods of increased or decreased incident rates,highlighting potential trends and patters.</p>
<p>In the vast tapestry of incident data,Kathmandu emerges as an undeniable focal point,adorned with the highest number of incidents,Kathmandu's data commands attention with its significant and imposing presence.Kathmandu's prominence serves as a potential call to action,urging us to channel our energis towards creating a safer,healthier and more secure environment for all.</p>
<p>Before the year 2021, Dang's incident data was unpredictable,with the number of incident going up and down without a clear pattern.The number of incident in Dang increased significantly,reaching the highest point ever recorded..</p>
<p>The number of incidents in Rupanehi was going up rapidlyBut in 2020, there was a decrease in incident,providing some relief.However after that the incidents started rising again.</p>
<p>The data from Silyan creates an intriguing pattern-despite having fewer cases compared to districts like Kathmandu, the incident counts in Silyan remains steady or show an upward trend.</p>
<p>In conclusion,the data analysis reveals that Kathmandu has consistently high cases of incidents,which is a cause for concern.The steady trend of incidents indicates a persistent issue that demands urgent attention and effective interventions to ensure the safety.</p>                       
''',unsafe_allow_html=True)
    st.markdown('''
    #### <span style = 'color:#EA7371'>Time of attack</span>
    Among all the time durations, we can observe the time patterns at which the events are likely occuring.
    ''',unsafe_allow_html=True)
    df_v1= pd.DataFrame(Time.groupby('District').size())
    df_v1.columns = ['Total number']
    df2= df_v1.sort_values(by='Total number',ascending = False)
    df3 = df2.head(20)
    d_is =list(df3.index)
    df4=Time[Time['District'].isin(d_is)]
    fig = px.scatter(df4, x="District", y="Time",color='Time',color_continuous_scale=px.colors.sequential.Sunsetdark,width = 1000)
    expander_3 = st.expander('Analysis -- Time by District')
    expander_3.markdown('*Here, for e.g. time = 3 denotes the time duration from 3 to 4*')
    expander_3.plotly_chart(fig)
    expander_3.markdown('''
<p style = 'color:#EA7371'><b>Analysis</b></p>
<p>In our examination of incident data across various districts, a conspicuous pattern emerges, shedding light on the times when most incidents tend to occur. Two key timeframes consistently stand out as being particularly noteworthy in terms of incident frequency.</p>
<p>2-3 AM:In almost every district under scrutiny, the period between 2 AM and 3 AM emerges as the peak time for incidents. This late-night to early-morning hour appears to be associated with a heightened risk of various events. The reasons behind this phenomenon could be multifaceted, including reduced visibility, lower presence of individuals, and potentially altered social dynamics.</p>
<p>13-14 (1 PM - 2 PM):Another time of increased incident occurrence across the surveyed districts is between 1 PM and 2 PM, notably in contrast to the early morning lull around 5 AM - 6 AM. This suggests that, for some reason, the early afternoon presents its own set of challenges or risk factors that contribute to incidents. Perhaps factors related to daily routines or social interactions play a role during this timeframe.</p>
<p> However, it is important to note that there is significant variation when we delve into district-specific data. In the case of Kathmandu, for instance, a different pattern emerges. Incidents in Kathmandu appear to peak between 10 AM and 3 PM, with the highest concentration of incidents occurring from 10 PM to 11 PM.</p>
''',unsafe_allow_html=True)       

    st.markdown('''
### <span style = 'color:#EA7371'>Conclusion</span>
<p>In summation, our analysis reveals compelling insights into the landscape of sexual-related cases in Nepal. Terai emerges as the epicenter of these incidents, registering the highest number of cases, while sexual assault remains the predominant form of abuse reported. Delving into the temporal dimension, patterns emerge, with 02:00 am appearing as a peak time for perpetrators, whereas particularly in the Kathmandu valley it is during the afternoon. The repercussions of these incidents are substantial, with physical injuries and a notable number of pregnancy cases being prevalent consequences.
</p><p>To combat this troubling trend, we propose several proactive measures. Firstly, the allocation of security personnel during these active time periods could enhance public safety. Secondly, organizing self-defense training programs in areas with a high incidents of physical injuries can empower potential victims to protect themselves. Finally, recognizing the significance of safe abortion services, especially in regions where pregnancy is a pronounced consequence, can provide essential support and care to those affected.
</p><p>In conclusion, our findings underscore the urgency of addressing sexual-related cases in Nepal through a multifaceted approach that combines preventative measures, community support, and timely interventions to protect the well-being of individuals and the broader society.
           </p> ''',unsafe_allow_html=True)                                      
