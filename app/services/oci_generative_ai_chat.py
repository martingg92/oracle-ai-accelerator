# oci_generative_ai_chat.py
# ============================================================
# Servicio de Chat con OCI GenAI - VERSIÓN SIN langchain-oci
# Usa OCI SDK directamente (igual que entel_rag_core)
# ============================================================

import os
import logging
from typing import List, Optional, Any

# OCI SDK - Igual que ENTEL
import oci
from oci.generative_ai_inference import GenerativeAiInferenceClient
from oci.generative_ai_inference.models import (
    OnDemandServingMode,
    ChatDetails,
    GenericChatRequest,
    SystemMessage,
    UserMessage,
    AssistantMessage,
    TextContent,
    ImageContent,
    ImageUrl,
)
from oci.retry import NoneRetryStrategy

# LangChain Core (para RAG, prompts, chains - NO para el LLM)
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage as LCSystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.prompts.chat import SystemMessagePromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableBranch, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from pydantic import Field

import components as component
import services.database as database
from dotenv import load_dotenv

# Initialize
load_dotenv()

logger = logging.getLogger("OCI_GenAI")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

# Initialize database services
db_doc_service = database.DocService()
db_agent_service = database.AgentService()


# =============================================================================
# CLIENTE OCI - Igual que ENTEL
# =============================================================================
def get_oci_genai_client() -> GenerativeAiInferenceClient:
    """
    Cliente OCI para Generative AI.
    Soporta: RESOURCE_PRINCIPAL, INSTANCE_PRINCIPAL, API_KEY
    """
    auth_type = os.getenv("CON_GEN_AI_AUTH_TYPE", "RESOURCE_PRINCIPAL")
    endpoint = os.getenv("CON_GEN_AI_SERVICE_ENDPOINT")
    
    try:
        if auth_type == "RESOURCE_PRINCIPAL":
            signer = oci.auth.signers.get_resource_principals_signer()
            client = GenerativeAiInferenceClient(
                config={},
                signer=signer,
                service_endpoint=endpoint,
                retry_strategy=NoneRetryStrategy(),
                timeout=(10, 240),
            )
        elif auth_type == "INSTANCE_PRINCIPAL":
            signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
            client = GenerativeAiInferenceClient(
                config={},
                signer=signer,
                service_endpoint=endpoint,
                retry_strategy=NoneRetryStrategy(),
                timeout=(10, 240),
            )
        else:
            # API_KEY - config file
            config = oci.config.from_file()
            oci.config.validate_config(config)
            client = GenerativeAiInferenceClient(
                config=config,
                service_endpoint=endpoint,
                retry_strategy=NoneRetryStrategy(),
                timeout=(10, 240),
            )
        
        logger.info(f"✅ Cliente OCI GenAI inicializado (auth={auth_type})")
        return client
        
    except Exception as e:
        logger.error(f"❌ Error inicializando cliente OCI: {e}")
        raise


