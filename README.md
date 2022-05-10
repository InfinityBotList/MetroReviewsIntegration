# MetroReviewsIntegration
Metro Reviews Integration for IBL

Can be used as sample code by other lists. The list specific code is present under ``act.py``

Run with `MONGO_DBNAME="infinity" MONGO_URL="mongodb://127.0.0.1:27017/infinity" python3.10 -m uvicorn app:app` 

`secrets.json` must have ``secret_key`` and ``token`` (bot token for sending approve/deny embeds)
