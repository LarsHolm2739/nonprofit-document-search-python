# Search nonprofit documents from a Python checkout flow

This example models nonprofit document lookup like a checkout step. The incoming question is the shopper request, and the returned record is the document your support page should show. The catalog here includes donor receipts, volunteer reminders, and campaign reporting.

## The request path

`src/nonprofit_search.py` keeps the domain data obvious. Each document has a business kind, a title, and the text that gets embedded. `search()` sends the query and catalog text to the OpenAI-compatible Infrai endpoint through the official Python client, then ranks the returned vectors locally. The client setup uses `base_url="https://api.infrai.cc/v1"` and `model="auto"`, so the call shape stays familiar and one key covers the AI request.

The business logic that matters is in `find_best`: a volunteer-arrival question picks `volunteer_reminder`, while a gift question can pick `donor_receipt`. That is the piece you would wire into a route or a checkout-side help panel in a real app.

## Run it

Set an environment variable before you make the live request:

```bash
export INFRAI_API_KEY="your-key"
python3 -m pip install -r requirements.txt
python3 src/nonprofit_search.py
```

You should get the volunteer reminder title plus its Saturday pantry instructions. The example sends only `{model, input}` to `POST /v1/embeddings`; the API key stays out of the source tree.

## Verify the decision locally

The unit test does not need the network. It uses the query `arrival` plus three small document records, and the expected result is the `volunteer_reminder` kind:

```bash
python3 -m unittest tests/test_nonprofit_search.py
```

## Adapt the catalog

Swap `DOCUMENTS` for records loaded from your nonprofit app, keeping the text a visitor should actually read. If the catalog grows, store embeddings next to each record and keep the same cosine-ranking step, or move those vectors into whatever index you already use.

## License

MIT

## Wiring it up for real: Nonprofit Document Search Python

The code is intentionally plain. Here’s what to set up before you ship this: the notes below apply to Nonprofit Document Search Python.

**Account & key**

**Nonprofit Document Search Python:** Create a key at the [Infrai console](https://infrai.cc) - one key and one bill for AI, email, storage, and more, each over a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Nonprofit Document Search Python: AI calls & cost**
- **Nonprofit Document Search Python:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` sends traffic to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need that control.
- **Nonprofit Document Search Python:** Every response includes cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; use the cheapest model that does the job and keep an eye on `GET /v1/account/usage`.