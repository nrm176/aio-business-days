from aiohttp import web
from business_days_util import BusinessDaysUtil
from lib.logtaker import logger
import os
# https://docs.aiohttp.org/en/latest/web_quickstart.html


util = BusinessDaysUtil.init()

routes = web.RouteTableDef()

@routes.get('/biz')
async def biz_days(request):
    peername = request.transport.get_extra_info('peername')
    if peername is not None:
        host, port = peername
        logger.info('request from {}:{}'.format(host, port))
    _from = request.rel_url.query.get('from')
    _n = request.rel_url.query.get('n')
    d = util.add_n_biz_days(from_date=_from, n=int(_n))
    return web.json_response({'date': d, 'from': _from, 'n': _n})

app = web.Application()
app.add_routes(routes)
web.run_app(app, port=os.getenv('PORT'))