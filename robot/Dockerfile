FROM python:3
RUN apt update && apt install -y chromium-driver
WORKDIR /robot
COPY . .
RUN pip install -r requirements.txt
CMD ["robot", "tests"]
