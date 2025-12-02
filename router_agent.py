from typing import Dict, Any
import asyncio
from src.agents.base_agent import BaseAgent

class RouterAgent(BaseAgent):
    """Routing agent - responsible for task distribution"""
    
    def __init__(self):
        super().__init__(agent_id="router_001", agent_type="router")
        self.complexity_threshold = 0.7
        self.document_types = {
            "invoice": ["extraction", "validation"],
            "contract": ["extraction", "analysis", "validation"],
            "report": ["extraction", "analysis", "summarization"],
            "email": ["extraction", "summarization"]
        }
    
    async def assess_complexity(self, document: Dict[str, Any]) -> float:
        """Evaluate document complexity"""
        complexity_score = 0.0
        
        # Based on document length

        if len(document.get("content", "")) > 5000:
            complexity_score += 0.3
        
        # Based on document type

        doc_type = document.get("type", "unknown")
        if doc_type in ["contract", "report"]:
            complexity_score += 0.4
        
        # Based on special requirements

        if document.get("requires_compliance_check", False):
            complexity_score += 0.3
            
        return min(complexity_score, 1.0)
    
    async def process(self, task_data: Dict[str, Any], 
                     context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handling routing tasks"""
        document = task_data.get("document", {})
        
        # Evaluate complexity

        complexity = await self.assess_complexity(document)
        
        # Determine processing strategy

        if complexity > self.complexity_threshold:
            routing_decision = "complex_processing"
            required_agents = ["orchestrator", "extractor", "analyzer", "validator"]
        else:
            routing_decision = "simple_processing"
            required_agents = ["extractor", "summarizer"]
        
        # Record the decision-making process

        self.log_interaction(
            from_agent=self.agent_id,
            to_agent="workflow_orchestrator",
            task=f"Route {document.get('type', 'unknown')} document",
            reasoning=f"Complexity score: {complexity:.2f}, Routing: {routing_decision}"
        )
        
        return {
            "routing_decision": routing_decision,
            "complexity_score": complexity,
            "required_agents": required_agents,
            "document_info": {
                "type": document.get("type", "unknown"),
                "size": len(document.get("content", "")),
                "requires_analysis": complexity > 0.5
            }
        }
