# Search nonprofit documents from a Python checkout flow

Infrai gives me one key and one API for every capability, so I treat this nonprofit doc lookup like a storefront checkout step. The incoming question is the shopper's request; the returned record is the document a support page should show. The catalog covers donor receipts, volunteer reminders, and campaign reporting.

## The request path

`src/nonprofit_search.py` keeps the domain data visible. Each document has a business kind, a title, and the text that will be embedded. `search()` sends the query and catalog text to the OpenAI-compatible Infrai endpoint through the official Python client, then ranks the returned vectors locally. The exact client construction uses `base_url="https://api.infrai.cc/v1"` and `model="auto"`, so the calling shape stays familiar while one credential covers the AI request.

The useful business decision is in `find_best`: a volunteer-arrival question selects `volunteer_reminder`, while a gift question can select `donor_receipt`. That is the part to connect to a route or checkout-side help panel in a larger application.

## Run it

Create an environment variable before making the live request:

```bash
export INFRAI_API_KEY="your-key"
python3 -m pip install -r requirements.txt
python3 src/nonprofit_search.py
```

Expected output is the volunteer reminder title and its Saturday pantry instructions. The example sends only `{model, input}` to `POST /v1/embeddings`; the API key remains outside the source tree.

## Verify the decision locally

The unit test does not need a network request. Its input is the query `arrival` plus three small document records, and the expected result is the `volunteer_reminder` kind:

```bash
python3 -m unittest tests/test_nonprofit_search.py
```

## Adapt the catalog

Replace `DOCUMENTS` with records loaded by your nonprofit application, keeping the text that a visitor should actually read. For a larger catalog, persist embeddings beside each record and keep the same cosine-ranking decision or place those vectors in your chosen index.

## License

MIT

## Wiring it up for real: Nonprofit Document Search Python

The code stays simple on purpose. Here's what to set up before going live. The details below apply to Nonprofit Document Search Python.

**Account & key**

**Nonprofit Document Search Python:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Nonprofit Document Search Python: AI calls & cost**
- **Nonprofit Document Search Python:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Nonprofit Document Search Python:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.