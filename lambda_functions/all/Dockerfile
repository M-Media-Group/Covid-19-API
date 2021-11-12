FROM public.ecr.aws/lambda/python:3.8

COPY main.py get_countries.py requirements.txt ./

RUN python3.8 -m pip install -r requirements.txt -t .

# Command can be overwritten by providing a different command in the template directly.
CMD ["main.lambda_handler"]
