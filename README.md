# Teltonika OwnTracks bridge

A Python module that can receive NMEA GPS data from a Teltonika router. transform it to [OwnTracks](https://owntracks.org/) format and send it to a MQTT broker.

## Installation

To build the module, run:

```
poetry install
.venv/bin/python -m teltonika_owntracks
```

Inspect `settings.py` to see how the bridge can be configured.

## How does it work?

The Python module starts a TCP packet listener that listens on a TCP port (8500) for NMEA sentences. These NMEA sentences come e.g. from a Teltonika router that has been configured to forward the NMEA GPRMC or GARMC sentences to this machine.

Don't forget to open the firewall on your computer for this particular port.

The listener will read and interpret the NMEA sentences and will convert then to OwnTracks data packets that are the sent to the configured MQTT server.

## Building docker container

The bridge can also be run in a docker container. For example:

```bash
docker buildx build . -t etxean/teltonika-owntracks --push
docker compose up -d
```

## Sending messages for testing

Using `netcat`, you can send messages to a TCP port. Start this in powershell with

```powershell
nc localhost 8500
```
