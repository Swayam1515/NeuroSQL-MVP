import asyncio
from vanna_setup import agent
from vanna.core.user.request_context import RequestContext

async def test_chat():
    try:
        ctx = RequestContext(user_id="default_user")
    except TypeError:
        # If it doesn't take user_id
        from vanna.core.user.models import User
        ctx = RequestContext(user=User(id="default_user"))
        
    question = "Show me the top 5 patients by total spending"
    print(f"Asking: {question}")
    
    components = []
    try:
        async for comp in agent.send_message(request_context=ctx, message=question):
            components.append(comp)
            print("Component type:", type(comp).__name__)
            # print all attributes
            print({k: v for k, v in vars(comp).items() if not k.startswith('_')})
            if hasattr(comp, 'to_dict'):
                print(comp.to_dict())
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chat())
