# NetBox Account Management

A NetBox plugin for managing the ownership of accounts.
Netbox `v3.5-2.6.1` is required.

## PIP Package

[Click here](https://pypi.org/project/adestis-netbox-certificate/)

## Development instructions

[Click here](DEVELOPMENT.md)

## Installation with Docker

The Plugin may be installed in a Netbox Docker deployment.
The package contains a Dockerfile for [Netbox-Community Docker](https://github.com/netbox-community/netbox-docker)
extension.

Download the Plugin and build from the source:

```
$ git clone https://github.com/adestis/netbox-account-management
$ cd adestis-netbox-certificate
$ docker build -f Dev-Dockerfile -t adestis-netbox-certificate-plugin .
```

Update a netbox image name in **docker-compose.yml** in a Netbox Community Docker project root:

```yaml
services:
  netbox: &netbox
    image: adestis-netbox-certificate-plugin:latest
```

Rebuild the running docker containers:

  ```bash
  cd netbox-docker
  docker-compose down
  docker-compose up -d
  ```

Stop the application container. Then add PLUGINS parameter and PLUGINS_CONFIG parameter to **configuration.py**. It is
stored in netbox-docker/configuration/ by default:

```python
PLUGINS = ['adestis_netbox_certificate_management']
```

After that you can start the application again and check the swagger file on `http://localhost:13000/api/schema/swagger-ui/` or access the graphql api on `http://localhost:13000/graphql/` !

## Common pitfalls

### I can not build the python package on my windows machine

Remove the MAX_PATH limitation (see https://docs.python.org/3/using/windows.html#removing-the-max-path-limitation)

### How to create a migration

Mount the migrations folder, start the infrastructure services and run `docker-compose run netbox sh -c "python manage.py makemigrations adestis_netbox_certificate_management"`. After that unmount the migrations folder and rebuild the docker container

## FAQ

### Why do I have Problems publishing the package to pypi with windows?

You must adjust the file path limit in the registry

### How can I import SSH Keys using the netbox csv import function?

Remark: If you leave the contact column empty, you do not assign to a contact.

Prepare a csv file (like the example below) and import it with the netbox import function on the ssh keys page:

```csv
contact,ssh_key_current_status,ssh_key_desired_status,raw_ssh_key,valid_from,valid_to
,active,active,ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJQ3Ggtvlqhg5pym5V2fnyf8qyNxqCAYFNIiKbKF1VO3 workstation,2024-09-01,2024-09-10
,active,active,ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMYuQ8o1+JEH7lzC5Q+tvVU3XVPXG8vpyxrxeb5uVYLj notebook,2024-09-01,2024-09-10
```

## Screenshots

![Login credentials](docs/login_credentials.png)
