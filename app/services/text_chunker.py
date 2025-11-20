"""
Text Chunker - Smart text chunking for recipes and documents
Handles recipe-specific chunking and general document chunking
"""

from typing import List, Dict, Any
import re
import logging

logger = logging.getLogger(__name__)

class TextChunk:
    """Represents a chunk of text with metadata"""
    
    def __init__(
        self,
        text: str,
        chunk_type: str,
        metadata: Dict[str, Any],
        chunk_index: int = 0
    ):
        self.text = text
        self.chunk_type = chunk_type
        self.metadata = metadata
        self.chunk_index = chunk_index
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "text": self.text,
            "chunk_type": self.chunk_type,
            "metadata": self.metadata,
            "chunk_index": self.chunk_index
        }


class TextChunker:
    """Text chunking service for recipes and documents"""
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        min_chunk_size: int = 100
    ):
        """
        Initialize text chunker
        
        Args:
            chunk_size: Target chunk size in characters
            chunk_overlap: Overlap between chunks
            min_chunk_size: Minimum chunk size
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
    
    def chunk_recipe(self, recipe_data: Dict[str, Any]) -> List[TextChunk]:
        """
        Chunk a recipe into semantic sections
        
        Args:
            recipe_data: Recipe dictionary with title, ingredients, steps, etc.
            
        Returns:
            List of TextChunk objects
        """
        chunks = []
        chunk_index = 0
        
        title = recipe_data.get("title", "")
        recipe_id = recipe_data.get("id", "unknown")
        
        # Base metadata
        base_metadata = {
            "recipe_id": recipe_id,
            "recipe_title": title,
            "content_type": "recipe"
        }
        
        # 1. Overview chunk (title + description)
        overview_parts = [title]
        if "description" in recipe_data:
            overview_parts.append(recipe_data["description"])
        if "difficulty" in recipe_data:
            overview_parts.append(f"Độ khó: {recipe_data['difficulty']}")
        if "prep_time" in recipe_data:
            overview_parts.append(f"Thời gian chuẩn bị: {recipe_data['prep_time']} phút")
        if "cook_time" in recipe_data:
            overview_parts.append(f"Thời gian nấu: {recipe_data['cook_time']} phút")
        
        overview_text = "\n".join(overview_parts)
        chunks.append(TextChunk(
            text=overview_text,
            chunk_type="recipe_overview",
            metadata={**base_metadata, "section": "overview"},
            chunk_index=chunk_index
        ))
        chunk_index += 1
        
        # 2. Ingredients chunk
        if "ingredients" in recipe_data and recipe_data["ingredients"]:
            ingredients = recipe_data["ingredients"]
            if isinstance(ingredients, list):
                ingredients_text = f"{title} - Nguyên liệu:\n"
                for ing in ingredients:
                    if isinstance(ing, dict):
                        name = ing.get("name", "")
                        quantity = ing.get("quantity", "")
                        unit = ing.get("unit", "")
                        ingredients_text += f"- {name}: {quantity} {unit}\n"
                    else:
                        ingredients_text += f"- {ing}\n"
            else:
                ingredients_text = f"{title} - Nguyên liệu:\n{ingredients}"
            
            chunks.append(TextChunk(
                text=ingredients_text,
                chunk_type="recipe_ingredients",
                metadata={**base_metadata, "section": "ingredients"},
                chunk_index=chunk_index
            ))
            chunk_index += 1
        
        # 3. Steps chunks (group steps if they're short)
        if "steps" in recipe_data and recipe_data["steps"]:
            steps = recipe_data["steps"]
            if isinstance(steps, list):
                current_group = []
                current_length = 0
                
                for i, step in enumerate(steps):
                    step_text = step if isinstance(step, str) else step.get("description", "")
                    step_line = f"Bước {i+1}: {step_text}"
                    step_length = len(step_line)
                    
                    if current_length + step_length > self.chunk_size and current_group:
                        # Save current group
                        group_text = f"{title} - Các bước:\n" + "\n".join(current_group)
                        chunks.append(TextChunk(
                            text=group_text,
                            chunk_type="recipe_steps",
                            metadata={**base_metadata, "section": "steps"},
                            chunk_index=chunk_index
                        ))
                        chunk_index += 1
                        current_group = []
                        current_length = 0
                    
                    current_group.append(step_line)
                    current_length += step_length
                
                # Save remaining steps
                if current_group:
                    group_text = f"{title} - Các bước:\n" + "\n".join(current_group)
                    chunks.append(TextChunk(
                        text=group_text,
                        chunk_type="recipe_steps",
                        metadata={**base_metadata, "section": "steps"},
                        chunk_index=chunk_index
                    ))
                    chunk_index += 1
            else:
                steps_text = f"{title} - Cách làm:\n{steps}"
                chunks.append(TextChunk(
                    text=steps_text,
                    chunk_type="recipe_steps",
                    metadata={**base_metadata, "section": "steps"},
                    chunk_index=chunk_index
                ))
                chunk_index += 1
        
        # 4. Tips chunk
        if "tips" in recipe_data and recipe_data["tips"]:
            tips_text = f"{title} - Mẹo và lưu ý:\n{recipe_data['tips']}"
            chunks.append(TextChunk(
                text=tips_text,
                chunk_type="recipe_tips",
                metadata={**base_metadata, "section": "tips"},
                chunk_index=chunk_index
            ))
            chunk_index += 1
        
        logger.debug(f"Chunked recipe '{title}' into {len(chunks)} chunks")
        return chunks
    
    def chunk_document(
        self,
        doc_text: str,
        doc_type: str,
        doc_metadata: Dict[str, Any]
    ) -> List[TextChunk]:
        """
        Chunk a general document
        
        Args:
            doc_text: Document text
            doc_type: Document type (technique, tip, etc.)
            doc_metadata: Document metadata
            
        Returns:
            List of TextChunk objects
        """
        chunks = []
        
        # Try to split by paragraphs first
        paragraphs = [p.strip() for p in doc_text.split("\n\n") if p.strip()]
        
        if not paragraphs:
            # No paragraph breaks, split by sentences
            paragraphs = [s.strip() for s in re.split(r'[.!?]+', doc_text) if s.strip()]
        
        current_chunk = []
        current_length = 0
        chunk_index = 0
        
        for para in paragraphs:
            para_length = len(para)
            
            # If single paragraph exceeds chunk size, split it
            if para_length > self.chunk_size:
                # Save current chunk if exists
                if current_chunk:
                    chunk_text = "\n\n".join(current_chunk)
                    chunks.append(TextChunk(
                        text=chunk_text,
                        chunk_type=doc_type,
                        metadata=doc_metadata,
                        chunk_index=chunk_index
                    ))
                    chunk_index += 1
                    current_chunk = []
                    current_length = 0
                
                # Split long paragraph
                words = para.split()
                temp_chunk = []
                temp_length = 0
                
                for word in words:
                    word_length = len(word) + 1  # +1 for space
                    if temp_length + word_length > self.chunk_size and temp_chunk:
                        chunk_text = " ".join(temp_chunk)
                        chunks.append(TextChunk(
                            text=chunk_text,
                            chunk_type=doc_type,
                            metadata=doc_metadata,
                            chunk_index=chunk_index
                        ))
                        chunk_index += 1
                        temp_chunk = []
                        temp_length = 0
                    
                    temp_chunk.append(word)
                    temp_length += word_length
                
                if temp_chunk:
                    current_chunk = temp_chunk
                    current_length = temp_length
            
            # Add paragraph to current chunk
            elif current_length + para_length > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = "\n\n".join(current_chunk)
                chunks.append(TextChunk(
                    text=chunk_text,
                    chunk_type=doc_type,
                    metadata=doc_metadata,
                    chunk_index=chunk_index
                ))
                chunk_index += 1
                
                # Start new chunk with overlap
                if current_chunk:
                    overlap_text = current_chunk[-1][-self.chunk_overlap:]
                    current_chunk = [overlap_text + para]
                    current_length = len(current_chunk[0])
                else:
                    current_chunk = [para]
                    current_length = para_length
            else:
                current_chunk.append(para)
                current_length += para_length
        
        # Save final chunk
        if current_chunk:
            chunk_text = "\n\n".join(current_chunk)
            if len(chunk_text) >= self.min_chunk_size:
                chunks.append(TextChunk(
                    text=chunk_text,
                    chunk_type=doc_type,
                    metadata=doc_metadata,
                    chunk_index=chunk_index
                ))
        
        logger.debug(f"Chunked document into {len(chunks)} chunks")
        return chunks
    
    def chunk_text_simple(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[TextChunk]:
        """
        Simple text chunking with fixed size
        
        Args:
            text: Text to chunk
            metadata: Optional metadata
            
        Returns:
            List of TextChunk objects
        """
        if not text:
            return []
        
        chunks = []
        metadata = metadata or {}
        
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk_text = text[i:i + self.chunk_size]
            if len(chunk_text) >= self.min_chunk_size:
                chunks.append(TextChunk(
                    text=chunk_text,
                    chunk_type="text",
                    metadata=metadata,
                    chunk_index=len(chunks)
                ))
        
        return chunks


# Singleton instance
text_chunker = TextChunker()
