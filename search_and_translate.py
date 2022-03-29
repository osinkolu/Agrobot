# -*- coding: utf-8 -*-
"""
Created on Friday January 14 1:27:03 2022
Created to search and translate search results in other languages.

@author: Olufemi Victor tolulope. @osinkolu on github.

Helper script with functions to call google's seach and translate libraries.
"""

from serpapi import GoogleSearch
from googletrans import Translator
translator = Translator()
def search_and_translate(search_string, dest_language):
  params = {
    "q": search_string,
    "hl": "en",
    "gl": "us",
    "api_key": "29a59059862fcd77aa92adc11a1b1db2e7edf7faa028ec0080c27e3df3dcca76"
  }

  search = GoogleSearch(params)
  results = search.get_dict()

  try:
    answers = (results['knowledge_graph']['description'])
  except Exception:
    try:
      answers = (results["answer_box"]["snippet"] + "\n" + "\n".join(results["answer_box"]["list"]).replace("...","") )
    except Exception:
      try:
        answers = (results["answer_box"]["snippet"])
      except Exception:
        try:
          answers = (results["organic_results"][0]["snippet"])
        except Exception:
          answers = ("No results found")
  if search_string.split()[-1] == "Nothing":
    return(translator.translate("I'm sorry I didn't find anything. Kindly refer to the list of possible detections above, or reduce the threshold in settings.Thanks for your understanding.", dest=dest_language, src= 'en').text)
  else:
    return(translator.translate(answers, dest=dest_language, src= 'en').text)

def translate_alone(answers,dest_language):
  return(translator.translate(answers, dest=dest_language, src= 'en').text)
