import pandas as pd
from openpyxl import Workbook
from datetime import timedelta
import streamlit as st
import openpyxl
from PIL import Image
import streamlit as st
import warnings


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
        Offers_dict = {'eb1':False,
                       'eb1 percentage':0,
                       'eb1 date':None,
                       'eb2':False,
                       'eb2 date':None,
                       'eb2 percentage':0,
                       'senior':False,
                       'senior percentage':0,
                       'long term':False,
                       'lt days':28,
                       'lt percentage':0,
                       'reduc1':False,
                       'reduc2':False,
                       'reduc1 percentage':0,
                       'reduc2 percentage':0}
        
        form_a = st.form("Offers")
        eb1 = False
        eb2 = False
        c11,c12 = form_a.columns([1,2])
        c21,c22,c23,c24 = form_a.columns([1,2,3,4])
        c31,c32 = form_a.columns([1,2])
        c41,c42,c43,c44 = form_a.columns([1,2,3,4])
        c51,c52 = form_a.columns([1,2])
        
        # checkboxes
        if 'Offers_dict' in st.session_state:
            Offers_dict = st.session_state["Offers_dict"]

        #eb1
        if "eb1" in st.session_state:
            eb1 =  c11.checkbox("Early booking 1",value=st.session_state['eb1'],key=1)
        else:
            eb1 =  c11.checkbox("Early booking 1",key=1)
                
        
        st.session_state["eb1"] = eb1
        if eb1:
            eb1_per = int(c11.text_input("eb1 percentage",Offers_dict['eb1 percentage'],key=3))
            eb1_date = c11.date_input("Early booking date",Offers_dict['eb1 date'])
            Offers_dict['eb1 percentage'] = eb1_per
            Offers_dict['eb1 date'] = eb1_date
            
        #eb2
        if "eb2" in st.session_state:
            eb2 =  c12.checkbox("Early booking 2",value=st.session_state['eb2'],key=4)
        else:
            eb2 =  c12.checkbox("Early booking 2",key=5)
                
        
        st.session_state["eb2"] = eb2
        if eb2:
            eb2_per = int(c12.text_input("eb2 percentage",Offers_dict['eb2 percentage'],key=6))
            eb2_date = c12.date_input("Early booking date",Offers_dict['eb2 date'],key=7)
            Offers_dict['eb2 percentage'] = eb2_per
            Offers_dict['eb2 date'] = eb2_date
            
        
        # senior
        if "senior" in st.session_state:
            senior =  c31.checkbox("senior",value=st.session_state["senior"],key=8)
        else:
            senior =  c31.checkbox("senior",key=8)
            
        
        st.session_state['senior'] = senior
        if senior:
            senior_per = int(c31.text_input("reduction percentage",Offers_dict['senior percentage'],key=10))
            Offers_dict['senior percentage'] = senior_per
            
            
        
        # long term
        if "lt" in st.session_state:
            lt =  c32.checkbox("Long term",value=st.session_state["lt"],key=11)
        else:
            lt =  c32.checkbox("long term",key=12)
        
        st.session_state['lt'] = lt
        if lt:
            lt_dats = int(c32.text_input("long term days",Offers_dict['lt days'],key=13))
            lt_per = int(c32.text_input("long term percentage",Offers_dict['lt percentage'],key=14))
            Offers_dict['lt days'] = lt_dats
            Offers_dict['lt percentage'] = lt_per
            
        # Another reduction 1
        if "reduc" in st.session_state:
            reduc =  c51.checkbox("another reduction 1",value=st.session_state["reduc"],key=15)
        else:
            reduc =  c51.checkbox("another reduction 1",key=16)
            
        st.session_state["reduc"] = reduc
        if reduc:
            reduc_per = int(c51.text_input("reduction percentage",Offers_dict['reduc1 percentage'],key=17))
            Offers_dict['reduc1 percentage'] = reduc_per
            
        
        # Another reduction 2
        if "reduc2" in st.session_state:
            reduc2 =  c52.checkbox("another reduction 2",value=st.session_state["reduc2"],key=18)
        else:
            reduc2 =  c52.checkbox("another reduction 2",key=19)
            
        st.session_state["reduc2"] = reduc2
        if reduc2:
            reduc2_per = int(c52.text_input("reduction 2 percentage",Offers_dict['reduc2 percentage'],key=20))
            Offers_dict['reduc2 percentage'] = reduc2_per
            
        
        submitted = form_a.form_submit_button()
        if submitted:
            st.experimental_rerun()
            
        # all
        Offers_dict['eb1'] = eb1
        Offers_dict['eb2'] = eb2
        Offers_dict['senior'] = senior
        Offers_dict['long term'] = lt
        Offers_dict['reduc1'] = reduc
        Offers_dict['reduc2'] = reduc2
        
        # st.write(Offers_dict)
        Combin_dict = {
        "senior_combin": False,
        "long term_combin": False,
        "reduction_combin": False,
        "reduction2_combin": False
        }
        st.session_state['Offers_dict'] = Offers_dict
        # Here we see if offers are combined or not
            
        selected = [senior,lt,reduc,reduc2]
        if (eb1) and any(selected):    
            form_c = st.form("Combinations")
            

            variables = {
                "senior": senior,
                "long term": lt,
                "reduction": reduc,
                "reduction2": reduc2
            }

            for var_name, value in variables.items():
                if value:
                    Combin_dict[str((var_name) + "_combin")] = form_c.checkbox("Early booking combined with " + var_name,key= str((var_name) + "_combin"))
            form_c.form_submit_button()
            st.session_state['Combin_dict'] = Combin_dict
            # st.write(Combin_dict)
else:
    
    st.markdown("""
                <h1 style='text-align: center; margin-bottom: 20px; color: #FFC107; font-family: "Roboto", sans-serif; font-size: 32px; font-weight: bold;'>
                Enter your password on the homepage to proceed.
                </h1>
            """, unsafe_allow_html=True
            )
