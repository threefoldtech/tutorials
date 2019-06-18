
## Filestash Tutorial

Filestash is a Dropbox-like file manager that let you manage your data anywhere it is located.
This tutorial will create a container running filestash and minio.

## prerequisites

- A previously [reserved 0-OS](https://github.com/threefoldfoundation/info_grid/blob/development/docs/capacity_reservation/README.md).

## what will happen

- A filesystem volume will be created on your 0-OS.
- A container will be created using [this](https://hub.grid.tf/tf-official-apps/filestash_with_minio_autostart.flist) flist. The container will mount the volume path to `/data` and forward traffic from port 9000 and 8334 on the container to the same port on the host.
- The flist has will autostart both filestash and minio and the minio credentials will be minio_admin/minio_password.
- Finally, it wlll return the url the filestash and minio server can be accessed on.


## try and deploy the tutorial

to try make sure a zos client called `tutorials` is created and points to the reserved 0-OS.

```bash
kosmos 'j.tutorials.filestash.run()'
```
