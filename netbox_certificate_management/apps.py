from django.apps import AppConfig

class AdestisCertificateManagementAppConfig(AppConfig):
    name = 'adestis_netbox_certificate_management'

    def ready(self):
        # Import erst hier drin, damit Models & Registry bereit sind
        from netbox_certificate_management.jobs import CertificateMetadataExtractorJob

        CertificateMetadataExtractorJob.schedule(
            name="certificate_metadata_extractor",
            interval=15  
        )