# =============================================================================
# WRAPPER LANGCHAIN - Usa OCI SDK directamente
# =============================================================================
class ChatOCIGenAIDirect(BaseChatModel):
    """
    LangChain ChatModel que usa OCI SDK directamente.
    Soporta TODOS los modelos de OCI GenAI incluyendo Gemini.
    
    Modelos soportados:
    - google.gemini-2.5-pro
    - google.gemini-2.5-flash  
    - google.gemini-2.5-flash-lite
    - cohere.command-a-03-2025
    - cohere.command-r-plus-08-2024
    - meta.llama-3.3-70b-instruct
    - meta.llama-4-scout-17b-16e-instruct
    - xai.grok-3
    - xai.grok-4
    """
    
    model_id: str = Field(default="google.gemini-2.5-pro")
    compartment_id: str = Field(default="")
    service_endpoint: str = Field(default="")
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=4096)
    top_p: float = Field(default=0.9)
    auth_type: str = Field(default="RESOURCE_PRINCIPAL")
    
    _client: Any = None
    
    def model_post_init(self, __context: Any) -> None:
        """Inicializa el cliente OCI después de la validación."""
        self._client = self._create_client()
    
    def _create_client(self) -> GenerativeAiInferenceClient:
        """Crea el cliente OCI GenAI."""
        auth_type = self.auth_type or os.getenv("CON_GEN_AI_AUTH_TYPE", "RESOURCE_PRINCIPAL")
        endpoint = self.service_endpoint or os.getenv("CON_GEN_AI_SERVICE_ENDPOINT")
        
        if auth_type == "RESOURCE_PRINCIPAL":
            signer = oci.auth.signers.get_resource_principals_signer()
            return GenerativeAiInferenceClient(
                config={},
                signer=signer,
                service_endpoint=endpoint,
                retry_strategy=NoneRetryStrategy(),
                timeout=(10, 240),
            )
        elif auth_type == "INSTANCE_PRINCIPAL":
            signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
            return GenerativeAiInferenceClient(
                config={},
                signer=signer,
                service_endpoint=endpoint,
                retry_strategy=NoneRetryStrategy(),
                timeout=(10, 240),
            )
        else:
            config = oci.config.from_file()
            oci.config.validate_config(config)
            return GenerativeAiInferenceClient(
                config=config,
                service_endpoint=endpoint,
                retry_strategy=NoneRetryStrategy(),
                timeout=(10, 240),
            )
    
    @property
    def _llm_type(self) -> str:
        return "oci-genai-direct"
    
    def _convert_messages(self, messages: List[BaseMessage]) -> List:
        """Convierte mensajes LangChain a formato OCI SDK."""
        oci_messages = []
        
        for msg in messages:
            if isinstance(msg, LCSystemMessage):
                oci_messages.append(
                    SystemMessage(content=[TextContent(text=msg.content)])
                )
            elif isinstance(msg, HumanMessage):
                # Manejar contenido multimodal
                if isinstance(msg.content, list):
                    content_parts = []
                    for part in msg.content:
                        if isinstance(part, dict):
                            if part.get("type") == "text":
                                content_parts.append(TextContent(text=part["text"]))
                            elif part.get("type") == "image_url":
                                image_url = part.get("image_url", {})
                                url = image_url.get("url", "") if isinstance(image_url, dict) else image_url
                                if url.startswith("data:image"):
                                    content_parts.append(ImageContent(source=ImageUrl(url=url)))
                        elif isinstance(part, str):
                            content_parts.append(TextContent(text=part))
                    oci_messages.append(UserMessage(content=content_parts))
                else:
                    oci_messages.append(
                        UserMessage(content=[TextContent(text=msg.content)])
                    )
            elif isinstance(msg, AIMessage):
                oci_messages.append(
                    AssistantMessage(content=[TextContent(text=msg.content)])
                )
        
        return oci_messages
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs
    ) -> ChatResult:
        """Genera respuesta usando OCI SDK directamente."""
        
        if self._client is None:
            self._client = self._create_client()
        
        oci_messages = self._convert_messages(messages)
        
        # Crear request - IGUAL QUE ENTEL
        chat_request = GenericChatRequest(
            api_format=GenericChatRequest.API_FORMAT_GENERIC,
            messages=oci_messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
        )
        
        chat_details = ChatDetails(
            compartment_id=self.compartment_id,
            serving_mode=OnDemandServingMode(model_id=self.model_id),
            chat_request=chat_request,
        )
        
        # Llamar API
        response = self._client.chat(chat_details)
        
        # Extraer texto - IGUAL QUE ENTEL
        text = ""
        chat_response = response.data.chat_response
        if hasattr(chat_response, 'choices') and chat_response.choices:
            choice = chat_response.choices[0]
            if hasattr(choice, 'message') and choice.message:
                for content_part in choice.message.content:
                    if hasattr(content_part, 'text'):
                        text += content_part.text
        
        return ChatResult(
            generations=[
                ChatGeneration(
                    message=AIMessage(content=text),
                    generation_info={"model": self.model_id}
                )
            ]
        )
    
    @property
    def _identifying_params(self) -> dict:
        return {
            "model_id": self.model_id,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }


# =============================================================================
# POLYFILLS para LangChain (sin chains.combine_documents)
# =============================================================================
from langchain_core.runnables import RunnableLambda

def create_stuff_documents_chain(llm, prompt):
    """
    Recreación de create_stuff_documents_chain.
    Retorna el texto de respuesta del LLM.
    """
    def format_docs(inputs):
        docs = inputs.get("context", [])
        if isinstance(docs, list) and len(docs) > 0:
            return "\n\n".join(doc.page_content for doc in docs)
        return ""
    
    def run_chain(inputs):
        # Formatear documentos
        formatted_context = format_docs(inputs)
        
        # Preparar inputs para el prompt
        prompt_inputs = {**inputs, "context": formatted_context}
        
        # Ejecutar prompt -> llm
        messages = prompt.invoke(prompt_inputs)
        response = llm.invoke(messages)
        
        # Extraer texto
        if hasattr(response, 'content'):
            return response.content
        return str(response)
    
    return RunnableLambda(run_chain)


def create_history_aware_retriever(llm, retriever, prompt):
    """
    Recreación de create_history_aware_retriever.
    Si hay historial, reformula la pregunta antes de buscar.
    """
    def run_retriever(inputs):
        chat_history = inputs.get("chat_history", inputs.get("history", []))
        
        if chat_history and len(chat_history) > 0:
            # Reformular pregunta con contexto del historial
            messages = prompt.invoke(inputs)
            response = llm.invoke(messages)
            
            if hasattr(response, 'content'):
                rephrased = response.content
            else:
                rephrased = str(response)
            
            # Buscar con pregunta reformulada
            return retriever.invoke(rephrased)
        else:
            # Sin historial, buscar directamente
            return retriever.invoke(inputs.get("input", ""))
    
    return RunnableLambda(run_retriever)


