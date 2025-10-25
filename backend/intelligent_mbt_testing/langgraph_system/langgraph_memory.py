#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangGraph长期记忆系统 - 智能体经验学习和知识积累
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import numpy as np
from dataclasses import dataclass, asdict
import pickle

from .langgraph_models import get_model_manager

@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    agent_type: str
    experience_type: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    timestamp: str
    success_score: float
    usage_count: int = 0
    last_accessed: str = None

class LangGraphLongTermMemory:
    """
    LangGraph长期记忆系统
    
    功能：
    - 智能体经验存储和检索
    - 向量化相似度搜索
    - 知识积累和学习
    - 成功案例推荐
    """
    
    def __init__(self, memory_dir: str = "./enhanced_workspace/long_term_memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # 内存中的记忆索引
        self.memory_index: Dict[str, MemoryEntry] = {}
        self.agent_memories: Dict[str, List[str]] = {
            "coordinator": [],
            "analyzer": [],
            "planner": [],
            "data_processor": [],
            "executor": [],
            "reporter": [],
            "system": []  # 添加系统级记忆
        }
        
        # 模型管理器
        self.model_manager = get_model_manager()
        self.embedding_model = None
        
        # 统计信息
        self.stats = {
            "total_memories": 0,
            "successful_retrievals": 0,
            "failed_retrievals": 0,
            "last_cleanup": datetime.now().isoformat()
        }
        
        print("🧠 LangGraph长期记忆系统初始化")
        print(f"   📁 记忆目录: {memory_dir}")
        
        # 加载现有记忆
        asyncio.create_task(self._load_existing_memories())
    
    async def _load_existing_memories(self):
        """加载现有记忆"""
        try:
            # 初始化嵌入模型
            self.embedding_model = self.model_manager.get_embedding_model()
            
            # 加载记忆文件
            memory_files = list(self.memory_dir.glob("*.json"))
            for file_path in memory_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        memory_entry = MemoryEntry(**data)
                        self.memory_index[memory_entry.id] = memory_entry
                        
                        # 确保智能体类型存在
                        if memory_entry.agent_type not in self.agent_memories:
                            self.agent_memories[memory_entry.agent_type] = []
                        
                        self.agent_memories[memory_entry.agent_type].append(memory_entry.id)
                except Exception as e:
                    print(f"⚠️ 加载记忆文件失败 {file_path}: {e}")
            
            self.stats["total_memories"] = len(self.memory_index)
            print(f"   ✅ 加载了 {self.stats['total_memories']} 条历史记忆")
            
        except Exception as e:
            print(f"⚠️ 长期记忆初始化失败: {e}")
    
    async def store_experience(self, agent_type: str, experience_type: str, 
                             content: str, metadata: Dict[str, Any] = None,
                             success_score: float = 0.5) -> str:
        """
        存储智能体经验
        
        Args:
            agent_type: 智能体类型
            experience_type: 经验类型 (success, failure, insight, pattern)
            content: 经验内容
            metadata: 元数据
            success_score: 成功评分 (0-1)
        
        Returns:
            记忆ID
        """
        try:
            # 生成记忆ID
            memory_id = f"{agent_type}_{experience_type}_{int(datetime.now().timestamp() * 1000)}"
            
            # 生成嵌入向量
            embedding = []
            if self.embedding_model:
                try:
                    embedding = await self.embedding_model.aembed_query(content)
                except:
                    # 如果异步失败，尝试同步
                    embedding = self.embedding_model.embed_query(content)
            
            # 创建记忆条目
            memory_entry = MemoryEntry(
                id=memory_id,
                agent_type=agent_type,
                experience_type=experience_type,
                content=content,
                embedding=embedding,
                metadata=metadata or {},
                timestamp=datetime.now().isoformat(),
                success_score=success_score,
                usage_count=0,
                last_accessed=None
            )
            
            # 存储到内存索引
            self.memory_index[memory_id] = memory_entry
            
            # 确保智能体类型存在
            if agent_type not in self.agent_memories:
                self.agent_memories[agent_type] = []
            
            self.agent_memories[agent_type].append(memory_id)
            
            # 持久化存储
            await self._persist_memory(memory_entry)
            
            self.stats["total_memories"] += 1
            
            print(f"🧠 [{agent_type}] 存储新经验: {experience_type}")
            print(f"   📝 内容: {content[:50]}...")
            print(f"   🎯 成功评分: {success_score:.2f}")
            
            return memory_id
            
        except Exception as e:
            print(f"❌ 存储经验失败: {e}")
            return None
    
    async def retrieve_similar_experiences(self, agent_type: str, query: str, 
                                         top_k: int = 5, min_similarity: float = 0.7) -> List[MemoryEntry]:
        """
        检索相似经验
        
        Args:
            agent_type: 智能体类型
            query: 查询内容
            top_k: 返回数量
            min_similarity: 最小相似度阈值
            
        Returns:
            相似记忆列表
        """
        try:
            if not self.embedding_model:
                return []
            
            # 生成查询向量
            try:
                query_embedding = await self.embedding_model.aembed_query(query)
            except:
                query_embedding = self.embedding_model.embed_query(query)
            
            # 计算相似度
            similarities = []
            agent_memory_ids = self.agent_memories.get(agent_type, [])
            
            for memory_id in agent_memory_ids:
                memory = self.memory_index.get(memory_id)
                if memory and memory.embedding:
                    similarity = self._cosine_similarity(query_embedding, memory.embedding)
                    if similarity >= min_similarity:
                        similarities.append((similarity, memory))
            
            # 按相似度排序
            similarities.sort(key=lambda x: x[0], reverse=True)
            
            # 更新访问记录
            results = []
            for similarity, memory in similarities[:top_k]:
                memory.usage_count += 1
                memory.last_accessed = datetime.now().isoformat()
                results.append(memory)
            
            self.stats["successful_retrievals"] += len(results)
            if len(results) == 0:
                self.stats["failed_retrievals"] += 1
            
            print(f"🔍 [{agent_type}] 检索到 {len(results)} 条相似经验")
            for i, memory in enumerate(results):
                print(f"   {i+1}. {memory.experience_type} (相似度: {similarities[i][0]:.3f})")
            
            return results
            
        except Exception as e:
            print(f"❌ 检索经验失败: {e}")
            self.stats["failed_retrievals"] += 1
            return []
    
    async def get_success_patterns(self, agent_type: str, experience_type: str = "success") -> List[MemoryEntry]:
        """获取成功模式"""
        try:
            agent_memory_ids = self.agent_memories.get(agent_type, [])
            success_memories = []
            
            for memory_id in agent_memory_ids:
                memory = self.memory_index.get(memory_id)
                if (memory and 
                    memory.experience_type == experience_type and 
                    memory.success_score > 0.7):
                    success_memories.append(memory)
            
            # 按成功评分和使用频率排序
            success_memories.sort(key=lambda x: (x.success_score, x.usage_count), reverse=True)
            
            print(f"📈 [{agent_type}] 找到 {len(success_memories)} 个成功模式")
            return success_memories[:10]  # 返回前10个
            
        except Exception as e:
            print(f"❌ 获取成功模式失败: {e}")
            return []
    
    async def learn_from_feedback(self, memory_id: str, feedback_score: float, feedback_content: str = ""):
        """从反馈中学习"""
        try:
            memory = self.memory_index.get(memory_id)
            if memory:
                # 更新成功评分（加权平均）
                old_score = memory.success_score
                memory.success_score = (old_score + feedback_score) / 2
                
                # 添加反馈到元数据
                if "feedback_history" not in memory.metadata:
                    memory.metadata["feedback_history"] = []
                
                memory.metadata["feedback_history"].append({
                    "score": feedback_score,
                    "content": feedback_content,
                    "timestamp": datetime.now().isoformat()
                })
                
                # 持久化更新
                await self._persist_memory(memory)
                
                print(f"📚 记忆学习更新: {memory_id}")
                print(f"   📊 评分变化: {old_score:.3f} → {memory.success_score:.3f}")
                
        except Exception as e:
            print(f"❌ 学习反馈失败: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        agent_stats = {}
        for agent_type, memory_ids in self.agent_memories.items():
            memories = [self.memory_index[mid] for mid in memory_ids if mid in self.memory_index]
            agent_stats[agent_type] = {
                "total": len(memories),
                "success_rate": sum(1 for m in memories if m.success_score > 0.7) / max(1, len(memories)),
                "avg_usage": sum(m.usage_count for m in memories) / max(1, len(memories))
            }
        
        return {
            "total_memories": self.stats["total_memories"],
            "retrieval_success_rate": self.stats["successful_retrievals"] / max(1, 
                self.stats["successful_retrievals"] + self.stats["failed_retrievals"]),
            "agent_stats": agent_stats,
            "last_cleanup": self.stats["last_cleanup"]
        }
    
    async def cleanup_old_memories(self, days_threshold: int = 30, min_usage_threshold: int = 1):
        """清理旧记忆"""
        try:
            cutoff_time = datetime.now().timestamp() - (days_threshold * 24 * 3600)
            cleaned_count = 0
            
            for memory_id in list(self.memory_index.keys()):
                memory = self.memory_index[memory_id]
                memory_time = datetime.fromisoformat(memory.timestamp).timestamp()
                
                # 删除旧的且很少使用的记忆
                if (memory_time < cutoff_time and 
                    memory.usage_count < min_usage_threshold and
                    memory.success_score < 0.5):
                    
                    # 从索引中删除
                    del self.memory_index[memory_id]
                    self.agent_memories[memory.agent_type].remove(memory_id)
                    
                    # 删除文件
                    memory_file = self.memory_dir / f"{memory_id}.json"
                    if memory_file.exists():
                        memory_file.unlink()
                    
                    cleaned_count += 1
            
            self.stats["last_cleanup"] = datetime.now().isoformat()
            self.stats["total_memories"] -= cleaned_count
            
            print(f"🧹 记忆清理完成: 删除了 {cleaned_count} 条旧记忆")
            
        except Exception as e:
            print(f"❌ 记忆清理失败: {e}")
    
    async def _persist_memory(self, memory: MemoryEntry):
        """持久化记忆"""
        try:
            memory_file = self.memory_dir / f"{memory.id}.json"
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(memory), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 持久化记忆失败: {e}")
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        try:
            if not vec1 or not vec2:
                return 0.0
            
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
            
        except Exception:
            return 0.0


# 全局长期记忆实例
_memory_instance = None

def get_long_term_memory() -> LangGraphLongTermMemory:
    """获取长期记忆单例"""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = LangGraphLongTermMemory()
    return _memory_instance
