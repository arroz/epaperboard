curl -d 'state=OK' http://localhost:8080/entry/build.status
curl -d 'state=WARNING' -d 'message=Security updates available' http://localhost:8080/entry/server1.pkg-audit
curl -d 'state=OK' http://localhost:8080/entry/server1.thermals
curl -d 'state=OK' http://localhost:8080/entry/server2.pkg-audit
curl -d 'state=CRITICAL' -d 'message=CPU is on fire!' http://localhost:8080/entry/server2.thermals
curl -d 'state=OK' http://localhost:8080/entry/router.lan
curl -d 'state=OK' http://localhost:8080/entry/router.wan
curl -d 'state=OK' -d 'message=Ping time: 4ms' http://localhost:8080/entry/external.ping
curl -d 'state=CRITICAL' -d 'message=No food left, cat is hungry!' http://localhost:8080/entry/cat.food
curl -d 'state=WARNING' -d 'message=Cat water running low.' http://localhost:8080/entry/cat.water
curl -d 'state=OK' http://localhost:8080/entry/furnace.alarm
