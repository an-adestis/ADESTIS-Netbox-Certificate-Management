import time

from adestis_netbox_certificate_management.models import Certificate
import logging

from core.choices import JobIntervalChoices
from netbox.jobs import JobRunner, system_job

from django.core.exceptions import ValidationError
import cert_utils 
import hashlib
import re
from django.shortcuts import get_object_or_404, redirect, render
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import ExtensionOID
from django.utils.translation import gettext_lazy as _
import logging

class CertificateMetadataExtractorJob(JobRunner):
    class Meta:
        name = "Zertifikats-Metadaten extrahieren"
        model = Certificate 
        
    def run(self, *args, **kwargs):
        time.sleep(2)

        
        created = []
        for certificate in Certificate.objects.all():
            cert_text = certificate.certificate
                        
            match = re.findall(r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----", cert_text, flags=re.DOTALL) # mit re.DOTALL werden Zeilenumbrüche (\n) mit eingebunden
            if not match:
                raise ValidationError("No valid certificate found in file")
            
            base_cert = match.pop(0)
            cleaned_cert = base_cert.replace("\r\n", "").replace("\n", "").strip()
            cert_data = cert_utils.parse_cert(base_cert)
            
            subject_key_identifier = cert_data.get("subject_key_identifier")
            if not subject_key_identifier:
                subject_key_identifier = hashlib.sha1(cleaned_cert.encode()).hexdigest()
            
            common_name = cert_data["subject"]
            for name,value in [ (pair.split("=")) for pair in cert_data["subject"].split("\n") ]:
                if name == "CN":
                    common_name=value
            
            certificate.certificate = base_cert
            certificate.name = common_name
            certificate.subject_key_identifier = subject_key_identifier
            certificate.save()
            
            while match:
                extra_cert = match.pop(0)
                cleaned_extra = extra_cert.replace("\r\n", "").replace("\n", "").strip()
                extra_data = cert_utils.parse_cert(extra_cert)

                extra_subject_key_identifier = extra_data.get("subject_key_identifier")
                if not extra_subject_key_identifier:
                    extra_subject_key_identifier = hashlib.sha1(cleaned_extra.encode()).hexdigest()

                extra_common_name = extra_data["subject"]
                for name,value in [ (pair.split("=")) for pair in extra_data["subject"].split("\n") ]:
                    if name == "CN":
                        extra_common_name=value

                existing = Certificate.objects.filter(certificate=extra_cert).first()
                if existing:
                    continue

                new_cert = Certificate.objects.create(
                    certificate=extra_cert,
                    name=extra_common_name,
                    subject_key_identifier=extra_subject_key_identifier
                )
                created.append(new_cert)
            
        for certificate in Certificate.objects.all():
                x509cert = x509.load_pem_x509_certificate(certificate.certificate.encode('utf-8'), default_backend())
                        
                subject_key_identifier = x509cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_KEY_IDENTIFIER)
                subject_hex = subject_key_identifier.value.digest.hex()
    
                certificate.subject_key_identifier = subject_hex
                
                cert_data = cert_utils.parse_cert(certificate.certificate)
                issuer = cert_data["issuer"].replace("\n", ";").strip()
                common_name = cert_data["subject"]
                for name,value in [ (pair.split("=")) for pair in cert_data["subject"].split("\n") ]:
                    if name == "CN":
                        common_name=value

                certificate.valid_from=cert_data["startdate"].date()
                certificate.valid_to=cert_data["enddate"].date()
                certificate.issuer=issuer
                certificate.subject=common_name
                certificate.key_technology=cert_data["key_technology"]
                certificate.subject_alternative_name=cert_data.get("SubjectAlternativeName", "")

                
                certificate.save(update_fields=["subject_key_identifier", "authority_key_identifier", "valid_from", "valid_to", "subject", "issuer", "subject_alternative_name", "key_technology"])

        for certificate in Certificate.objects.all():
            x509cert = x509.load_pem_x509_certificate(certificate.certificate.encode("utf-8"), default_backend())

            authority_identifier = x509cert.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_KEY_IDENTIFIER)
            authority_hex = authority_identifier.value.key_identifier.hex()

            subject_key_identifier = x509cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_KEY_IDENTIFIER)
            subject_hex = subject_key_identifier.value.digest.hex()
    
            certificate.subject_key_identifier = subject_hex
            
            certificate.authority_identifier = authority_hex
            issuer_parent_certificate = Certificate.objects.filter(
                subject_key_identifier=authority_hex
            ).first()
            
            successor_certificates = Certificate.objects.filter(
                authority_identifier=subject_hex
            )
            

            certificate.successor_certificate.set(successor_certificates)
            certificate.authority_key_identifier = issuer_parent_certificate
            certificate.save(update_fields=["authority_key_identifier", "subject_key_identifier", "successor_certificates", "authority_identifier"])