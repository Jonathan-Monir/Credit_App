    
import json
import pandas as pd
from openpyxl import Workbook
from datetime import timedelta
import streamlit as st
import openpyxl
from PIL import Image
import streamlit as st
import warnings
import datetime
current_date = datetime.date.today()
formatted_date = current_date.strftime('%d-%m-%Y')

dd = ''.join(formatted_date.split('-')[:2])
ps = dd +"@0111Jo"

st.markdown("""
    <h1 style='text-align: center; margin-bottom: 30px;'>
    Account Receivable Invoice PRO
    </h1>
""", unsafe_allow_html=True
)
def convert_dates_to_strings(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_dates_to_strings(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = convert_dates_to_strings(data[i])
    elif isinstance(data, datetime.date) or isinstance(data, datetime.datetime):
        return data.strftime("%Y-%m-%d %H:%M:%S")  # Customize the format as needed
    return data

def remove_spo_key(d):
    for key in list(d.keys()):
        for sub_key in list(d[key].keys()):
            if sub_key == "SPO":
                del d[key][sub_key] 
    return d

if "password" in st.session_state:
    if st.session_state["password"] != ps:
        st.markdown("""
                <h1 style='text-align: center; margin-bottom: 20px; color: #FFC107; font-family: "Roboto", sans-serif; font-size: 32px; font-weight: bold;'>
                Enter your password on the homepage to proceed.
                </h1>
            """, unsafe_allow_html=True
            )

    else:
        import json  # Import the json module

        
        
        
        file_path = "reductions.json"
        #loading files
        try:
            with open(file_path, 'r') as json_file:
                # Attempt to load the JSON content
                try:
                    load_dict = json.load(json_file)
                    # Check if the loaded data structure is not empty
                    if load_dict:
                        red_dict = load_dict
                    else:
                        red_dict = dict()
                except json.JSONDecodeError as e:
                    red_dict = dict()
        except FileNotFoundError:
            pass
        except Exception as e:
            pass
        
        file_path = "combinations.json"
        #loading files
        try:
            with open(file_path, 'r') as json_file:
                # Attempt to load the JSON content
                try:
                    load_dict = json.load(json_file)
                    # Check if the loaded data structure is not empty
                    if load_dict:
                        com_dict = load_dict
                    else:
                        com_dict = dict()
                except json.JSONDecodeError as e:
                    com_dict = dict()
        except FileNotFoundError:
            pass
        except Exception as e:
            pass
            
            
            
        file_path = "spo.json"
        
        
        try:
            with open(file_path, 'r') as json_file:
                # Attempt to load the JSON content
                try:
                    load_dict = json.load(json_file)
                    # Check if the loaded data structure is not empty
                    if load_dict:
                        s_dict = load_dict
                        
                    else:
                        s_dict = dict()
                        
                except json.JSONDecodeError as e:
                    s_dict = dict()
                    
        except FileNotFoundError:
            pass
        except Exception as e:
            pass
            
    
        file_path = "extra.json"
        
        
        try:
            with open(file_path, 'r') as json_file:
                # Attempt to load the JSON content
                try:
                    load_dict = json.load(json_file)
                    # Check if the loaded data structure is not empty
                    if load_dict:
                        e_dict = load_dict
                    else:
                        e_dict = dict()
                except json.JSONDecodeError as e:
                    e_dict = dict()
        except FileNotFoundError:
            pass
        except Exception as e:
            pass

        def delete_dictionary_from_json(file_path, key_to_delete):
            try:
                # Step 1: Read the JSON file into a Python data structure
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
            except FileNotFoundError:
                return False

            # Step 2: Remove the dictionary or key-value pair you want to delete
            if key_to_delete in data:
                del data[key_to_delete]
            else:
                return False

            # Step 3: Write the updated data structure back to the JSON file
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            return True

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
        st.session_state["Offers_dict_None"] = Offers_dict
        red_dict[None] = Offers_dict.copy()
        if "null" in s_dict.keys():
            delete_dictionary_from_json('spo.json','null')
            del s_dict['null']
            
        if "null" in red_dict.keys():
            delete_dictionary_from_json('reductions.json','null')
            del red_dict['null']
        selected_setting = st.selectbox("select the setting you want to use.",options=red_dict.keys(), index= len(red_dict)-1)
        if selected_setting is not None:
            delete = st.button("delete costum")
            if delete:
                delete_dictionary_from_json("spo.json",selected_setting)
                delete_dictionary_from_json("reductions.json",selected_setting)
                delete_dictionary_from_json("extra.json",selected_setting)
                delete_dictionary_from_json("combinations.json",selected_setting)
                del red_dict[selected_setting]
                del s_dict[selected_setting]
                del e_dict[selected_setting]
                del com_dict[selected_setting]
                selected_setting = None
                st.experimental_rerun()
        old_file_dict = red_dict
        
           
        column1,column2 = st.columns([1,3.5])
                
        # Recuctions
        column1.markdown("""
                <h1 style='text-align: center; margin-bottom: 0px; font-family: "Roboto", sans-serif; font-size: 25px; font-weight: bold;'>
                Discounts
                </h1>
            """, unsafe_allow_html=True
            )
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
            st.session_state['Offers_dict'] = Offers_dict     
                   
        if 'Offers_dict' in st.session_state:
            Offers_dict = st.session_state["Offers_dict"]
        if 'new offers' in st.session_state:
            Offers_dict = st.session_state['new offers']
            Offers_dict['eb1 date'] = pd.to_datetime(Offers_dict['eb1 date'])
            Offers_dict['eb2 date'] = pd.to_datetime(Offers_dict['eb2 date'])
        if selected_setting is not None:
            Offers_dict = red_dict[selected_setting]
            None_file_dict = red_dict[selected_setting]
        #eb1
        if selected_setting is not None:
            eb1 =  c11.checkbox("Early booking 1",value=Offers_dict['eb1'],key=1)
        elif "eb1" in st.session_state:
            eb1 =  c11.checkbox("Early booking 1",value=st.session_state['eb1'],key=1)
        else:
            eb1 =  c11.checkbox("Early booking 1",key=1)
                
        
        st.session_state["eb1"] = eb1
        if eb1:
            eb1_per = int(c11.text_input("eb1 percentage",Offers_dict['eb1 percentage'],key=3))
            eb1_date = c11.date_input("Early booking date",pd.to_datetime(Offers_dict['eb1 date']))
            Offers_dict['eb1 percentage'] = eb1_per
            Offers_dict['eb1 date'] = eb1_date
            
        #eb2
        if selected_setting is not None:
            eb2 =  c12.checkbox("Early booking 2",value=Offers_dict['eb2'],key=4)
        elif "eb2" in st.session_state:
            eb2 =  c12.checkbox("Early booking 2",value=st.session_state['eb2'],key=4)
        else:
            eb2 =  c12.checkbox("Early booking 2",key=5)
                
        
        st.session_state["eb2"] = eb2
        if eb2:
            eb2_per = int(c12.text_input("eb2 percentage",Offers_dict['eb2 percentage'],key=6))
            eb2_date = c12.date_input("Early booking date",pd.to_datetime(Offers_dict['eb2 date']),key=7)
            Offers_dict['eb2 percentage'] = eb2_per
            Offers_dict['eb2 date'] = eb2_date
            
        
        # senior
        if selected_setting is not None:
            senior =  c31.checkbox("senior",value=Offers_dict['senior'],key=8)
        elif "senior" in st.session_state:
            senior =  c31.checkbox("senior",value=st.session_state["senior"],key=8)
        else:
            senior =  c31.checkbox("senior",key=8)
            
        
        st.session_state['senior'] = senior
        if senior:
            senior_per = int(c31.text_input("reduction percentage",Offers_dict['senior percentage'],key=10))
            Offers_dict['senior percentage'] = senior_per
            
            
        
        # long term
        if selected_setting is not None:
            lt =  c32.checkbox("Long term",value=Offers_dict['long term'],key=11)
        elif "lt" in st.session_state:
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
        if selected_setting is not None:
            reduc =  c51.checkbox("another reduction 1",value=Offers_dict['reduc1'],key=15)
        elif "reduc" in st.session_state:
            reduc =  c51.checkbox("another reduction 1",value=st.session_state["reduc"],key=15)
        else:
            reduc =  c51.checkbox("another reduction 1",key=16)
            
        st.session_state["reduc"] = reduc
        if reduc:
            reduc_per = int(c51.text_input("reduction percentage",Offers_dict['reduc1 percentage'],key=17))
            Offers_dict['reduc1 percentage'] = reduc_per
            
        
        # Another reduction 2
        if selected_setting is not None:
            reduc2 =  c52.checkbox("another reduction 2",value=Offers_dict['reduc2'],key=18)
        elif "reduc2" in st.session_state:
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
        combination = {
        "senior_combin": False,
        "long term_combin": False,
        "reduction_combin": False,
        "reduction2_combin": False
        }
        # if 'Combin_dict' in st.session_state:
        #     Combin_dict = st.session_state['Combin_dict']
            
    
        Combin_dict = {
        "senior_combin": False,
        "long term_combin": False,
        "reduction_combin": False,
        "reduction2_combin": False
        }
        # Here we see if offers are combined or not
            
        variables = {
            "senior": senior,
            "long term": lt,
            "reduction": reduc,
            "reduction2": reduc2
        }
        if selected_setting is not None:
            Combin_dict = com_dict[selected_setting]

        selected = [senior,lt,reduc,reduc2]
        if (eb1) and any(selected):    
            "***"
            column1,column2 = st.columns([1,3])
                
            # Combinations
            column1.markdown("""
                    <h1 style='text-align: center; margin-bottom: 0px; font-family: "Roboto", sans-serif; font-size: 25px; font-weight: bold;'>
                    Combinations
                    </h1>
                """, unsafe_allow_html=True
                )
            form_c = st.form("Combinations")
            

            for var_name, value in variables.items():
                if value:
                    if selected_setting is not None:
                        combination[str((var_name) + "_combin")] = form_c.checkbox("Early booking combined with " + var_name,key= str((var_name) + "hh"),value = Combin_dict[str((var_name) + "_combin")])
                    elif "combination" in st.session_state:
                        combination[str((var_name) + "_combin")] = form_c.checkbox("Early booking combined with " + var_name,key= str((var_name) + "hh"),value = st.session_state['combination'][str((var_name) + "_combin")])
                    else:
                        combination[str((var_name) + "_combin")] = form_c.checkbox("Early booking combined with " + var_name,key= str((var_name) + "hh"))
                else:
                    combination[str((var_name) + "_combin")] = False
                st.session_state['combination'][str((var_name) + "_combin")] = combination
                    
            form_c.form_submit_button()
        st.session_state['combination'] = combination
        st.session_state['Combin_dict'] = combination
        st.session_state['Offers_dict'] = Offers_dict
            
            
            
            
        "***"    
        # SPO *******************************************************************
        
        column1,column2 = st.columns([1,3])
                
        # Special Offers
        column1.markdown("""
                <h1 style='text-align: center; margin-bottom: 0px; font-family: "Roboto", sans-serif; font-size: 25px; font-weight: bold;'>
                Special Offers
                </h1>
            """, unsafe_allow_html=True
            )
        
        def spo_offers(i,Spo_dict,old,Offers_dict):
            eb1 = False
            eb2 = False    
            c11,c12 = st.columns([1,2])
            c21,c22,c23,c24 = st.columns([1,2,3,4])
            c31,c32 = st.columns([1,2])
            c41,c42,c43,c44 = st.columns([1,2,3,4])
            c51,c52 = st.columns([1,2])
                
            
            
            #eb1
            if "Offers_dict" in st.session_state:
                spo_def_dict = Spo_dict.copy()
                if selected_setting is None:
                    for key, value in Offers_dict.items():
                        try:
                            spo_def_dict[key][i] = value
                        except:
                            spo_def_dict[key].append(value)
                            
                    # spo_def_dict = Offers_dict
                eb1 =  c11.checkbox("Early booking 1",key=i*8885,value=spo_def_dict['eb1'][i])
                if not old:
                    Spo_dict['eb1'].append(eb1)
                else:
                    Spo_dict['eb1'][i] = (eb1)
                if eb1:
                    
                    eb1_per = float(c11.text_input("eb1 percentage",spo_def_dict['eb1 percentage'][i],key=(i+1)*25100))
                    eb1_date = c11.date_input("Early booking date",pd.to_datetime(spo_def_dict['eb1 date'][i]),key=(i+1)*1532)
                    if not old:
                        Spo_dict['eb1 percentage'].append(eb1_per)
                        Spo_dict['eb1 date'].append(eb1_date)
                    else:
                        Spo_dict['eb1 percentage'][i] = (eb1_per)
                        Spo_dict['eb1 date'][i] = (eb1_date)
                else:
                    if not old:
                        Spo_dict['eb1 percentage'].append(0)
                        Spo_dict['eb1 date'].append(None)
                    else:
                        Spo_dict['eb1 percentage'][i] = (0)
                        Spo_dict['eb1 date'][i] = (None)
                    
                #eb2
                eb2 =  c12.checkbox("Early booking 2",key=i+11020,value=spo_def_dict['eb2'][i])
                
                if not old:
                    Spo_dict['eb2'].append(eb2)
                else:
                    Spo_dict['eb2'][i] = (eb2)
                    
                if eb2:
                    eb2_per = float(c12.text_input("eb2 percentage",spo_def_dict['eb2 percentage'][i],key=(i+1)*101))
                    eb2_date = c12.date_input("Early booking date",pd.to_datetime(spo_def_dict['eb2 date'][i]),key=(i+1)*102)
                    if not old:
                        Spo_dict['eb2 percentage'].append(eb2_per)
                        Spo_dict['eb2 date'].append(eb2_date)

                    else:
                        Spo_dict['eb2 percentage'][i] = (eb2_per)
                        Spo_dict['eb2 date'][i] = (eb2_date)
                        
                else:
                    if not old:
                        Spo_dict['eb2 percentage'].append(0)
                        Spo_dict['eb2 date'].append(None)

                    else:
                        Spo_dict['eb2 percentage'][i] = (0)
                        Spo_dict['eb2 date'][i] = (None)
                            
                # senior
                senior =  c31.checkbox("senior",key=i+20242,value=spo_def_dict['senior'][i])
                if not old:
                    Spo_dict['senior'].append(senior)

                else:
                    Spo_dict['senior'][i] = (senior)
                
                if senior:
                    senior_per = float(c31.text_input("reduction percentage",spo_def_dict['senior percentage'][i],key=(i+1)*103))
                    if not old:
                        Spo_dict['senior percentage'].append(senior_per)

                    else:
                        Spo_dict['senior percentage'][i] = (senior_per)
                
                else:
                    if not old:
                        Spo_dict['senior percentage'].append(0)

                    else:
                        Spo_dict['senior percentage'][i] = (0) 
                    
                # long term
                lt =  c32.checkbox("long term",key=i+8930,value=spo_def_dict['long term'][i])
                if not old:
                    Spo_dict['long term'].append(lt)

                else:
                    Spo_dict['long term'][i] = (lt)
                
                if lt:
                    lt_dats = int(c32.text_input("long term days",spo_def_dict['lt days'][i],key=(i+1)*104))
                    lt_per = float(c32.text_input("long term percentage",spo_def_dict['lt percentage'][i],key=(i+1)*105))
                    if not old:
                        Spo_dict['lt days'].append(lt_dats)
                        Spo_dict['lt percentage'].append(lt_per)

                    else:
                        Spo_dict['lt days'][i] = (lt_dats)
                        Spo_dict['lt percentage'][i] = (lt_per)
                    
                else:
                    if not old:
                        Spo_dict['lt days'].append(0)
                        Spo_dict['lt percentage'].append(0)

                    else:
                        Spo_dict['lt days'][i] = (0)
                        Spo_dict['lt percentage'][i] = (0)
                    
                # Another reduction 1
                reduc1 =  c51.checkbox("another reduction 1",key=i+401313,value=spo_def_dict['reduc1'][i])
                if not old:
                    Spo_dict['reduc1'].append(reduc1)

                else:
                    Spo_dict['reduc1'][i] = (reduc1)
                    
                if reduc1:
                    reduc_per = float(c51.text_input("reduction percentage",spo_def_dict['reduc1 percentage'][i],key=(i+1)*106))
                    if not old:
                        Spo_dict['reduc1 percentage'].append(reduc_per)

                    else:
                        Spo_dict['reduc1 percentage'][i] = (reduc_per)
                    
                else:
                    if not old:
                        Spo_dict['reduc1 percentage'].append(0)

                    else:
                        Spo_dict['reduc1 percentage'][i] = (0)
                    
                # Another reduction 2
                reduc2 =  c52.checkbox("another reduction 2",key=i+50,value=spo_def_dict['reduc2'][i])
                
                if not old:
                    Spo_dict['reduc2'].append(reduc2)

                else:
                    Spo_dict['reduc2'][i] = (reduc2)
                
                if reduc2:
                    reduc2_per = float(c52.text_input("reduction 2 percentage",spo_def_dict['reduc2 percentage'][i],key=(i+1)*107))
                    if not old:
                        Spo_dict['reduc2 percentage'].append(reduc2_per)

                    else:
                        Spo_dict['reduc2 percentage'][i] = (reduc2_per)
                
                else:
                    if not old:
                        Spo_dict['reduc2 percentage'].append(0)  

                    else:
                        Spo_dict['reduc2 percentage'][i] = (0)    
                    
            else:
                eb1 =  c11.checkbox("Early booking 1",key=(i+1)*108)
                if not old:
                    Spo_dict['eb1'].append(eb1)

                else:
                    Spo_dict['eb1'][i] = (eb1)
                
                if eb1:
                    eb1_per = float(c11.text_input("eb1 percentage",0,key=(i+1)*109))
                    eb1_date = c11.date_input("Early booking date",key = (i+1)*1500)
                    if not old:
                        Spo_dict['eb1 percentage'].append(eb1_per)
                        Spo_dict['eb1 date'].append(eb1_date)

                    else:
                        Spo_dict['eb1 percentage'][i] = (eb1_per)
                        Spo_dict['eb1 date'][i] = (eb1_date)
                    
                else:
                    if not old:
                        Spo_dict['eb1 percentage'].append(0)
                        Spo_dict['eb1 date'].append(None)

                    else:
                        Spo_dict['eb1 percentage'][i] = (0)
                        Spo_dict['eb1 date'][i] = (None)
                    
                        
                #eb2
                eb2 =  c12.checkbox("Early booking 2",key=(i+1)*110)
                if not old:
                    Spo_dict['eb2'].append(eb2)

                else:
                    Spo_dict['eb2'][i] = (eb2)
                
                if eb2:
                    eb2_per = float(c12.text_input("eb2 percentage",0,key=(i+1)*111))
                    eb2_date = c12.date_input("Early booking date",key=(i+1)*112)
                    if not old:
                        Spo_dict['eb2 percentage'].append(eb2_per)
                        Spo_dict['eb2 date'].append(eb2_date)

                    else:
                        Spo_dict['eb2 percentage'][i] = (eb2_per)
                        Spo_dict['eb2 date'][i] = (eb2_date)
                    
                else:
                    if not old:
                        Spo_dict['eb2 percentage'].append(0)
                        Spo_dict['eb2 date'].append(None)

                    else:
                        Spo_dict['eb2 percentage'][i] = (0)
                        Spo_dict['eb2 date'][i] = (None)
                    
                # senior
                senior =  c31.checkbox("senior",key=(i+1)*113)
                if not old:
                    Spo_dict['senior'].append(senior)

                else:
                    Spo_dict['senior'][i] = (senior)
                
                if senior:
                    senior_per = float(c31.text_input("reduction percentage",0,key=(i+1)*114))
                    if not old:
                        Spo_dict['senior percentage'].append(senior_per)

                    else:
                        Spo_dict['senior percentage'][i] = (senior_per)
                    
                else:
                    if not old:
                        Spo_dict['senior percentage'].append(0)

                    else:
                        Spo_dict['senior percentage'][i] = (0)
                
                # long term
                lt =  c32.checkbox("long term",key=(i+1)*115)
                if not old:
                    Spo_dict['long term'].append(lt)

                else:
                    Spo_dict['long term'][i] = (lt)
                
                if lt:
                    lt_dats = int(c32.text_input("long term days",28,key=(i+1)*313))
                    lt_per = float(c32.text_input("long term percentage",0,key=(i+1)*314))
                    if not old:
                        Spo_dict['lt days'].append(lt_dats)
                        Spo_dict['lt percentage'].append(lt_per)

                    else:
                        Spo_dict['lt days'][i] = (lt_dats)
                        Spo_dict['lt percentage'][i] = (lt_per)
                    
                else:
                    if not old:
                        Spo_dict['lt days'].append(0)
                        Spo_dict['lt percentage'].append(0)

                    else:
                        Spo_dict['lt days'][i] = (0)
                        Spo_dict['lt percentage'][i] = (0)
                    
                # Another reduction 1
                reduc1 =  c51.checkbox("another reduction 1",key=i*40)
                if not old:
                    Spo_dict['reduc1'].append(reduc1)

                else:
                    Spo_dict['reduc1'][i] = (reduc1)
                    
                if reduc1:
                    reduc_per = float(c51.text_input("reduction percentage",0,key=(i+1)*17))
                    if not old:
                        Spo_dict['reduc1 percentage'].append(reduc_per)

                    else:
                        Spo_dict['reduc1 percentage'][i] = (reduc_per)
                    
                else:
                    if not old:
                        Spo_dict['reduc1 percentage'].append(0)

                    else:
                        Spo_dict['reduc1 percentage'][i] = (0)
                    
                # Another reduction 2
                reduc2 =  c52.checkbox("another reduction 2",key=(i+1)*5000)
                if not old:
                    Spo_dict['reduc2'].append(reduc2)

                else:
                    Spo_dict['reduc2'][i] = (reduc2)
                
                if reduc2:
                    reduc2_per = float(c52.text_input("reduction 2 percentage",0,key=(i+1)*200))
                    if not old:
                        Spo_dict['reduc2 percentage'].append(reduc2_per)

                    else:
                        Spo_dict['reduc2 percentage'][i] = (reduc2_per)
                    
                else:
                    if not old:
                        Spo_dict['reduc2 percentage'].append(0)

                    else:
                        Spo_dict['reduc2 percentage'][i] = (0)
            # if selected_setting is None:
            #     Offers_dict = Offers_dict_old
            
                    
        
        
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
        s_dict[None] = Spo_dict
        if "Spo_dict" in st.session_state:
                Spo_dict = st.session_state['Spo_dict']
                
        if selected_setting is not None:
            lista = ['eb1 date','eb2 date','start_date','end_date']
            for key in lista:
                if len(Spo_dict) > 0:
                    for element in range(len(Spo_dict[key])):
                        if key in Spo_dict and Spo_dict[key] is not None:
                            Spo_dict[key][element] = pd.to_datetime(Spo_dict[key][element])
            # date_format = "%Y-%m-%d"

        if "sheet_names" not in st.session_state:
            st.markdown("""
                <h1 style='text-align: center; margin-bottom: 20px; color: #FFC107; font-family: "Roboto", sans-serif; font-size: 32px; font-weight: bold;'>
                Please insert the file first to proceed.
                </h1>
            """, unsafe_allow_html=True)
        else:
            # if "Spo_dict" in st.session_state:
            #     Spo_dict = st.session_state['Spo_dict']
            if selected_setting is not None:
                Spo_dict = s_dict[selected_setting]
                Spo_dict['SPO'] = list()
            
            sheet_names = st.session_state['sheet_names']
            count = 0
            for i in range(100):
                Spo_number = "spo"+str(i)
                # name
                if (len(Spo_dict['name']) >= i+1):
                    old = True
                    if (selected_setting is not None) and (Spo_dict['name'][i] in sheet_names) and (Spo_dict['name'][i] is not None):
                        sheet_index = sheet_names.index(Spo_dict['name'][i])
                    elif ("Spo_dict" in st.session_state):
                        if (Spo_dict['name'][i] in sheet_names) and (Spo_dict['name'][i] is not None):
                            sheet_index = sheet_names.index(st.session_state['Spo_dict']['name'][i])
                    
                    Spo_name = st.selectbox('Choose spo ' + str(i+1),sheet_names, key=Spo_number, index = sheet_index)

                else:
                    old = False
                    Spo_name = st.selectbox('Choose spo ' + str(i+1),sheet_names, key=Spo_number)
                    
                if Spo_name is None:
                    Spo_dict['count'] = count
                    if len(Spo_dict['name']) >= i:
                        Spo_dict['name'] = Spo_dict['name'][:i]
                    
                    break
                else:
                    if selected_setting is not None:
                        if len(Spo_dict['name']) == i:
                            selected_setting = None
                            
                    count +=1
                if not old:
                    Spo_dict['name'].append(Spo_name)
                else:
                    Spo_dict['name'][i] = Spo_name
                
                # SPO
                SPO = pd.read_excel(st.session_state["uploaded file"],sheet_name=Spo_name)
                if 'SPO' not in Spo_dict:
                    if 'Spo_dict' in st.session_state:
                        if 'SPO' in st.session_state['Spo_dict']:
                            Spo_dict['SPO'] = st.session_state['Spo_dict']['SPO']
                    else:
                        Spo_dict['SPO'] = range(20)
                    
                if selected_setting is not None:
                    Spo_dict['SPO'].append(SPO)
                if not old:
                    Spo_dict['SPO'].append(SPO)
                else:
                    Spo_dict['SPO'][i] = SPO
                
                # date
                cl1, cl2 = st.columns([1,2])
                s_date = SPO["first date"][0]
                if selected_setting is not None:
                    s_date = Spo_dict['start_date'][i]
                start_res = cl1.date_input("from",key="start"+str(i),value=pd.to_datetime(s_date))
                if not old:
                    Spo_dict['start_date'].append(start_res)
                else:
                    Spo_dict['start_date'][i] = start_res
                
                e_date = SPO["second date"].dropna().iloc[-1]
                if selected_setting is not None:
                    e_date = Spo_dict['end_date'][i]
                end_res = cl2.date_input("to",key="end"+str(i),value = pd.to_datetime(e_date))
                if not old:
                    Spo_dict['end_date'].append(end_res)
                else:
                    Spo_dict['end_date'][i] = end_res
                
                # offers
                spo_offers(i,Spo_dict,old,Offers_dict)
                
                st.divider()
            st.session_state['Spo_dict'] = Spo_dict
            
            
            "***"
            column1,column2 = st.columns([1,8.4])
                
            # Extra
            column1.markdown("""
                    <h1 style='text-align: center; margin-bottom: 0px; font-family: "Roboto", sans-serif; font-size: 25px; font-weight: bold;'>
                    Reductions
                    </h1>
                """, unsafe_allow_html=True
                )
            
            
            Dis_dict = {'amount':list(),
                        'type':list(),
                        'days':list(),
                        'column':list()}
            all_dis_types = [None,'reduction','extra']
                
            if selected_setting is not None:
                Dis_dict = e_dict[selected_setting]
                
            statment = pd.read_excel(st.session_state["uploaded file"],sheet_name='statment')
            
            for i in range(15):
                red_number = "red"+str(i)
                if(len(Dis_dict['type'])>=i+1):
                    old = True
                    
                    if (selected_setting is not None):
                        if (Dis_dict['type'][i] is not None):
                            index = all_dis_types.index(Dis_dict['type'][i])
                        
                    elif ("Dis_dict" in st.session_state):
                        if (Dis_dict['type'][i] is not None):
                            index = all_dis_types.index(st.session_state['Dis_dict']['type'][i])
                            
                    dis_type = st.selectbox("Choose the type of change " + str(i+1),all_dis_types,index=index,key='121'*(12+i))
                            
                else:
                    old = False
                    dis_type = st.selectbox("Choose the type of change " + str(i+1),all_dis_types,key='101'*(10+i))
                    
                if dis_type is None:
                    if len(Dis_dict['type'])>=i:
                        Dis_dict['type']=Dis_dict['type'][:i]
                    break
                
                if not old:
                    Dis_dict['type'].append(dis_type)
                else:
                    Dis_dict['type'][i] = (dis_type)
                if dis_type is not None:
                    
                    if all_dis_types.index(dis_type) == 1:
                        text = "reduction percentage"
                        cl1, cl2 = st.columns([1,2])
                    elif all_dis_types.index(dis_type) == 2:
                        text = "extra amount"
                        cl1, cl2, cl3 = st.columns([1,2,2])
                    if (len(Dis_dict['type'])>= i+1) and (len(Dis_dict['column'])>= i+1):
                        if selected_setting is not None:
                            amount_val = Dis_dict['amount'][i]
                            days_val = Dis_dict['days'][i]
                                
                            index = list(statment.columns.insert(0,None)).index(Dis_dict['column'][i])
                        elif 'Dis_dict' in st.session_state:
                                amount_val = st.session_state['Dis_dict']['amount'][i]
                                days_val = st.session_state['Dis_dict']['days'][i]
                                index = list(statment.columns.insert(0,None)).index(st.session_state['Dis_dict']['column'][i])
                        amount = float(cl1.text_input(text,amount_val,key = "1www"*(2+i+i*2)))
                        if all_dis_types.index(dis_type) == 2:
                            days = float(cl3.text_input('Minimum days',days_val,key = "1w"*(12+i)))
                        else:
                            days = 0
                        column = cl2.selectbox("Please select the column for the action",statment.columns.insert(0,None),index = index,key = 'aa'*(i+1))    
                    else:
                        amount = float(cl1.text_input(text,0,key = "1w"*(2+i*3)))
                        if all_dis_types.index(dis_type) == 2:
                            days = float(cl3.text_input('Minimum days',7,key = "1w"*(2+i+i*3+9)))
                        column = cl2.selectbox("Please select the column for the action",statment.columns.insert(0,None),key = 'aa'*(i+1))
                    
                    if not old:
                        Dis_dict['amount'].append(amount)
                        Dis_dict['column'].append(column)
                        if all_dis_types.index(dis_type) == 2:
                            Dis_dict['days'].append(days)
                        else:
                            Dis_dict['days'].append(0)
                    else:
                        Dis_dict['amount'][i] = amount
                        Dis_dict['column'][i] = column
                        if all_dis_types.index(dis_type) == 2:
                            Dis_dict['days'][i] = days
                        else:
                            Dis_dict['days'][i] = 0
                st.divider()
            st.session_state['Dis_dict'] = Dis_dict
            
            "***"
            
            column1,column2 = st.columns([1,2.5])
                

            column1.markdown("""
                <h1 style='text-align: center; margin-bottom: 0px; font-family: "Roboto", sans-serif; font-size: 25px; font-weight: bold;'>
                Add new custom
                </h1>
            """, unsafe_allow_html=True)

            user_input = st.text_input('settings name')
            apply_button = st.button("Add a new custom")
            
            file_dict_save = dict()
            comb_dict = dict()
            import json
            #load
            
            file_path = "reductions.json"
            # save
            r_save_data = Offers_dict.copy()
            spo_save_data = Spo_dict.copy()
            
            
            # end
            
            if apply_button:

            
                if len(user_input) > 0:
                    
                    if (r_save_data['eb1 date'] is not None) and not isinstance(r_save_data['eb1 date'], str):
                        r_save_data['eb1 date'] = r_save_data['eb1 date'].strftime("%Y-%m-%d")
                    if (r_save_data['eb2 date'] is not None) and not isinstance(r_save_data['eb2 date'], str):
                        r_save_data['eb2 date'] = r_save_data['eb2 date'].strftime("%Y-%m-%d")
                    # if (r_save_data['start_date'] is not None) and not isinstance(r_save_data['start_date'], str):
                    #     r_save_data['start_date'] = r_save_data['start_date'].strftime("%Y-%m-%d")
                    # if (r_save_data['end_date'] is not None) and not isinstance(r_save_data['eb2 date'], str):
                    #     r_save_data['end_date'] = r_save_data['end_date'].strftime("%Y-%m-%d")
                    
                    file_dict_save[user_input] = r_save_data
                    for key in old_file_dict.keys():
                        if (old_file_dict[key]['eb1 date'] is not None) and not isinstance(old_file_dict[key]['eb1 date'], str):
                            old_file_dict[key]['eb1 date'] = old_file_dict[key]['eb1 date'].strftime("%Y-%m-%d")
                        if (old_file_dict[key]['eb2 date'] is not None) and not isinstance(old_file_dict[key]['eb2 date'], str):
                            old_file_dict[key]['eb2 date'] = old_file_dict[key]['eb2 date'].strftime("%Y-%m-%d")
                    r_dict = {**old_file_dict, **file_dict_save}
                    convert_dates_to_strings(r_dict)

                
                with open(file_path, "w") as json_file:
                    json.dump(r_dict, json_file)

                # save
                ssd1 = len(spo_save_data['eb1 date'])
                ssd2 = len(spo_save_data['eb2 date'])
                rs1 = len(spo_save_data['start_date'])
                rs2 = len(spo_save_data['end_date'])
                if len(user_input) > 0:
                    del spo_save_data['SPO']
                    if len(spo_save_data['eb1 date']) > 0:
                        for i in range(len(spo_save_data)):
                            if i < ssd1:
                                if spo_save_data['eb1 date'][i]:
                                    if not(type(spo_save_data['eb1 date'][i]) == str):
                                        spo_save_data['eb1 date'][i] = spo_save_data['eb1 date'][i].strftime("%Y-%m-%d")
                    if len(spo_save_data['eb2 date']) > 0:
                        for i in range(len(spo_save_data['eb2 date'])):
                            if i < ssd2:
                                if spo_save_data['eb2 date'][i]:
                                    if not(type(spo_save_data['eb2 date'][i]) == str):
                                        spo_save_data['eb2 date'][i] = spo_save_data['eb2 date'][i].strftime("%Y-%m-%d")
                    if len(spo_save_data['start_date']) > 0:
                        for i in range(len(spo_save_data['start_date'])):
                            if i < rs1:
                                if spo_save_data['start_date'][i]:
                                    if not(type(spo_save_data['start_date'][i]) == str):
                                        spo_save_data['start_date'][i] = spo_save_data['start_date'][i].strftime("%Y-%m-%d")
                    if len(spo_save_data['end_date']) > 0:
                        for i in range(len(spo_save_data['end_date'])):
                            if i < rs2:
                                if spo_save_data['end_date'][i]:
                                    if not(type(spo_save_data['end_date'][i]) == str):
                                        spo_save_data['end_date'][i] = spo_save_data['end_date'][i].strftime("%Y-%m-%d")
                    if "SPO" in spo_save_data:
                        del spo_save_data["SPO"]
                    file_dict_save = dict()
                    file_dict_save[user_input] = spo_save_data
                    s_dict = {**s_dict, **file_dict_save}
                    s_dict = convert_dates_to_strings(s_dict)
                    
                    s_dict = remove_spo_key(s_dict)
                    
                with open("spo.json", "w") as json_file:
                    json.dump(s_dict, json_file)    
                    
                
                if len(user_input) > 0:
                    
                    file_dict_save = dict()
                    file_dict_save[user_input] = combination
                    com_dict = {**com_dict, **file_dict_save}

                    with open("combinations.json", "w") as json_file:
                        json.dump(com_dict, json_file)
                        
                if len(user_input) > 0:
                    
                    file_dict_save = dict()
                    file_dict_save[user_input] = Dis_dict
                    e_dict = {**e_dict, **file_dict_save}

                    with open("extra.json", "w") as json_file:
                        json.dump(e_dict, json_file)     
        dicts = [red_dict,s_dict,com_dict,e_dict]
        # download json
        cnt=0
        for i in range(len(dicts)):
            dicts[i] = convert_dates_to_strings(dicts[i])
            dicts[i] = remove_spo_key(dicts[i])
            json_string = json.dumps(dicts[i])
            # st.json(json_string, expanded=True)

            st.download_button(
                label="Download JSON",
                file_name=str(dicts[i])+".json",
                mime="application/json",
                data=json_string,
            )                     

else:
    
    st.markdown("""
                <h1 style='text-align: center; margin-bottom: 20px; color: #FFC107; font-family: "Roboto", sans-serif; font-size: 32px; font-weight: bold;'>
                Enter your password on the homepage to proceed.
                </h1>
            """, unsafe_allow_html=True
            )

formatted_date = current_date.strftime('%d-%m-%Y')
