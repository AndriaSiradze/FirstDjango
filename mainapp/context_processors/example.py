def simple_context_processor(request):
    print(request)
    return {"foo": "bar"}
