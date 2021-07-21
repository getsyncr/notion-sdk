<p align="center">
    <p align="center">
        <a href="https://syncr.so?utm_source=github&utm_medium=logo" target="_blank">
        <img src="https://user-images.githubusercontent.com/37115765/122721304-ca788c00-d270-11eb-8059-67f8ca53450c.png" alt="Syncr" height="100" width="100">
        </a>
    </p>
    <div align="center">
        <h1>Notion SDK for Python</h1>
        <p>
            <b>A simple and easy to use Python client for the <a href="https://developers.notion.com">Notion API</a> </b>
        </p>
        <br>
    </div>
</p>

`Notion SDK` is a fully typed Python library to use the Notion API. It supports asyncio.
It uses the great [httpx](https://github.com/encode/httpx) as an HTTP client and [pydantic](https://github.com/samuelcolvin/pydantic)
for data validation and typing. This client is meant to be a Python version of the reference [JavaScript SDK](https://github.com/makenotion/notion-sdk-js), so usage should be pretty similar between both.

## Installation

```shell
$ pip install notion-sdk
```

## Usage

Import and initialize a client using an **integration token** or an OAuth **access token**.

```python
from notion import NotionClient

notion = NotionClient(auth="YOUR_ACCESS_TOKEN")

def fetch_databases() -> None:
    response = notion.databases.list()
    for database in response.results:
        print(database.title)

if __name__ == "__main__":
    fetch_databases()
```

More example are available in the [examples](examples) folder.

## Async Usage

This library supports asynchronous calls to Notion API.

Each method returns a `Coroutine` that have to be awaited to retreive the typed response.

The same methods are available for sync or async but you have to use the `NotionAsyncClient` like
in the following example:

```python
import asyncio

from notion import NotionAsyncClient

notion = NotionAsyncClient(auth="YOUR_ACCESS_TOKEN")

async def fetch_databases() -> None:
    response = await notion.databases.list()
    for database in response.results:
        print(database.title)

if __name__ == "__main__":
    asyncio.run(fetch_databases())
```

## Clients options

`NotionClient` and `NotionAsyncClient` support the following options on initialization.
These options are all keys in the single constructor parameter.

<!-- markdownlint-disable -->
| Option | Default value | Type | Description |
|--------|---------------|---------|-------------|
| `auth` | `None` | `string` | Bearer token for authentication. If left undefined, the `auth` parameter should be set on each request. |
| `timeout` | `60` | `int` | Number of seconds to wait before emitting a `RequestTimeoutError` |
| `base_url` | `"https://api.notion.com/v1/"` | `string` | The root URL for sending API requests. This can be changed to test with a mock server. |
| `user_agent` | `notion-sdk/VERSION (https://github.com/getsyncr/notion-sdk)` | `string` | A custom user agent send with every request. |
<!-- markdownlint-enable -->

## Requirements

This package supports the following minimum versions:

* Python >= `3.7`
* `httpx` >= `0.15.0`
* `pydantic` >= `1.7`

Earlier versions may still work, but we encourage people building new applications
to upgrade to the current stable.

## License

Distributed under the Apache License. See [LICENSE](LICENSE) for more information.
