
## Ownhub Tutorial

Allow people to create their own hub: create flist + launch script which launches container who has everything which hub has so people can use this to develop full life cycle management

## prerequisites
- itsyouonline client (id and secret)
- zos client (remote node)

## what will happen
- you can deploy your ownhub locally or on remote zos container
- get odoo builder's flist and deploy it to a zos container
- merge flists on zhub and ownhub

## try and deploy the tutorial
to run: 
```bash
kosmos 'j.tutorials.ownhub.run()'
```
to cleanup:
```bash
kosmos 'j.tutorials.ownhub.cleanup()'
