import asynctest
import asyncio
from src.core.error import EventError
from src.core.event.event_manager import EventManager


class EventManagerTest(asynctest.TestCase):
    def setUp(self):
        self.ev = EventManager()

    def tearDown(self):
        pass

    def test_whenRegisteringService_expectNoThorw(self):
        ident = 'test_service'
        try:
            self.ev.register_service(ident)
        except EventError as e:
            self.fail(str(e))

    def test_whenRegisteringServiceTwice_expectThrow(self):
        ident = 'test_service'
        try:
            self.ev.register_service(ident)
            self.ev.register_service(ident)
        except EventError as e:
            return
        self.fail("Service registered twice!")

    def test_whenRegisteringService_expectReturningProperIdent(self):
        ident = 'test_service'
        a = self.ev.register_service(ident)
        self.assertEqual(a.ident, ident)

    async def test_whenSendintMessage_expectCorrectResultWithoutTimeout(self):
        loop = asyncio.get_event_loop()
        s1 = self.ev.register_service('service1')
        s2 = self.ev.register_service('service2')
        payload = {
            'msg': 'hello'
        }
        result_payload = {
            'msg': 'world'
        }

        async def emit_event():
            try:
                res = await s1.emit_event_to('service2', payload, timeout=5)
            except EventError as e:
                self.fail(str(e))
            self.assertEqual(res.payload['msg'], result_payload['msg'])

        async def send_result():
            async def event_waiter():
                while True:
                    e = s2.get_event()
                    if e is not None:
                        return e
                    asyncio.sleep(0.1)

            try:
                e = await asyncio.wait_for(
                    loop.create_task(event_waiter()), 3.0
                )
            except asyncio.TimeoutError as e:
                self.fail("Service2 did not received event")
            self.assertEqual(e.payload['msg'], payload['msg'])
            id = e.id
            s2.send_result('service1', result_payload, id)

        t1 = loop.create_task(emit_event())
        t2 = loop.create_task(send_result())
        await t2
        await t1

    async def test_whenSendingMessageToUnregisteredService_expectThrow(self):
        loop = asyncio.get_event_loop()
        s1 = self.ev.register_service('service1')
        timeout = 3.0
        try:
            await asyncio.wait_for(
                loop.create_task(s1.emit_event_to('unknown_service', {}, timeout=timeout)), timeout=timeout
            )
        except EventError as e:
            return
        except asyncio.TimeoutError:
            self.fail("timeout error")
        self.fail("emit_event did not throw exception")

    async def test_whenTimeoutOnSendingMessage_expectThrow(self):
        s1 = self.ev.register_service('service1')
        self.ev.register_service('service2')

        try:
            await s1.emit_event_to('service2', {}, timeout=0.1)
        except EventError as e:
            return
        self.fail("emit_event_to did not throw exception during timeout!")
