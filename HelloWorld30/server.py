#!/usr/bin/env python3
"""
HelloWorld30 REST API Server
FastAPI-based greeting service supporting 30 languages
"""

import json
import uvicorn
from pathlib import Path
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class GreetingRequest(BaseModel):
    """Request model for greeting generation."""
    language: str
    name: Optional[str] = None


class GreetingResponse(BaseModel):
    """Response model for greeting."""
    greeting: str
    language: str
    language_code: str
    name: Optional[str] = None


class LanguageInfo(BaseModel):
    """Model for language information."""
    code: str
    name: str
    hello: str


class HelloWorld30Server:
    """HelloWorld30 REST API server."""

    def __init__(self):
        """Initialize server with language data."""
        self.languages_file = Path(__file__).parent / "languages.json"
        self.languages = self._load_languages()
        self.app = self._create_app()

    def _load_languages(self) -> Dict[str, Any]:
        """Load language data from JSON file."""
        try:
            with open(self.languages_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('languages', {})
        except FileNotFoundError:
            raise RuntimeError(f"Language file not found: {self.languages_file}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON in language file: {e}")

    def _create_app(self) -> FastAPI:
        """Create and configure FastAPI application."""
        app = FastAPI(
            title="HelloWorld30 API",
            description="Greeting service supporting 30 languages",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )

        # Health check endpoint
        @app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "service": "HelloWorld30", "languages": len(self.languages)}

        # Root endpoint
        @app.get("/")
        async def root():
            """Root endpoint with API information."""
            return {
                "service": "HelloWorld30 API",
                "version": "1.0.0",
                "description": "Greeting service supporting 30 languages",
                "endpoints": {
                    "GET /": "API information",
                    "GET /hello": "Get greeting (query params: lang, name)",
                    "POST /hello": "Get greeting (JSON body)",
                    "GET /languages": "List all supported languages",
                    "GET /health": "Health check"
                },
                "total_languages": len(self.languages)
            }

        # Get greeting via query parameters
        @app.get("/hello", response_model=GreetingResponse)
        async def get_greeting(
            lang: str = Query(..., description="Language name or code"),
            name: Optional[str] = Query(None, description="Name to include in greeting")
        ):
            """Get greeting in specified language via query parameters."""
            try:
                greeting, lang_info = self._generate_greeting(lang, name)
                return GreetingResponse(
                    greeting=greeting,
                    language=lang_info['name'],
                    language_code=lang_info['code'],
                    name=name
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

        # Get greeting via JSON body
        @app.post("/hello", response_model=GreetingResponse)
        async def post_greeting(request: GreetingRequest):
            """Get greeting in specified language via JSON body."""
            try:
                greeting, lang_info = self._generate_greeting(request.language, request.name)
                return GreetingResponse(
                    greeting=greeting,
                    language=lang_info['name'],
                    language_code=lang_info['code'],
                    name=request.name
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

        # List all languages
        @app.get("/languages")
        async def list_languages():
            """Get list of all supported languages."""
            languages_list = []
            for key, data in sorted(self.languages.items()):
                languages_list.append(LanguageInfo(
                    code=data.get('code', '??'),
                    name=data.get('name', key.title()),
                    hello=data.get('hello', '???')
                ))

            return {
                "total": len(languages_list),
                "languages": languages_list
            }

        # Get specific language info
        @app.get("/languages/{language}")
        async def get_language_info(language: str):
            """Get information about a specific language."""
            lang_key = language.lower()

            # Find language by name or code
            for key, data in self.languages.items():
                if (key == lang_key or
                    data.get('code', '').lower() == lang_key or
                    data.get('name', '').lower() == lang_key):
                    return LanguageInfo(
                        code=data.get('code', '??'),
                        name=data.get('name', key.title()),
                        hello=data.get('hello', '???')
                    )

            raise HTTPException(
                status_code=404,
                detail=f"Language '{language}' not found"
            )

        return app

    def _generate_greeting(self, language: str, name: Optional[str] = None) -> tuple[str, Dict[str, str]]:
        """Generate greeting in specified language.

        Args:
            language: Language name or code
            name: Optional name to include

        Returns:
            Tuple of (greeting_string, language_info)
        """
        # Normalize language input
        lang_key = language.lower()

        # Find language by name or code
        lang_data = None
        for key, data in self.languages.items():
            if (key == lang_key or
                data.get('code', '').lower() == lang_key or
                data.get('name', '').lower() == lang_key):
                lang_data = data
                break

        if not lang_data:
            available = list(self.languages.keys())
            raise ValueError(f"Language '{language}' not supported. Available: {available}")

        hello_text = lang_data['hello']

        if name:
            greeting = f"{hello_text}, {name}!"
        else:
            greeting = f"{hello_text}, World!"

        return greeting, {
            'name': lang_data.get('name', language.title()),
            'code': lang_data.get('code', '??'),
            'hello': hello_text
        }


# Global server instance
server = HelloWorld30Server()
app = server.app


def main():
    """Run the server."""
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
