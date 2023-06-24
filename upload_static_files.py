import os
from botocore.exceptions import NoCredentialsError
import boto3

os.environ["BUCKET_NAME"] = "personal-misho"

text_type_extensions = {"css": "css", "js": "javascript"}

image_type_extensions = {"svg": "svg+xml"}


def replace_urls_in_html(html, urls):
    # TODO: add support for static files which can be more than one
    # e.g. .svg .png 
    # TODO: figure out how to work with the public directory

    for url in urls:
        url_parts = url.split("?")
        file_name = url_parts[0].split("/")[-1]
        # href = f"{'/assets' if file_name.split('.')[-1] in text_type_extensions.keys() else ''}/{file_name}"

        # ! supports only .css and .js 
        href = f"/assets/{file_name}"
        html = html.replace(
            href,
            url
        )

    return html


"""
Cors policy for bucket:

[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "HEAD"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": [],
        "MaxAgeSeconds": 3000
    }
]
"""


def upload_to_aws(local_file, s3_file):
    s3 = boto3.client("s3")

    extension = local_file.split(".")[-1]

    content_type = ""

    if extension in text_type_extensions.keys():
        content_type = f"text/{text_type_extensions.get(extension)}"
    elif extension in image_type_extensions.keys():
        content_type = f"image/{image_type_extensions.keys()}"

    try:
        s3.upload_file(
            local_file,
            os.environ["BUCKET_NAME"],
            s3_file,
            ExtraArgs={"ContentType": content_type},
        )
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": os.environ["BUCKET_NAME"], "Key": s3_file},
            ExpiresIn=24 * 3600,
        )

        print("Upload Successful", url)
        return url
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None


def main():
    build_dir = "react/dist/assets"
    urls = []

    for file_name in os.listdir(build_dir):
        local_file = os.path.join(build_dir, file_name)
        urls.append(upload_to_aws(local_file, file_name))

    html = open("react/dist/index.html", "r").read()

    html = replace_urls_in_html(html, urls)
    with open("src/index.html", "w") as file:
        file.write(html)


if __name__ == "__main__":
    main()
