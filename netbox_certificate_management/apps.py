from django.apps import AppConfig

class AdestisCertificateManagementAppConfig(AppConfig):
    name = 'netbox_certificate_management'

    def ready(self):
        from netbox_certificate_management.jobs import CertificateMetadataExtractorJob

        CertificateMetadataExtractorJob.schedule(
            name="certificate_metadata_extractor",
            interval=15  
        )
