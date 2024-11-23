import json
from pathlib import Path

from rfb_cnpj_metadata.constants import auxiliary_tables, datasets, docs, tax_regimes
from rfb_cnpj_metadata.fetcher import Fetcher


def save_json(data: list[dict], dest_filepath: Path):
    dest_filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, default=str, ensure_ascii=False)


def main():
    fetcher = Fetcher()
    dest_dir = Path("metadata")
    for dataset in datasets:
        metadata = fetcher.fetch_dataset(dataset)
        save_json(metadata, dest_dir / "datasets" / f"{dataset}.json")
    for dataset in auxiliary_tables:
        metadata = fetcher.fetch_auxiliary_tables(dataset)
        save_json(metadata, dest_dir / "auxiliary-tables" / f"{dataset}.json")
    for dataset in tax_regimes:
        metadata = fetcher.fetch_tax_regime(dataset)
        save_json(metadata, dest_dir / "tax-regimes" / f"{dataset}.json")
    for dataset in docs:
        metadata = fetcher.fetch_docs(dataset)
        save_json(metadata, dest_dir / "docs" / f"{dataset}.json")
    fetcher.client.close()


if __name__ == "__main__":
    main()
