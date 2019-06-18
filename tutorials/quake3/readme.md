
## Quake3 Tutorial

Quake III Arena is a multiplayer-focused first-person shooter video game. The tutorial installs a quake3 server on a virtual 0-OS.

## prerequisites

- A previously [reserved 0-OS](https://github.com/threefoldfoundation/info_grid/blob/development/docs/capacity_reservation/README.md).
- A legally bought quake3 software.

## what will happen

- A filesystem volume will be created on your 0-OS.
- The pak0.pk3 of your legally bought software will be uploaded under this volume.
- The [configuration file](./quake3-server.cfg) will be uploaded under this volume.
- A container will be created using [this](https://hub.grid.tf/glendc/glendc-quake3-latest.flist) flist. The container will mount the volume path to `/data` and forward udp traffic from port 27960 on the container to the same port on the host.
- Finally, it wlll return the url the quake3 server can be accessed on.


## try and deploy the tutorial

to try supply the local location of the pak0.pk3 binary from your legally bought software and make sure a zos client called `tutorials` is created and points to the reserved 0-OS.

```bash
kosmos 'j.tutorials.quake3.run("local path to <pak0.pk3>")'
```
