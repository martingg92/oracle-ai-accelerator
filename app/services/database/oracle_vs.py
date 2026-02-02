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
        self, query: str, k: int = 7, filter: dict = None, **kwargs: Any
    ) -> List[Document]:
        """Realiza búsqueda vectorial usando Oracle 23ai con filtro opcional."""
        embedding = self.embedding_function.embed_query(query)
        
        # Construir WHERE dinámico
        where_clause = ""
        bind_vars = {"embedding": array.array("f", embedding), "k": k}
        
        if filter and "file_id" in filter:
            file_ids = filter["file_id"]
            if isinstance(file_ids, list):
                placeholders = ", ".join([f":fid{i}" for i in range(len(file_ids))])
                where_clause = f"WHERE file_id IN ({placeholders})"
                for i, fid in enumerate(file_ids):
                    bind_vars[f"fid{i}"] = fid
            else:
                where_clause = "WHERE file_id = :file_id"
                bind_vars["file_id"] = file_ids
        
        sql = f"""
            SELECT id, text, metadata, file_id
            FROM {self.table_name}
            {where_clause}
            ORDER BY VECTOR_DISTANCE(embedding, :embedding, {self.distance_strategy})
            FETCH FIRST :k ROWS ONLY
        """
        
        cursor = self.client.cursor()
        try:
            cursor.execute(sql, bind_vars) #cursor.execute(sql, **bind_vars)
            docs = []
            for row in cursor:
                text_obj = row[1]
                page_content = text_obj.read() if hasattr(text_obj, "read") else str(text_obj or "")
                
                meta_obj = row[2]
                meta_str = meta_obj.read() if hasattr(meta_obj, "read") else str(meta_obj or "")
                
                meta = json.loads(meta_str) if meta_str.strip().startswith("{") else {"content": meta_str}
                meta["file_id"] = row[3]  # Agregar file_id a metadata
                
                docs.append(Document(page_content=page_content, metadata=meta))
            return docs
        finally:
            cursor.close()

    @classmethod
    def from_texts(cls, *args, **kwargs):
        raise NotImplementedError("Usar constructor directo init")
