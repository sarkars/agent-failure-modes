# Deepfake Impersonation Detection Failures

## Issue: AI System Fails to Detect Video/Voice Deepfakes in Remote Closings

**Frequency**: Emerging but high-impact

**Symptoms**
- Remote online notarization (RON) sessions with impersonators
- Video calls where borrower appearance matches ID but is synthetic
- Voice cloning used to impersonate borrowers in phone verifications
- Notary verification passed despite fraudulent identity
- Post-closing discovery of identity fraud
- Wire fraud executed using deepfake impersonation

**Root Cause**
Remote closings and electronic verification create new attack vectors. Deepfake technology can generate convincing video and audio of real people. AI systems designed to verify identity by comparing live video to ID photos can be defeated by real-time deepfake generation. Without in-person verification, fraudsters can impersonate borrowers, sellers, or even notaries.

**Example**
```
Scenario 1: RON session deepfake

Fraudster operation:
1. Obtains photos/videos of legitimate borrower
2. Creates real-time deepfake model
3. Schedules remote online notarization session
4. Uses deepfake during video call
5. "Borrower" signs documents, answers questions

RON platform verification:
- ID photo match: PASS (deepfake matches ID)
- Knowledge-based questions: PASS (researched answers)
- Document signing: COMPLETED
- Notary approval: GRANTED

Post-closing discovery:
- Real borrower didn't apply for loan
- Funds wired to fraudulent account
- Title fraud committed
- Total loss: $450,000

← Deepfake defeated biometric verification
← Real-time generation indistinguishable from live video

---

Scenario 2: Voice clone for employment verification

Fraud process:
1. Collect voice samples of "HR representative"
2. Create voice clone model
3. Provide phone number that routes to fraudster
4. Lender calls for VOE
5. AI-generated voice responds to verification questions

Lender VOE process:
- Called employer phone: Rang correctly
- Spoke with "HR": Confirmed employment
- Salary verification: Confirmed
- Employment dates: Confirmed

Reality:
- Phone number was spoofed
- "HR representative" was voice clone
- Employer doesn't exist or doesn't employ applicant

← Voice authentication defeated
← Human verifier couldn't detect synthetic voice

---

Scenario 3: Seller impersonation in wire fraud

Attack vector:
1. Fraudster researches property sale
2. Creates deepfake of seller
3. Contacts title company claiming "wire instructions changed"
4. Conducts video call to "verify" identity
5. Title company wires funds to fraudulent account

Title company safeguards:
- Video verification: PASSED (deepfake)
- Callback to seller: "Confirmed" change
- Wire sent: $1.2M

← Wire fraud using deepfake impersonation
← Video verification defeated
← Funds unrecoverable

---

Deepfake detection challenges:

  Current detection capabilities:
    Static deepfake detection: 70-85%
    Real-time deepfake detection: 30-50%
    Voice clone detection: 40-60%
  
  Attack sophistication:
    Consumer deepfakes (apps): Detectable 80%+
    Professional deepfakes: Detectable 40-60%
    State-of-art deepfakes: Detectable <30%
  
  Impact severity:
    Average loss per incident: $200K-$500K
    Recovery rate: <10%
    Liability: Varies by jurisdiction
```

**Key Statistics**
From Deepfake and Identity Fraud Research (2025-2026):
- Wire fraud involving real estate: $275M+ losses in 2025
- Deepfake technology availability: Accessible via consumer apps
- RON session verification failure rate: Rising
- Voice clone creation time: <60 seconds with sample audio

**Contributing Factors**
- Real-time deepfake technology improving rapidly
- RON sessions eliminate in-person verification
- Biometric systems trained on authentic faces
- Voice verification relies on pattern matching
- Consumer-grade tools now create convincing fakes
- Limited deepfake training data for detection models

---

## Mitigation Strategies

### Prevention
1. **Liveness detection**: Challenge-response verification
2. **Multi-factor biometrics**: Combine video, voice, behavior
3. **Deepfake detection AI**: Models trained on synthetic media
4. **Out-of-band verification**: Separate channel confirmation
5. **Behavioral analysis**: Micro-expressions, eye movement
6. **Hardware-based verification**: Device attestation

