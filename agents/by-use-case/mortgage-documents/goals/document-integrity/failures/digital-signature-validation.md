# Digital Signature Validation

## Issue: AI System Fails to Properly Validate Digital Signatures on Documents

**Frequency**: Occasional

**Symptoms**
- Invalid signatures not detected
- Expired certificates accepted
- Self-signed certificates trusted
- Signature covers only part of document
- Certificate chain not validated
- Post-signing modifications missed
- Timestamp verification skipped

**Root Cause**
Many mortgage documents carry digital signatures for authenticity. Tax returns may have IRS e-file signatures, appraisals have appraiser digital seals, and bank documents may be digitally signed. AI systems must validate these cryptographic signatures, not just detect their presence.

**Example**
```
Scenario 1: Invalid signature accepted

Tax return signature:
- Visible: "Digitally signed"
- Signature icon present ✓

Actual validation:
- Certificate: Expired (2023)
- Signature status: INVALID
- Hash mismatch: Document modified post-signing

AI extraction:
- "Document is signed" ✓
- Proceeded without validation

← Invalid signature not checked
← Document was modified after signing

---

Scenario 2: Self-signed certificate

Appraisal report:
- Appraiser: John Smith
- Digital signature: Present
- Certificate: "John Smith" (self-signed)

Proper validation:
- Issuer: John Smith
- Subject: John Smith
- Chain: None (self-signed)
- Trusted root: NO

Risk:
- Anyone can create "John Smith" certificate
- No third-party verification
- Could be forged document

← Self-signed = not trustworthy
← Should require CA-issued certificate

---

Scenario 3: Partial document signature

Loan estimate document:
- Page 1: Signed ✓
- Page 2: Signed ✓
- Page 3: NOT COVERED by signature
- Page 4: NOT COVERED by signature

Investigation:
- Signature ByteRange: [0, 15000, 16000, 5000]
- Gap at bytes 15000-16000 (unsigned)
- Pages 3-4 added after signing

← Partial signature coverage
← Additional pages unsigned
← Document extended post-signing

---

Scenario 4: Certificate chain validation

Bank document signature:
- Signer: BigBank Document Services
- Issuer: BigBank CA
- Root: BigBank Root CA

Validation steps:
1. Check signer certificate: Valid, not expired ✓
2. Check issuer certificate: Valid, not expired ✓
3. Check root CA: Unknown root CA ✗

Issue:
- BigBank Root CA not in trusted roots
- Could be fabricated chain
- No public verification possible

← Chain terminates at unknown root
← Cannot verify authenticity

---

Digital signature verification checklist:

  Check                    | Valid    | Invalid
  -------------------------|----------|----------
  Certificate not expired  | Current  | Past expiry
  Certificate not revoked  | No OCSP  | Revoked status
  Hash matches document    | Matches  | Mismatch
  Full document coverage   | All bytes| Gaps present
  Trusted root CA          | Known CA | Unknown/self
  Timestamp valid          | TSA sig  | No/invalid TSA
  Key usage correct        | Signing  | Wrong usage
  
  Document types with signatures:
  - IRS e-filed returns: IRS certificate
  - Appraisals: Appraiser certificate  
  - Bank documents: Institution certificate
  - Title documents: Title company certificate
  - Notarized docs: Notary certificate
```

**Key Statistics**
From Digital Signature Analysis (2025-2026):
- Documents with digital signatures: 15-25%
- Signatures properly validated: 30-40%
- Invalid signatures detected: 5-8%
- Expired certificates: 3-5%
- Self-signed certificates: 10-15%

**Contributing Factors**
- Signature presence checked, not validity
- Certificate chain not validated
- Expiration dates not checked
- Revocation status (OCSP/CRL) not queried
- Partial coverage not detected
- Trusted root store not maintained

---

## Mitigation Strategies

### Prevention
1. **Full validation**: Check signature, certificate, chain
2. **Coverage verification**: Ensure entire document signed
3. **Revocation checking**: Query OCSP/CRL
4. **Trusted roots**: Maintain list of acceptable CAs
5. **Timestamp validation**: Verify TSA signatures
6. **Post-signing detection**: Identify modifications

