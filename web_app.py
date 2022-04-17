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
from object_detection_helper import *
import snapshot as snap
import helper as help
import numpy as np
import pandas as pd
from search_and_translate import search_and_translate,translate_alone
from settings import model_influencer


lang_table = pd.read_csv("languages_by_victor.csv")

def output_from_the_image(detector,image_np,language, model, type):
    # Run object detection estimation using the model.
    detections = detector.detect(image_np)
    try:
        image_np, class_name,num_detections = visualize(image_np, detections)
    except Exception:
        image_np, class_name, num_detections = image_np, "Nothing", "0"
                                        
            
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

    elif type == "count":
        st.info("I can count " + str(num_detections) +" "+ class_name + "s"+ " here.")
    
    # Reminder to change settings above
    st.write(translate_alone("Please feel free to change the language in settings to view results in your preferred local language", language))




def UX_main(image_np, thresh, model, language,type):
    options = ObjectDetectorOptions(
    num_threads=4,
    score_threshold=thresh,
    )
    detector = ObjectDetector(model_path='model zoo/'+model.name+'.tflite', options=options)
    output_from_the_image(detector,image_np,language, model,type)

def roll_the_UX(demo_img, thresh, model, language,type):
    st.image(demo_img)
    im = Image.open(demo_img).convert('RGB') #convert in case we have a wierd number of channels in the image.
    im.thumbnail((512, 512), Image.ANTIALIAS)
    image_np = np.asarray(im)
    UX_main(image_np, thresh, model, language,type)




def main():
    
    # ===================== Set page config and background =======================
    # Main panel setup
    # Set website details
    st.set_page_config(page_title ="Victor's Crop Analysis Add-On", 
                       page_icon=':camera:', 
                       layout='centered')
    
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

if __name__ == "__main__":
    main()     
