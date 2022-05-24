# -*- coding: utf-8 -*-
"""
First modified on Tuesday January 4 12:36:03 2022

@author: Olufemi Victor Tolulope. @osinkolu on github.
Comments and explanations done by Olufemi Victor Tolulpe.
@Teacher: TNIKOLIC

A streamlit app to call streamlit component webrtc and load a tf lite model for object detection
"""

#  import main packages
import streamlit as st 
from PIL import Image # PIL is used to display images 
import os # used to save images in a directory
from object_detection_helper import * #import everything from object detection 
import snapshot as snap #for your snapshot
import helper as help # import my text script.
import numpy as np 
import pandas as pd
from search_and_translate import search_and_translate,translate_alone # import functions from the script
from settings import model_influencer # very important to attribute your models
from find_nearby_business import find_nearby_pest_shop, my_folium_map #import to find nearby shops.
from streamlit_folium import st_folium

# import what you need to track users.
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

# Bring in my language codes csv file
lang_table = pd.read_csv("languages_by_victor.csv")

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

#Define a function to find nearby Pesticides and herbicides shop. 
def find_nearby_shop_ux():
    st.write("Hi there, We can help you find the nearest Pesticides and herbicides shop")
    st.error("Do you permit us to use your location to improve results?")
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

    if result:
        if "GET_LOCATION" in result:
            lat = result.get("GET_LOCATION")["lat"]
            lon = result.get("GET_LOCATION")["lon"]
            m  = my_folium_map([lat,lon])
            st_data = st_folium(m)
            st.info("This is where you are: We are searching for the nearest crop pest & disease control store.")
            try:
                print("here")
                shops_list  =  find_nearby_pest_shop(5, lat, lon)
                print("passed")
                business_names = shops_list[0]
                business_status = shops_list[1]
                address = shops_list[2]
                latitudes = shops_list[3]
                longitudes = shops_list[4]
                for i in range(len(business_names)):
                    with st.expander(business_names[i]):
                        m  = my_folium_map([latitudes[i],longitudes[i]])
                        st_data_ = st_folium(m)
                        st.write("Address: " + address[i])
                        st.write("Current Status: "+business_status[i])
            except:
                st.warning("I'm sorry, we didn't find anybody closeby.")
            
    if st.button("Stop! don't use my location"):
        del result
        st.error("No worries, We've destroyed our location tracker, you can use google maps to find the nearest herbicides shops.")


#Write Main Script.
#..............................................................................................................
def main():
    # Set the background
    help.set_bg_hack() 
    # ===================== Set header and site info =============================
    # Set app header
    help.header('Crop Disease and Pest Detection')
    

    # Set text and pass to sub_text function
    text = """
    <center> <br> Welcome to the Victor's Crop Disease & Pest Detection Add-On. </br> </center>
    <center> This App is an add-on for the Larger Centralized Food Platform aimed at reducing food loss and food waste. You can either take or upload photos of your crop to use the A.I.
    </center>
    """
    help.sub_text(text)
    
    # Set expander with references and special mentions
    help.expander()
    
    
    # ======================= Get tf lite model details ==========================
    #labels, colors, height, width, interpreter = detect.define_tf_lite_model()
    
    # ============================= Main app =====================================

   # model = model_influencer("crop_disease")
   # model.set_params()
        # Get explainations 

    with st.expander("Settings"):
        # choose your model type
        model_option = st.selectbox('Kindly select use case or preferred model',('crop_disease','Pests_attack (Not available yet)','fruits_harvest', 'weeds', 'chicken'))
        model = model_influencer(model_option)
        model.set_params()
        # Get explainations in your native language
        language = st.selectbox('Get explainations in your preferred language',tuple(lang_table.language_name.values))
        language = lang_table[lang_table["language_name"]==language].language_name.values[0]
        # I used a slider to set-up an adjustable threshold
        thresh = st.slider("Set threshold for predictions.",0.0,1.0,model.initial_threshold,0.05)
        st.write('Threshold:', thresh, )

    with st.expander("List of Possible Detections"):
        help.sub_text(model.detectables)

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

            UX_main(image_np, thresh, model, language, model.type)

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

            UX_main(image_np, thresh, model, language,model.type)

    elif option == 'Use demo image 01':
        roll_the_UX(model.demo1,thresh,model,language,model.type)

    elif option == 'Use demo image 02':
        roll_the_UX(model.demo2,thresh,model,language,model.type)

    elif option == 'Use demo image 03':
        roll_the_UX(model.demo3,thresh,model,language,model.type)
    else:
        help.header(translate_alone("Please select the method you want to use to upload photo.", language))
        help.sub_text(translate_alone("Note: A.I may use up to 120 seconds for inference.", language))


#...........................................................................................................
#Run Pages.
if __name__ == "__main__":
    # =========== Set page configs =======# Main panel setup======# Set website details
    st.set_page_config(page_title ="Victor's Crop Analysis Add-On", page_icon=':camera:', layout='centered')
    my_page = st.sidebar.radio('Page Navigation', ['Crop Analysis', 'Find pest control shop', 'Test'])
    if my_page == 'Crop Analysis':
        main()
    elif my_page == 'Find pest control shop':
        find_nearby_shop_ux()
    else:
        m = leafmap.Map(google_map="TERRAIN")
        m