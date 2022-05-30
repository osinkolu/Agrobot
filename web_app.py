# -*- coding: utf-8 -*-
"""
First modified on Tuesday January 4 12:36:03 2022

@author: Olufemi Victor Tolulope. @osinkolu on github.
Comments and explanations done by Olufemi Victor Tolulpe.
@Teacher: TNIKOLIC

A streamlit app to call streamlit component webrtc and load a tf lite model for object detection
"""

#  import main packages
from requests import session
import streamlit as st 
from PIL import Image # PIL is used to display images 
import os # used to save images in a directory
from object_detection_helper import * #import everything from object detection 
import snapshot as snap #for your snapshot
import helper as help # import my text script.
import numpy as np 
import pandas as pd
from search_and_translate import search_and_translate, translate_alone # import functions from the script
from settings import model_influencer # very important to attribute your models
from find_nearby_business import find_nearby_pest_shop #import to find nearby shops.
from streamlit_folium import st_folium
import folium
from streamlit_option_menu import option_menu
from customer_support import send_email

# import what you need to track users.
from bokeh.models.widgets import Button, Div
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

# Bring in my language codes csv file
lang_table = pd.read_csv("languages_by_victor.csv")
if "model_option" not in st.session_state:
    st.session_state.model_option = 'crop_disease'
model = model_influencer(st.session_state.model_option)
model.set_params()
if "language" not in st.session_state:
    st.session_state.language = "en"
if "thresh" not in st.session_state:
    st.session_state.thresh = model.initial_threshold

#define a function to rollout UI from detections.
def output_from_the_image(detector,image_np,language, model, type):
    # Run object detection estimation using the model.
    detections = detector.detect(image_np)
    try:
        image_np, class_name,num_detections = visualize(image_np, detections)
    except Exception:
        image_np, class_name, num_detections = image_np, "Nothing", "0"
                                        
    #display detected image with bbox drawn on it
    st.image(Image.fromarray(image_np), use_column_width=True)

    #Write label name
    st.write(translate_alone(class_name, language))


    # fixing search string depending on the model selected.
    if type == "search":
        string1 = model.string1
        string2 = model.string2
        string3 = model.string3
        # Search and Translate.
        st.info(search_and_translate(string1+ class_name, language))
        # Intoduce cure
        st.write(translate_alone(string2, language))
        # Search and Translate Cure.
        st.info(search_and_translate(string3 + class_name, language))

    #The UI if we need to count rather than use search results 
    elif type == "count":
        st.info("I can count " + str(num_detections) +" "+ class_name + "s"+ " here.")
    
    # Reminder to change settings above
    st.write(translate_alone("Please feel free to change the language in settings to view results in your preferred local language", language))


# Direct function that draws the UI.
def UX_main(image_np, thresh, model, language,type):
    options = ObjectDetectorOptions(
    num_threads=4,
    score_threshold=thresh,
    )
    detector = ObjectDetector(model_path='model zoo/'+model.name+'.tflite', options=options)
    output_from_the_image(detector,image_np,language, model,type)

# Direct function that draws the UI.
def roll_the_UX(demo_img, thresh, model, language,type):
    st.image(demo_img)
    im = Image.open(demo_img).convert('RGB') #convert in case we have a wierd number of channels in the image.
    im.thumbnail((512, 512), Image.ANTIALIAS)
    image_np = np.asarray(im)
    UX_main(image_np, thresh, model, language,type)





########################################## NEARBY PEST SHOPS APP #################################################
#Define a function to find nearby Pesticides and herbicides shop. 
def find_nearby_shop_ux():
    st.write("Hi there, We can help you find the nearest Pesticides and herbicides shop, click on get location to find nearby pest control store.")
    # Leverage Javascript code to get location unlike normal python geocode.
    loc_button = Button(label="Get Location")
    loc_button.js_on_event("button_click", CustomJS(code="""
            navigator.geolocation.getCurrentPosition(
                    (loc) => {
                        document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
                    }
                )
                """))
    result = streamlit_bokeh_events(
                loc_button,
                events="GET_LOCATION",
                key="get_location",
                refresh_on_update=False,
                override_height=40,
                debounce_time=0)
