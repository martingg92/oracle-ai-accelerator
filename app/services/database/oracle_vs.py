# app/services/database/oracle_vs.py
from __future__ import annotations
import logging
from typing import Any, Iterable, List, Optional, Type, Dict
import oracledb
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document
import array
import json

logger = logging.getLogger(__name__)

class OracleVS(VectorStore):
    """Oracle AI Vector Search Wrapper compatible con OCI."""
    
    def __init__(
        self,
        client: oracledb.Connection,
        embedding_function: Embeddings,
        table_name: str,
        distance_strategy: str = "COSINE",
        query: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
    ):
        self.client = client
        self.embedding_function = embedding_function
        self.table_name = table_name
        self.distance_strategy = distance_strategy
        self.query = query
        self.params = params

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> List[str]:
        return []

    def similarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        """Realiza búsqueda vectorial usando Oracle 23ai."""
        embedding = self.embedding_function.embed_query(query)
        
        # SQL corregido (usa 'embedding')
        sql = f"""
            SELECT id, text, metadata 
            FROM {self.table_name}
            ORDER BY VECTOR_DISTANCE(embedding, :embedding, {self.distance_strategy})
            FETCH FIRST :k ROWS ONLY
        """
        
        # Convertir embedding a array float
        embedding_array = array.array("f", embedding)

        cursor = self.client.cursor()
        try:
            cursor.execute(sql, embedding=embedding_array, k=k)
            
            docs = []
            for row in cursor:
                # row[0]=id, row[1]=text (CLOB), row[2]=metadata (CLOB)
                
                # --- CORRECCIÓN CLOB TEXTO ---
                text_obj = row[1]
                if hasattr(text_obj, "read"): # Si es un LOB, leerlo
                    page_content = text_obj.read()
                else:
                    page_content = str(text_obj) if text_obj else ""

                # --- CORRECCIÓN CLOB METADATA ---
                meta_obj = row[2]
                meta_str = ""
                if hasattr(meta_obj, "read"): # Si es un LOB, leerlo
                    meta_str = meta_obj.read()
                else:
                    meta_str = str(meta_obj) if meta_obj else ""

                # Parsear JSON de metadata
                meta = {}
                if meta_str:
                    try:
                        # Intentamos parsear si parece un JSON
                        if meta_str.strip().startswith("{"):
                            meta = json.loads(meta_str)
                        else:
                            meta = {"content": meta_str}
                    except json.JSONDecodeError:
                        meta = {"content": meta_str}
                
                # Crear documento compatible con LangChain
                docs.append(Document(page_content=page_content, metadata=meta))
                
            return docs
        except Exception as e:
            logger.error(f"Error en similarity_search: {e}")
            raise e
        finally:
            cursor.close()

    @classmethod
    def from_texts(cls, *args, **kwargs):
        raise NotImplementedError("Usar constructor directo init")
