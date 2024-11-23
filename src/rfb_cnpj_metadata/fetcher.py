import datetime
import re
from urllib.parse import unquote

import httpx

from .constants import INITIAL_DATE, auxiliary_tables, datasets, docs, tax_regimes

START_DATE = datetime.datetime.strptime(INITIAL_DATE, "%Y-%m")
TODAY = datetime.datetime.now()


class Fetcher:

    def __init__(self) -> None:
        self.client = httpx.Client(timeout=600, verify=False)

    def fetch_dataset(self, dataset: str) -> list[dict]:
        data = []
        fn_pattern = datasets[dataset].get("fn_pattern")
        date_ref = START_DATE
        while date_ref < TODAY:
            for i in range(10):
                url = datasets[dataset]["url_format"].format(date_ref=date_ref, i=i)
                file_meta = self.get_file_metadata(url) | {
                    "dataset": dataset,
                    "date_ref": date_ref.strftime("%Y-%m"),
                }
                if file_meta["file_size"] < 1000:
                    # raise ValueError(f"File {file_meta['name']} is empty.")
                    break
                if fn_pattern:
                    partition, = re.search(fn_pattern, file_meta["name"]).groups()
                    file_meta |= {"partition": partition}

                print(file_meta)

                data.append(file_meta)

            if date_ref.month == 12:
                date_ref = date_ref.replace(year=date_ref.year + 1, month=1)
            else:
                date_ref = date_ref.replace(month=date_ref.month + 1)

        return data

    def fetch_auxiliary_tables(self, auxiliary_table: str):
        data = []
        date_ref = START_DATE
        while date_ref < TODAY:
            url = auxiliary_tables[auxiliary_table]["url_format"].format(date_ref=date_ref)
            file_meta = self.get_file_metadata(url) | {
                "dataset": auxiliary_table,
                "group": "tabelas-auxiliares",
                "date_ref": date_ref.strftime("%Y-%m"),
            }

            print(file_meta)

            data.append(file_meta)

            if date_ref.month == 12:
                date_ref = date_ref.replace(year=date_ref.year + 1, month=1)
            else:
                date_ref = date_ref.replace(month=date_ref.month + 1)

        return data

    def fetch_tax_regime(self, tax_regime: str):
        data = []
        for url in tax_regimes[tax_regime]["urls"]:
            file_meta = self.get_file_metadata(url) | {
                "dataset": tax_regime,
                "group": "regimes-tributarios",
            }

            print(file_meta)

            data.append(file_meta)

        return data

    def fetch_docs(self, doc: str):
        data = []
        for url in docs[doc]["urls"]:
            file_meta = self.get_file_metadata(url) | {
                "dataset": doc,
                "group": "documentacao",
            }

            print(file_meta)

            data.append(file_meta)

        return data

    def get_file_metadata(self, url: str) -> dict:
        filename = unquote(url.rsplit("/", 1)[1])
        name, extension = filename.rsplit(".", 1)
        r = self.client.head(url)
        file_size = int(r.headers.get("content-length", 0))
        if last_modified := r.headers.get("last-modified"):
            last_modified = datetime.datetime.strptime(
                r.headers.get("last-modified"),
                "%a, %d %b %Y %H:%M:%S %Z",
            )
        return {
            "name": name,
            "extension": extension,
            "url": url,
            "file_size": file_size,
            "last_modified": last_modified.isoformat() if last_modified else None,
        }
