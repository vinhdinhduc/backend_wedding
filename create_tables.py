#!/usr/bin/env python3

import asyncio

from src.infrastructure.database.bootstrap import bootstrap_database


if __name__ == "__main__":
    asyncio.run(bootstrap_database())
    print("✓ Database initialized and sample data seeded.")
