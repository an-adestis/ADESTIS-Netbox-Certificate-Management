from django.apps import AppConfig

class AdestisCertificateManagementAppConfig(AppConfig):
    name = 'adestis_netbox_certificate_management'

    def ready(self):
        from adestis_netbox_certificate_management.jobs import CertificateMetadataExtractorJob

        CertificateMetadataExtractorJob.schedule(
            name="certificate_metadata_extractor",
            interval=15  
        )
