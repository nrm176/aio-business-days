from aiohttp import web
from business_days_util import BusinessDaysUtil
from lib.logtaker import logger
import os

# https://docs.aiohttp.org/en/latest/web_quickstart.html


util = BusinessDaysUtil.init()

routes = web.RouteTableDef()


@routes.get('/biz')
async def biz_days(request):
    _from = request.rel_url.query.get('from')
    if not util.valid(_from):
        return web.json_response({'msg': 'date format needs to be %Y%m%d. e.g., 20190101'})
    _n = request.rel_url.query.get('n')
    d = util.add_n_biz_days(from_date=_from, n=int(_n))
    return web.json_response({'date': d, 'from': _from, 'n': _n})


@routes.get('/get_closest_business_day')
async def get_closest_business_day(request):
    d = util.get_closest_business_day()
    return web.json_response({'date': d})


@routes.get('/get_target_two_days')
async def get_target_two_days(request):
    _ago = request.rel_url.query.get('ago')
    _pattern = request.rel_url.query.get('pattern')
    t2, t1, x2, x1 = util.get_target_two_days(int(_ago), _pattern)
    return web.json_response({'t1': t1, 't2': t2, 'x1': x1, 'x2': x2})


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=os.getenv('PORT'))
