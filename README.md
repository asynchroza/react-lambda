# Proof of concept: Utilizing AWS Lambda to Render React Applications in the Browser

## Workflow:

In preparation for lambda deployment, a Makefile phony command initiates a Vite build and executes a python script.  
This script is responsible for uploading the generated static files to an S3 object, which will serve as a reference point within the shipped index.html file.
The Lambda function exclusively serves the static index.html file without any server-side rendering involved. The entire application is constructed on the client's side.

## Has to be figured out:

Exploring the process of uploading static files that may have the same file extension as others and referencing them within the bundled JavaScript code. One possible approach involves traversing all the code and substituting the src properties with the complete path to the corresponding S3 object. Here's an example:

```jsx
return <img src="/react.svg"/>
return <img src="https://personal-misho.s3.amazonaws/public/react.svg"/>
```