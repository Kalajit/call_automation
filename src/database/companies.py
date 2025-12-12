from typing import Optional, Dict
from src.database.connection import get_db_pool
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


async def get_company_config(
    company_id: int, 
    prompt_key: str = None, 
    agent_instance_id: int = None
) -> Optional[Dict]:
    """Fetch company, agent config, and agent instance from database"""
    db_pool = get_db_pool()
    
    async with db_pool.acquire() as conn:
        # Get company info
        company = await conn.fetchrow(
            "SELECT * FROM companies WHERE id = $1", company_id
        )
        if not company:
            logger.error(f"❌ Company {company_id} not found")
            return None
        
        # Get agent instance if provided
        agent_instance = None
        if agent_instance_id:
            agent_instance = await conn.fetchrow(
                "SELECT * FROM agent_instances WHERE id = $1 AND company_id = $2 AND is_active = TRUE",
                agent_instance_id, company_id
            )

            if not agent_instance:
                logger.warning(f"⚠️ Agent instance {agent_instance_id} not found, using default config")
        
        # Get agent config (use instance's config or default)
        config_id = agent_instance['agent_config_id'] if agent_instance else None
        
        if config_id:
            agent_config = await conn.fetchrow(
                "SELECT * FROM agent_configs WHERE id = $1", config_id
            )
        else:
            # Fallback to default config
            query = """
                SELECT * FROM agent_configs 
                WHERE company_id = $1 AND is_active = TRUE
            """
            params = [company_id]
            
            if prompt_key:
                query += " AND prompt_key = $2"
                params.append(prompt_key)
            else:
                query += " ORDER BY created_at DESC LIMIT 1"
            
            agent_config = await conn.fetchrow(query, *params)
        
        if not agent_config:
            logger.error(f"❌ No agent config found for company {company_id}")
            return None
        
        # Override with agent instance customizations
        agent_dict = dict(agent_config)
        if agent_instance:
            if agent_instance['custom_prompt']:
                agent_dict['prompt_preamble'] = agent_instance['custom_prompt']
            if agent_instance['custom_voice']:
                agent_dict['voice'] = agent_instance['custom_voice']
            if agent_instance['phone_number']:
                company_dict = dict(company)
                company_dict['phone_number'] = agent_instance['phone_number']
                company = company_dict
        
        return {
            "company": dict(company),
            "agent": agent_dict,
            "agent_instance": dict(agent_instance) if agent_instance else None
        }