import asyncio

from app.memory.gateway import MemoryGateway


def test_memory_gateway_defines_write_contract():
    async def run():
        gateway = MemoryGateway()

        try:
            await gateway.remember(
                content="A validated fact.",
                conversation_id="memory-test",
                memory_type="knowledge",
            )
        except NotImplementedError:
            return

        raise AssertionError("MemoryGateway.remember must define the contract")

    asyncio.run(run())
