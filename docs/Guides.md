# Guides

## Nötige Installationen

1. **Python** und **Python Extension Pack v1.7.0** von Don Jayamanne in **VS-Code** herunterladen
2. **Docker** installieren
3. **Todo Tree v0.0.226** herunterladen

> **Erfolg!** 🎉

---

## Venv erstellen

1. Öffne die `setup.py` Datei.
2. Klicke auf die aktuelle Python-Version in der Statusanzeige in VS-Code.
   - Wähle **Create Virtual Environment**.
   - Wähle **Venv** aus.
   - Stelle sicher, dass das Venv aktiviert ist (die Aktivierung wird in der Statusleiste angezeigt).
3. Um das virtuelle Environment zu aktivieren, öffne das Terminal und führe den entsprechenden Befehl aus.
4. Wenn du das Venv deaktivieren möchtest, kannst du es ebenfalls über das Terminal tun.

> **Tipp:** Das virtuelle Environment sollte immer aktiviert sein, wenn du mit dem Projekt arbeitest, um Abhängigkeiten zu isolieren.

> **Erfolg!** 🎉

---

## Netbox in Venv installieren

1. Gehe zu: [Netbox v4.1.11 GitHub Repository](https://github.com/netbox-community/netbox/tree/v4.1.11)
2. Klicke auf den **CODE** Button und lade die ZIP-Datei herunter.
3. Entpacke das ZIP-Archiv und navigiere zum `netbox` Ordner.
4. Kopiere alle Ordner und gehe zu:  
   `.venv/lib/python3.12/site-packages`.
5. Öffne den Ordner in einem File Explorer und füge die kopierten Ordner hier ein.

> **Erfolg!** 🎉

---

## Docker einrichten

1. Öffne das Terminal und navigiere zum Docker-Verzeichnis.
2. Baue und starte den Docker-Container.
3. In Docker: Öffne **local_docker_netbox_cars_plugin**.
4. In VS-Code: Gehe zu **Ports** und füge den Port `13000` hinzu.
5. Warte, bis der Docker-Container vollständig geladen ist.

> **Erfolg!** 🎉

---

## Netbox Community

1. Öffne im Browser: [http://localhost:13000/](http://localhost:13000/)
2. Klicke auf **Log In**.
3. Melde dich mit folgenden Zugangsdaten an:
   - **User**: admin
   - **Passwort**: admin

> **Erfolg!** 🎉

---

## Hinzufügen von neuen Feldern

### Anpassungen im Programm

1. **Felder und Fieldsets** anpassen:
   - Gehe zu: `../forms/application.py` und füge die Felder nach den Vorgaben hinzu.
2. Im **Models**:
   - Gehe zu: `../models/application.py` und ergänze die neuen Felder.
3. In den **Tabellen**:
   - Gehe zu: `../tables/application.py` und ergänze die Felder sowie `default_columns`.
4. Je nach Vorgabe:
   - Entweder die Datei `application.html` anpassen oder
   - Ein neues HTML-File unter `templates/adestis_netbox` hinzufügen.

> **Erfolg!** 🎉

---

## Anlegen der Migrations

### Entwicklungsumgebung anpassen

> **Workaround:**  
> TODO: Ersetze diesen Workaround durch eine Fehlerbehebung!

1. Im Terminal, wechsle in das Docker-Verzeichnis.
2. Kommentiere in der Datei `docker-compose.override.yml` die Zeilen für `user:` und `volumes:` aus.

3. Um Migrationen zu erstellen, führe im Terminal den Befehl:

   ```shell
   docker-compose run netbox sh -c "python manage.py makemigrations netbox_cars
   ```

> **Erfolg!** 🎉

---

## Verknüpfung mit Netbox Entities

### Anpassungen im Programm

1. **Module anpassen:**

   - Gehe zu: `../models/application.py` und importiere die benötigten Module.
   - Beispiel:
      ```python
      from tenancy.models import *
      from dcim.models import *
      from virtualization.models import *
      ```

2. **Models anpassen:**

   - Gehe zu: `../models/application.py` und füge die Entitäten nach den Vorgaben hinzu.
   - Beispiel:
     ```python
     contact = django_models.ForeignKey(
         to='tenancy.Contact',
         on_delete=django_models.PROTECT,
         related_name='logincredentials_contact',
         null=True,
         verbose_name='Contact',
         help_text='Contact that uses the System'
     )
     ```

3. **Tabellen anpassen:**

   - Gehe zu: `../tables/application.py` und ergänze die Felder sowie `default_columns`

4. **Felder und Fieldsets anpassen:**

   - Gehe zu: `../forms/application.py` und füge die Felder nach den Vorgaben hinzu.

5. **HTML-Datei anpassen:**

   - Wenn erforderlich, passe die Datei `application.html` an, um die neuen Felder in der Benutzeroberfläche anzuzeigen.

6. **Migration erstellen:**
   - Erstelle eine Migration, um die Änderungen in der Datenbank zu übernehmen.
   - Verwende den folgenden Befehl, um Migrationen zu erstellen:
     ```shell
     docker-compose run netbox sh -c "python manage.py makemigrations netbox_cars"
     ```

> **Erfolg!** 🎉

---

## Bulk Edit bearbeiten

### Anpassungen im Programm

1. **Module anpassen**

- Gehe zu: `../forms/application.py` und importiere die bönitigten Module:
- Eingabe:
  ```python
  from utilities.forms.fields import (
   TagFilterField,
   CSVModelChoiceField,
   DynamicModelChoiceField,
   DynamicModelMultipleChoiceField,
  )
  from tenancy.models import Tenant, TenantGroup
  from dcim.models import *
  from virtualization.models import *
  ```

2. **Module Anpassen**

- Gehe zu: `../forms/application.py` und füge die fields nach den Vorgaben hinzu.
- Beispiele:

  ```python
  status = forms.ChoiceField(
       required=False,
       choices=ApplicationStatusChoices,
  )

  description = forms.CharField(
       max_length=500,
       required=False,
       label=_("Description"),
  )

  virtual_machine = DynamicModelChoiceField(
       queryset=VirtualMachine.objects.all(),
       required = False,
       label = ("Virtual Machines")
  )
  ```

3. **Module Anpassen**

- Gehe zu: `../forms/application.py` und ergänze die fieldsets:
- Beispiel:

   ```python
   fieldsets = (
        FieldSet('name', 'description', 'url', 'tags', 'status', 'version', 'comments', name=_('Application')),
   )
   ```
> **Erfolg!** 🎉

---

## Import Bearbeiten
### Anpassungen im Programm

1. **Module anpassen**

- Gehe zu: `../forms/application.py` und vervollständige NetboxModelImportForm:
- Eingabe:     
   ```python
   status = CSVChoiceField(
        choices=ApplicationStatusChoices,
        help_text=_('Status'),
        required=True,
    )
    
    tenant_group = CSVModelChoiceField(
        label=_('Tenant Group'),
        queryset=TenantGroup.objects.all(),
        required=False,
        to_field_name='name',
        help_text=('Assigned tenant group')
    )
    ```
2. **Module Anpassen**

- Gehe zu: `../forms/application.py` und ergänze die fields:
- Beispiel:
   ```python
   fields = ['name' ,'status', 'description', 'url', 'tags', 'tenant', 'tenant_group', 'manufacturer', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'comments', 'version']
   ``` 

> **Erfolg!** 🎉

---

## Pypi verbindung
### Ordner erstellen

1. **Erstellung**

- Im terminal Eingeben:
   ```shell 
      sudo mkdir -p  ../../data/local_account_management_plugin/postgres
   ```
   - Danach wieder aufbauen:
   ```shell
      docker compose up --build -d
   ```
   - Danach einen Ordner zurückgehen mit:
   ```shell
      cd .. 
   ```
   - Daraufhin die nötige Instalation mit:
   ```shell
      pip install -r requirements.txt
   ```

2. **PyPi Token Erstellen**

- Auf https://pypi.org/ gehen und einen Account erstellen.
   - eine 2FA verrifizierung ist nötig 

- Unter Account settings einen Token erstellen.
- Den Recovery Code und Die Token Addrese kopieren

3. **Veröffentlichen**

- Im Terminal eingeben:
   ```shell 
   pip install  setuptools
   ```
   - Nach der Installation im Terminal:
   ```shell
   ./publish.sh 
   ```
   Eingeben und die Token Addrese einfügen. 

> **Erfolg!** 🎉

---

## Filters bearbeiten
### Anpassungen im Programm

1. **Module Anpassen**
- Gehe zu: `../forms/application.py` und vervollständige NetBoxModelFilterSetForm:
- Eingabe:     
   ```python
       status = forms.MultipleChoiceField(
        choices=ApplicationStatusChoices,
        required=False,
        label=_('Status')
    )
    
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'cluster_id': '$cluster_id',
        },
        label=_('Device')
    )
    ```
- Erweitere den fieldsets:
   ```python
      fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'url', 'tag', 'status', name=_('Application')),
        FieldSet('tenant_group_id', 'tenant_id', name=_('Tenant')),
        FieldSet('manufacturer_id', 'cluster_id', 'cluster_group_id', 'virtual_machine_id', name=_('Virtualization')),
        FieldSet('device_id', name=_('Device'))
    )
   ```

> **Erfolg!** 🎉

---

## Serializers bearbeiten
### Anpassungen im Programm 
1. **Module Anpassen**
- Gehe zu: `../serializers/application_serializer.py` und vervollständige NetBoxModelSerializer:
- Eingabe:
   ```python
         fields = ('id', 'tags', 'custom_fields', 'display', 'url', 'created', 'last_updated',
                     'custom_field_data', 'status', 'comments', 'tenant', 'tenant_group', 'manufacturer', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'description', 'version')
         brief_fields = ('id', 'tags', 'custom_fields', 'display', 'url', 'created', 'last_updated',
                           'custom_field_data', 'status', 'comments', 'tenant', 'tenant_group', 'manufacturer', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'description', 'version')
   ```

> **Erfolg!** 🎉

---

