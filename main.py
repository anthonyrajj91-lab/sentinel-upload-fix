from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Sentinel AI API & Storefront")

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Sentinel AI - Early Warning System</title>
        <style>
          body { font-family: system-ui, sans-serif; background: #0b1120; color: #f8fafc; padding: 40px; }
          .card { background: #1e293b; border-radius: 8px; padding: 24px; max-width: 600px; margin: 0 auto; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
          h1 { color: #38bdf8; margin-top: 0; }
          .badge { background: #0369a1; color: #e0f2fe; padding: 4px 10px; border-radius: 4px; font-size: 14px; font-weight: bold; }
          .status { color: #4ade80; font-weight: bold; }
        </style>
      </head>
      <body>
        <div class="card">
          <span class="badge">AI-POWERED EARLY WARNING</span>
          <h1>Sentinel AI</h1>
          <p>Detect the unusual. Explain the risk. Act before it escalates.</p>
          <hr style="border-color: #334155; margin: 20px 0;">
          <p>Service Status: <span class="status">● ONLINE & ACTIVE</span></p>
          <p>API Documentation: <a href="/docs" style="color: #38bdf8;">Interactive Swagger Docs (/docs)</a></p>
        </div>
      </body>
    </html>
    """

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "sentinel-api", "version": "1.0.0"}
