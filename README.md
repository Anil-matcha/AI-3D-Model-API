# AI 3D Model API: model comparison and examples

Generate textured 3D assets from text, a single image, or multi-view images through Muapi’s unified AI 3D Model API. This repository compares the live Tripo3D and Meshy endpoints and documents copy-paste HTTP examples for game assets, product visualization, AR/VR, and 3D-printing workflows.

[Open the AI 3D Model API landing page](https://muapi.ai/ai-3d-model-api) · [Get an API key](https://muapi.ai/access-keys) · [API reference](https://muapi.ai/docs/api-reference)

## Related Projects

- [Open Generative AI](https://github.com/Anil-matcha/Open-Generative-AI) — curated open generative-AI tools and resources.
- [Muapi ComfyUI](https://github.com/SamurAIGPT/muapi-comfyui) — visual workflow integration for Muapi models.
- [Generative Media Skills](https://github.com/SamurAIGPT/muapi-skills) — reusable generative-media workflows.
- [Awesome Generative AI Apps](https://github.com/Anil-matcha/awesome-generative-ai-apps) — application and workflow discovery.

## What this repository covers

- Tripo3D H3.1, Tripo3D P1, and Meshy 6 text-to-3D, image-to-3D, and multi-image workflows.
- A comparison of input requirements, topology/material controls, output formats, and typical use cases.
- `curl` and Python examples for submitting an asynchronous job and polling its result.
- Request payload notes for prompts, image URLs, multi-view image lists, and output persistence.

## Model comparison

| Endpoint family | Inputs | Best for | Output notes |
|---|---|---|---|
| Tripo3D H3.1 | Text, image, or 2–4 multi-view images | Strong price-to-quality and game-ready assets | Textured `.glb`; quality/topology options vary by endpoint |
| Tripo3D P1 | Text or image | Premium Tripo3D generation | Textured `.glb` with premium quality tier |
| Meshy 6 | Text, image, or 1–4 images | Configurable topology and export flexibility | `.glb` plus FBX, OBJ, and USDZ alternatives |

Choose text-to-3D for concept exploration, image-to-3D for a single known reference, and multi-view generation when the back and sides of an asymmetric object matter. See the [live page](https://muapi.ai/ai-3d-model-api) for current pricing and model availability.

## Quick start with curl

```bash
export MUAPI_API_KEY="your_key"

curl -X POST "https://api.muapi.ai/api/v1/tripo3d-h31-text-to-3d" \
  -H "x-api-key: $MUAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"a low-poly red panda astronaut, game-ready asset, clean studio lighting"}'
```

For image-to-3D, pass a publicly reachable image URL:

```bash
curl -X POST "https://api.muapi.ai/api/v1/meshy-6-image-to-3d" \
  -H "x-api-key: $MUAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://example.com/product-front.jpg"}'
```

The submission response contains a request identifier. Poll until completion:

```bash
export REQUEST_ID="id_from_the_submission_response"
curl "https://api.muapi.ai/api/v1/predictions/$REQUEST_ID/result" \
  -H "x-api-key: $MUAPI_API_KEY"
```

See [`examples/quickstart.py`](examples/quickstart.py) for a complete polling loop.

## API workflow

1. Create an API key and keep it server-side.
2. Select the endpoint that matches the input type and output requirements.
3. Submit `POST /api/v1/{model-slug}` with JSON input.
4. Poll `GET /api/v1/predictions/{request_id}/result` until the job succeeds or fails.
5. Copy the output URL into durable storage before a temporary result expires.

For multi-view reconstruction, use the endpoint’s documented `images_list` input and keep the images consistently framed and lit. Do not commit reference images, generated assets, or API keys to this repository.

## Common failure modes

| Symptom | Check |
|---|---|
| Validation error | Endpoint slug, required image field, reachable URL, and JSON array shape. |
| Inconsistent geometry | Use 2–4 distinct views with a shared subject, scale, and background where possible. |
| Missing export format | Meshy provides the broadest documented export set; inspect the result payload before assuming every format is present. |
| Unknown job state | Poll the result endpoint instead of submitting duplicates; persist the request ID. |

## License

Documentation and examples are MIT licensed. Generated meshes, textures, and model-provider usage remain subject to the applicable Muapi and provider terms.
