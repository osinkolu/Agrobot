# Feature Update (May 2022): Ability to find nearest pest control store.
We've given more knowledge power to the farmers, after detecting pest or disease in the farm, they can use the nearby store tool to find the nearest pest control shops based on their current location.

# Update (April 2022): Chicken detection model added.

We updated the model zoo with a model to detect and count the number of chickens.

#### Deployed app on streamlit share is [here](https://share.streamlit.io/osinkolu/agrobot/main/web_app.py).

# Update (March 2022): Weed detection model added.

To make the Agrobot a model place for Agro-related-A.I, we've added a weeds model to help detect weeds in the farm.

#### Deployed app on streamlit share is [here](https://share.streamlit.io/osinkolu/agrobot/main/web_app.py).

# Streamlitwebcam 📸

This repository is home to the webrtc snapshot object detection Stremlit app, and multiple custom trained tflite object detection models hosted like a plug and play. That was a mouthful, right? :D

# App parts 🖥

The app contains 4 major blocks - the webrtc snapshot component, the multi tf lite object detection part(Crop disease and Pest Detection), Information pulling on disease or pest (about it and top solutions), Language translation.

## Object detection functionality ✨

There are several models implemented in this object detection app, I have added all the jupyter notebooks used to train these models in the noebooks folder and have taken time to explain every line of code.

## Snapshot functionality 📷

The webrtc snapshot functionality was shared in [this](https://discuss.streamlit.io/t/new-component-streamlit-webrtc-a-new-way-to-deal-with-real-time-media-streams/8669/23?u=whitphx) discussion by the author of the component whitphx.

## Information pulling via search 🔍

I've embedded a search pipeline to search for pest or disease information as well as the best solution to pest type or crop disease type detected by the A.I model, this pipeline simply involves pulling top search results from Google's search engine. All this was simply implemented using [Google's search API](https://serpapi.com/search-api)

## Language Translation 📣

To resolve language barriers, I've also embedded Google's MLT to translate the crop diseases and detected pests' names to over 150 languages. This is quite important as many local farmers know the names of some crop diseases only in their local language. To maximize this, I allowed for translation on the search results, as well as the solutions proferred. Feel free to check out the library on [PyPi](https://pypi.org/project/googletrans/).


## Streamlit boilerplate
Much thanks to Tijana Nikolic who published the streamlit boiler plate tutorial used for building this app. her blogpost is published on [Medium](https://medium.com/sogetiblogsnl/streamlit-to-the-rescue-7d5f2f663465).

Thanks so much to both authors and their amazing work 🤲
