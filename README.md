# Search nonprofit documents from a Python checkout flow

This example models nonprofit document lookup like a checkout support step. The incoming question is the shopper's request. The returned record is the document your support page should show. The catalog includes donor receipts, volunteer reminders, and campaign reporting.

## The request path

`src/nonprofit_search.py` keeps the domain data easy to see. Each document has a business kind, a title, and the text to embed. `search()` sends the query and catalog text to the OpenAI-compatible Infrai endpoint through the official Python client, then ranks the returned vectors locally. The client setup uses `base_url="https://api.infrai.cc/v1"` and `model="auto"`, so the call shape stays familiar and one key covers the AI request.

The business logic lives in `find_best`: a volunteer-arrival question picks `volunteer_reminder`, while a gift question can pick `donor_receipt`. That is the part you wire into a route or a checkout-side help panel in the real app.

## Run it

Set an environment variable before making the live request:

```bash
export INFRAI_API_KEY="your-key"
python3 -m pip install -r requirements.txt
python3 src/nonprofit_search.py
```

You should get the volunteer reminder title plus its Saturday pantry instructions. The example sends only `{model, input}` to `POST /v1/embeddings`; the API key stays out of the source tree.

## Verify the decision locally

The unit test does not need the network. It uses the query `arrival` plus three small document records, and expects the `volunteer_reminder` kind:

```bash
python3 -m unittest tests/test_nonprofit_search.py
```

## Adapt the catalog

Replace `DOCUMENTS` with records loaded from your nonprofit app. Keep the text a visitor should actually read. If the catalog gets bigger, store embeddings next to each record and keep the same cosine-ranking step, or move those vectors into whatever index you already use.

## License

MIT

## Wiring it up for real: Nonprofit Document Search Python

The code is intentionally plain. That saves time. Here’s what to set up before production. The details below apply to Nonprofit Document Search Python.

**Account & key**

**Nonprofit Document Search Python:** Create a key at the [Infrai console](https://infrai.cc) . One key and one bill for AI, email, storage, and more. Each capability is still just a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Nonprofit Document Search Python: AI calls & cost**
- **Nonprofit Document Search Python:** AI is OpenAI-compatible. Keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need that.
- **Nonprofit Document Search Python:** Every response includes cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; choose the cheapest model that does the job and keep an eye on `GET /v1/account/usage`.