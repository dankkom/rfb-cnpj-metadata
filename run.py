import json
from pathlib import Path

from rfb_cnpj_metadata import fetcher, constants


def save_json(data: list[dict], dest_filepath: Path):
    dest_filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, default=str, ensure_ascii=False)


def main():
    bot = fetcher.Bot()
    dest_dir = Path("metadata")
    for dataset in constants.datasets:
        metadata = bot.fetch_dataset(dataset)
        save_json(metadata, dest_dir / "datasets" / f"{dataset}.json")
    for dataset in constants.auxiliary_tables:
        metadata = bot.fetch_auxiliary_tables(dataset)
        save_json(metadata, dest_dir / "auxiliary-tables" / f"{dataset}.json")
    for dataset in constants.tax_regimes:
        metadata = bot.fetch_tax_regime(dataset)
        save_json(metadata, dest_dir / "tax-regimes" / f"{dataset}.json")
    for dataset in constants.docs:
        metadata = bot.fetch_docs(dataset)
        save_json(metadata, dest_dir / "docs" / f"{dataset}.json")
    bot.client.close()


if __name__ == "__main__":
    main()
