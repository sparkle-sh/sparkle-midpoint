import sanic


def setup_agent_endpoints():
    bp = sanic.Blueprint('agent', url_prefix='/agent')

    @bp.post("/")
    async def agent_post(req):
        return sanic.response.json({"hello": "post"})

    @bp.delete("/")
    async def agent_delete(req):
        return sanic.response.json({"hello": "delete"})

    return bp
