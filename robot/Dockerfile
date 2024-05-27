FROM python:3
RUN apt update && apt install -y chromium-driver
WORKDIR /robot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["robot", "tests"]
