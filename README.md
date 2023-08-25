
# Script for Extracting Article Summaries and Creating Twitter Threads

This script is designed to automate the process of searching for relevant articles, extracting content, generating summaries, and creating Twitter threads based on a given query.

> see the 'shared_research_agent.ipynb' file , its Google Colab Notebook , you can chck it out directly .
And Prepare Open AI and SERPER API key beforhand

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Warnings and Tips](#warnings-and-tips)
- [Extras](#extras)

## Installation

Before running the script, make sure you have the necessary dependencies installed. You can install them using the following command:

```bash
!pip install openai langchain playwright beautifulsoup4 unstructured[local-inference] requests
```

Also, update the OpenAI API key and other necessary keys in the script before running it.

## Usage

1. **Define OPEN AI API Key**: Set your OpenAI API key in the appropriate section of the script.

2. **Search Query**: Modify the `query` variable to specify the topic you want to search for.

3. **Running the Script**: Run the script step by step, following the provided instructions and waiting for a minute or two between functions if you encounter a "RateLimitError."

4. **View Results**: The script will output the extracted article content and the generated Twitter thread.

## Dependencies

- [openai](https://pypi.org/project/openai/): Python client for the OpenAI GPT-3 API.
- [langchain](https://pypi.org/project/langchain/): A library for working with AI models, text generation, and more.
- [playwright](https://pypi.org/project/playwright/): A browser automation library for Python.
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/): HTML parsing and data extraction library.
- [unstructured](https://pypi.org/project/unstructured/): A toolkit for text analysis and extraction.
- [requests](https://pypi.org/project/requests/): A library for making HTTP requests.

## Warnings and Tips

- If you encounter a "RateLimitError" from the OpenAI API, wait for a minute or two before running the script again.

## Extras

If you're facing any issues, consider running each function individually, waiting a bit between executions.

Feel free to customize and enhance this readme with additional information, explanations, usage examples, and any other relevant details. This will help anyone who comes across your script to understand its purpose and functionality.
