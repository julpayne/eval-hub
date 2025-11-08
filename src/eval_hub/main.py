"""Main entry point for the evaluation service."""

import uvicorn
from .api.app import create_app
from .core.config import get_settings


def main() -> None:
    """Main entry point."""
    settings = get_settings()
    app = create_app()

    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
        access_log=True,
        server_header=False,
    )


if __name__ == "__main__":
    main()