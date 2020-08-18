import websockets
import asyncio
import aio_pika
import random
import toml


class RMQ_Connection:

    def __init__(self, config, buffer):
        self.config = config

        self._connection = None
        self._channel = None
        self._queue = None
        self._exchange = None
        #self.buffer = buffer


    async def _create_connection(self):
        #logger.info("Creating connection")
        return await aio_pika.connect_robust(
                "amqp://{}:{}@{}/{}".format(
                    self.config['rabbitmq']['username'],
                    self.config['rabbitmq']['password'],
                    self.config['rabbitmq']['host'],
                    self.config['rabbitmq']['username']))
    

    async def connect(self):
        #logger.info("Connecting to RMQ")
        self._connection = await self._create_connection()
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
        self.config['rabbitmq']['sensor_exchange'], aio_pika.ExchangeType.FANOUT, durable=True
        )

        self._queue = await self._channel.declare_queue(exclusive=True)
        await self._queue.bind(self._exchange)
        print("connected to RMQ")


    async def disconnect(self):
        #logger.info("Closing connection to RMQ")
        await self._connection.close()
        self._connection = None
        self._channel = None
        self._exchange = None
        self._running = False

    async def consume(self):
        async with self._queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    if(message.body == b'"hello"'):
                        print( "[x] Received %r" % message.body)
                    #await self.buffer.put(message.body.decode())
                    #if queue.name in message.body.decode():
                     #   break

    def get_queue_iter(self):
        return self._queue.iterator()

'''
class WS_Server:
    def __init__(self, config, buffer):
        self.config = config['websocket']
        self.connected = set()
        self.server = websockets.serve(self.handler, config['websocket']['ip'], config['websocket']['port'])
        self.buffer = buffer

    async def handler(self, websocket, path):
        # Register.
        self.connected.add(websocket)
        print("client connected")
        try:
            while True:
                msg = await websocket.recv()
                print("message received: "+msg)
                #await asyncio.wait([ws.send("Hello!") for ws in connected])
                #await asyncio.sleep(10)
        except websockets.ConnectionClosedOK:
            print("disconnected")
        except websockets.ConnectionClosedError:
            print("ConnectionClosedError")
        finally:
            print("removed ws from connected")
            self.connected.remove(websocket)

    async def broadcast(self):
        while True:
            msg = await self.buffer.get()
            if len(self.connected) > 0:
                await asyncio.wait([ws.send(msg) for ws in self.connected])          

    def start(self):
        asyncio.ensure_future(self.server)
'''

async def main():
    config = toml.load("config.toml")
    buffer = asyncio.Queue(maxsize=10)

    rmq = RMQ_Connection(config, buffer)
    await rmq.connect()
    
    #wss = WS_Server(config, buffer)
    #wss.start()
    loop = asyncio.get_event_loop()
    task1 = loop.create_task(rmq.consume())
    await task1
    #asyncio.create_task(rmq.consume())
    #asyncio.create_task(wss.broadcast())

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
