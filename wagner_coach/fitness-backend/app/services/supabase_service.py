"""
Supabase Service Module

Provides centralized Supabase client management with connection pooling,
caching, and support for both service-role and user-scoped access.
"""

import logging
import threading
from typing import Dict, Optional

from supabase import Client, create_client

from app.config import settings

logger = logging.getLogger(__name__)


class SupabaseService:
    """
    Supabase client management with connection pooling.

    Provides:
    - Service role client (bypasses RLS) for admin operations
    - User-scoped clients (respects RLS) for user operations
    - Connection caching and reuse
    - Thread-safe singleton pattern
    """

    _instance: Optional["SupabaseService"] = None
    _service_client: Optional[Client] = None
    _user_clients: Dict[str, Client] = {}
    _lock: threading.Lock = threading.Lock()
    MAX_USER_CLIENTS = 100

    def __new__(cls) -> "SupabaseService":
        """Ensure singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def get_service_client(self) -> Client:
        """
        Get service role client (bypasses RLS).

        Returns cached client if available, otherwise creates new one.
        Service client has admin access and bypasses Row Level Security.

        Returns:
            Client: Supabase client with service role key

        Raises:
            Exception: If client creation fails
        """
        if self._service_client is None:
            with self._lock:
                # Double-check locking pattern
                if self._service_client is None:
                    logger.info("Creating new service role Supabase client")
                    self._service_client = self._create_service_client()
        return self._service_client

    def get_user_client(self, access_token: str) -> Client:
        """
        Get user-scoped client (respects RLS).

        Returns cached client for token if available, otherwise creates new one.
        User client respects Row Level Security policies.

        Args:
            access_token: User's JWT access token

        Returns:
            Client: Supabase client with user's access token

        Raises:
            ValueError: If access_token is invalid
            Exception: If client creation fails
        """
        if not access_token or len(access_token) < 10:
            raise ValueError("Invalid access token")

        # Check cache
        if access_token in self._user_clients:
            return self._user_clients[access_token]

        # Create new client
        with self._lock:
            # Double-check after acquiring lock
            if access_token in self._user_clients:
                return self._user_clients[access_token]

            logger.debug(f"Creating new user-scoped Supabase client")
            client = self._create_user_client(access_token)

            # Cache client
            self._user_clients[access_token] = client

            # Clean up old clients if cache too large
            self._cleanup_user_clients()

            return client

    def clear_cache(self) -> None:
        """
        Clear all cached clients.

        Useful for testing and memory management.
        """
        with self._lock:
            self._service_client = None
            self._user_clients.clear()
            logger.info("Cleared Supabase client cache")

    def health_check(self) -> bool:
        """
        Check if Supabase connection is healthy.

        Performs a simple query to verify database connectivity.

        Returns:
            bool: True if connection is healthy, False otherwise
        """
        try:
            client = self.get_service_client()
            # Simple query to test connection
            result = client.table("profiles").select("id").limit(1).execute()
            logger.info("Supabase health check passed")
            return True
        except Exception as e:
            logger.error(f"Supabase health check failed: {e}")
            return False

    def _create_service_client(self) -> Client:
        """
        Create service role client.

        Returns:
            Client: Supabase client with service role key

        Raises:
            Exception: If client creation fails
        """
        try:
            return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
        except Exception as e:
            logger.error(f"Failed to create service role client: {e}")
            raise

    def _create_user_client(self, access_token: str) -> Client:
        """
        Create user-scoped client.

        Args:
            access_token: User's JWT access token

        Returns:
            Client: Supabase client with user's access token

        Raises:
            Exception: If client creation fails
        """
        try:
            return create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY,
                options={"headers": {"Authorization": f"Bearer {access_token}"}},
            )
        except Exception as e:
            logger.error(f"Failed to create user-scoped client: {e}")
            raise

    def _cleanup_user_clients(self) -> None:
        """
        Clean up old user clients if cache too large.

        Removes oldest 20% of clients when max size exceeded.
        """
        if len(self._user_clients) > self.MAX_USER_CLIENTS:
            # Remove oldest 20% of clients (FIFO)
            num_to_remove = int(self.MAX_USER_CLIENTS * 0.2)
            tokens_to_remove = list(self._user_clients.keys())[:num_to_remove]

            for token in tokens_to_remove:
                del self._user_clients[token]

            logger.info(
                f"Cleaned up {num_to_remove} user clients "
                f"(cache size: {len(self._user_clients)})"
            )


# Singleton instance
_supabase_service: Optional[SupabaseService] = None


def get_supabase_service() -> SupabaseService:
    """
    Get SupabaseService singleton.

    Returns:
        SupabaseService: Singleton service instance
    """
    global _supabase_service
    if _supabase_service is None:
        _supabase_service = SupabaseService()
    return _supabase_service


def get_service_client() -> Client:
    """
    Convenience function to get service role client.

    Returns:
        Client: Supabase client with service role key
    """
    return get_supabase_service().get_service_client()


def get_user_client(access_token: str) -> Client:
    """
    Convenience function to get user-scoped client.

    Args:
        access_token: User's JWT access token

    Returns:
        Client: Supabase client with user's access token
    """
    return get_supabase_service().get_user_client(access_token)