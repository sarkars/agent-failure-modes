# Image Forensics Failures

## Issue: AI System Fails to Detect Manipulated Images in Documents

**Frequency**: Occasional

**Symptoms**
- Photo-edited signatures not detected
- Copy-paste artifacts missed
- Compression artifacts indicate editing
- EXIF data shows manipulation
- Clone stamping patterns not identified
- Spliced images not detected

**Root Cause**
Mortgage documents may contain images: signatures, photos, stamps, or scanned elements. Fraudsters manipulate these using photo editing software. AI systems extracting only text miss image-level tampering indicators like compression artifacts, inconsistent lighting, or metadata anomalies.

**Example**
```
Scenario 1: Signature copy-paste

Driver's license submitted:
- Photo: Appears authentic
- Signature: Looks valid

Image analysis:
- Photo: JPEG quality 85%
- Signature area: JPEG quality 92% ← DIFFERENT
- Signature has sharper edges than surrounding
- Compression block boundaries misaligned

Conclusion:
- Signature was pasted from another source
- Higher quality indicates different origin
- Block boundary analysis shows splice

← Signature transplanted from another document

---

Scenario 2: Bank balance manipulation

Bank statement image analysis:

Balance field area:
- Font rendering: Anti-aliased
- Background: Slightly different shade ← EDIT
- Noise pattern: Inconsistent with document

Surrounding text:
- Font rendering: Aliased (scan artifact)
- Background: Consistent paper texture
- Noise pattern: Uniform

Conclusion:
- Balance was edited digitally
- Then printed and re-scanned
- Forensic artifacts remain

← Digital edit followed by re-scan (common pattern)

---

Scenario 3: Clone stamp detection

Pay stub company logo area:

Analysis:
- Repeating pixel patterns detected
- 3 identical 8x8 pixel blocks
- Pattern suggests clone stamp tool
- Used to cover original text/number

What was hidden?
- Likely original gross pay amount
- Or employer name/logo

← Clone stamp used to obscure original content

---

Scenario 4: EXIF metadata reveals editing

Submitted "original" document:

File metadata:
- Software: Adobe Photoshop 2024
- Created: 2025-04-15
- Modified: 2025-04-16
- Color profile: sRGB (edited)
- History: 12 actions recorded ← MULTIPLE EDITS

Expected for authentic scan:
- Software: Scanner driver or "Windows Imaging"
- Created = Modified
- No edit history

← EXIF shows Photoshop editing with multiple actions

---

Scenario 5: Lighting/shadow inconsistency

Photo ID on application:

Face photo analysis:
- Light source: Upper left
- Shadow direction: Consistent

Signature area:
- Light source: Direct front ← DIFFERENT
- No shadows

Background:
- Lighting: Flat, uniform ← DIFFERENT

Conclusion:
- Elements from different images combined
- Lighting analysis reveals composite

← Composite image from multiple sources

---

Image forensics indicators:

  Indicator           | Detection Method      | Risk Level
  --------------------|----------------------|------------
  JPEG quality variance| Block analysis       | High
  Clone patterns      | Pattern detection    | High
  Noise inconsistency | Noise analysis       | Medium
  EXIF editing        | Metadata extraction  | High
  Shadow mismatch     | Lighting analysis    | Medium
  Edge artifacts      | ELA analysis         | Medium
  
  Common manipulation tools:
  - Photoshop: Most capable, leaves traces
  - GIMP: Open source alternative
  - Mobile apps: Quick edits, obvious artifacts
  - PDF editors: Text + image manipulation
```

**Key Statistics**
From Image Forensics (2025-2026):
- Documents with manipulated images: 1-2%
- Image manipulation in fraud cases: 30-40%
- EXIF analysis performed: 10-15%
- Compression artifact detection: 5-10%
- Successful manipulation detection: 60-70%

**Contributing Factors**
- Images treated as opaque data
- EXIF metadata not extracted
- Compression analysis not performed
- No lighting/shadow analysis
- Clone detection not implemented
- Error Level Analysis (ELA) not used

---

## Mitigation Strategies

### Prevention
1. **EXIF extraction**: Analyze image metadata
2. **ELA analysis**: Error Level Analysis for edits
3. **Noise analysis**: Detect inconsistent noise patterns
4. **Compression analysis**: Compare JPEG quality levels
5. **Clone detection**: Find repeated patterns
6. **Lighting analysis**: Verify consistent lighting

