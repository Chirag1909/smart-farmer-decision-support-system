"""Compatibility Flask entrypoint preserved during non-destructive migration."""

from application.app import app  # Reuse existing Flask implementation without moving originals.

