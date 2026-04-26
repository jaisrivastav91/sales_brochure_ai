import json
from .scraper import Website
from IPython.display import Markdown, display, update_display


link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""


brochure_system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
"""


def get_links_user_prompt(w: Website):
    user_prompt = f"""
Here is the list of links on the website {w.url} -
Please decide which of these are relevant web links for a brochure about the company,
respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links:

"""
    user_prompt += "\n".join(w.links)
    return user_prompt


def select_relevant_links(client, model, w: Website):
    print(f"Selecting relevant links for {w.url} by calling {model}")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(w)},
        ],
        response_format={"type": "json_object"},
    )
    result = response.choices[0].message.content or '{"links":[]}'
    links = json.loads(result)
    print(f"Found {len(links.get('links', []))} relevant links")
    return links


def fetch_page_and_all_relevant_links(client, model, w: Website):
    landing = w.contents
    relevant_links = select_relevant_links(client, model, w)

    result = f"## Landing Page:\n\n{landing}\n## Relevant Links:\n"
    # for link in relevant_links.get("links", []):
    #     link_type = link.get("type", "relevant page")
    #     link_url = link.get("url")
    #     if not link_url:
    #         continue
    #     try:
    #         linked_site = Website(link_url)
    #         result += f"\n\n### Link: {link_type}\n"
    #         result
    for link in relevant_links['links']:
        result += f"\n\n### Link: {link['type']}\n"
        result += link.get("url", "No URL provided")
    return result


def get_brochure_user_prompt(client, model, w: Website):
    user_prompt = f"""
You are looking at a company called: {w.name}
Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.
"""
    user_prompt += fetch_page_and_all_relevant_links(client, model, w)
    user_prompt = user_prompt[:5_000]  # truncate long prompt
    return user_prompt

def create_brochure(client, model, w: Website):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(client, model, w)},
        ],
    )
    display(Markdown(response.choices[0].message.content or ""))

def stream_brochure(client, model, w: Website):
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(client, model, w)},
        ],
        stream=True,
    )    
    response = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        update_display(Markdown(response), display_id=display_handle.display_id)
