import redis
import json
import uuid
from datetime import datetime
from loguru import logger
import os
from typing import Dict, Any, Optional

class SharedMemory:
    """Shared memory module for storing context across agents.
    
    This module provides a centralized storage for maintaining context
    across different agents in the system. It stores information such as
    source, type, timestamp, extracted values, and conversation IDs.
    """
    
    def __init__(self):
        """Initialize the shared memory module.
        
        Attempts to connect to Redis if REDIS_URL is provided in environment variables,
        otherwise falls back to in-memory storage.
        """
        self.use_redis = os.getenv("REDIS_URL") is not None
        
        if self.use_redis:
            try:
                self.redis_client = redis.from_url(os.getenv("REDIS_URL"))
                logger.info("Connected to Redis for shared memory")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {str(e)}. Falling back to in-memory storage.")
                self.use_redis = False
        
        if not self.use_redis:
            logger.info("Using in-memory storage for shared memory")
            self.memory_store = {}
            
        self.last_entry_id = None
    
    def store(self, data: Dict[str, Any]) -> str:
        """Store data in shared memory.
        
        Args:
            data: Dictionary containing data to store
            
        Returns:
            str: ID of the stored entry
        """
        # Generate a unique ID for this entry
        entry_id = str(uuid.uuid4())
        
        # Add metadata
        entry = {
            "id": entry_id,
            "timestamp": datetime.now().isoformat(),
            **data
        }
        
        # Store in Redis or in-memory
        if self.use_redis:
            self.redis_client.set(f"memory:{entry_id}", json.dumps(entry))
        else:
            self.memory_store[entry_id] = entry
        
        # Update last entry ID
        self.last_entry_id = entry_id
        
        logger.debug(f"Stored entry in memory with ID: {entry_id}")
        return entry_id
    
    def get_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve an entry from shared memory.
        
        Args:
            entry_id: ID of the entry to retrieve
            
        Returns:
            Dict or None: The retrieved entry or None if not found
        """
        if self.use_redis:
            entry_data = self.redis_client.get(f"memory:{entry_id}")
            if entry_data:
                return json.loads(entry_data)
            return None
        else:
            return self.memory_store.get(entry_id)
    
    def update_entry(self, entry_id: str, data: Dict[str, Any]) -> bool:
        """Update an existing entry in shared memory.
        
        Args:
            entry_id: ID of the entry to update
            data: New data to update the entry with
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        # Get the existing entry
        existing_entry = self.get_entry(entry_id)
        if not existing_entry:
            logger.error(f"Entry with ID {entry_id} not found for update")
            return False
        
        # Update the entry
        updated_entry = {**existing_entry, **data, "updated_at": datetime.now().isoformat()}
        
        # Store the updated entry
        if self.use_redis:
            self.redis_client.set(f"memory:{entry_id}", json.dumps(updated_entry))
        else:
            self.memory_store[entry_id] = updated_entry
        
        logger.debug(f"Updated entry in memory with ID: {entry_id}")
        return True
    
    def get_last_entry_id(self) -> Optional[str]:
        """Get the ID of the last stored entry.
        
        Returns:
            str or None: ID of the last stored entry or None if no entries exist
        """
        return self.last_entry_id
    
    def get_entries_by_thread(self, thread_id: str) -> list:
        """Get all entries for a specific conversation thread.
        
        Args:
            thread_id: ID of the conversation thread
            
        Returns:
            list: List of entries for the specified thread
        """
        if self.use_redis:
            # This is a simplified implementation and might not be efficient for large datasets
            # In a production environment, you might want to use Redis search capabilities
            all_keys = self.redis_client.keys("memory:*")
            entries = []
            
            for key in all_keys:
                entry_data = self.redis_client.get(key)
                if entry_data:
                    entry = json.loads(entry_data)
                    if entry.get("thread_id") == thread_id:
                        entries.append(entry)
            
            return entries
        else:
            return [entry for entry in self.memory_store.values() if entry.get("thread_id") == thread_id]