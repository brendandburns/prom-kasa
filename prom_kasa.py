import kasa
from prometheus_client import start_http_server, Gauge
import asyncio
import time

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
    time.sleep(60)

if __name__ == '__main__':
    strip = kasa.SmartStrip('192.168.2.14')
    start_http_server(8000)
    while True:
        asyncio.run(do_update(strip))