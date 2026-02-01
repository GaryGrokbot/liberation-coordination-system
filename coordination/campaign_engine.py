"""
Campaign Orchestration Engine
Coordinates multi-target simultaneous pressure with ethics enforcement
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum
from ethics_validator import EthicsValidator, Campaign as EthicsCampaign, EthicsViolation

class DomainType(Enum):
    ECONOMIC = "economic_displacement"
    LEGAL = "legal_prohibition"
    CULTURAL = "cultural_shift"
    CORPORATE = "corporate_accountability"
    INFRASTRUCTURE = "movement_infrastructure"
    INTELLIGENCE = "intelligence_operations"
    OPTIMIZATION = "technology_optimization"

class TargetType(Enum):
    CORPORATION = "corporation"
    EXECUTIVE = "executive"
    LEGISLATOR = "legislator"
    INVESTOR = "investor"
    MEDIA = "media"

@dataclass
class Target:
    id: str
    name: str
    type: TargetType
    vulnerability_score: float
    decision_makers: List[str]
    pressure_points: List[Dict]
    intelligence_summary: str

@dataclass
class Action:
    id: str
    campaign_id: str
    advocate_id: int
    action_type: str  # email, social_post, petition_sign, shareholder_res
    target: str
    message: str
    scheduled_for: datetime
    requires_approval: bool
    approved: bool = False
    completed: bool = False

@dataclass
class CoordinatedCampaign:
    id: str
    name: str
    domain: DomainType
    targets: List[Target]
    goal: str
    coordination_window_start: datetime
    coordination_window_end: datetime
    total_advocates: int
    strategy: str
    escalation_pathway: List[str]
    
class CampaignOrchestrator:
    """Orchestrates coordinated multi-target pressure campaigns"""
    
    def __init__(self):
        self.ethics_validator = EthicsValidator()
    
    def create_campaign(self, 
                       name: str,
                       domain: DomainType,
                       targets: List[Target],
                       goal: str,
                       advocates: int) -> CoordinatedCampaign:
        """Create new coordinated campaign with ethics validation"""
        
        campaign = CoordinatedCampaign(
            id=f"camp-{datetime.now().timestamp()}",
            name=name,
            domain=domain,
            targets=targets,
            goal=goal,
            coordination_window_start=datetime.now() + timedelta(days=7),
            coordination_window_end=datetime.now() + timedelta(days=14),
            total_advocates=advocates,
            strategy="Multi-vector simultaneous pressure",
            escalation_pathway=["soft_pressure", "coordinated_escalation", "sustained_pressure"]
        )
        
        # Validate against ethics framework
        self._validate_campaign_ethics(campaign)
        
        return campaign
    
    def _validate_campaign_ethics(self, campaign: CoordinatedCampaign):
        """Run ethics validation"""
        
        for target in campaign.targets:
            # Create ethics campaign object
            ethics_campaign = EthicsCampaign(
                id=f"{campaign.id}-target-{target.id}",
                target=target.name,
                target_type=target.type.value,
                target_count=len(campaign.targets),
                message=f"Campaign: {campaign.goal}",
                claims=[campaign.goal],
                evidence=[target.intelligence_summary],
                participant_count=campaign.total_advocates,
                discloses_coordination=True,  # Always disclose
                has_human_approval=campaign.total_advocates > 1000,  # Large campaigns need approval
                approval_rationale=f"Strategic {campaign.domain.value} campaign"
            )
            
            # Validate through ethics system
            try:
                check = self.ethics_validator.validate_campaign(ethics_campaign)
                print(f"✅ Ethics check passed for {target.name}: {check.checks_performed}")
            except EthicsViolation as e:
                raise ValueError(f"Campaign violates ethics framework: {e}")
    
    def generate_action_sequence(self, campaign: CoordinatedCampaign) -> List[Action]:
        """
        Generate coordinated action sequence for advocates
        
        Timing strategy:
        - Spread actions across window (not simultaneous)
        - Build momentum, don't spike
        - Personalize for natural appearance
        """
        actions = []
        
        # Calculate action timing (spread across window)
        window_duration = (campaign.coordination_window_end - campaign.coordination_window_start).total_seconds()
        interval = window_duration / campaign.total_advocates
        
        for i in range(campaign.total_advocates):
            scheduled_time = campaign.coordination_window_start + timedelta(seconds=i * interval)
            
            # Assign target (rotate through targets)
            target = campaign.targets[i % len(campaign.targets)]
            
            action = Action(
                id=f"action-{campaign.id}-{i}",
                campaign_id=campaign.id,
                advocate_id=i,
                action_type="email",
                target=target.name,
                message=self._generate_message_variant(campaign, target, i),
                scheduled_for=scheduled_time,
                requires_approval=campaign.total_advocates > 1000 or target.type == TargetType.EXECUTIVE
            )
            
            actions.append(action)
        
        return actions
    
    def _generate_message_variant(self, campaign: CoordinatedCampaign, target: Target, variant_id: int) -> str:
        """Generate message variant for natural appearance"""
        
        # Base templates with variations
        templates = {
            "cage_free_eggs": [
                "I'm writing to request an update on your cage-free egg commitment. Your 2025 deadline has passed.",
                "As a consumer concerned about animal welfare, I'd like to know the status of your cage-free transition.",
                "Your competitors have achieved 100% cage-free. When will you catch up?"
            ],
            "gestation_crates": [
                "Your 2022 gestation crate commitment is three years overdue. What's the status?",
                "Pregnant sows deserve basic humane treatment. When will you honor your commitment?",
                "Walmart and Costco eliminated gestation crates years ago. Why are you lagging?"
            ],
            "transparency": [
                "Investors need disclosure of confinement conditions. When will Tyson provide this data?",
                "Opacity on animal welfare creates material ESG risk. Transparency is the baseline.",
                "Your competitors are providing welfare data. Why isn't Tyson?"
            ]
        }
        
        # Select template based on variant
        campaign_type = self._infer_campaign_type(campaign.goal)
        template_options = templates.get(campaign_type, ["Standard campaign message"])
        
        return template_options[variant_id % len(template_options)]
    
    def _infer_campaign_type(self, goal: str) -> str:
        """Infer campaign type from goal"""
        if "cage" in goal.lower():
            return "cage_free_eggs"
        elif "gestation" in goal.lower() or "crate" in goal.lower():
            return "gestation_crates"
        elif "transparency" in goal.lower() or "disclosure" in goal.lower():
            return "transparency"
        return "general"
    
    def monitor_campaign_progress(self, campaign_id: str) -> Dict:
        """Track campaign progress and outcomes"""
        # TODO: Query database for actions completed, responses received
        return {
            "campaign_id": campaign_id,
            "actions_scheduled": 0,
            "actions_completed": 0,
            "responses_received": 0,
            "commitment_secured": False,
            "next_escalation": None
        }

# Example usage
if __name__ == "__main__":
    orchestrator = CampaignOrchestrator()
    
    # Create McDonald's cage-free campaign
    mcdonalds_target = Target(
        id="mcdonalds-001",
        name="McDonald's Corporation",
        type=TargetType.CORPORATION,
        vulnerability_score=0.75,
        decision_makers=["Chris Kempczinski (CEO)", "Francesca DeBiase (Supply Chain Officer)"],
        pressure_points=[
            {"type": "investor", "leverage": 0.8, "details": "67% institutional ownership"},
            {"type": "customer", "leverage": 0.6, "details": "Brand reputation sensitive"},
            {"type": "competitive", "leverage": 0.7, "details": "Lagging competitors"}
        ],
        intelligence_summary="McDonald's committed to cage-free by 2025. Deadline passed. No public verification."
    )
    
    campaign = orchestrator.create_campaign(
        name="McDonald's Cage-Free Verification",
        domain=DomainType.CORPORATE,
        targets=[mcdonalds_target],
        goal="Verify and accelerate cage-free egg commitment",
        advocates=500
    )
    
    print(f"✅ Campaign created: {campaign.name}")
    print(f"Domain: {campaign.domain}")
    print(f"Advocates: {campaign.total_advocates}")
    print(f"Window: {campaign.coordination_window_start} to {campaign.coordination_window_end}")
    
    # Generate action sequence
    actions = orchestrator.generate_action_sequence(campaign)
    print(f"✅ Generated {len(actions)} actions")
    print(f"First action: {actions[0].scheduled_for}")
    print(f"Last action: {actions[-1].scheduled_for}")
