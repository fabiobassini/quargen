"""
Gestione centralizzata delle operazioni asincrone.
"""

import asyncio
import logging

logger = logging.getLogger(__name__)

class AsyncManager:
    def __init__(self):
        self.task_queue = asyncio.Queue()
        self.worker_task = None
        self.running = False

    async def start(self):
        self.running = True
        self.worker_task = asyncio.create_task(self._worker_loop())
        logger.info("[AsyncManager] Worker loop avviato.")

    async def stop(self):
        self.running = False
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                logger.info("[AsyncManager] Worker loop cancellato.")
            self.worker_task = None
        logger.info("[AsyncManager] Fermato.")

    async def schedule_task(self, coro_func, *args, **kwargs):
        await self.task_queue.put((coro_func, args, kwargs))
        logger.info(f"[AsyncManager] Task {coro_func.__name__} programmato.")

    async def _worker_loop(self):
        while self.running:
            try:
                coro_func, args, kwargs = await self.task_queue.get()
                try:
                    await coro_func(*args, **kwargs)
                except Exception as e:
                    self.handle_task_error(e, coro_func, args, kwargs)
                finally:
                    self.task_queue.task_done()
            except asyncio.CancelledError:
                logger.info("[AsyncManager] Worker loop cancellato, esco dal ciclo.")
                break
            except Exception as e:
                self.handle_task_error(e, None, None, None)
        logger.info("[AsyncManager] Worker loop terminato.")

    def handle_task_error(self, exc, coro_func, args, kwargs):
        logger.error(
            "[AsyncManager] ERRORE durante l'esecuzione di %s con args=%s kwargs=%s.\nEccezione: %s",
            coro_func.__name__ if coro_func else "task sconosciuto",
            args,
            kwargs,
            repr(exc)
        )
