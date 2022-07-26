import json
import requests
import pandas as pd


def get_products_of_week():
    """Function that queries Product Hunt to get specific
    information and returns a JSON with the result"""
    API_URL = "https://api.producthunt.com/v2/api/graphql"
    # Specify your API token
    MY_API_TOKEN = "Secret"

    # Specify your query
    query = {"query": """
    query MostVotedProducts {
      posts (postedAfter: "2022-07-14T00:01:00Z", order: VOTES) {
        edges {
          node {
            name
            tagline
            description
            url
            votesCount
            user {
              username
              twitterUsername
              websiteUrl
            }
            productLinks {
              url
            }
            topics {
              edges {
                node {
                  name
                }
              }
            }
            createdAt
          }
        }
      }
    }
    """}

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + MY_API_TOKEN,
        'Host': 'api.producthunt.com'
    }

    posts = requests.post(API_URL,
                                headers=headers,
                                data=json.dumps(query))

    posts = posts.json()
    return posts


def organize_info_to_df():
    """Function that normalizes the information received
    from Product Hunt and returns a Pandas DataFrame"""
    posts = get_products_of_week()
    data = []

    for p in posts.get("data").get("posts").get("edges"):
        product = p.get("node")
        t = product.get("topics").get("edges")
        topics = [topic.get("node").get("name") for topic in t]
        tw = product.get('user').get('twitterUsername')

        data.append({
            "Product name": product.get("name"),
            "Tagline": product.get("tagline"),
            "Description": product.get("description"),
            "Post URL": product.get("url"),
            "Votes": product.get("votesCount"),
            "Username": product.get("user").get("username"),
            "Twitter": f"https://twitter.com/{tw}" if tw is not None else "",
            "User website": product.get("user").get("websiteUrl"),
            "Product website": product.get("productLinks")[0].get("url"),
            "Topics": ','.join(topics),
            "Post created at": product.get("createdAt")
        })

    df = pd.DataFrame(data)

    return df
