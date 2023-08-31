import pandas as pd
from openpyxl import Workbook
from datetime import timedelta
import streamlit as st
import openpyxl
from PIL import Image
import streamlit as st
import warnings

def spo_offers(i,spo_dict):
    eb1 = False
    eb2 = False    
    c11,c12 = st.columns([1,2])
    c21,c22,c23,c24 = st.columns([1,2,3,4])
    c31,c32 = st.columns([1,2])
    c41,c42,c43,c44 = st.columns([1,2,3,4])
    c51,c52 = st.columns([1,2])
        
    #eb1
    if "Offers_dict" in st.session_state:
        # st.write(st.session_state["Offers_dict"])
        Offers_dict = st.session_state['Offers_dict']
        eb1 =  c11.checkbox("Early booking 1",key=i*88,value=Offers_dict['eb1'])
        spo_dict['eb1'].append(eb1)
        
        if eb1:
            eb1_per = int(c11.text_input("eb1 percentage",Offers_dict['eb1 percentage'],key=(i+1)*100))
            eb1_date = c11.date_input("Early booking date",Offers_dict['eb1 date'],key=(i+1)*1532)
            Spo_dict['eb1 percentage'].append(eb1_per)
            Spo_dict['eb1 date'].append(eb1_date)
        else:
            Spo_dict['eb1 percentage'].append(0)
            Spo_dict['eb1 date'].append(None)
            
        #eb2
        eb2 =  c12.checkbox("Early booking 2",key=i+11,value=Offers_dict['eb2'])
        spo_dict['eb2'].append(eb2)
        
        if eb2:
            eb2_per = int(c12.text_input("eb2 percentage",Offers_dict['eb2 percentage'],key=(i+1)*101))
            eb2_date = c12.date_input("Early booking date",Offers_dict['eb2 date'],key=(i+1)*102)
            Spo_dict['eb2 percentage'].append(eb2_per)
            Spo_dict['eb2 date'].append(eb2_date)
        
        else:
            Spo_dict['eb2 percentage'].append(0)
            Spo_dict['eb2 date'].append(None)
            
        # senior
        senior =  c31.checkbox("senior",key=i+20,value=Offers_dict['senior'])
        spo_dict['senior'].append(senior)
        
        if senior:
            senior_per = int(c31.text_input("reduction percentage",Offers_dict['senior percentage'],key=(i+1)*103))
            Spo_dict['senior percentage'].append(senior_per)
        
        else:
            Spo_dict['senior percentage'].append(0) 
               
        # long term
        lt =  c32.checkbox("long term",key=i+30,value=Offers_dict['long term'])
        spo_dict['long term'].append(lt)
        
        if lt:
            lt_dats = int(c32.text_input("long term days",Offers_dict['lt days'],key=(i+1)*104))
            lt_per = int(c32.text_input("long term percentage",Offers_dict['lt percentage'],key=(i+1)*105))
            Spo_dict['lt days'].append(lt_dats)
            Spo_dict['lt percentage'].append(lt_per)
            
        else:
            Spo_dict['lt days'].append(0)
            Spo_dict['lt percentage'].append(0)
            
        # Another reduction 1
        reduc1 =  c51.checkbox("another reduction 1",key=i+40,value=Offers_dict['reduc1'])
        spo_dict['reduc1'].append(reduc1)
            
        if reduc1:
            reduc_per = int(c51.text_input("reduction percentage",Offers_dict['reduc1 percentage'],key=(i+1)*106))
            Spo_dict['reduc1 percentage'].append(reduc_per)
            
        else:
            Spo_dict['reduc1 percentage'].append(0)
            
        # Another reduction 2
        reduc2 =  c52.checkbox("another reduction 2",key=i+50,value=Offers_dict['reduc2'])
        spo_dict['reduc2'].append(reduc2)
        
        if reduc2:
            reduc2_per = int(c52.text_input("reduction 2 percentage",Offers_dict['reduc2 percentage'],key=(i+1)*107))
            Spo_dict['reduc2 percentage'].append(reduc2_per)
        
        else:
            Spo_dict['reduc2 percentage'].append(0)    
    else:
        eb1 =  c11.checkbox("Early booking 1",key=(i+1)*108)
        spo_dict['eb1'].append(eb1)
        
        if eb1:
            eb1_per = int(c11.text_input("eb1 percentage",0,key=(i+1)*109))
            eb1_date = c11.date_input("Early booking date",key = (i+1)*1500)
            Spo_dict['eb1 percentage'].append(eb1_per)
            Spo_dict['eb1 date'].append(eb1_date)
            
        else:
            Spo_dict['eb1 percentage'].append(0)
            Spo_dict['eb1 date'].append(None)
            
                
        #eb2
        eb2 =  c12.checkbox("Early booking 2",key=(i+1)*110)
        spo_dict['eb2'].append(eb2)
        
        if eb2:
            eb2_per = int(c12.text_input("eb2 percentage",0,key=(i+1)*111))
            eb2_date = c12.date_input("Early booking date",key=(i+1)*112)
            Spo_dict['eb2 percentage'].append(eb2_per)
            Spo_dict['eb2 date'].append(eb2_date)
            
        else:
            Spo_dict['eb2 percentage'].append(0)
            Spo_dict['eb2 date'].append(None)
            
        # senior
        senior =  c31.checkbox("senior",key=(i+1)*113)
        spo_dict['senior'].append(senior)
        
        if senior:
            senior_per = int(c31.text_input("reduction percentage",0,key=(i+1)*114))
            spo_dict['senior percentage'].append(senior_per)
            
        else:
            spo_dict['senior percentage'].append(0)
        
        # long term
        lt =  c32.checkbox("long term",key=(i+1)*115)
        spo_dict['long term'].append(lt)
        
        if lt:
            lt_dats = int(c32.text_input("long term days",28,key=(i+1)*313))
            lt_per = int(c32.text_input("long term percentage",0,key=(i+1)*314))
            spo_dict['lt days'].append(lt_dats)
            spo_dict['lt percentage'].append(lt_per)
            
        else:
            spo_dict['lt days'].append(0)
            spo_dict['lt percentage'].append(0)
            
        # Another reduction 1
        reduc1 =  c51.checkbox("another reduction 1",key=i*40)
        spo_dict['reduc1'].append(reduc1)
            
        if reduc1:
            reduc_per = int(c51.text_input("reduction percentage",0,key=(i+1)*17))
            spo_dict['reduc1 percentage'].append(reduc_per)
            
        else:
            spo_dict['reduc1 percentage'].append(0)
            
        # Another reduction 2
        reduc2 =  c52.checkbox("another reduction 2",key=(i+1)*5000)
        spo_dict['reduc2'].append(reduc2)
        
        if reduc2:
            reduc2_per = int(c52.text_input("reduction 2 percentage",0,key=(i+1)*200))
            spo_dict['reduc2 percentage'].append(reduc2_per)
            
        else:
            spo_dict['reduc2 percentage'].append(0)
            
            
    # st.write(spo_dict)
    
        