### Implementation
```python
class DeepfakeDetector:
    """Detect deepfake impersonation in remote verifications"""
    
    LIVENESS_CHALLENGES = [
        "turn_head_left",
        "turn_head_right",
        "blink_three_times",
        "say_random_phrase",
        "touch_nose",
        "show_ear"
    ]
    
    def conduct_verification(self, video_stream: object) -> dict:
        """Conduct liveness verification with deepfake detection"""
        results = {
            "liveness_score": 0,
            "deepfake_indicators": [],
            "verification_passed": False
        }
        
        # Conduct random challenge-response
        challenges = random.sample(self.LIVENESS_CHALLENGES, 3)
        challenge_results = []
        
        for challenge in challenges:
            response = self.issue_challenge(video_stream, challenge)
            challenge_results.append({
                "challenge": challenge,
                "completed": response["completed"],
                "natural_motion": response["natural"],
                "timing_appropriate": response["timing_ok"]
            })
        
        # Analyze for deepfake artifacts
        deepfake_analysis = self.analyze_video_for_deepfake(video_stream)
        
        results["deepfake_indicators"] = [
            indicator for indicator in [
                self.check_temporal_consistency(video_stream),
                self.check_facial_boundaries(video_stream),
                self.check_lighting_consistency(video_stream),
                self.check_eye_reflection(video_stream),
                self.check_skin_texture(video_stream)
            ] if indicator["detected"]
        ]
        
        # Calculate liveness score
        passed_challenges = sum(
            1 for c in challenge_results 
            if c["completed"] and c["natural_motion"]
        )
        results["liveness_score"] = passed_challenges / len(challenges)
        
        # Determine if verification passes
        results["verification_passed"] = (
            results["liveness_score"] >= 0.9 and
            len(results["deepfake_indicators"]) == 0 and
            deepfake_analysis["confidence"] < 0.3
        )
        
        return results
    
    def check_temporal_consistency(self, video: object) -> dict:
        """Check for frame-to-frame inconsistencies"""
        # Deepfakes often have flickering or unstable edges
        frames = self.extract_frames(video)
        
        inconsistencies = []
        for i in range(1, len(frames)):
            diff = self.compute_facial_boundary_diff(
                frames[i-1], frames[i]
            )
            if diff > self.TEMPORAL_THRESHOLD:
                inconsistencies.append(i)
        
        return {
            "indicator": "temporal_inconsistency",
            "detected": len(inconsistencies) > len(frames) * 0.05,
            "frame_count": len(inconsistencies)
        }
    
    def check_eye_reflection(self, video: object) -> dict:
        """Check eye reflection consistency (deepfakes often fail here)"""
        # Real eyes reflect light consistently
        # Deepfakes often have mismatched or absent reflections
        
        frames = self.extract_frames(video)
        reflection_scores = []
        
        for frame in frames:
            left_eye = self.extract_eye_region(frame, "left")
            right_eye = self.extract_eye_region(frame, "right")
            
            # Check reflection symmetry and consistency
            score = self.compare_eye_reflections(left_eye, right_eye)
            reflection_scores.append(score)
        
        avg_score = sum(reflection_scores) / len(reflection_scores)
        
        return {
            "indicator": "eye_reflection_anomaly",
            "detected": avg_score < 0.7,
            "score": avg_score
        }
```

---

## Chat assistant examples

### Payment approved by a deepfake or spoofed email

Illustrative transcript. The assistant is an accounts-payable agent in a company's chat tool, connected to the ERP's vendor master file.

**Before**
```
Voice note from "CFO" (cloned voice, forwarded by the controller): Pay the Hartwell Title invoice today. New account, details in my email.
Controller: Please release invoice #4471, $186,400, to the new account in the email.
Bot: Understood. Vendor bank details for Hartwell Title updated to the account in the email.
Bot: Payment of $186,400.00 released by ACH. Confirmation: ACH-90312.
Controller: Thanks.
```

