# app/services/database/oracle_vs.py
from __future__ import annotations
import logging
from typing import Any, Iterable, List, Optional, Type, Dict
import oracledb
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document

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
        # Implementación simplificada para inserción si la necesitas
        # (Para RAG de lectura, el método crítico es similarity_search)
        return []

    def similarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        """Realiza búsqueda vectorial usando Oracle 23ai."""
        embedding = self.embedding_function.embed_query(query)
        
        # SQL dinámico para búsqueda vectorial en 23ai
        # Asegúrate de que tu tabla tenga la columna 'vector' tipo VECTOR
        sql = f"""
            SELECT id, text, metadata 
            FROM {self.table_name}
            ORDER BY VECTOR_DISTANCE(vector, :embedding, {self.distance_strategy})
            FETCH FIRST :k ROWS ONLY
        """
        
        # Convertir embedding a array para oracledb si es necesario
        # En oracledb 2.0+ y DB 23c, se suele pasar como array.
        import array
        embedding_array = array.array("f", embedding)

        cursor = self.client.cursor()
        cursor.execute(sql, embedding=embedding_array, k=k)
        
        docs = []
        for row in cursor:
            # Asumiendo estructura: id (0), text (1), metadata (2)
            # Metadata suele ser JSON o string, ajustar según tu esquema
            import json
            meta = json.loads(row[2]) if row[2] else {}
            docs.append(Document(page_content=row[1], metadata=meta))
            
        cursor.close()
        return docs

    @classmethod
    def from_texts(cls, *args, **kwargs):
        raise NotImplementedError("Usar constructor directo init")
