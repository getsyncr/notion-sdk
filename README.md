<p align="center">
    <p align="center">
        <a href="https://syncr.so?utm_source=github&utm_medium=logo" target="_blank">
        <img src="https://user-images.githubusercontent.com/37115765/122721304-ca788c00-d270-11eb-8059-67f8ca53450c.png" alt="Syncr" height="100">
        </a>
    </p>
    <div align="center">
        <h1>Notion SDK for Async Python</h1>
        <p>
            <b>A simple and easy to use Python async client for the 
            <a href="https://developers.notion.com">Notion API</a> 
            made with ❤️ by <a href="https://syncr.so">Syncr.so</a></b>
        </p>
        <br>
    </div>
</p>

## Installation

```
pip install notionsdk
```

## Usage

Import and initialize a client using an **integration token** or an OAuth **access token**.

```python
import Client from notion

notion = Client(auth="YOUR_ACCESS_TOKEN")
```

## License

Distributed under the Apache License. See [LICENSE](LICENSE) for more information.
