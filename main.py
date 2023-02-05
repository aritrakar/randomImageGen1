import openai
import streamlit as st

from io import BytesIO
from PIL import Image
import os
import requests
import random

# os.environ["OPENAI_API_KEY"]
openai.api_key = "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"
prompt = "generate a random prompt for an ai-generated art piece"
model = "text-davinci-003"
n = 4
maxtokens = 100
temperature = 0.8


def callGPT():
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=maxtokens,
        n=n,
    )
    resp = []
    for a in range(len(response.choices)):
        resp.append(response.choices[a].text.replace('\n', ''))
    return resp


def getImageFromPrompt(prompt: str):
    response = openai.Image.create(
        prompt=prompt,
        size="512x512",
        n=1,
        response_format="url"
    )
    response = requests.get(response["data"][0]["url"])
    return Image.open(BytesIO(response.content))


def getPromptAndImage():
    with st.spinner("Loading..."):
        result = callGPT()
        chosen = random.choice(result)
        return (chosen, getImageFromPrompt(chosen))


st.title("Random image generator")
st.write("Click the button below to generate a random prompt from ChatGPT and a corresponding image from DALL-E.")

if st.button("Get random prompt"):
    (chosen, image) = getPromptAndImage()
    st.write(f"#### **Prompt: {chosen}**")
    st.image(image, use_column_width=True)
