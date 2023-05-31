FROM python:3.11-rc-bullseye
WORKDIR /opt
COPY ./app/requirements /opt/requirements
RUN \
  apt update && apt upgrade -y && \
	apt install --no-install-recommends -y nano wireless-tools tcpdump fping && \
	python3 -m pip install --upgrade pip wheel && \
	apt autoremove -y && apt clean && \
	pip3 install -r ./requirements/requirements.txt
COPY ./app .
CMD ["python3", "index.py"]
