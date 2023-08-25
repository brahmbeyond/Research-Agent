
from dotenv import find_dotenv, load_dotenv
import json
import requests
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains.llm import LLMChain

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


# 3. get get content from ach urls 
def get_content_from_urls(urls):
  loader = UnstructuredURLLoader(urls=urls)
  data = loader.load()
  print(data)
  return data

# 4. summarise them by dividing into smaller chunks
def summary(data,query):
  text_splitter = CharacterTextSplitter(
    separator = "\n\n",
    chunk_size = 3000,
    chunk_overlap  = 200,
    length_function = len,
  )
  text = text_splitter.split_documents(data)

  llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=.7)
  template = """
   {text}
   You are a world class journalist, and you have to summarise the text above in one sentence only in order to create a twitter thread about {query}
   Please follow all of the following rules:
   1/ Make sure the content is engaging, informative with good data
   2/ Make sure the content is very very short(like only a  sentence ), it should be no more than 3-5 tweets
   3/ The content should address the {query} topic very well
   4/ The content needs to be viral, and get at least 1000 likes
   5/ The content needs to be written in a way that is easy to  read and understand
   6/ The content needs to give audience actionable advice and insights too
   and again last and most important keep it very short(like only a  sentence )
  SUMMARY:
  """

  prompt_template = PromptTemplate(
        input_variables=["text", "query"], template=template
    )

  summariser_chain = LLMChain(
      llm=llm, prompt=prompt_template, verbose=True
    )
  summaries= []

  for chunk in enumerate(text):
    summary = summariser_chain.predict(text=chunk,query=query)
    summaries.append(summary)

  print(summaries)
  return summaries

# 5. Create Twittr thread

def write_twitter_thread(summaries,query):

  sumaaries_str = str(summaries)

  llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=.7)
  template = """
   {sumaaries_str}
  You are a world class journalist & twitter influencer, text above is sore context about (query)
   Please write a viral twitter thread about (query) using the text above, and following all rules below:
    1/ The thread needs to be engaging, informative with good data
    2/ The thread needs to be around than 3-5 tweets
    3/ The thread needs to address the (query) topic very well
    4/ The thread needs to be viral, and get at least 1000 likes
    5/The thread needs to be written in away that is easy to read and understand
    6/ The thread needs to give audience actionable advice & insights too
  TWITTER THREAD:

  """

  prompt_template = PromptTemplate( input_variables=["sumaaries_str"], template=template )

  twitter_thread_chain = LLMChain(
      llm=llm, prompt=prompt_template, verbose=True
    )
  twitter_thread = twitter_thread_chain.predict(sumaaries_str=sumaaries_str,query=query)
  print(twitter_thread)
  return twitter_thread

searchResult = search(query)
bestUrls = find_best_article_urls(searchResult,query)
content = get_content_from_urls(bestUrls)
summaryResult = summary(content,query)
thread = write_twitter_thread(summaryResult,query)

    
