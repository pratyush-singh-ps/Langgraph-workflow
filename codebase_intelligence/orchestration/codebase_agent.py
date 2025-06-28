"""
Codebase Agent - LangGraph Workflow

Responsible for:
- Orchestrating the complete codebase analysis workflow
- Managing state transitions between retrieval and generation
- Coordinating between code retrieval and LLM response generation
- Providing a unified interface for codebase queries
"""

# Requirements: pip install langchain langgraph openai tiktoken faiss-cpu
try:
    import langgraph
    from langgraph.graph import StateGraph, END
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from langchain_openai import ChatOpenAI
except ImportError as e:
    print("Missing dependencies. Please run: pip install langchain langgraph openai tiktoken faiss-cpu")
    raise e

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from codebase_intelligence.retrieval.codebase_retriever import CodebaseRetriever

# Define the state schema
from typing import TypedDict, List, Optional, Union
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """State schema for the LangGraph workflow."""
    messages: List[BaseMessage]
    query: str
    codebase: Optional[str]  # "ccp-vap", "ccp-execute", or "both"
    retrieved_docs: List
    response: Optional[str]

class CodebaseAgent:
    """
    Main agent class that orchestrates codebase analysis using LangGraph.
    
    Responsibilities:
    - Building and managing LangGraph workflows
    - Coordinating code retrieval and response generation
    - Managing conversation state and context
    - Providing a clean interface for codebase queries
    """
    
    def __init__(self):
        """Initialize the CodebaseAgent with retriever and LLM."""
        self.retriever = CodebaseRetriever()
        
        # Initialize the LLM for LangGraph
        self.llm = ChatOpenAI(
            base_url="https://ciq-litellm-proxy-service.prod-dbx.commerceiq.ai",
            api_key="sk-WRDSNGPePp-cHG5Q6WhRjA",  # type: ignore
            model="openai/gpt-4o"
        )
        
        # Define system prompt for structured responses
        self.system_prompt = """You are a codebase analysis assistant. When responding to queries about code:

1. **Always provide responses in a point-wise manner** using bullet points or numbered lists
2. **For any code snippets mentioned, always include the file name and its parent directory** (not the full path) where the code is located
3. **Be specific and concise** in your explanations
4. **Reference the actual code** when making statements about functionality
5. **Use clear formatting** with proper markdown for code blocks

**IMPORTANT**: When you see a full file path like `/path/to/controller/filename.java`, mention `controller/filename.java` in your response.

Example format:
• **Point 1**: Description with reference to `controller/filename.java`
• **Point 2**: Another description with reference to `service/another_file.java`

When showing code snippets, always include the file name and parent directory:
```java
// File: controller/filename.java
public class Example {
    // code here
}
```

Focus on providing actionable insights and clear explanations based on the actual codebase."""
        
        # Build the workflow
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        """
        Build the LangGraph workflow with nodes and edges.
        
        Returns:
            Compiled LangGraph workflow
        """
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("retrieve_code", self._retrieve_code_node)
        workflow.add_node("generate_response", self._generate_response_node)
        
        # Add edges
        workflow.add_edge("retrieve_code", "generate_response")
        workflow.add_edge("generate_response", END)
        
        # Set entry point
        workflow.set_entry_point("retrieve_code")
        
        return workflow.compile()
    
    def _retrieve_code_node(self, state: AgentState) -> AgentState:
        """
        Retrieve relevant code based on the query.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with retrieved documents
        """
        query = state["query"]
        codebase = state.get("codebase", "both")
        
        print(f"🔍 Retrieving code for: {query}")
        print(f"📁 Codebase: {codebase}")
        
        # Retrieve relevant documents
        if codebase == "ccp-vap":
            docs = self.retriever.retrieve_from_vap(query, k=5)
        elif codebase == "ccp-execute":
            docs = self.retriever.retrieve_from_execute(query, k=5)
        else:  # both
            docs = self.retriever.retrieve_from_both(query, k=5)
        
        print(f"📄 Found {len(docs)} relevant code chunks")
        
        # Update state with retrieved documents
        state["retrieved_docs"] = docs
        
        # Add context to messages
        context = self.retriever.format_retrieved_docs(docs)
        if context:
            context_message = f"Here is relevant code from the codebase:\n{context}\n\nPlease use this code to answer the user's question."
            state["messages"].append(HumanMessage(content=context_message))
        
        return state
    
    def _generate_response_node(self, state: AgentState) -> AgentState:
        """
        Generate response using the LLM with retrieved context.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with generated response
        """
        # Create messages with system prompt
        messages = [SystemMessage(content=self.system_prompt)] + state["messages"]
        
        print("🤖 Generating response with LLM...")
        
        try:
            # Use the LLM to generate response
            response = self.llm.invoke(messages)
            state["response"] = str(response.content)
            
            print("✅ Response generated successfully")
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            state["response"] = f"Sorry, I encountered an error while generating the response: {str(e)}"
        
        return state
    
    def query_codebase(self, query: str, codebase: str = "both") -> str:
        """
        Main method to query the codebase.
        
        Args:
            query: User's question about the codebase
            codebase: Which codebase to search ("ccp-vap", "ccp-execute", or "both")
            
        Returns:
            Generated response based on codebase analysis
        """
        # Initialize state
        state = AgentState(
            messages=[HumanMessage(content=query)],
            query=query,
            codebase=codebase,
            retrieved_docs=[],
            response=None
        )
        
        # Run the workflow
        result = self.workflow.invoke(state)
        
        return result["response"]

# Example usage
if __name__ == "__main__":
    agent = CodebaseAgent()
    
    # Test queries
    test_queries = [
        ("Show me the controller classes", "both"),
        ("What services are available in ccp-vap?", "ccp-vap"),
        ("How is execution handled in ccp-execute?", "ccp-execute"),
    ]
    
    for query, codebase in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"Codebase: {codebase}")
        print(f"{'='*60}")
        
        response = agent.query_codebase(query, codebase)
        print(f"\nResponse:\n{response}")
        print(f"\n{'-'*60}") 