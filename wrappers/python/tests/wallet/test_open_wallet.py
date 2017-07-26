from indy import IndyError
from indy import wallet
from indy.error import ErrorCode

from ..utils import storage

import pytest
import logging

logging.basicConfig(level=logging.DEBUG)


@pytest.yield_fixture(autouse=True)
def before_after_each():
    storage.cleanup()
    yield
    storage.cleanup()


@pytest.mark.asyncio
async def test_open_wallet_works():
    await wallet.create_wallet('pool1', 'wallet1', None, None, None)
    wallet_handle = await wallet.open_wallet('wallet1', None, None)
    assert wallet_handle is not None

    await wallet.close_wallet(wallet_handle)


@pytest.mark.asyncio
async def test_open_wallet_works_for_config():
    await wallet.create_wallet('pool1', 'wallet2', None, None, None)
    wallet_handle = await wallet.open_wallet('wallet2', '{"freshness_time":1000}', None)
    assert wallet_handle is not None

    await wallet.close_wallet(wallet_handle)


@pytest.mark.asyncio
async def test_open_wallet_works_for_not_created_wallet():
    with pytest.raises(IndyError) as e:
        await wallet.open_wallet('wallet_not_created', None, None)
    assert ErrorCode.CommonIOError == e.value.error_code


@pytest.mark.asyncio
async def test_open_wallet_works_for_twice():
    with pytest.raises(IndyError) as e:
        await wallet.create_wallet('pool1', 'wallet_twice', None, None, None)
        await wallet.open_wallet('wallet_twice', None, None)
        await wallet.open_wallet('wallet_twice', None, None)
    assert ErrorCode.WalletAlreadyOpenedError == e.value.error_code