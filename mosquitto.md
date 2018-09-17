Basic mosquitto interface
=========================


Install mosquitto
-----------------

```
yaourt -S mosquitto
go get github.com/RedBeardLab/mqtt-stereo
```

Run mosquitto
-------------

```
systemctl start mosquitto
```

Read a simple topic
-------------------

```
mosquitto_sub -h localhost -t "sensor/temperature"
```

Write on a single topic
-----------------------

```
mosquitto_pub -h localhost -t sensor/temperature -m 22.5
```

Record MQTT message:
--------------------

```
go run github.com/RedBeardLab/mqtt-stereo --topic=sensor/temperature record
```

Play MQTT message:
--------------------

```
go run github.com/RedBeardLab/mqtt-stereo --topic=sensor/temperature play
```


