from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.google import GeminiLlmService
import os
from dotenv import load_dotenv
import re
from vanna.integrations.openai import OpenAILlmService

load_dotenv()
def validate_sql(sql: str) -> bool:
    """Validate SQL against dangerous statements and system tables."""
    sql_upper = sql.upper()
    
    # Must be SELECT only
    stripped_sql = sql.strip().upper()
    if not stripped_sql.startswith("SELECT"):
        return False
        
    # No dangerous keywords
    dangerous_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "EXEC", "XP_", "SP_", "GRANT", "REVOKE", "SHUTDOWN"]
    for word in dangerous_keywords:
        if re.search(r'\b' + re.escape(word) + r'\b', sql_upper):
            return False

    # No system tables
    system_tables = ["SQLITE_MASTER", "SQLITE_SEQUENCE", "SQLITE_STAT1"]
    for table in system_tables:
        if table in sql_upper:
            return False
            
    return True

class ValidatedSqliteRunner(SqliteRunner):
    def run_sql(self, args, context):
        sql = args.sql
        if not validate_sql(sql):
            raise ValueError("Invalid SQL: only SELECT queries are allowed, and no system tables or dangerous keywords.")
        return super().run_sql(args, context)

# 1. LLM Services
google_api_key = os.environ.get("GOOGLE_API_KEY")
llm_gemini = GeminiLlmService(
    api_key=google_api_key,
    model="gemini-2.5-flash"
)

z_api_key = os.environ.get("ZAI_API_KEY", "")
llm_glm = OpenAILlmService(
    api_key=z_api_key,
    model="glm-4.5-flash",
    base_url="https://api.z.ai/api/paas/v4/"
)

# 2. SqliteRunner with Validation
runner = ValidatedSqliteRunner(database_path='clinic.db')

# 3. ToolRegistry
registry = ToolRegistry()
registry.register_local_tool(RunSqlTool(sql_runner=runner), ["*"])
registry.register_local_tool(VisualizeDataTool(), ["*"])

# 4. Agent Memory
memory = DemoAgentMemory()
registry.register_local_tool(SaveQuestionToolArgsTool(), ["*"])
registry.register_local_tool(SearchSavedCorrectToolUsesTool(), ["*"])

# 5. UserResolver
class DefaultUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(id="default_user")

user_resolver = DefaultUserResolver()

# 6. Create Agents
config = AgentConfig()

agent_gemini = Agent(
    llm_service=llm_gemini,
    tool_registry=registry,
    agent_memory=memory,
    user_resolver=user_resolver,
    config=config
)

agent_glm = Agent(
    llm_service=llm_glm,
    tool_registry=registry,
    agent_memory=memory,
    user_resolver=user_resolver,
    config=config
)