def create_retrieval_chain(retriever, combine_docs_chain):
    """
    Recreación de create_retrieval_chain.
    Retorna dict con keys: input, context, answer
    """
    def run_chain(inputs):
        # Obtener documentos
        docs = retriever.invoke(inputs)
        
        # Preparar inputs con contexto
        chain_inputs = {**inputs, "context": docs}
        
        # Ejecutar chain de documentos
        answer = combine_docs_chain.invoke(chain_inputs)
        
        # Retornar en formato esperado
        return {
            "input": inputs.get("input", ""),
            "context": docs,
            "answer": answer,
            "chat_history": inputs.get("chat_history", inputs.get("history", [])),
        }
    
    return RunnableLambda(run_chain)


# =============================================================================
# SERVICIO PRINCIPAL - GenerativeAIService
# =============================================================================
class GenerativeAIService:
    """
    Servicio para crear cadenas RAG con OCI GenAI.
    Soporta todos los modelos incluyendo Gemini.
    """

    @staticmethod
    def get_llm(user_id, agent_id):
        """
        Obtiene el LLM configurado para el agente.
        Usa OCI SDK directamente - funciona con TODOS los modelos.
        """
        df_agents = db_agent_service.get_all_agents_cache(user_id)[
            lambda df: df["AGENT_ID"] == agent_id
        ]
        
        provider = str(df_agents["AGENT_MODEL_PROVIDER"].values[0]).lower()
        model_name = str(df_agents["AGENT_MODEL_NAME"].values[0])
        temperature = float(df_agents["AGENT_TEMPERATURE"].values[0])
        
        # Usar ChatOCIGenAIDirect para TODOS los proveedores
        # (google, cohere, meta, xai - todos funcionan igual)
        llm = ChatOCIGenAIDirect(
            model_id=model_name,
            service_endpoint=os.getenv("CON_GEN_AI_SERVICE_ENDPOINT"),
            compartment_id=os.getenv("CON_COMPARTMENT_ID"),
            auth_type=os.getenv("CON_GEN_AI_AUTH_TYPE", "RESOURCE_PRINCIPAL"),
            temperature=temperature,
            max_tokens=4096,
        )
        
        logger.info(f"✅ LLM inicializado: {model_name} (provider={provider})")
        return llm

    @staticmethod
    def get_chain(file_id, user_id, agent_id, history, input, input_imagen):
        """
        Crea una cadena RAG para el agente.
        """
        df_agents = db_agent_service.get_all_agents_cache(user_id)[
            lambda df: df["AGENT_ID"] == agent_id
        ]
        
        llm = GenerativeAIService.get_llm(user_id, agent_id)
        
        # Vector store
        vector_store = db_doc_service.get_vector_store()
        
        # Retriever
        context_retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 5,
                "filter": {"file_id": file_id}
            }
        )
        
        # Prompt de reformulación
        reformulation_prompt = ChatPromptTemplate.from_messages([
            ("system", str(df_agents["AGENT_PROMPT_SYSTEM"].values[0])),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        history_aware_retriever = create_history_aware_retriever(
            llm,
            context_retriever,
            reformulation_prompt
        )
        
        # Prompt de Q&A
        if input_imagen:
            question_answer_prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate(
                    prompt=PromptTemplate(
                        template=str(df_agents['AGENT_PROMPT_MESSAGE'].values[0]),
                        input_variables=["context"],
                    )
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", [
                    {"type": "text", "text": f"{str(df_agents['AGENT_PROMPT_MESSAGE'].values[0])}"},
                    {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,{input_imagen}"}, "detail": "high"}
                ]),
                ("human", "{input}")
            ])
        else:
            question_answer_prompt = ChatPromptTemplate.from_messages([
                ("system", str(df_agents["AGENT_PROMPT_MESSAGE"].values[0])),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}")
            ])
        
        combine_docs_chain = create_stuff_documents_chain(llm, question_answer_prompt)
        
        chain = create_retrieval_chain(
            retriever=history_aware_retriever,
            combine_docs_chain=combine_docs_chain
        )
        
        # Invocar
        if input_imagen:
            result = chain.invoke({
                "history": history,
                "input": input,
                "input_imagen": input_imagen
            })
        else:
            result = chain.invoke({
                "input": input,
                "history": history
            })
        
        return result

    @staticmethod
    def get_agent(user_id, agent_id, input):
        """
        Invocación directa al LLM sin RAG.
        """
        df_agents = db_agent_service.get_all_agents_cache(user_id)[
            lambda df: df["AGENT_ID"] == agent_id
        ]
        
        llm = GenerativeAIService.get_llm(user_id, agent_id)
        
        system_text = str(df_agents["AGENT_PROMPT_SYSTEM"].values[0])
        system_prompt = PromptTemplate(
            input_variables=["system_text", "query"],
            template="{system_text}\n{query}"
        )
        chain = system_prompt | llm
        
        response = chain.invoke({"system_text": system_text, "query": input})
        
        if hasattr(response, 'content'):
            return response.content
        return str(response)
