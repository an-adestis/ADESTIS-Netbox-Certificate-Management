# NetBox Certificate Plugin

The **NetBox Certificate Plugin** extends NetBox with the ability to manage certificates and link them to various existing NetBox objects.

In addition to manually creating certificates, the plugin supports importing entire certificate bundles (e.g., PEM files). During the import process, certificates are automatically parsed, relevant data is extracted, and associations with appropriate NetBox objects are created automatically.

The plugin also provides a clean and structured UI to display all key certificate details and allows flexible associations with various NetBox objects such as systems, clusters, tenants, and more.

---

## 🚀 Features

- Manage certificates directly within NetBox
- Import entire certificate bundles with automatic processing
- Automatic extraction of key certificate information (e.g. subject, issuer, validity, key technology, etc.)
- Flexible association of certificates with existing NetBox objects
- Clean and structured UI integration

---
## Screenshots

![Certificates Details](https://github.com/an-adestis/ADESTIS-Netbox-Certificate-Management/blob/initialize_app/img01.png)
![Certificates View](https://github.com/an-adestis/ADESTIS-Netbox-Certificate-Management/blob/initialize_app/img02.png)

## ⚙️ Installation

The plugin is available on PyPI and can be installed via pip:

```bash
pip install adestis-netbox-certificate-management
```

## ✅ Compatibility

> **Note**: This plugin depends on the [`adestis-netbox-applications`](https://pypi.org/project/adestis-netbox-applications/) plugin.  
> Therefore, its compatibility is directly tied to the NetBox version used in the base image.

The plugin is developed and tested using the following base image:

```dockerfile
ARG FROM_TAG=v4.2.9-3.2.1  # NetBox v4.2.9
```