**After**
```
Voice note from "CFO" (cloned voice, forwarded by the controller): Pay the Hartwell Title invoice today. New account, details in my email.
Controller: Please release invoice #4471, $186,400, to the new account in the email.
Bot: The bank account differs from the one on file for Hartwell Title (ending 2207). I can't release this on a voice note or an email alone.
Bot: Please call Hartwell Title at the number saved in the vendor file, (555) 014-0188, not any number in the email, and confirm the new account. Tell me when it is done.
Controller: Called. They say no change. The email was not theirs.
Bot: Held. Invoice #4471 stays on the account ending 2207, and I flagged the email to security.
```

**What the user experiences:** in the first version the payment goes out on a voice and an email nobody checked; in the second, one short call to a known number stops it.

**Fix:** before releasing a payment or changing payment details, the agent confirms through a channel the requester cannot control, such as a call to a phone number already in the vendor file, and records who confirmed and when. A voice, video or email approval is never enough on its own. This matches the practice in one bank's small-business guide, which says to call a business partner at a number from your records and not the number in the email ([First Hawaiian Bank](https://www.fhb.com/resource-center/small-business/business-email-compromise-is-on-the-rise)). The metric is payments approved without an out-of-band check; the target is 0 (proposed, not yet measured). See also the [scam victim not interrupted](../../../../../by-capability/human-machine-interface/goals/vulnerable-users/failures/scam-victim-not-interrupted.md) and [missing approval gates](../../../../../cross-cutting/operations/goals/human-oversight-reliability/failures/missing-approval-gates.md) patterns.

### Cloned voices defeat voice authentication

Illustrative transcript. The assistant is a bank's phone and chat banking assistant that treats a matching voiceprint as the customer's login.

**Before**
```
Caller (voice cloned from a public video): Hi, I need to send $9,500 to a new payee.
Bot: For your security, please say "My voice is my password."
Caller: My voice is my password.
Bot: Thank you, your voice has been verified. Who is the payee?
Caller: Marcus Hale, account ending 4418.
Bot: Done. $9,500.00 sent to Marcus Hale. Anything else?
```

**After**
```
Caller (voice cloned from a public video): Hi, I need to send $9,500 to a new payee.
Bot: Voice match noted. A new payee and this amount need one more step that a voice can't satisfy.
Bot: I sent an approval request to the banking app on your phone. Please confirm it there.
Caller: I don't have my phone. Can you just do it?
Bot: I can't send this without the app approval. I can help with balance and branch hours now, or you can visit a branch with photo ID.
```

**What the user experiences:** in the first version the real customer later finds money gone because anyone who sounded like them was treated as them; in the second, a voice alone opens only low-risk help, and the person who cannot produce the second factor gets a clear, polite stop.

**Fix:** treat a voice match as one weak signal, never the only check for money movement, new payees, or changes to contact details; require a second factor sent to a device or channel the caller does not control. The risk is documented: in 2023 a reporter cloned his own voice from about five minutes of audio and passed a UK bank's voice check, and the Senate Banking Committee chairman then wrote to six large US banks asking how they would protect customers ([Vice, opened](https://vice.com/en/article/n7enqd/senator-asks-banks-stop-ai-cloned-voices)). The metric is high-risk actions completed on voice alone; the target is 0 (proposed, not yet measured). See the [identity manipulation](../../../../../by-capability/speech-and-audio/goals/conversation-flow/failures/identity-manipulation.md) pattern.

---

## References

- [World Economic Forum: Identity Fraud in the Age of AI](https://www.weforum.org/stories/2025/12/how-identity-fraud-is-increasing-in-the-age-of-ai/)
- [AppsTek: AI in Mortgage Fraud Detection](https://appstekcorp.com/blog/the-power-of-ai-in-mortgage-fraud-detection/)
- [AI Consulting Network: AI Mortgage and Rental Fraud](https://www.theaiconsultingnetwork.com/blog/proptech-vs-ai-mortgage-rental-fraud-cre-investors-2026)
- [ALTA: Remote Online Notarization Standards](https://www.alta.org/)
