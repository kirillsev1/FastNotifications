import json
import asyncio
import argparse
from pathlib import Path
from typing import List

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from src.integrations.postgres import async_session
from src.models.meta import metadata

parser = argparse.ArgumentParser()

parser.add_argument('fixtures', nargs='+', help='<Required> Set flag')

args = parser.parse_args()


async def main(fixtures: List[str]) -> None:
    for fixture in fixtures:
        fixture_path = Path(fixture)
        print(fixture_path, fixture)
        model = metadata.tables[fixture_path.stem]

        with open(fixture_path, 'r') as file:
            values = json.load(file)
        async with async_session() as session:
            try:
                await session.execute(insert(model).values(values))
            except IntegrityError:
                await session.rollback()
            else:
                await session.commit()


if __name__ == '__main__':
    asyncio.run(main(args.fixtures))
