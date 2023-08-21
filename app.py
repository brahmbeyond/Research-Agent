import os
import json
from dotenv import find_dotenv, load_dotenv
import requests
from langchain import OpenAI, LLMChain, PromptTemplate
import openai

load_dotenv(find_dotenv())
SERPAPI_API_KEY = os.getenv("SERPER_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

query = "how did jeff bezoss get rich?"

# 1. serp req. to get list of releveant articles


def search(query):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    }
    )
    headers = {
        'X-API-KEY': SERPAPI_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = response.json()
    # print("search results :", response_data)
    return response_data
# search(query)


# 2. llm to choose best articles and return urls
def find_best_article_urls(response_data, query):
    response_str = json.dumps(response_data)

    llm = OpenAI(model_name="gpt-3.5-turbo", temperature=.7)
    template = """
    Your are a world class journalist & researcher, you are extremely good at finding most relevant articles to certain topics;
    {response_str}
    Above is the list of search results for the query {query}.
    Pleas choose the besrt 3 articles from trhe list , return ONLY an array of the urls , do not include anything else
    """

    prompt_template = PromptTemplate(
        input_variables=["response_str", "query"], template=template
    )

    article_picker_chain = LLMChain(
        llm=llm, prompt=prompt_template, verbose=True
    )
    urls = article_picker_chain.predict(response_str=response_str, query=query)

    url_list = json.loads(urls)
    # print(url_list)
    return url_list


# 3. get get content from ach urls and summarise them
# def get_content_from_urls(urls):
#     loader = UnstructuredURLLoader(urls=urls)
#     data = loader.load()
#     return data


results = search(query)
urls = find_best_article_urls(results, query)
print(urls)
# data = get_content_from_urls(urls)
# print(data)
