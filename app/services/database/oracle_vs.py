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
        
        # --- CORRECCIÓN REALIZADA AQUÍ ---
        # Antes decía 'vector', ahora usa 'embedding' que es el nombre real 
        # confirmado en tu archivo j.TABLE_DOCS.sql
        sql = f"""
            SELECT id, text, metadata 
            FROM {self.table_name}
            ORDER BY VECTOR_DISTANCE(embedding, :embedding, {self.distance_strategy})
            FETCH FIRST :k ROWS ONLY
        """
        
        # Convertir embedding a array float (requerido por oracledb 2.0+)
        embedding_array = array.array("f", embedding)

        cursor = self.client.cursor()
        try:
            cursor.execute(sql, embedding=embedding_array, k=k)
            
            docs = []
            for row in cursor:
                # row[0]=id, row[1]=text, row[2]=metadata
                # Manejo seguro de metadata (puede ser None o string JSON)
                meta_content = row[2]
                if meta_content:
                    if isinstance(meta_content, str):
                        try:
                            meta = json.loads(meta_content)
                        except json.JSONDecodeError:
                            meta = {"content": meta_content}
                    elif isinstance(meta_content, dict):
                        meta = meta_content
                    else:
                        meta = {}
                else:
                    meta = {}

                docs.append(Document(page_content=row[1], metadata=meta))
                
            return docs
        except Exception as e:
            logger.error(f"Error en similarity_search: {e}")
            raise e
        finally:
            cursor.close()

    @classmethod
    def from_texts(cls, *args, **kwargs):
        raise NotImplementedError("Usar constructor directo init")
