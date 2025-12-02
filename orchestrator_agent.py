from typing import Dict, Any, List
import asyncio
from src.agents.base_agent import BaseAgent
from src.agents.extractor_agent import ExtractorAgent
from src.agents.analyzer_agent import AnalyzerAgent
from src.agents.summarizer_agent import SummarizerAgent
from src.agents.validator_agent import ValidatorAgent

class OrchestratorAgent(BaseAgent):
    
    def __init__(self, federated_memory):
        super().__init__(agent_id="orchestrator_001", agent_type="orchestrator")
        self.federated_memory = federated_memory
        self.agents = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """初始化子智能体"""
        self.agents = {
            "extractor": ExtractorAgent(),
            "analyzer": AnalyzerAgent(),
            "summarizer": SummarizerAgent(),
            "validator": ValidatorAgent()
        }
    
    async def create_workflow_plan(self, routing_result: Dict[str, Any], 
                                 document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """创建工作流执行计划"""
        required_agents = routing_result.get("required_agents", [])
        complexity = routing_result.get("complexity_score", 0.0)
        
        workflow_steps = []
        
        if "complex_processing" in routing_result.get("routing_decision", ""):
            workflow_steps = [
                {"step": 1, "agent": "extractor", "action": "extract_data"},
                {"step": 2, "agent": "analyzer", "action": "analyze_content"},
                {"step": 3, "agent": "summarizer", "action": "generate_summary"},
                {"step": 4, "agent": "validator", "action": "validate_output"}
            ]
        else:
            workflow_steps = [
                {"step": 1, "agent": "extractor", "action": "extract_data"},
                {"step": 2, "agent": "summarizer", "action": "generate_summary"}
            ]
        
        return workflow_steps
    
    async def execute_workflow(self, workflow_plan: List[Dict[str, Any]], 
                              original_document: Dict[str, Any]) -> Dict[str, Any]:
        execution_context = {
            "original_document": original_document,
            "intermediate_results": {},
            "start_time": datetime.now(),
            "status": "running"
        }
        
        try:
            for step in workflow_plan:
                agent_type = step["agent"]
                action = step["action"]
                
                agent = self.agents.get(agent_type)
                if not agent:
                    raise ValueError(f"Unknown agent type: {agent_type}")
                
                task_data = {
                    "action": action,
                    "document": original_document,
                    "context": execution_context
                }
                
                self.log_interaction(
                    from_agent=self.agent_id,
                    to_agent=agent.agent_id,
                    task=f"Execute step {step['step']}: {action}",
                    reasoning=f"Delegating {action} to {agent_type} agent"
                )
                
                result = await agent.process(task_data, execution_context)
                
                execution_context["intermediate_results"][f"step_{step['step']}"] = result
                
                if result.get("key_insights"):
                    self.federated_memory.store(
                        fact=result["key_insights"],
                        metadata={
                            "agent_type": agent_type,
                            "action": action,
                            "document_id": original_document.get("id", "unknown")
                        }
                    )
            
            execution_context["status"] = "completed"
            execution_context["end_time"] = datetime.now()
            
            final_output = self._compile_final_output(execution_context)
            
            return final_output
            
        except Exception as e:
            execution_context["status"] = "failed"
            execution_context["error"] = str(e)
            raise e
    
    def _compile_final_output(self, execution_context: Dict[str, Any]) -> Dict[str, Any]:
        intermediate_results = execution_context["intermediate_results"]
        
        final_output = {
            "status": "success",
            "processing_time": str(
                execution_context["end_time"] - execution_context["start_time"]
            ),
            "extracted_data": intermediate_results.get("step_1", {}),
            "analysis_results": intermediate_results.get("step_2", {}),
            "summary": intermediate_results.get("step_3", {}),
            "validation_status": intermediate_results.get("step_4", {}),
            "audit_trail": self.get_audit_trail()
        }
        
        return final_output