st.markdown("""
    <h1 style='text-align: center; margin-bottom: 30px;'>
    Account Receivable Invoice PRO
    </h1>
""", unsafe_allow_html=True
)
if "password" in st.session_state:
    if st.session_state["password"] != "0111@Jo":
        st.markdown("""
                <h1 style='text-align: center; margin-bottom: 20px; color: #FFC107; font-family: "Roboto", sans-serif; font-size: 32px; font-weight: bold;'>
                Enter your password on the homepage to proceed.
                </h1>
            """, unsafe_allow_html=True
            )

    else:
        if "sheet_names" not in st.session_state:
            st.markdown("""
                <h1 style='text-align: center; margin-bottom: 20px; color: #FFC107; font-family: "Roboto", sans-serif; font-size: 32px; font-weight: bold;'>
                Please insert the file first to proceed.
                </h1>
            """, unsafe_allow_html=True
            )
        else: 
            Spo_dict = {'name':list(),
                        'eb1':list(),
                        'eb1 percentage':list(),
                        'eb1 date':list(),
                        'eb2':list(),
                        'eb2 date':list(),
                        'eb2 percentage':list(),
                        'count':list(),
                        'SPO':list(),
                        'senior':list(),
                        'senior percentage':list(),                        
                        'long term':list(),
                        'lt days':list(),
                        'lt percentage':list(),
                        'reduc1':list(),
                        'reduc2':list(),
                        'reduc1 percentage':list(),
                        'reduc2 percentage':list(),
                        'start_date':list(),
                        'end_date':list()}
            
            sheet_names = st.session_state["sheet_names"]
            count = 0
            for i in range(100):
                Spo_number = "spo"+str(i)
                # name
                Spo_name = st.selectbox(
                    'Choose spo ' + str(i+1),
                    sheet_names, key=Spo_number)
                if Spo_name is None:
                    Spo_dict['count'] = count
                    break
                else:
                    count +=1
                Spo_dict['name'].append(Spo_name)
                
                # SPO
                SPO = pd.read_excel(st.session_state["uploaded file"],sheet_name=Spo_name)
                Spo_dict['SPO'].append(SPO)
                
                # date
                cl1, cl2 = st.columns([1,2])
                s_date = SPO["first date"][0]
                start_res = cl1.date_input("from",key="start"+str(i),value=s_date)
                Spo_dict['start_date'].append(start_res)
                
                e_date = SPO["second date"].dropna().iloc[-1]
                end_res = cl2.date_input("to",key="end"+str(i),value = e_date)
                Spo_dict['end_date'].append(end_res)
                
                # offers
                spo_offers(i,Spo_dict)
                
                
                st.divider()
                    
            st.session_state['Spo_dict'] = Spo_dict
            # st.write(Spo_dict)
        # form_Spo = st.form("Spo_Combinations")
        # st.write(statment)