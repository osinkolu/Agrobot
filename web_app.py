# -*- coding: utf-8 -*-
"""
Modified on Tuesday January 4 12:36:03 2022

@author: Olufemi Victor tolulope. @osinkolu on github.
@Original author: TNIKOLIC

A streamlit app to call streamlit component webrtc and load a tf lite model for object detection
"""

# import main packages
from pickletools import string1
import streamlit as st 
from PIL import Image # PIL is used to display images 
import os # used to save images in a directory
from object_detection_helper import *
import snapshot as snap
import helper as help
import numpy as np
import pandas as pd
from search_and_translate import search_and_translate,translate_alone


lang_table = pd.read_csv("languages_by_victor.csv")

def output_from_the_image(detector,image_np,language, model_option):
  # Run object detection estimation using the model.
  detections = detector.detect(image_np)
  try:
      image_np, class_name = visualize(image_np, detections)
  except Exception:
      image_np, class_name = image_np, "Nothing"
                                        
            
  st.image(Image.fromarray(image_np), use_column_width=True)

  #Write label name
  st.write(translate_alone(class_name, language))

  # fixing search string depending on the model selected
  print(model_option)

  if model_option == "fruits_harvest":
      string1 = ""
      string2 = "Top health benefits of "
      string3 = "Health benefits"
  else:
      string1 = "what is "
      string2 = "Latest on curing "
      string3 = "how to cure "


  # Search and Translate.
  st.info(search_and_translate(string1+ class_name, language))
  # Intoduce cure
  st.write(translate_alone(string2, language))
  # Search and Translate Cure.
  st.info(search_and_translate(string3 + class_name, language))
  # Reminder to change settings above
  st.write(translate_alone("Please feel free to change the language in settings to view results in your preferred local language", language))



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

    with st.expander("List of Possible Detections"):
        help.sub_text("This contains the list of what the A.I can detect in order of best accuracy.<p> </p>Blueberry leaf <p> </p> Tomato leaf yellow virus <p> </p> Peach leaf <p> </p> Raspberry leaf <p> </p> Strawberry leaf <p> </p> Tomato Septoria leaf spot <p> </p> Tomato leaf <p> </p> Corn leaf blight <p> </p> Bell_pepper leaf <p> </p> Potato leaf early blight <p> </p> Tomato mold leaf <p> </p> Tomato leaf bacterial spot <p> </p> Soyabean leaf <p> </p> Bell_pepper leaf spot <p> </p> Tomato leaf mosaic virus <p> </p> Squash Powdery mildew leaf <p> </p> Apple leaf <p> </p> Potato leaf late blight <p> </p> Cherry leaf <p> </p> grape leaf <p> </p> Tomato leaf late blight <p> </p> Tomato Early blight leaf <p> </p> Apple rust leaf <p> </p> Apple Scab Leaf <p> </p> grape leaf black rot <p> </p> Corn rust leaf <p> </p> Corn Gray leaf spot <p> </p> Soybean leaf <p> </p> Potato leaf <p> </p> Tomato two spotted spider mites leaf <p> </p>")
    



    with st.expander("Settings"):
        # choose your model type
        model_option = st.selectbox('Kindly select use case or preferred model',('crop_disease','Pests_attack (Not available yet)','fruits_harvest'))
        
        # Get explainations in your native language
        language = st.selectbox('Get explainations in your preferred language',tuple(lang_table.language_name.values))
        language = lang_table[lang_table["language_name"]==language].language_name.values[0]
        # I used a slider to set-up an adjustable threshold
        thresh = st.slider("Set threshold for predictions.",0.0,1.0,0.5,0.05)
        st.write('Threshold:', thresh, )

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

            im = Image.open(file_name)
            im.thumbnail((512, 512), Image.ANTIALIAS)
            image_np = np.asarray(im)


            options = ObjectDetectorOptions(
            num_threads=4,
            score_threshold=thresh,
)

            detector = ObjectDetector(model_path='model zoo/'+model_option+'.tflite', options=options)
            output_from_the_image(detector,image_np,language)
            
        else:
            
            st.warning('Waiting for snapshot to be taken')
           
    # If option is upload photo, allow upload and pass to model
    elif option == 'Upload photo':
        
        uploaded_file = st.file_uploader("Upload a photo", type=["jpg","png"])
        
        if uploaded_file is not None:
            
            st.image(uploaded_file)
            
            with open(os.path.join("tempDir",uploaded_file.name),"wb") as f: 
                f.write(uploaded_file.getbuffer())  
             
            im = Image.open("tempDir/" + uploaded_file.name).convert('RGB')
            im.thumbnail((512, 512), Image.ANTIALIAS)

            image_np = np.asarray(im)


            options = ObjectDetectorOptions(
            num_threads=4,
            score_threshold=thresh,
)

            detector = ObjectDetector(model_path='model zoo/'+model_option+'.tflite', options=options)
            output_from_the_image(detector,image_np,language,model_option)

    elif option == 'Use demo image 01':
        demo_img = "tempDir/10609.jpg"
        st.image(demo_img)

        im = Image.open(demo_img)
        im.thumbnail((512, 512), Image.ANTIALIAS)
        image_np = np.asarray(im)


        options = ObjectDetectorOptions(
        num_threads=4,
        score_threshold=thresh,
        )
        detector = ObjectDetector(model_path='model zoo/'+model_option+'.tflite', options=options)
        print(detector.model_path)
        output_from_the_image(detector,image_np,language)

    elif option == 'Use demo image 02':
        demo_img = "tempDir/hgic_veg_septoria leaf spot1_1600.jpg"
        st.image(demo_img)
        im = Image.open(demo_img)
        im.thumbnail((512, 512), Image.ANTIALIAS)
        image_np = np.asarray(im)


        options = ObjectDetectorOptions(
        num_threads=4,
        score_threshold=thresh,
        )
        detector = ObjectDetector(model_path='model zoo/'+model_option+'.tflite', options=options)
        output_from_the_image(detector,image_np,language)

    elif option == 'Use demo image 03':
        demo_img = "tempDir/corn-Goss-NCLB-lesions-same-leaf.jpg"
        st.image(demo_img)
        im = Image.open(demo_img)
        im.thumbnail((512, 512), Image.ANTIALIAS)
        image_np = np.asarray(im)


        options = ObjectDetectorOptions(
        num_threads=4,
        score_threshold=thresh,
        )
        detector = ObjectDetector(model_path='model zoo/'+model_option+'.tflite', options=options)
        output_from_the_image(detector,image_np,language)

    else:
        help.header(translate_alone("Please select the method you want to use to upload photo.", language))
        help.sub_text(translate_alone("Note: A.I may use up to 120 seconds for inference.", language))

if __name__ == "__main__":
    main()     
