import time
import json
import logging
from adestis_netbox_certificate_management.models import Certificate, CertificateStatusChoices
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
from cryptography.x509.extensions import ExtensionNotFound

from datetime import datetime, date, timedelta

logger = logging.getLogger(__name__)

class CertificateMetadataExtractorJob(JobRunner):
    class Meta:
        name = "Zertifikats-Metadaten extrahieren"
        model = Certificate 

    def run(self, *args, **kwargs):
        time.sleep(2)

        certificates = list(Certificate.objects.all().order_by("id"))

        for certificate in certificates:
            try:
                self.clean_and_extract(certificate)
            except Exception as e:
                logger.error(f"[clean_and_extract] Fehler bei Certificate ID {certificate.id}: {e}")

        for certificate in certificates:
            try:
                self.extract_and_set_fields(certificate)
            except Exception as e:
                logger.error(f"[extract_and_set_fields] Fehler bei Certificate ID {certificate.id}: {e}")

        for certificate in certificates:
            try:
                self.set_predecessor_certificate(certificate)
            except Exception as e:
                logger.error(f"[set_predecessor_certificate] Fehler bei Certificate ID {certificate.id}: {e}")

        today = date.today()
        for certificate in certificates:
            # Objekt neu aus DB laden, damit Status aktuell ist
            certificate.refresh_from_db()
            if certificate.valid_to is None or certificate.valid_to < today:
                certificate.status = CertificateStatusChoices.STATUS_INVALIDE
                logger.warning(f"Status -> INVALIDE für Certificate ID {certificate.id}")
            else:
                certificate.status = CertificateStatusChoices.STATUS_ACTIVE
                logger.info(f"Status -> ACTIVE für Certificate ID {certificate.id}")

            certificate.save(update_fields=["status"])

    def clean_and_extract(self, certificate: Certificate): 
        cert_text = certificate.certificate

        logger.debug(f"[clean_and_extract] Starte für Certificate ID {certificate.id}")

        match = re.findall(
            r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----", 
            cert_text, flags=re.DOTALL
        ) 

        if not match:
            raise ValidationError(f"Certificate ID {certificate.id}: Kein gültiges PEM-Zertifikat gefunden")

        base_cert = match.pop(0)

        # Subject Key Identifier auslesen
        try:
            x509cert = x509.load_pem_x509_certificate(
                base_cert.encode('utf-8'),
                default_backend()
            )
            ski = x509cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_KEY_IDENTIFIER)
            certificate.subject_key_identifier = ski.value.digest.hex()
            logger.debug(f"[clean_and_extract] SKI gesetzt für ID {certificate.id}")
        except ExtensionNotFound:
            logger.warning(f"[clean_and_extract] Kein SKI in Certificate ID {certificate.id}")
        except Exception as e:
            logger.error(f"[clean_and_extract] Fehler beim SKI-Auslesen für ID {certificate.id}: {e}")

        # Metadaten per cert_utils auslesen
        try:
            cert_data = cert_utils.parse_cert(base_cert)
            logger.error(f"[cert_data Längen] ID {certificate.id}: { {k: len(str(v)) for k, v in cert_data.items()} }")
        except Exception as e:
            logger.error(f"[clean_and_extract] cert_utils.parse_cert FEHLGESCHLAGEN für ID {certificate.id}: {e}")
            raise

        issuer = cert_data.get("issuer", "")
        for pair in issuer.split("\n"):
            if "=" in pair:
                name, value = pair.split("=", 1)
                if name == "CN":
                    issuer = value

        common_name = cert_data.get("subject", "")
        for pair in common_name.split("\n"):
            if "=" in pair:
                name, value = pair.split("=", 1)
                if name == "CN":
                    common_name = value

        certificate.certificate = base_cert
        certificate.valid_from = cert_data.get("startdate").date() if cert_data.get("startdate") else None
        certificate.valid_to = cert_data.get("enddate").date() if cert_data.get("enddate") else None
        certificate.name = common_name
        certificate.issuer = issuer
        certificate.subject = common_name
        certificate.key_technology = cert_data.get("key_technology", "")
        certificate.subject_alternative_name = cert_data.get("SubjectAlternativeName", "")

        certificate.save(update_fields=[
            "certificate",
            "subject_key_identifier",
            "valid_from",
            "valid_to",
            "name",
            "issuer",
            "subject",
            "key_technology",
            "subject_alternative_name",
        ])
        logger.debug(f"[clean_and_extract] Gespeichert für ID {certificate.id}")

        # Zusätzliche Zertifikate in der Datei verarbeiten
        while match:
            extra_cert = match.pop(0)
            extra_data = cert_utils.parse_cert(extra_cert)

            extra_common_name = extra_data.get("subject", "")
            for pair in extra_common_name.split("\n"):
                if "=" in pair:
                    name, value = pair.split("=", 1)
                    if name == "CN":
                        extra_common_name = value

            existing = Certificate.objects.filter(certificate=extra_cert).first()
            if existing:
                continue

    def set_predecessor_certificate(self, certificate: Certificate):
        logger.debug(f"[set_predecessor] Starte für Certificate ID {certificate.id}")
        try:
            x509cert = x509.load_pem_x509_certificate(
                certificate.certificate.encode("utf-8"), 
                default_backend()
            )
            
            authority_identifier = x509cert.extensions.get_extension_for_oid(
                ExtensionOID.AUTHORITY_KEY_IDENTIFIER
            )
            authority_hex = authority_identifier.value.key_identifier.hex()
            certificate.authority_identifier = authority_hex

            subject_key_identifier = x509cert.extensions.get_extension_for_oid(
                ExtensionOID.SUBJECT_KEY_IDENTIFIER
            )
            subject_hex = subject_key_identifier.value.digest.hex()
            certificate.subject_key_identifier = subject_hex

            issuer_parent_certificate = Certificate.objects.filter(
                subject_key_identifier=authority_hex
            ).first()

            if issuer_parent_certificate:
                certificate.authority_key_identifier = issuer_parent_certificate
                logger.debug(f"[set_predecessor] Parent gefunden für ID {certificate.id}: {issuer_parent_certificate.id}")
            else:
                logger.warning(f"[set_predecessor] Kein Parent gefunden für ID {certificate.id} (authority_hex={authority_hex})")

            certificate.save(update_fields=[
                "authority_key_identifier", 
                "subject_key_identifier", 
                "authority_identifier"
            ])

        except ExtensionNotFound:
            logger.warning(f"[set_predecessor] Extension nicht gefunden für ID {certificate.id} – wird übersprungen")
            return

    def extract_and_set_fields(self, certificate: Certificate):
        logger.debug(f"[extract_and_set_fields] Starte für Certificate ID {certificate.id}")
        try:
            x509cert = x509.load_pem_x509_certificate(
                certificate.certificate.encode('utf-8'), 
                default_backend()
            )
            ski = x509cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_KEY_IDENTIFIER)
            certificate.subject_key_identifier = ski.value.digest.hex()
        except ExtensionNotFound:
            logger.warning(f"[extract_and_set_fields] Kein SKI für ID {certificate.id}")
        except Exception as e:
            logger.error(f"[extract_and_set_fields] SKI-Fehler für ID {certificate.id}: {e}")

        try:
            cert_data = cert_utils.parse_cert(certificate.certificate)
        except Exception as e:
            logger.error(f"[extract_and_set_fields] cert_utils.parse_cert FEHLGESCHLAGEN für ID {certificate.id}: {e}")
            raise

        issuer = cert_data.get("issuer", "")
        common_name = cert_data.get("subject", "")
        for pair in common_name.split("\n"):
            if "=" in pair:
                name, value = pair.split("=", 1)
                if name == "CN":
                    common_name = value

        certificate.valid_from = cert_data["startdate"].date()
        certificate.valid_to = cert_data["enddate"].date()
        certificate.issuer = issuer
        certificate.subject = common_name
        certificate.key_technology = cert_data.get("key_technology", "")
        certificate.subject_alternative_name = cert_data.get("SubjectAlternativeName", "")

        # Nur einmal speichern am Ende
        certificate.save(update_fields=[
            "subject_key_identifier",
            "valid_from",
            "valid_to",
            "subject",
            "issuer",
            "subject_alternative_name",
            "key_technology",
        ])
        logger.debug(f"[extract_and_set_fields] Gespeichert für ID {certificate.name}")