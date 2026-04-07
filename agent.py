import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv
load_dotenv()

# 1. Đọc System Prompt bằng đường dẫn tuyệt đối
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()
# 2. Khai báo State
class AgentState (TypedDict):
    messages: Annotated[list, add_messages]
# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it", 
    temperature=0  )
llm_with_tools = llm.bind_tools (tools_list)
# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    if not isinstance (messages [0], SystemMessage):
         messages = [SystemMessage (content=SYSTEM_PROMPT) ] + messages
    response = llm_with_tools.invoke (messages)
# # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Gọi tool: {tc['name']} ({tc['args']})")
    else:
        print(f"Trả lời trực tiếp")
    return {"messages": [response]}
# 5. xây dựng Graph
builder = StateGraph (AgentState)
builder.add_node("agent", agent_node)
tool_node = ToolNode(tools_list)
builder.add_node ("tools", tool_node)
builder.add_edge(START, "agent")

# Luồng điều kiện: Sau khi agent xử lý, kiểm tra xem có yêu cầu gọi tool không
# - Nếu có tool_calls: Đi sang node "tools"
# - Nếu không (trả lời xong): Đi đến END
builder.add_conditional_edges(
    "agent", 
    tools_condition, 
)
# Luồng quay lại: Sau khi node "tools" thực hiện xong, phải quay lại "agent" 
# để LLM đọc kết quả từ tool và tổng hợp câu trả lời
builder.add_edge("tools", "agent")

# Biên dịch Graph
graph = builder.compile()
graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__ ":
    print("=" * 60)
    print("TravelBuddy - Trợ lý Du lịch Thông minh")
    print(" Gõ 'quit' để thoát")
    print("=" * 60)
while True:
    user_input = input("\nBạn: ").strip()
    if user_input.lower() in ("quit", "exit", "q"):
        break
    print("\nTravelBuddy đang suy nghĩ...")
    result = graph.invoke({"messages": [("human", user_input) ]})
    final = result["messages"][-1]
    if isinstance(final.content, list):
        for part in final.content:
            if isinstance(part, dict) and part.get('type') == 'text':
                print(f"\nTravelBuddy: {part['text']}")
    else:
        print(f"\nTravelBuddy: {final.content}")
    
    