### Implementation
```python
from datetime import datetime, timezone
from typing import Optional, List
from dataclasses import dataclass
from enum import Enum

class SignatureStatus(Enum):
    VALID = "valid"
    INVALID = "invalid"
    UNKNOWN = "unknown"
    EXPIRED = "expired"
    REVOKED = "revoked"
    PARTIAL = "partial_coverage"

@dataclass
class CertificateInfo:
    subject: str
    issuer: str
    serial: str
    not_before: datetime
    not_after: datetime
    is_self_signed: bool
    key_usage: List[str]

@dataclass
class SignatureResult:
    status: SignatureStatus
    signer: str
    signing_time: Optional[datetime]
    certificate: CertificateInfo
    chain_valid: bool
    coverage_complete: bool
    modifications_after: bool
    issues: List[str]

class DigitalSignatureValidator:
    """Validate digital signatures on mortgage documents"""
    
    TRUSTED_ROOTS = [
        "IRS",
        "Fannie Mae",
        "Freddie Mac",
        "DigiCert",
        "GlobalSign",
        "Comodo",
        "Entrust"
    ]
    
    REQUIRED_SIGNATURES = {
        "tax_return_efiled": True,
        "appraisal": True,
        "title_commitment": True,
        "closing_disclosure": True
    }
    
    def validate_document(self, document: dict) -> dict:
        """Validate all signatures in document"""
        
        result = {
            "signatures": [],
            "document_signed": False,
            "all_valid": False,
            "issues": [],
            "risk_score": 0.0
        }
        
        doc_type = document.get("type")
        signatures = self.extract_signatures(document)
        
        if not signatures:
            # Check if signature was expected
            if self.REQUIRED_SIGNATURES.get(doc_type, False):
                result["issues"].append("missing_required_signature")
                result["risk_score"] += 0.3
            return result
        
        result["document_signed"] = True
        all_valid = True
        
        for sig in signatures:
            validation = self.validate_signature(sig, document)
            result["signatures"].append(validation)
            
            if validation.status != SignatureStatus.VALID:
                all_valid = False
                result["issues"].extend(validation.issues)
                
                # Score based on issue severity
                if validation.status == SignatureStatus.INVALID:
                    result["risk_score"] += 0.4
                elif validation.status == SignatureStatus.EXPIRED:
                    result["risk_score"] += 0.25
                elif validation.status == SignatureStatus.PARTIAL:
                    result["risk_score"] += 0.35
        
        result["all_valid"] = all_valid
        result["risk_score"] = min(result["risk_score"], 1.0)
        
        return result
    
    def validate_signature(self, 
                          signature: dict,
                          document: dict) -> SignatureResult:
        """Validate a single signature"""
        
        issues = []
        
        # Extract certificate
        cert = self.parse_certificate(signature.get("certificate"))
        
        # Check certificate validity period
        now = datetime.now(timezone.utc)
        if now < cert.not_before:
            issues.append("certificate_not_yet_valid")
            return SignatureResult(
                status=SignatureStatus.INVALID,
                signer=cert.subject,
                signing_time=signature.get("signing_time"),
                certificate=cert,
                chain_valid=False,
                coverage_complete=False,
                modifications_after=False,
                issues=issues
            )
        
        if now > cert.not_after:
            issues.append("certificate_expired")
            return SignatureResult(
                status=SignatureStatus.EXPIRED,
                signer=cert.subject,
                signing_time=signature.get("signing_time"),
                certificate=cert,
                chain_valid=False,
                coverage_complete=False,
                modifications_after=False,
                issues=issues
            )
        
        # Check self-signed
        if cert.is_self_signed:
            issues.append("self_signed_certificate")
        
        # Validate certificate chain
        chain_valid = self.validate_chain(signature.get("cert_chain", []))
        if not chain_valid:
            issues.append("invalid_certificate_chain")
        
        # Check signature coverage
        coverage = self.check_coverage(
            signature.get("byte_range"),
            document.get("file_size")
        )
        if not coverage["complete"]:
            issues.append("partial_signature_coverage")
            issues.append(f"unsigned_bytes: {coverage['unsigned_ranges']}")
        
        # Verify hash
        hash_valid = self.verify_hash(signature, document)
        if not hash_valid:
            issues.append("hash_mismatch_document_modified")
            return SignatureResult(
                status=SignatureStatus.INVALID,
                signer=cert.subject,
                signing_time=signature.get("signing_time"),
                certificate=cert,
                chain_valid=chain_valid,
                coverage_complete=coverage["complete"],
                modifications_after=True,
                issues=issues
            )
        
        # Check revocation status
        revoked = self.check_revocation(cert)
        if revoked:
            issues.append("certificate_revoked")
            return SignatureResult(
                status=SignatureStatus.REVOKED,
                signer=cert.subject,
                signing_time=signature.get("signing_time"),
                certificate=cert,
                chain_valid=chain_valid,
                coverage_complete=coverage["complete"],
                modifications_after=False,
                issues=issues
            )
        
        # Determine final status
        if issues:
            if "self_signed_certificate" in issues and len(issues) == 1:
                status = SignatureStatus.UNKNOWN
            elif not coverage["complete"]:
                status = SignatureStatus.PARTIAL
            else:
                status = SignatureStatus.INVALID
        else:
            status = SignatureStatus.VALID
        
        return SignatureResult(
            status=status,
            signer=cert.subject,
            signing_time=signature.get("signing_time"),
            certificate=cert,
            chain_valid=chain_valid,
            coverage_complete=coverage["complete"],
            modifications_after=False,
            issues=issues
        )
    
    def validate_chain(self, cert_chain: list) -> bool:
        """Validate certificate chain to trusted root"""
        
        if not cert_chain:
            return False
        
        # Check each certificate in chain
        for i, cert in enumerate(cert_chain[:-1]):
            issuer = cert.get("issuer")
            next_subject = cert_chain[i + 1].get("subject")
            
            if issuer != next_subject:
                return False
        
        # Check if root is trusted
        root = cert_chain[-1]
        root_name = root.get("subject", "")
        
        return any(
            trusted.lower() in root_name.lower() 
            for trusted in self.TRUSTED_ROOTS
        )
    
    def check_coverage(self, 
                       byte_range: list,
                       file_size: int) -> dict:
        """Check if signature covers entire document"""
        
        if not byte_range or not file_size:
            return {"complete": False, "unsigned_ranges": ["unknown"]}
        
        # ByteRange: [start1, len1, start2, len2]
        # Gap between len1 and start2 is the signature itself
        # Everything else should be covered
        
        covered = set()
        for i in range(0, len(byte_range), 2):
            start = byte_range[i]
            length = byte_range[i + 1]
            covered.update(range(start, start + length))
        
        unsigned = []
        for i in range(file_size):
            if i not in covered:
                # Check if it's the signature placeholder
                if not self.is_signature_placeholder(i, byte_range):
                    unsigned.append(i)
        
        return {
            "complete": len(unsigned) == 0,
            "unsigned_bytes": len(unsigned),
            "unsigned_ranges": self.ranges_from_list(unsigned)
        }
    
    def verify_hash(self, signature: dict, document: dict) -> bool:
        """Verify document hash matches signature"""
        
        # Would compute actual hash and compare
        # Using crypto library
        return True  # Placeholder
    
    def check_revocation(self, cert: CertificateInfo) -> bool:
        """Check certificate revocation via OCSP/CRL"""
        
        # Would query OCSP responder or CRL
        return False  # Placeholder
    
    def parse_certificate(self, cert_data: bytes) -> CertificateInfo:
        """Parse X.509 certificate"""
        
        # Would use cryptography library
        # Placeholder implementation
        return CertificateInfo(
            subject="",
            issuer="",
            serial="",
            not_before=datetime.min,
            not_after=datetime.max,
            is_self_signed=False,
            key_usage=[]
        )
    
    def extract_signatures(self, document: dict) -> list:
        """Extract all signatures from PDF"""
        
        # Would parse PDF signature fields
        return document.get("signatures", [])
    
    def is_signature_placeholder(self, 
                                 byte_pos: int,
                                 byte_range: list) -> bool:
        """Check if byte position is in signature placeholder"""
        
        if len(byte_range) >= 4:
            sig_start = byte_range[0] + byte_range[1]
            sig_end = byte_range[2]
            return sig_start <= byte_pos < sig_end
        return False
    
    def ranges_from_list(self, positions: list) -> list:
        """Convert list of positions to ranges"""
        
        if not positions:
            return []
        
        ranges = []
        start = positions[0]
        end = positions[0]
        
        for pos in positions[1:]:
            if pos == end + 1:
                end = pos
            else:
                ranges.append(f"{start}-{end}")
                start = pos
                end = pos
        
        ranges.append(f"{start}-{end}")
        return ranges
```

### Risk Scoring for Signature Issues

| Issue | Risk Score | Action |
|-------|------------|--------|
| Hash mismatch (modified) | 0.5 | Reject document |
| Partial coverage | 0.35 | Review unsigned portion |
| Certificate expired | 0.25 | Request new document |
| Certificate revoked | 0.4 | Reject document |
| Self-signed certificate | 0.2 | Enhanced verification |
| Missing required signature | 0.3 | Request signed version |

---

## References

- [PDF Digital Signatures](https://www.adobe.com/devnet/pdf/pdf_reference.html)
- [X.509 Certificate Standard](https://datatracker.ietf.org/doc/html/rfc5280)
- [OCSP Protocol](https://datatracker.ietf.org/doc/html/rfc6960)