# Get location and draw the Map
    if result:
        if "GET_LOCATION" in result:
            lat = result.get("GET_LOCATION")["lat"]
            lon = result.get("GET_LOCATION")["lon"]
            st.info("This is where you are: We are searching for the nearest crop pest & disease control store.")
            m  = folium.Map([lat,lon],zoom_start = 11)
            folium.Marker([lat, lon], popup="Your location", tooltip="You", icon=folium.Icon(color="green")).add_to(m)   
            try:
                # Find the shops.
                shops_list  =  find_nearby_pest_shop(5, lat, lon)
                business_names = shops_list[0]
                business_status = shops_list[1]
                address = shops_list[2]
                latitudes = shops_list[3]
                longitudes = shops_list[4]

                #  Construct the Map and the widgets
                for i in range(len(business_names)):
 #                   html=f"""
 #       <h1> {business_names[i]}</h1>
 #       <p>You can use any html here! Let's do a list:</p>
 #       <ul>
 #           <li>{address[i]}</li>
 #           <li>{business_status[i]}</li>
 #       </ul>
 #       </p>
 #       <p>And that's a <a href="https://www.python-graph-gallery.com">link</a></p>
 #      """
 #                  iframe = folium.IFrame(html=html, width=200, height=200)
                    popup = folium.Popup("Address: " + address[i], max_width=2650)

                    folium.Marker([latitudes[i], longitudes[i]], tooltip=business_names[i],popup=popup, icon=folium.Icon(color="blue") ).add_to(m)
                    with st.expander(business_names[i]):
                        st.write("Address: " + address[i])
                        st.write("Current Status: "+business_status[i])
                st_data_ = st_folium(m, width= 700)
            except:
                st.warning("I'm sorry, we didn't find anybody closeby.")
                st_data_ = st_folium(m, width= 700)

            
    if st.button("Stop! don't use my location"):
        del result
        st.error("No worries, We've destroyed our location tracker, you can use google maps to find the nearest herbicides shops.")


########################################## Settings Page ####################################################################
#This function returns the whole settings page
def settings():
    use_cases = ['crop_disease','Pests_attack (Not available yet)','fruits_harvest', 'weeds', 'chicken']
    # Just in case there's nothing in session state yet, set it.
    if "use_cases_index" not in st.session_state:
        st.session_state.use_cases_index=0
    # You must keep model option as you move across states, it's too important.
    st.session_state.model_option = st.selectbox('Kindly select use case or preferred model',tuple(use_cases), index=st.session_state.use_cases_index)
    # update the index incase you come back, you'll def want it selected
    st.session_state.use_cases_index = use_cases.index(st.session_state.model_option)

    #Reset the model because you've changed model option
    model = model_influencer(st.session_state.model_option)
    model.set_params()

    # Get explainations in your native language
    language_names = lang_table.language_name.values.tolist()

    if "language_index" not in st.session_state:
        st.session_state.language_index=0
    language = st.selectbox('Select your preferred language',tuple(language_names), index=st.session_state.language_index)
    st.session_state.language = lang_table[lang_table["language_name"]==language].language_name.values[0]
    st.session_state.language_index = language_names.index(st.session_state.language)

    # I used a slider to set-up an adjustable threshold
    st.session_state.thresh = st.slider("Set threshold for predictions.",0.0,1.0,model.initial_threshold,0.05)
    st.write('Threshold:', st.session_state.thresh, )
    help.sub_text("<center>You can read more about the models in the about section</center>")

########################## ABOUT MODELS PAGE #########################################################################

def about_models():
    # Set text and pass to sub_text function
    text = """
    <center> <br> Welcome to the Victor's Crop Disease & Pest Detection Add-On. </br> </center>
    <center> This App is an add-on for the Larger Centralized Food Platform aimed at reducing food loss and food waste. You can either take or upload photos of your crop to use the A.I.
    </center>
    """
    help.sub_text(text)
    
    # Set expander with references and special mentions
    help.expander()
    



    # Set text and pass to sub_text function
    text = """
    <center> Learn more about the Predictions of the A.I model <p> </p> </center>
    """
    help.sub_text(text)
    for models in ['crop_disease','fruits_harvest', 'weeds', 'chicken']:
        model = model_influencer(models)
        model.set_params()
        with st.expander("About the " + models.title() + " A.I model"):
            help.sub_text(model.detectables)

################################# HOME PAGE ###########################################################
def home():
    help.header("Welcome to Agrobot")
    help.sub_text("A place where A.I meets Farming to give you the best Agro-experience<p> </p>")
    from PIL import Image
    image = Image.open('agrobot.png')
    image.thumbnail((1000,1000), Image.ANTIALIAS)
    st.image(image, caption='We offer our farmers the best tools')


#################### Customer Support Page #############################################################
def customer_support():
    help.sub_text("Feel free to make your complaints here: Both Agricultural & Technical support are avialble")
    with st.form(key = 'form1', clear_on_submit=True):
        first_name = st.text_input("Firstname")
        recepient = st.text_input("Your email or Phone No.")
        email_subject = st.text_input("Subject")
        email_body = st.text_area("Complaint")
        submit_button = st.form_submit_button()

    if submit_button:
        send_email(first_name, recepient, email_subject, email_body)
        st.success("Hi {}, your complaint has been sent, help will come soon.".format(first_name))

