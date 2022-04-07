FROM ubuntu:18.04

RUN apt update

# Set timezone to Auckland
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y locales tzdata git
RUN locale-gen en_NZ.UTF-8
RUN dpkg-reconfigure locales
RUN echo "Pacific/Auckland" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
ENV LANG en_NZ.UTF-8
ENV LANGUAGE en_NZ:en

# Create user 'bounds' to create home directory
RUN useradd bounds
RUN mkdir -p /code
RUN ln -s /code /home/bounds
RUN chown -R bounds:bounds /code
ENV HOME /home/bounds

# Install apt packages
RUN apt update
RUN apt install -y awscli curl software-properties-common ffmpeg libsm6 libxext6
RUN add-apt-repository ppa:deadsnakes/ppa

# Install python
ENV PYTHON_VERSION 3.10
RUN apt update
RUN apt install make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev -y
RUN apt install -y python${PYTHON_VERSION}-dev python${PYTHON_VERSION}-distutils
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python${PYTHON_VERSION}
# RUN apt install libgdbm-dev uuid-dev -y

# Install python packages
RUN python${PYTHON_VERSION} -m pip install --upgrade pip
COPY requirements.txt /root/requirements.txt
RUN python${PYTHON_VERSION} -m pip install --ignore-installed PyYAML
RUN python${PYTHON_VERSION} -m pip install -r /root/requirements.txt

# Install local package
COPY computational_bound_for_bdhs /code/computational_bound_for_bdhs
COPY setup.py /code
RUN python${PYTHON_VERSION} -m pip install -e /code
ENV PYTHONPATH="/code/computational_bound_for_bdhs:${PYTHONPATH}"
