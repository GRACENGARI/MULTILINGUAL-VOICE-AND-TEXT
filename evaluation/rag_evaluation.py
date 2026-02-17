#!/usr/bin/env python3
"""
RAG System Evaluation Framework
Measures performance of the African Language AI Tutor RAG system
"""

import json
import time
from typing import List, Dict, Any
from datetime import datetime
import numpy as np
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

class RAGEvaluator:
    """Comprehensive RAG evaluation metrics"""
    
    def __init__(self, language="Kiswahili"):
        self.language = language
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
        
    # ============================================
    # 1. RETRIEVAL METRICS
    # ============================================
    
    def evaluate_retrieval_precision(self, query: str, retrieved_docs: List[Document], 
                                     relevant_docs: List[str]) -> float:
        """
        Precision = (Relevant Retrieved) / (Total Retrieved)
        Measures accuracy of retrieval
        """
        retrieved_content = [doc.page_content for doc in retrieved_docs]
        relevant_retrieved = sum(1 for doc in retrieved_content if any(rel in doc for rel in relevant_docs))
        
        precision = relevant_retrieved / len(retrieved_docs) if retrieved_docs else 0
        return precision
    
    def evaluate_retrieval_recall(self, query: str, retrieved_docs: List[Document], 
                                  relevant_docs: List[str]) -> float:
        """
        Recall = (Relevant Retrieved) / (Total Relevant)
        Measures completeness of retrieval
        """
        retrieved_content = [doc.page_content for doc in retrieved_docs]
        relevant_retrieved = sum(1 for rel in relevant_docs if any(rel in doc for doc in retrieved_content))
        
        recall = relevant_retrieved / len(relevant_docs) if relevant_docs else 0
        return recall
    
    def evaluate_retrieval_f1(self, precision: float, recall: float) -> float:
        """
        F1 Score = 2 * (Precision * Recall) / (Precision + Recall)
        Harmonic mean of precision and recall
        """
        if precision + recall == 0:
            return 0
        return 2 * (precision * recall) / (precision + recall)
    
    def evaluate_mrr(self, query: str, retrieved_docs: List[Document], 
                     relevant_doc: str) -> float:
        """
        Mean Reciprocal Rank (MRR)
        Measures rank of first relevant document
        """
        for i, doc in enumerate(retrieved_docs, 1):
            if relevant_doc in doc.page_content:
                return 1.0 / i
        return 0.0
    
    def evaluate_ndcg(self, retrieved_docs: List[Document], 
                      relevance_scores: List[float], k: int = 5) -> float:
        """
        Normalized Discounted Cumulative Gain (NDCG@k)
        Measures ranking quality
        """
        def dcg(scores):
            return sum((2**score - 1) / np.log2(i + 2) for i, score in enumerate(scores[:k]))
        
        actual_dcg = dcg(relevance_scores)
        ideal_dcg = dcg(sorted(relevance_scores, reverse=True))
        
        return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0.0
    
    # ============================================
    # 2. GENERATION METRICS
    # ============================================
    
    def evaluate_answer_relevance(self, query: str, answer: str) -> float:
        """
        Measures how relevant the answer is to the query
        Uses semantic similarity
        """
        query_embedding = self.embeddings.embed_query(query)
        answer_embedding = self.embeddings.embed_query(answer)
        
        # Cosine similarity
        similarity = np.dot(query_embedding, answer_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(answer_embedding)
        )
        return float(similarity)
    
    def evaluate_faithfulness(self, answer: str, context: str) -> float:
        """
        Measures if answer is grounded in retrieved context
        Checks for hallucination
        """
        prompt = f"""
        Rate how faithful this answer is to the context (0-1 scale):
        
        Context: {context}
        Answer: {answer}
        
        Return only a number between 0 and 1, where:
        - 1.0 = Answer is completely grounded in context
        - 0.5 = Answer is partially grounded
        - 0.0 = Answer contradicts or ignores context
        
        Score:"""
        
        try:
            response = self.llm.invoke(prompt)
            score = float(response.content.strip())
            return max(0.0, min(1.0, score))
        except:
            return 0.5  # Default if parsing fails
    
    def evaluate_answer_correctness(self, answer: str, ground_truth: str) -> float:
        """
        Compares answer with ground truth
        Uses semantic similarity
        """
        answer_embedding = self.embeddings.embed_query(answer)
        truth_embedding = self.embeddings.embed_query(ground_truth)
        
        similarity = np.dot(answer_embedding, truth_embedding) / (
            np.linalg.norm(answer_embedding) * np.linalg.norm(truth_embedding)
        )
        return float(similarity)
    
    def evaluate_answer_completeness(self, answer: str, expected_points: List[str]) -> float:
        """
        Checks if answer covers all expected points
        """
        covered = sum(1 for point in expected_points if point.lower() in answer.lower())
        return covered / len(expected_points) if expected_points else 0.0
    
    # ============================================
    # 3. CONTEXT METRICS
    # ============================================
    
    def evaluate_context_relevance(self, query: str, context: str) -> float:
        """
        Measures relevance of retrieved context to query
        """
        query_embedding = self.embeddings.embed_query(query)
        context_embedding = self.embeddings.embed_query(context)
        
        similarity = np.dot(query_embedding, context_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(context_embedding)
        )
        return float(similarity)
    
    def evaluate_context_precision(self, context: str, answer: str) -> float:
        """
        Measures how much of the context is actually used in the answer
        """
        context_sentences = context.split('.')
        used_sentences = sum(1 for sent in context_sentences if sent.strip() and sent.strip() in answer)
        
        return used_sentences / len(context_sentences) if context_sentences else 0.0
    
    # ============================================
    # 4. PERFORMANCE METRICS
    # ============================================
    
    def evaluate_latency(self, start_time: float, end_time: float) -> Dict[str, float]:
        """
        Measures response time
        """
        latency = end_time - start_time
        return {
            "latency_seconds": latency,
            "latency_ms": latency * 1000,
            "is_acceptable": latency < 5.0  # 5 seconds threshold
        }
    
    def evaluate_throughput(self, num_queries: int, total_time: float) -> float:
        """
        Queries per second
        """
        return num_queries / total_time if total_time > 0 else 0.0
    
    # ===========================================