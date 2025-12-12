import logging
from typing import Optional
from vocode.streaming.models.agent import AgentConfig
from vocode.streaming.models.synthesizer import SynthesizerConfig
from vocode.streaming.agent.base_agent import BaseAgent
from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
from vocode.streaming.synthesizer.stream_elements_synthesizer import StreamElementsSynthesizer
from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig
from src.calling.agent import ProductionLangchainAgent
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class CustomAgentFactory:
    """Factory for creating agents with company-specific configs"""
    
    def __init__(self, conversation_store: dict):
        self.conversation_store = conversation_store
    
    def create_agent(
        self, 
        agent_config: AgentConfig, 
        logger: Optional[logging.Logger] = None,
        conversation_id: Optional[str] = None
    ) -> BaseAgent:
        if agent_config.type == "agent_langchain":
            agent = ProductionLangchainAgent(
                agent_config=agent_config,
                conversation_id=conversation_id
            )
            
            # Set lead_id if available in conversation store
            if conversation_id and conversation_id in self.conversation_store:
                agent.lead_id = self.conversation_store[conversation_id].get('lead_id')
                agent.current_language = self.conversation_store[conversation_id].get('language', 'en')
            
            return agent
        
        raise Exception(f"Invalid agent config: {agent_config.type}")


class CustomSynthesizerFactory:
    """Factory for creating synthesizers"""
    
    def create_synthesizer(self, synthesizer_config: SynthesizerConfig) -> BaseSynthesizer:
        if isinstance(synthesizer_config, StreamElementsSynthesizerConfig):
            return StreamElementsSynthesizer(synthesizer_config)
        
        raise Exception(f"Invalid synthesizer config: {synthesizer_config.type}")