#############################  MARKET PLACE ############################################################
def marketplace():
    help.header("Our Own Marketplace is coming soon!")
    help.sub_text("while we build our very own marketplace, we have extended other platforms here for you to sell your farm produce online")
    col1,col2, col3 = st.columns([1,1,1])
    
    with col1:    
        if st.button('Agrimp online Market'):
            js = "window.open('https://agrimp.com/')"  # New tab or window
            js = "window.location.href = 'https://agrimp.com/'"  # Current tab
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
        elif st.button('Mkulimayoung online Market'):
            js = "window.open('https://www.mkulimayoung.com/')"  # New tab or window
            js = "window.location.href = 'https://www.mkulimayoung.com/'"  # Current tab
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
    with col2:
        if st.button('Agribros Online Market'):
            js = "window.open('https://www.agribros.market/marketplace')"  # New tab or window
            js = "window.location.href = 'https://www.agribros.market/marketplace'"  # Current tab
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)   
        elif st.button('Krishi Online Market'):
            js = "window.open('https://www.krishi-market.com/')"  # New tab or window
            js = "window.location.href = 'https://www.krishi-market.com/'"  # Current tab
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
    with col3:        
        if st.button('Agrolinka Online Market'):
            js = "window.open('https://agrolinka.com/Home/Product')"  # New tab or window
            js = "window.location.href = 'https://agrolinka.com/Home/Product'"  # Current tab
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
        elif st.button('Crop Spot Online Market'):
            js = "window.open('https://www.cropspot.com/en/farmer/')"  # New tab or window
            js = "window.location.href = 'https://www.cropspot.com/en/farmer/'"  # Current tab
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)

#Write Main Script.
#..............................................................................................................
def main():
    # Set the background
    help.set_bg_hack() 
    # ===================== Set header and site info =============================
    # Set app header
    help.header('Crop Analysis')
    
    # choosing the input method for the app.
    option = st.selectbox(
        'Please select photo input type',
        ('None', 'Take photo', 'Upload photo',"Use demo image 01","Use demo image 02","Use demo image 03"))
    
    # Start with app logic:
    if option == 'Take photo':
        
        # In case Take photo is selected, run the webrtc component, 
        # save photo and pass it to the object detection model
        out_image = snap.streamlit_webrtc_snapshot()
        
        if out_image is not None:
            
            help.header("Your photo")
            
            st.image(out_image, channels="BGR")
            
            file_name = help.write_image(out_image)

            im = Image.open(file_name).convert('RGB')  #convert in case we have a wierd number of channels in the image.
            im.thumbnail((512, 512), Image.ANTIALIAS)
            image_np = np.asarray(im)

            UX_main(image_np, st.session_state.thresh, model, st.session_state.language, model.type)

        else:

            st.warning('Waiting for snapshot to be taken')
           
    # If option is upload photo, allow upload and pass to model
    elif option == 'Upload photo':
        
        uploaded_file = st.file_uploader("Upload a photo", type=["jpg","png"])
        
        if uploaded_file is not None:
            
            st.image(uploaded_file)
            
            with open(os.path.join("tempDir",uploaded_file.name),"wb") as f: 
                f.write(uploaded_file.getbuffer())  
             
            im = Image.open("tempDir/" + uploaded_file.name).convert('RGB') #convert in case we have a wierd number of channels in the image.
            im.thumbnail((512, 512), Image.ANTIALIAS)

            image_np = np.asarray(im)

            UX_main(image_np, st.session_state.thresh, model, st.session_state.language,model.type)

    elif option == 'Use demo image 01':
        roll_the_UX(model.demo1,st.session_state.thresh,model,st.session_state.language,model.type)

    elif option == 'Use demo image 02':
        roll_the_UX(model.demo2,st.session_state.thresh,model,st.session_state.language,model.type)

    elif option == 'Use demo image 03':
        roll_the_UX(model.demo3,st.session_state.thresh,model,st.session_state.language,model.type)
    else:
        help.header(translate_alone("Please select the method you want to use to upload photo.", st.session_state.language))
        help.sub_text(translate_alone("Note: A.I may use up to 30 seconds for inference.", st.session_state.language))


#...........................................................................................................
#Run Pages.
if __name__ == "__main__":
    # =========== Set page configs ==========================================
    st.set_page_config(page_title ="Victor's Crop Analysis Add-On", page_icon=':camera:', layout='centered')
    ############################ HIDE STREAMLIT SIDE BAR ################################################
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    # footer {visibility: hidden;}
    # </style>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    with st.sidebar:
        my_page = option_menu(
            menu_title=None,
            options = ["Home", "Crop Analysis","Pest Control shops","Marketplace","Advanced settings","Contact Specialist", "About the A.I"],
            icons=["house-fill", "flower1", "shop","shop-window", "tools","person",],
        )
    #my_page = st.sidebar.radio('Page Navigation', ['Crop Analysis', 'Find pest control shop'])
    if my_page == 'Crop Analysis':
        main()
    elif my_page == 'Home':
        home()
    elif my_page == 'Contact Specialist':
        customer_support()
    elif my_page == 'Pest Control shops':
        find_nearby_shop_ux()
    elif my_page == 'Advanced settings':
        settings()
    elif my_page == 'About the A.I':
        about_models()
    elif my_page == 'Marketplace':
        marketplace()
    else:
        st.write("Noting to see here")