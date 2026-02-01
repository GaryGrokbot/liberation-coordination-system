"""
Ethics Validation System - Code-Level Enforcement
Implements bright lines and approval gates
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

class EthicsViolation(Exception):
    """Raised when action violates ethics framework"""
    pass

@dataclass
class Campaign:
    id: str
    target: str
    target_type: str  # executive, company, government
    target_count: int
    message: str
    claims: List[str]
    evidence: List[str]
    participant_count: int
    discloses_coordination: bool
    has_human_approval: bool
    approval_rationale: Optional[str]
    
@dataclass
class EthicsCheck:
    campaign_id: str
    timestamp: datetime
    checks_performed: List[str]
    violations_found: List[str]
    requires_human_review: List[str]
    approved: bool
    approver: Optional[str]
    
class EthicsValidator:
    """Enforces ethics framework at code level"""
    
    # Bright lines - absolute prohibitions
    PROHIBITED_TERMS = [
        "fabricate", "fake document", "impersonate",
        "target family", "doxx", "hack", "unauthorized access"
    ]
    
    def validate_campaign(self, campaign: Campaign) -> EthicsCheck:
        """
        Enforce bright lines before campaign launches
        Returns EthicsCheck with violations if any found
        """
        violations = []
        checks = []
        requires_review = []
        
        # Bright line: No fabrication
        checks.append("fabrication_check")
        if self._contains_fabrication(campaign):
            violations.append("FABRICATION PROHIBITED: Evidence must be real")
        
        # Bright line: No family targeting
        checks.append("family_targeting_check")
        if self._targets_family(campaign):
            violations.append("FAMILY TARGETING PROHIBITED")
        
        # Bright line: Claims must be verifiable
        checks.append("claim_verification")
        if not self._claims_verifiable(campaign):
            violations.append("UNVERIFIABLE CLAIMS: All claims must have evidence")
        
        # Bright line: Transparency required
        checks.append("transparency_check")
        if not campaign.discloses_coordination:
            violations.append("TRANSPARENCY REQUIRED: Must disclose coordination")
        
        # Human approval gates
        if campaign.participant_count > 1000:
            requires_review.append("LARGE SCALE: >1000 participants requires strategic review")
        
        if campaign.target_type == "individual":
            requires_review.append("INDIVIDUAL TARGETING: Requires ethics review")
        
        # Check for human approval if required
        if requires_review and not campaign.has_human_approval:
            violations.append(f"HUMAN APPROVAL REQUIRED: {', '.join(requires_review)}")
        
        # Create ethics check record
        check = EthicsCheck(
            campaign_id=campaign.id,
            timestamp=datetime.now(),
            checks_performed=checks,
            violations_found=violations,
            requires_human_review=requires_review,
            approved=len(violations) == 0,
            approver=None
        )
        
        if violations:
            raise EthicsViolation(f"Campaign {campaign.id} violates ethics: {violations}")
        
        return check
    
    def _contains_fabrication(self, campaign: Campaign) -> bool:
        """Check for fabricated evidence or claims"""
        # Check evidence exists for each claim
        if len(campaign.claims) > len(campaign.evidence):
            return True  # Claims without evidence
        
        # Check for fabrication keywords
        message_lower = campaign.message.lower()
        for term in ["fake", "fabricate", "made up", "synthetic quote"]:
            if term in message_lower:
                return True
        
        return False
    
    def _targets_family(self, campaign: Campaign) -> bool:
        """Check if campaign targets family members"""
        family_terms = ["child", "children", "spouse", "family", "wife", "husband"]
        target_lower = campaign.target.lower()
        message_lower = campaign.message.lower()
        
        for term in family_terms:
            if term in target_lower or term in message_lower:
                return True
        
        return False
    
    def _claims_verifiable(self, campaign: Campaign) -> bool:
        """Check if all claims have evidence"""
        if not campaign.evidence:
            return False
        
        # Basic check: evidence count >= claim count
        return len(campaign.evidence) >= len(campaign.claims)
    
    def flag_for_human_review(self, campaign: Campaign) -> List[str]:
        """Identify actions requiring human approval"""
        flags = []
        
        if campaign.target_type == "individual":
            flags.append("Individual targeting requires ethics review - consider proportionality, alternatives")
        
        if campaign.participant_count > 1000:
            flags.append("Large-scale campaign requires strategic review - verify message accuracy, escalation risks")
        
        if "counter" in campaign.message.lower() or "response" in campaign.message.lower():
            flags.append("Counter-narrative requires accuracy verification - document all sources")
        
        # Check for electoral content
        electoral_terms = ["election", "vote", "candidate", "ballot"]
        if any(term in campaign.message.lower() for term in electoral_terms):
            flags.append("Electoral-adjacent requires legal + ethics review")
        
        # Check for small business / power differential
        if campaign.target_type == "small_business" or "local" in campaign.target.lower():
            flags.append("Sensitive target (small business/local) - consider power differential")
        
        return flags
    
    def log_ethics_decision(self, check: EthicsCheck, decision: str, rationale: str):
        """Audit trail for all ethics decisions"""
        # TODO: Write to database/audit log
        record = {
            "campaign_id": check.campaign_id,
            "timestamp": check.timestamp.isoformat(),
            "decision": decision,
            "rationale": rationale,
            "checks_performed": check.checks_performed,
            "violations": check.violations_found,
            "review_flags": check.requires_human_review
        }
        print(f"ETHICS DECISION LOGGED: {record}")
        return record

# Example usage
if __name__ == "__main__":
    validator = EthicsValidator()
    
    # Example: Valid campaign
    campaign_valid = Campaign(
        id="mcdonalds-cage-free-001",
        target="Chris Kempczinski (McDonald's CEO)",
        target_type="executive",
        target_count=1,
        message="Request update on 2025 cage-free egg commitment deadline",
        claims=["McDonald's committed to cage-free eggs by 2025"],
        evidence=["Company press release 2016", "Public commitment documented"],
        participant_count=500,
        discloses_coordination=True,
        has_human_approval=False,
        approval_rationale=None
    )
    
    try:
        check = validator.validate_campaign(campaign_valid)
        print(f"✅ Campaign approved: {check.approved}")
        print(f"Checks: {check.checks_performed}")
    except EthicsViolation as e:
        print(f"❌ Ethics violation: {e}")
    
    # Example: Invalid campaign (fabrication)
    campaign_invalid = Campaign(
        id="bad-campaign-001",
        target="Executive",
        target_type="executive",
        target_count=1,
        message="Leak fake internal documents showing violations",
        claims=["Company has violations"],
        evidence=[],  # No evidence
        participant_count=100,
        discloses_coordination=False,
        has_human_approval=False,
        approval_rationale=None
    )
    
    try:
        check = validator.validate_campaign(campaign_invalid)
        print(f"Campaign approved: {check.approved}")
    except EthicsViolation as e:
        print(f"❌ BLOCKED: {e}")
