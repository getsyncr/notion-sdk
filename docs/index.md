# Notion SDK

A simple and easy to use Python async client for the [Notion API](https://developers.notion.com)
made with ❤️ by [Syncr.so](https://syncr.so)

## Installation

```shell
pip install notion-sdk
```

### Client options

`Client` support the following options on initialization.
These options are all keys in the single constructor parameter.

<!-- markdownlint-disable -->
| Option | Default value | Type | Description |
|--------|---------------|---------|-------------|
| `auth` | `None` | `string` | Bearer token for authentication. If left undefined, the `auth` parameter should be set on each request. |
| `timeout` | `60` | `int` | Number of seconds to wait before emitting a `RequestTimeoutError` |
| `base_url` | `"https://api.notion.com"` | `string` | The root URL for sending API requests. This can be changed to test with a mock server. |
| `logger` | Log to console | `logging.Logger` | A custom logger. |
<!-- markdownlint-enable -->

## Requirements

This package supports the following minimum versions:

* Python >= 3.7
* httpx >= 0.15.0

Earlier versions may still work, but we encourage people building new applications
to upgrade to the current stable.

## License

Distributed under the Apache License. See [LICENSE](https://github.com/getsyncr/notion-sdk/blob/main/LICENSE) for more information.
