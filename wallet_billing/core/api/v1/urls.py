from ninja import Router

from core.api.v1.wallets.handlers import router as wallets_router

router = Router()

router.add_router('/wallets', wallets_router)