### Implementation
```python
from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import io

class ManipulationType(Enum):
    COPY_PASTE = "copy_paste"
    CLONE_STAMP = "clone_stamp"
    CONTENT_EDIT = "content_edit"
    COMPOSITE = "composite"
    RESAVE = "resave"
    UNKNOWN = "unknown"

@dataclass
class ForensicFinding:
    type: ManipulationType
    location: Optional[tuple]  # (x, y, width, height)
    confidence: float
    description: str
    evidence: str

class ImageForensicsAnalyzer:
    """Analyze images for manipulation indicators"""
    
    EDITING_SOFTWARE = [
        "photoshop", "gimp", "paint.net", "pixlr",
        "lightroom", "affinity", "corel", "photopea"
    ]
    
    def analyze_image(self, image_path: str) -> dict:
        """Perform comprehensive image forensics"""
        
        result = {
            "metadata_analysis": {},
            "compression_analysis": {},
            "ela_analysis": {},
            "clone_detection": {},
            "findings": [],
            "risk_score": 0.0
        }
        
        # Load image
        try:
            img = Image.open(image_path)
        except Exception as e:
            return {"error": str(e)}
        
        # EXIF/Metadata analysis
        metadata = self.analyze_metadata(img)
        result["metadata_analysis"] = metadata
        
        if metadata.get("editing_detected"):
            result["findings"].append(ForensicFinding(
                type=ManipulationType.CONTENT_EDIT,
                location=None,
                confidence=0.9,
                description="Editing software detected in metadata",
                evidence=metadata.get("software", "")
            ))
            result["risk_score"] += 0.3
        
        # Compression analysis (JPEG)
        if img.format == "JPEG":
            compression = self.analyze_compression(img, image_path)
            result["compression_analysis"] = compression
            
            if compression.get("quality_variance"):
                result["findings"].append(ForensicFinding(
                    type=ManipulationType.COPY_PASTE,
                    location=compression.get("variance_region"),
                    confidence=compression.get("confidence", 0.7),
                    description="JPEG quality inconsistency detected",
                    evidence=f"Quality variance: {compression['variance_value']}"
                ))
                result["risk_score"] += 0.35
        
        # Error Level Analysis
        ela_result = self.perform_ela(img)
        result["ela_analysis"] = ela_result
        
        if ela_result.get("manipulation_regions"):
            for region in ela_result["manipulation_regions"]:
                result["findings"].append(ForensicFinding(
                    type=ManipulationType.CONTENT_EDIT,
                    location=region["bbox"],
                    confidence=region["confidence"],
                    description="ELA detected potential manipulation",
                    evidence=f"Error level: {region['level']}"
                ))
            result["risk_score"] += 0.25
        
        # Clone detection
        clones = self.detect_clones(img)
        result["clone_detection"] = clones
        
        if clones.get("patterns"):
            result["findings"].append(ForensicFinding(
                type=ManipulationType.CLONE_STAMP,
                location=clones["patterns"][0]["location"],
                confidence=clones["confidence"],
                description="Clone stamp patterns detected",
                evidence=f"Pattern count: {len(clones['patterns'])}"
            ))
            result["risk_score"] += 0.35
        
        result["risk_score"] = min(result["risk_score"], 1.0)
        
        return result
    
    def analyze_metadata(self, img: Image) -> dict:
        """Analyze image EXIF and metadata"""
        
        result = {
            "software": None,
            "created": None,
            "modified": None,
            "editing_detected": False,
            "edit_history": []
        }
        
        # Extract EXIF
        exif_data = img._getexif() if hasattr(img, '_getexif') else None
        
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                
                if tag == "Software":
                    result["software"] = str(value)
                    # Check for editing software
                    if any(ed.lower() in str(value).lower() 
                           for ed in self.EDITING_SOFTWARE):
                        result["editing_detected"] = True
                
                elif tag == "DateTime":
                    result["created"] = str(value)
                
                elif tag == "DateTimeDigitized":
                    result["digitized"] = str(value)
        
        # Check for XMP data (Photoshop history)
        xmp = self.extract_xmp(img)
        if xmp:
            result["edit_history"] = xmp.get("history", [])
            if len(result["edit_history"]) > 1:
                result["editing_detected"] = True
        
        return result
    
    def analyze_compression(self, img: Image, path: str) -> dict:
        """Analyze JPEG compression for inconsistencies"""
        
        result = {
            "overall_quality": None,
            "quality_variance": False,
            "variance_region": None,
            "confidence": 0.0
        }
        
        # Estimate overall JPEG quality
        # Would use library like jpeglib for accurate analysis
        
        # Divide image into blocks and compare quantization
        width, height = img.size
        block_size = 64
        qualities = []
        
        for y in range(0, height - block_size, block_size):
            for x in range(0, width - block_size, block_size):
                region = img.crop((x, y, x + block_size, y + block_size))
                quality = self.estimate_jpeg_quality(region)
                qualities.append({
                    "x": x, "y": y,
                    "quality": quality
                })
        
        if qualities:
            avg_quality = np.mean([q["quality"] for q in qualities])
            result["overall_quality"] = avg_quality
            
            # Find outliers
            for q in qualities:
                if abs(q["quality"] - avg_quality) > 10:
                    result["quality_variance"] = True
                    result["variance_region"] = (
                        q["x"], q["y"], block_size, block_size
                    )
                    result["variance_value"] = abs(q["quality"] - avg_quality)
                    result["confidence"] = 0.8
                    break
        
        return result
    
    def perform_ela(self, img: Image) -> dict:
        """Perform Error Level Analysis"""
        
        result = {
            "manipulation_regions": [],
            "overall_consistency": True
        }
        
        # Save at lower quality
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        buffer.seek(0)
        resaved = Image.open(buffer)
        
        # Compare original to resaved
        original_array = np.array(img.convert("RGB"))
        resaved_array = np.array(resaved.convert("RGB"))
        
        # Calculate error levels
        diff = np.abs(original_array.astype(int) - resaved_array.astype(int))
        error_level = np.mean(diff, axis=2)
        
        # Find high-error regions (potential edits)
        threshold = np.mean(error_level) + 2 * np.std(error_level)
        
        high_error = error_level > threshold
        
        # Find contiguous regions
        regions = self.find_regions(high_error)
        
        for region in regions:
            if region["size"] > 100:  # Minimum size
                result["manipulation_regions"].append({
                    "bbox": region["bbox"],
                    "level": region["avg_level"],
                    "confidence": min(region["avg_level"] / 100, 0.95)
                })
                result["overall_consistency"] = False
        
        return result
    
    def detect_clones(self, img: Image) -> dict:
        """Detect clone stamp or copy-paste regions"""
        
        result = {
            "patterns": [],
            "confidence": 0.0
        }
        
        # Convert to grayscale for pattern matching
        gray = np.array(img.convert("L"))
        
        # Use block-based matching
        block_size = 16
        blocks = {}
        
        height, width = gray.shape
        
        for y in range(0, height - block_size, 4):
            for x in range(0, width - block_size, 4):
                block = gray[y:y+block_size, x:x+block_size]
                block_hash = self.hash_block(block)
                
                if block_hash in blocks:
                    # Found duplicate block
                    orig = blocks[block_hash]
                    distance = np.sqrt((x - orig[0])**2 + (y - orig[1])**2)
                    
                    # Ignore adjacent blocks
                    if distance > block_size * 2:
                        result["patterns"].append({
                            "original": orig,
                            "clone": (x, y),
                            "location": (x, y, block_size, block_size),
                            "distance": distance
                        })
                else:
                    blocks[block_hash] = (x, y)
        
        if result["patterns"]:
            result["confidence"] = min(
                len(result["patterns"]) * 0.1 + 0.5, 
                0.95
            )
        
        return result
    
    def hash_block(self, block: np.ndarray) -> str:
        """Create hash for image block comparison"""
        
        # Simplify block and hash
        simplified = (block // 16).astype(np.uint8)
        return simplified.tobytes().hex()
    
    def estimate_jpeg_quality(self, region: Image) -> float:
        """Estimate JPEG quality of image region"""
        
        # Simplified quality estimation
        # Would use actual DCT coefficient analysis
        buffer = io.BytesIO()
        region.save(buffer, format="JPEG", quality=100)
        size_100 = buffer.tell()
        
        buffer = io.BytesIO()
        region.save(buffer, format="JPEG", quality=50)
        size_50 = buffer.tell()
        
        # Estimate based on compression ratio
        return 50 + (size_100 - region.size[0] * region.size[1]) / 100
    
    def find_regions(self, binary_mask: np.ndarray) -> List[dict]:
        """Find contiguous regions in binary mask"""
        
        # Would use connected component analysis
        regions = []
        # Placeholder - actual implementation would use scipy or cv2
        return regions
    
    def extract_xmp(self, img: Image) -> Optional[dict]:
        """Extract XMP metadata from image"""
        
        # Would parse XMP data for edit history
        return None
```

### Risk Scoring for Image Issues

| Finding | Risk Score | Action |
|---------|------------|--------|
| Editing software in EXIF | 0.3 | Further analysis |
| JPEG quality variance | 0.35 | Region edited |
| ELA high-error region | 0.25 | Potential edit |
| Clone patterns detected | 0.35 | Clone stamp used |
| Composite lighting | 0.3 | Multiple sources |
| Multiple edit history | 0.25 | Extensively edited |

---

## References

- [FotoForensics](https://fotoforensics.com/)
- [NIST Digital Image Forensics](https://www.nist.gov/)
- [Error Level Analysis](https://en.wikipedia.org/wiki/Error_level_analysis)
