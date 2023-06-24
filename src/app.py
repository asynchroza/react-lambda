def replace_urls_in_html(html, urls):
    for url in urls:
        url_parts = url.split("?")
        file_name = url_parts[0].split("/")[-1]
        html = html.replace(file_name, url)

    return html
    

def lambda_handler(event, context):
    html = ""

    try:
        html = open("index.html", "r").read()
    
    except Exception as e:
        print(e)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": html
    }
