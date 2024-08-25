import kasa
from prometheus_client import Gauge
from prometheus_async.aio.web import start_http_server
import asyncio

WATTS = Gauge('power_strip_milliwatts', 'Current power reading in milli-watts', ['plug'])
VOLTS = Gauge('power_strip_millivolts', 'Observed voltage in milli-volts')
AMPS = Gauge('power_strip_milliamps', 'Observed current in milli-amps', ['plug'])

def return_true(self):
    return True

async def do_update(strip):
    await strip.update()
    volts = 0
    for child in strip.children:
        child._SmartStripPlug__has_emeter = True
        val = await child.get_emeter_realtime()
        WATTS.labels(child.alias).set(val['power_mw'])
        AMPS.labels(child.alias).set(val['current_ma'])
        volts += val['voltage_mv']
    volts /= len(strip.children)
    VOLTS.set(volts)
    await asyncio.sleep(60)

async def main():
    strip = kasa.SmartStrip('192.168.2.14')
    server = asyncio.create_task(start_http_server(port=8000))
    while True:
        await do_update(strip)
    await server

if __name__ == '__main__':
    asyncio.run(main())
