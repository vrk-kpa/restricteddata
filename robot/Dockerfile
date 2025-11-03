FROM python:3.12
RUN apt update && apt install -y chromium-driver
WORKDIR /robot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["robot", "-d", "results", "tests"]
