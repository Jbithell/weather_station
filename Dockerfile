FROM resin/%%RESIN_MACHINE_NAME%%-python

RUN apt-get update && apt-get install -yq python3-pip && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

RUN pip3 install gpiozero RPi.GPIO thingspeak

COPY . ./

ENV INITSYSTEM on

CMD ["bash","src/main.bash"]