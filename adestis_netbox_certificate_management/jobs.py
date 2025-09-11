import time
import json
from adestis_netbox_certificate_management.models import Certificate
from core.choices import JobIntervalChoices
from netbox.jobs import JobRunner, system_job
from django.forms.models import model_to_dict
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
from cryptography.x509.extensions import ExtensionNotFound

class CertificateMetadataExtractorJob(JobRunner):
    class Meta:
        name = "Zertifikats-Metadaten extrahieren"
        model = Certificate 
        
    def run(self, *args, **kwargs):
        time.sleep(2)
        for certificate in Certificate.objects.all():
            self.clean_and_extract(certificate)
        
        for certificate in Certificate.objects.all():
            self.extract_and_set_fields(certificate)
        
        for certificate in Certificate.objects.all():
            self.set_predecessor_certificate(certificate)
        



    def clean_and_extract(self, certificate: Certificate): 
        cert_text = certificate.certificate
        x509cert = x509.load_pem_x509_certificate(certificate.certificate.encode('utf-8'), default_backend())               
        match = re.findall(r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----", cert_text, flags=re.DOTALL) 
        if not match:
            raise ValidationError("No valid certificate found in file")
        
        # Take the first certificate in the chain as the base (main) certificate        
        base_cert = match.pop(0)
        
        subject_key_identifier = x509cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_KEY_IDENTIFIER)
        subject_hex = subject_key_identifier.value.digest.hex()
    
        certificate.subject_key_identifier = subject_hex
        
        cert_data = cert_utils.parse_cert(base_cert)
        issuer = cert_data["issuer"].replace("\n", ";").strip()
        
        issuer = cert_data["issuer"]
        for name,value in [ (pair.split("=")) for pair in cert_data["issuer"].split("\n") ]:
            if name == "CN":
                issuer=value
        
            
        common_name = cert_data["subject"]
        for name,value in [ (pair.split("=")) for pair in cert_data["subject"].split("\n") ]:
            if name == "CN":
                common_name=value
            
        certificate.certificate = base_cert
        certificate.valid_from=cert_data["startdate"].date()
        certificate.valid_to=cert_data["enddate"].date()
        certificate.name = common_name
        certificate.issuer=issuer
        certificate.subject=common_name
        certificate.key_technology=cert_data["key_technology"]
        certificate.subject_alternative_name=cert_data.get("SubjectAlternativeName", "")
        certificate.save()
        
        certificate.save(update_fields=["valid_from", "valid_to", "subject", "issuer", "subject_alternative_name", "key_technology"])
        
        # Process any additional certificates in the chain (e.g., intermediates)
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

                # Avoid saving duplicates — skip if this cert already exists
                existing = Certificate.objects.filter(certificate=extra_cert).first()
                if existing:
                    continue

                new_cert = Certificate.objects.create(
                        certificate=extra_cert,
                        name=extra_common_name,
                        subject_key_identifier=extra_subject_key_identifier
                )
            
    def set_predecessor_certificate(self, certificate: Certificate):
            x509cert = x509.load_pem_x509_certificate(certificate.certificate.encode("utf-8"), default_backend())
            
            try:
                authority_identifier = x509cert.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_KEY_IDENTIFIER)
                authority_hex = authority_identifier.value.key_identifier.hex()
                
                certificate.authority_identifier = authority_hex
                
                subject_key_identifier = x509cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_KEY_IDENTIFIER)
                subject_hex = subject_key_identifier.value.digest.hex()
        
                certificate.subject_key_identifier = subject_hex
                
                
                issuer_parent_certificate = Certificate.objects.filter(
                    subject_key_identifier=authority_hex
                ).first()
                
                certificate.authority_key_identifier = issuer_parent_certificate
                certificate.save(update_fields=["authority_key_identifier", "subject_key_identifier", "authority_identifier"])
                
            except ExtensionNotFound:
             return
            
            
    def extract_and_set_fields(self, certificate: Certificate):
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

