import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Sentinel AI - Intelligent Early Warning & Store Platform")

# In-memory store for generated demo licenses and telemetry
LICENSES_DB = {
    "SENTINEL-PRO-DEMO-2026": {
        "tier": "Developer Pro",
        "seats": 3,
        "used_seats": 1,
        "status": "active",
        "created_at": "2026-11-21T00:00:00Z"
    }
}

class LicensePurchaseRequest(BaseModel):
    tier: str
    email: str
    billing_cycle: Optional[str] = "monthly"

class LicenseVerifyRequest(BaseModel):
    license_key: str

@app.get("/api/v1/plans")
def get_plans():
    return {
        "plans": [
            {
                "id": "community",
                "name": "Community Edition",
                "price": 0,
                "billing": "Forever Free",
                "seats": 1,
                "features": [
                    "Single machine local monitor",
                    "Baseline CPU/RAM anomaly scoring",
                    "Local React webview dashboard",
                    "Community Discord support"
                ]
            },
            {
                "id": "dev-pro",
                "name": "Developer Pro",
                "price": 19,
                "billing": "per month",
                "seats": 3,
                "popular": True,
                "features": [
                    "Up to 3 workstations",
                    "CPU, RAM, Network & Process tracking",
                    "Custom anomaly sensitivity threshold",
                    "Explainable AI root-cause analysis",
                    "Instant Slack / Webhook alerts"
                ]
            },
            {
                "id": "enterprise",
                "name": "Enterprise Fleet",
                "price": 99,
                "billing": "per month",
                "seats": 25,
                "features": [
                    "25 nodes / servers included",
                    "Multi-device centralized telemetry grid",
                    "Automated threat remediation hooks",
                    "99.9% SLA & dedicated support",
                    "SAML / SSO integration"
                ]
            }
        ]
    }

@app.post("/api/v1/licenses/purchase")
def purchase_license(req: LicensePurchaseRequest):
    prefix = "COMM" if "community" in req.tier.lower() else ("ENT" if "enterprise" in req.tier.lower() else "PRO")
    key = f"SENTINEL-{prefix}-{uuid.uuid4().hex[:4].upper()}-{uuid.uuid4().hex[:4].upper()}"
    seats = 1 if prefix == "COMM" else (25 if prefix == "ENT" else 3)
    
    LICENSES_DB[key] = {
        "tier": req.tier,
        "email": req.email,
        "seats": seats,
        "used_seats": 0,
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    return {
        "success": True,
        "license_key": key,
        "tier": req.tier,
        "seats": seats,
        "download_command": f"sentinel-cli activate --key {key}"
    }

@app.post("/api/v1/licenses/verify")
def verify_license(req: LicenseVerifyRequest):
    key = req.license_key.strip().upper()
    if key in LICENSES_DB:
        lic = LICENSES_DB[key]
        return {
            "valid": True,
            "status": lic["status"],
            "tier": lic["tier"],
            "seats": lic["seats"],
            "used_seats": lic.get("used_seats", 0)
        }
    raise HTTPException(status_code=404, detail="License key not found or expired.")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "sentinel-api", "version": "2.4.0", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/", response_class=HTMLResponse)
def serve_storefront():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Sentinel AI — Intelligent Early Warning System & Store</title>
      <script src="https://cdn.tailwindcss.com"></script>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
      <style>
        body { background-color: #070c18; color: #f1f5f9; font-family: ui-sans-serif, system-ui, -apple-system, sans-serif; }
        .gradient-text { background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .grid-bg { background-image: radial-gradient(rgba(56, 189, 248, 0.08) 1px, transparent 0); background-size: 32px 32px; }
        .glass-card { background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(12px); border: 1px solid rgba(56, 189, 248, 0.15); }
        .glass-card:hover { border-color: rgba(56, 189, 248, 0.35); box-shadow: 0 0 20px rgba(56, 189, 248, 0.12); }
        @keyframes pulse-slow { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
        .animate-pulse-slow { animation: pulse-slow 3s infinite; }
      </style>
    </head>
    <body class="min-h-screen grid-bg">

      <!-- TOP TELEMETRY STATUS BAR -->
      <div class="bg-[#050811] border-b border-slate-800 text-xs py-2 px-4 flex flex-wrap items-center justify-between text-slate-400 gap-2">
        <div class="flex items-center space-x-2">
          <span class="h-2 w-2 rounded-full bg-emerald-400 animate-ping"></span>
          <span class="h-2 w-2 rounded-full bg-emerald-500 -ml-3"></span>
          <span class="font-mono text-emerald-400 font-semibold tracking-wider">SENTINEL TELEMETRY GRID: SYSTEM HEALTH NOMINAL</span>
        </div>
        <div class="flex items-center space-x-6 font-mono text-slate-300">
          <span>Guarded Endpoints: <strong class="text-sky-400 font-semibold">28,450+</strong></span>
          <span class="hidden md:inline">|</span>
          <span class="hidden md:inline">Threats Prevented (24h): <strong class="text-emerald-400 font-semibold">1,429</strong></span>
          <span class="hidden lg:inline">|</span>
          <span class="hidden lg:inline text-amber-300">Promo Code: <strong class="bg-amber-950/80 px-2 py-0.5 rounded border border-amber-500/40">SENTINEL20 (-20%)</strong></span>
        </div>
      </div>

      <!-- MAIN NAVIGATION -->
      <nav class="sticky top-0 z-50 bg-[#070c18]/90 backdrop-blur-md border-b border-slate-800/80 px-6 py-3.5 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="h-10 w-10 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 text-lg shadow-[0_0_15px_rgba(56,189,248,0.3)]">
            <i class="fa-solid fa-shield-halved"></i>
          </div>
          <div>
            <div class="flex items-center space-x-1.5">
              <span class="font-black text-xl tracking-tight text-white">SENTINEL</span>
              <span class="font-black text-xl tracking-tight text-sky-400">AI</span>
            </div>
            <div class="text-[10px] tracking-widest text-slate-400 uppercase font-mono">Intelligent Early Warning System</div>
          </div>
        </div>

        <div class="hidden lg:flex items-center space-x-8 text-sm font-medium text-slate-300">
          <a href="#editions" class="hover:text-sky-400 transition">Editions & Plans</a>
          <a href="#demo" class="hover:text-sky-400 transition">Live Telemetry Demo</a>
          <a href="#pipeline" class="hover:text-sky-400 transition">Pipeline</a>
          <a href="#why" class="hover:text-sky-400 transition">Why Sentinel</a>
        </div>

        <div class="flex items-center space-x-3">
          <button onclick="triggerAttackSimulation()" class="bg-rose-950/60 hover:bg-rose-900 border border-rose-500/50 text-rose-300 text-xs font-semibold px-3.5 py-2 rounded-md transition flex items-center space-x-1.5 shadow-[0_0_10px_rgba(244,63,94,0.2)]">
            <i class="fa-solid fa-triangle-exclamation"></i>
            <span>Test Security / Pentest</span>
          </button>
          <button onclick="openVerifyModal()" class="bg-slate-800/80 hover:bg-slate-800 border border-slate-700 text-slate-200 text-xs font-medium px-3 py-2 rounded-md transition flex items-center space-x-1.5">
            <i class="fa-solid fa-key text-sky-400"></i>
            <span>Verify License</span>
          </button>
          <a href="#editions" class="bg-sky-500 hover:bg-sky-400 text-slate-950 text-xs font-bold px-4 py-2 rounded-md transition flex items-center space-x-1.5 shadow-lg shadow-sky-500/25">
            <i class="fa-solid fa-cart-shopping"></i>
            <span>Get License</span>
          </a>
        </div>
      </nav>

      <!-- HERO SECTION WITH INTERACTIVE RADAR -->
      <section class="max-w-7xl mx-auto px-6 pt-16 pb-20 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        <div class="lg:col-span-7 space-y-6">
          <div class="inline-flex items-center space-x-2 bg-sky-950/60 border border-sky-500/30 text-sky-300 px-3.5 py-1.5 rounded-full text-xs font-mono font-semibold tracking-wide">
            <span class="w-1.5 h-1.5 rounded-full bg-sky-400 animate-ping"></span>
            <span>AI-POWERED EARLY WARNING</span>
          </div>
          
          <h1 class="text-4xl sm:text-6xl font-black tracking-tight text-white leading-none">
            SENTINEL <span class="gradient-text">AI</span>
            <span class="block text-2xl sm:text-3xl font-semibold text-slate-300 mt-3 font-sans">
              Intelligent Early Warning System
            </span>
          </h1>

          <p class="text-lg text-sky-200/90 italic font-medium border-l-2 border-sky-500 pl-4 py-1">
            "Detect the unusual. Explain the risk. Act before it escalates."
          </p>

          <p class="text-slate-400 text-sm sm:text-base leading-relaxed max-w-xl">
            Traditional monitoring only displays isolated metrics after a failure happens. Sentinel AI continuously learns normal system behavior across CPU, RAM, network, and processes—scoring risk with explainable AI and recommending safe actions.
          </p>

          <div class="flex flex-wrap items-center gap-4 pt-4">
            <a href="#editions" class="bg-gradient-to-r from-sky-500 to-indigo-500 hover:from-sky-400 hover:to-indigo-400 text-slate-950 font-bold px-6 py-3.5 rounded-lg transition shadow-lg shadow-sky-500/25 flex items-center space-x-2 text-sm">
              <span>Explore Sentinel Products</span>
              <i class="fa-solid fa-arrow-right"></i>
            </a>
            <a href="#demo" class="bg-slate-900/80 hover:bg-slate-800 border border-slate-700 text-slate-200 font-medium px-5 py-3.5 rounded-lg transition text-sm flex items-center space-x-2">
              <i class="fa-solid fa-bolt text-amber-400"></i>
              <span>Interactive Telemetry Demo</span>
            </a>
          </div>
        </div>

        <!-- RADAR VISUAL COMPONENT -->
        <div class="lg:col-span-5">
          <div class="glass-card rounded-2xl p-6 relative overflow-hidden shadow-2xl">
            <div class="flex items-center justify-between mb-4">
              <span class="text-xs font-mono font-bold tracking-widest text-sky-400 uppercase">PROACTIVE THREAT AWARENESS ENGINE</span>
              <span id="radarStatus" class="text-[11px] font-mono text-emerald-400 bg-emerald-950/60 border border-emerald-500/30 px-2 py-0.5 rounded">SWEEPING</span>
            </div>

            <div class="flex justify-center py-2 relative">
              <canvas id="radarCanvas" width="340" height="340" class="rounded-full bg-[#030712] border border-sky-500/20 shadow-[inset_0_0_40px_rgba(56,189,248,0.15)]"></canvas>
            </div>

            <div class="grid grid-cols-4 gap-2 pt-4 border-t border-slate-800 text-center">
              <div class="p-2 rounded bg-slate-900/50 border border-slate-800">
                <div class="text-[10px] text-slate-400 uppercase">AI Monitoring</div>
                <div class="text-xs font-bold text-sky-400 font-mono mt-0.5">Active</div>
              </div>
              <div class="p-2 rounded bg-slate-900/50 border border-slate-800">
                <div class="text-[10px] text-slate-400 uppercase">Anomaly</div>
                <div id="radarAnomalyBadge" class="text-xs font-bold text-emerald-400 font-mono mt-0.5">0.12 (Low)</div>
              </div>
              <div class="p-2 rounded bg-slate-900/50 border border-slate-800">
                <div class="text-[10px] text-slate-400 uppercase">Explainable XAI</div>
                <div class="text-xs font-bold text-indigo-400 font-mono mt-0.5">Ready</div>
              </div>
              <div class="p-2 rounded bg-slate-900/50 border border-slate-800">
                <div class="text-[10px] text-slate-400 uppercase">Threat Shield</div>
                <div class="text-xs font-bold text-sky-400 font-mono mt-0.5">Armed</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- SLIDE 06 CONCEPT - REAL-TIME TELEMETRY SIMULATION -->
      <section id="demo" class="max-w-7xl mx-auto px-6 py-16 border-t border-slate-800/80">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
          <div>
            <div class="text-xs font-mono font-bold tracking-widest text-sky-400 uppercase mb-1">SLIDE 06 CONCEPT · PRODUCT DASHBOARD</div>
            <h2 class="text-3xl font-black text-white">One dashboard. Complete system awareness.</h2>
            <p class="text-slate-400 text-sm mt-1">Illustrative dashboard concept with live simulated metrics & explainable alerts.</p>
          </div>
          <div class="flex items-center space-x-3">
            <span class="text-xs text-slate-400">Simulation Mode:</span>
            <button onclick="toggleSimulationSpike()" id="spikeBtn" class="bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 px-3.5 py-1.5 rounded border border-slate-700 transition">
              Inject CPU Spike
            </button>
          </div>
        </div>

        <div class="glass-card rounded-2xl p-6 md:p-8 space-y-6">
          <div class="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <span class="text-sm font-bold text-white font-mono">SENTINEL AI · SYSTEM OVERVIEW</span>
            </div>
            <div class="flex items-center space-x-2">
              <span class="text-xs font-mono font-bold text-emerald-400 bg-emerald-950/70 border border-emerald-500/30 px-3 py-1 rounded-full flex items-center space-x-1.5">
                <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span id="healthLabel">SYSTEM HEALTH · NOMINAL</span>
              </span>
            </div>
          </div>

          <!-- 5 METRIC CARDS -->
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
            <div class="bg-slate-900/70 border border-slate-800 p-4 rounded-xl">
              <div class="text-xs font-mono text-slate-400 uppercase">CPU USAGE</div>
              <div id="metricCpu" class="text-3xl font-black font-mono text-white mt-2">68%</div>
              <div class="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
                <div id="barCpu" class="bg-sky-400 h-full rounded-full transition-all duration-500" style="width: 68%;"></div>
              </div>
            </div>

            <div class="bg-slate-900/70 border border-slate-800 p-4 rounded-xl">
              <div class="text-xs font-mono text-slate-400 uppercase">RAM CONSUMPTION</div>
              <div id="metricRam" class="text-3xl font-black font-mono text-white mt-2">42%</div>
              <div class="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
                <div class="bg-indigo-400 h-full rounded-full" style="width: 42%;"></div>
              </div>
            </div>

            <div class="bg-slate-900/70 border border-slate-800 p-4 rounded-xl">
              <div class="text-xs font-mono text-slate-400 uppercase">NETWORK ACTIVITY</div>
              <div id="metricNet" class="text-3xl font-black font-mono text-white mt-2">1.8 MB/s</div>
              <div class="text-[10px] text-slate-500 mt-2 font-mono">TX: 1.2M / RX: 0.6M</div>
            </div>

            <div class="bg-slate-900/70 border border-slate-800 p-4 rounded-xl">
              <div class="text-xs font-mono text-slate-400 uppercase">ACTIVE PROCESSES</div>
              <div id="metricProc" class="text-3xl font-black font-mono text-white mt-2">124</div>
              <div class="text-[10px] text-emerald-400 mt-2 font-mono">0 unfamiliar</div>
            </div>

            <div class="bg-slate-900/70 border border-amber-500/30 bg-amber-950/10 p-4 rounded-xl col-span-2 sm:col-span-1">
              <div class="text-xs font-mono text-amber-300 uppercase">ANOMALY SCORE</div>
              <div class="flex items-baseline space-x-2 mt-2">
                <span id="metricScore" class="text-3xl font-black font-mono text-amber-400">0.74</span>
                <span id="badgeRisk" class="text-xs font-bold font-mono bg-amber-900/80 text-amber-200 border border-amber-500/40 px-2 py-0.5 rounded">REVIEW</span>
              </div>
              <div class="text-[10px] text-slate-400 mt-2 font-mono">Isolation Forest Model</div>
            </div>
          </div>

          <!-- DETAILED CHARTS & ALERTS SECTION -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
            <!-- Simulated activity bars -->
            <div class="lg:col-span-4 bg-slate-900/50 border border-slate-800 p-5 rounded-xl">
              <div class="text-xs font-mono text-slate-400 uppercase mb-4">SYSTEM ACTIVITY · ILLUSTRATIVE</div>
              <div class="flex items-end space-x-2 h-36 pt-6">
                <div class="bg-sky-500/40 w-full h-[30%] rounded-t"></div>
                <div class="bg-sky-500/40 w-full h-[45%] rounded-t"></div>
                <div class="bg-sky-500/50 w-full h-[25%] rounded-t"></div>
                <div class="bg-sky-500/60 w-full h-[55%] rounded-t"></div>
                <div class="bg-sky-500/40 w-full h-[35%] rounded-t"></div>
                <div class="bg-amber-400 w-full h-[85%] rounded-t animate-pulse"></div>
                <div class="bg-amber-400 w-full h-[95%] rounded-t animate-pulse"></div>
                <div class="bg-amber-400 w-full h-[80%] rounded-t animate-pulse"></div>
                <div class="bg-sky-500/40 w-full h-[40%] rounded-t"></div>
                <div class="bg-sky-500/30 w-full h-[50%] rounded-t"></div>
              </div>
            </div>

            <!-- Recent Alerts -->
            <div class="lg:col-span-3 bg-slate-900/50 border border-slate-800 p-5 rounded-xl">
              <div class="text-xs font-mono text-slate-400 uppercase mb-4">RECENT ALERTS · 03</div>
              <div class="space-y-3">
                <div class="flex items-center justify-between text-xs pb-2 border-b border-slate-800">
                  <span class="text-slate-300">CPU behaviour</span>
                  <span id="alertCpu" class="px-2 py-0.5 rounded bg-rose-950 border border-rose-500/40 text-rose-300 font-mono font-bold">ELEVATED</span>
                </div>
                <div class="flex items-center justify-between text-xs pb-2 border-b border-slate-800">
                  <span class="text-slate-300">Process activity</span>
                  <span class="px-2 py-0.5 rounded bg-amber-950 border border-amber-500/40 text-amber-300 font-mono font-bold">REVIEW</span>
                </div>
                <div class="flex items-center justify-between text-xs">
                  <span class="text-slate-300">Network pattern</span>
                  <span class="px-2 py-0.5 rounded bg-emerald-950 border border-emerald-500/40 text-emerald-300 font-mono font-bold">CLEAR</span>
                </div>
              </div>
            </div>

            <!-- Explainable AI Explanation -->
            <div class="lg:col-span-5 bg-gradient-to-br from-slate-900 to-sky-950/40 border border-sky-500/30 p-5 rounded-xl flex flex-col justify-between shadow-lg">
              <div>
                <div class="flex items-center space-x-2 text-xs font-mono text-sky-400 uppercase mb-2">
                  <i class="fa-solid fa-brain"></i>
                  <span>AI EXPLANATION</span>
                </div>
                <h4 id="xaiTitle" class="text-base font-bold text-white mb-2">Unusual CPU behaviour detected.</h4>
                <p id="xaiBody" class="text-xs text-slate-300 leading-relaxed">
                  CPU usage has increased significantly compared with the system's recent baseline. A transient worker thread is consuming disproportionate compute cycles.
                </p>
              </div>
              <div class="mt-4 pt-3 border-t border-sky-500/20 text-xs font-mono text-sky-300 flex items-center space-x-2">
                <i class="fa-solid fa-arrow-right"></i>
                <span id="xaiAction">Review the active processes and investigate the resource-intensive application.</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- EDITIONS & ONLINE STORE SECTION -->
      <section id="editions" class="max-w-7xl mx-auto px-6 py-20 border-t border-slate-800/80">
        <div class="text-center max-w-2xl mx-auto mb-16">
          <span class="text-xs font-mono font-bold tracking-widest text-sky-400 uppercase">EDITIONS & PRICING</span>
          <h2 class="text-3xl sm:text-4xl font-black text-white mt-1">Get Sentinel AI for your machines</h2>
          <p class="text-slate-400 text-sm mt-2">Deploy from single developer workstations to enterprise server clusters.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 items-stretch">
          
          <!-- Plan 1: Community -->
          <div class="glass-card rounded-2xl p-8 flex flex-col justify-between">
            <div>
              <div class="text-xs font-mono text-slate-400 uppercase tracking-widest">PERSONAL COMPUTERS</div>
              <h3 class="text-2xl font-bold text-white mt-1">Community</h3>
              <p class="text-xs text-slate-400 mt-2">Perfect for individual laptops and exploratory use.</p>
              
              <div class="my-6">
                <span class="text-4xl font-black text-white">$0</span>
                <span class="text-slate-400 text-xs font-mono">/ forever free</span>
              </div>

              <ul class="space-y-3 text-xs text-slate-300 mb-8">
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span>1 Monitored Device</span></li>
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span>Baseline CPU/RAM tracker</span></li>
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span>Local interactive dashboard</span></li>
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span>Community support</span></li>
              </ul>
            </div>
            <button onclick="orderLicense('Community Edition', 0)" class="w-full bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs py-3 rounded-lg border border-slate-700 transition">
              Download Free License
            </button>
          </div>

          <!-- Plan 2: Developer Pro (Popular) -->
          <div class="glass-card rounded-2xl p-8 border-2 border-sky-500/50 flex flex-col justify-between relative shadow-[0_0_30px_rgba(56,189,248,0.15)] bg-[#0d1627]">
            <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-sky-500 text-slate-950 text-[10px] font-black uppercase tracking-wider px-3 py-1 rounded-full shadow">
              MOST POPULAR
            </div>
            <div>
              <div class="text-xs font-mono text-sky-400 uppercase tracking-widest">DEVELOPER WORKSTATIONS</div>
              <h3 class="text-2xl font-bold text-white mt-1">Developer Pro</h3>
              <p class="text-xs text-slate-400 mt-2">Comprehensive protection for active development machines.</p>
              
              <div class="my-6">
                <span class="text-4xl font-black text-white">$19</span>
                <span class="text-slate-400 text-xs font-mono">/ month</span>
              </div>

              <ul class="space-y-3 text-xs text-slate-300 mb-8">
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span><strong>3 Monitored Devices</strong></span></li>
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span>Network & Process Behavior Engine</span></li>
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span>Isolation Forest anomaly scoring</span></li>
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span>Explainable AI Root Cause Reports</span></li>
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span>Slack & Webhook Integrations</span></li>
              </ul>
            </div>
            <button onclick="orderLicense('Developer Pro', 19)" class="w-full bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs py-3 rounded-lg transition shadow-lg shadow-sky-500/25">
              Order Developer Pro License
            </button>
          </div>

          <!-- Plan 3: Enterprise -->
          <div class="glass-card rounded-2xl p-8 flex flex-col justify-between">
            <div>
              <div class="text-xs font-mono text-slate-400 uppercase tracking-widest">ENTERPRISE IT & LABS</div>
              <h3 class="text-2xl font-bold text-white mt-1">Enterprise Fleet</h3>
              <p class="text-xs text-slate-400 mt-2">Centralized monitoring across server fleets and computer labs.</p>
              
              <div class="my-6">
                <span class="text-4xl font-black text-white">$99</span>
                <span class="text-slate-400 text-xs font-mono">/ month</span>
              </div>

              <ul class="space-y-3 text-xs text-slate-300 mb-8">
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span><strong>25 Monitored Nodes / Servers</strong></span></li>
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span>Centralized Cloud Dashboard</span></li>
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span>Multi-device anomaly cross-correlation</span></li>
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span>Automated remediation webhooks</span></li>
                <li class="flex items-center space-x-2.5"><i class="fa-solid fa-check text-sky-400"></i><span>99.9% SLA & Dedicated Support</span></li>
              </ul>
            </div>
            <button onclick="orderLicense('Enterprise Fleet', 99)" class="w-full bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs py-3 rounded-lg border border-slate-700 transition">
              Order Enterprise Fleet
            </button>
          </div>
        </div>
      </section>

      <!-- LICENSE MODAL (GENERATOR & CHECKOUT) -->
      <div id="licenseModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="glass-card rounded-2xl max-w-md w-full p-6 border border-sky-500/40 shadow-2xl relative">
          <button onclick="closeModal('licenseModal')" class="absolute top-4 right-4 text-slate-400 hover:text-white">
            <i class="fa-solid fa-xmark text-lg"></i>
          </button>
          
          <div class="text-center">
            <div class="h-12 w-12 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 flex items-center justify-center mx-auto text-xl mb-3">
              <i class="fa-solid fa-shield-check"></i>
            </div>
            <h3 class="text-xl font-bold text-white" id="modalPlanName">Developer Pro License</h3>
            <p class="text-xs text-slate-400 mt-1">Instant fulfillment and key activation.</p>
          </div>

          <div class="mt-6 space-y-4">
            <div>
              <label class="text-xs font-mono text-slate-300 block mb-1">YOUR EMAIL ADDRESS</label>
              <input type="email" id="customerEmail" placeholder="admin@company.com" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-sky-500">
            </div>

            <div id="licenseResultArea" class="hidden bg-slate-950 border border-sky-500/40 p-4 rounded-xl space-y-3">
              <div class="text-xs text-slate-400 font-mono">YOUR ACTIVATION KEY:</div>
              <div id="generatedKey" class="font-mono text-sm text-sky-400 font-bold bg-slate-900 px-3 py-2 rounded border border-slate-800 select-all">
                SENTINEL-PRO-XXXX-YYYY
              </div>
              <div class="text-[11px] text-slate-400">
                To activate on your server or workstation, run:
                <pre class="bg-black/60 p-2 rounded mt-1 font-mono text-slate-200 select-all" id="activationCmd">sentinel-cli activate --key SENTINEL-PRO-XXXX</pre>
              </div>
            </div>

            <button id="checkoutBtn" onclick="confirmPurchase()" class="w-full bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs py-3 rounded-lg transition shadow-lg shadow-sky-500/25">
              Confirm & Generate Key
            </button>
          </div>
        </div>
      </div>

      <!-- VERIFY MODAL -->
      <div id="verifyModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="glass-card rounded-2xl max-w-md w-full p-6 border border-slate-700 shadow-2xl relative">
          <button onclick="closeModal('verifyModal')" class="absolute top-4 right-4 text-slate-400 hover:text-white">
            <i class="fa-solid fa-xmark text-lg"></i>
          </button>
          
          <h3 class="text-lg font-bold text-white mb-2 flex items-center space-x-2">
            <i class="fa-solid fa-key text-sky-400"></i>
            <span>Verify License Key</span>
          </h3>
          <p class="text-xs text-slate-400 mb-4">Check validity and seat allocation for your Sentinel AI instance.</p>

          <div class="space-y-4">
            <input type="text" id="verifyKeyInput" placeholder="SENTINEL-PRO-XXXX-YYYY" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3.5 py-2.5 text-xs text-white font-mono focus:outline-none focus:border-sky-500">
            <button onclick="submitVerifyKey()" class="w-full bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs py-2.5 rounded-lg transition">
              Verify Key
            </button>
            <div id="verifyOutput" class="hidden text-xs font-mono p-3 rounded bg-slate-950 border"></div>
          </div>
        </div>
      </div>

      <!-- FOOTER -->
      <footer class="border-t border-slate-800/80 bg-[#050811] py-10 px-6 text-center text-xs text-slate-500">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div class="flex items-center space-x-2">
            <span class="font-bold text-slate-300">SENTINEL AI</span>
            <span>· Intelligent Early Warning System</span>
          </div>
          <div class="space-x-6">
            <a href="/docs" class="text-sky-400 hover:underline">API Documentation (/docs)</a>
            <a href="/health" class="text-slate-400 hover:underline">Health Check (/health)</a>
          </div>
        </div>
      </footer>

      <!-- INTERACTIVE JAVASCRIPT & RADAR ANIMATION -->
      <script>
        // ----------------------------------------------------
        // 1. RADAR CANVAS SWEEP ANIMATION
        // ----------------------------------------------------
        const canvas = document.getElementById('radarCanvas');
        const ctx = canvas.getContext('2d');
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const maxRadius = 145;
        let angle = 0;

        // Simulated anomaly blips
        let blips = [
          { r: 75, angle: 0.9, color: '#f59e0b', pulse: 0, label: 'CPU Shift' },
          { r: 110, angle: 3.4, color: '#38bdf8', pulse: 0, label: 'Port Scan' },
          { r: 45, angle: 4.8, color: '#10b981', pulse: 0, label: 'Baseline' }
        ];

        function drawRadar() {
          ctx.fillStyle = 'rgba(3, 7, 18, 0.15)';
          ctx.fillRect(0, 0, canvas.width, canvas.height);

          // Concentric circles
          ctx.strokeStyle = 'rgba(56, 189, 248, 0.18)';
          ctx.lineWidth = 1;
          for (let r = 35; r <= maxRadius; r += 35) {
            ctx.beginPath();
            ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
            ctx.stroke();
          }

          // Cross hairs
          ctx.beginPath();
          ctx.moveTo(centerX - maxRadius, centerY);
          ctx.lineTo(centerX + maxRadius, centerY);
          ctx.moveTo(centerX, centerY - maxRadius);
          ctx.lineTo(centerX, centerY + maxRadius);
          ctx.strokeStyle = 'rgba(56, 189, 248, 0.12)';
          ctx.stroke();

          // Rotating sweep line
          angle += 0.035;
          const sweepX = centerX + Math.cos(angle) * maxRadius;
          const sweepY = centerY + Math.sin(angle) * maxRadius;

          const gradient = ctx.createLinearGradient(centerX, centerY, sweepX, sweepY);
          gradient.addColorStop(0, 'rgba(56, 189, 248, 0.6)');
          gradient.addColorStop(1, 'rgba(56, 189, 248, 0.05)');

          ctx.beginPath();
          ctx.moveTo(centerX, centerY);
          ctx.arc(centerX, centerY, maxRadius, angle - 0.25, angle);
          ctx.fillStyle = 'rgba(56, 189, 248, 0.08)';
          ctx.fill();

          ctx.beginPath();
          ctx.moveTo(centerX, centerY);
          ctx.lineTo(sweepX, sweepY);
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 2;
          ctx.stroke();

          // Draw blips
          blips.forEach(b => {
            const bx = centerX + Math.cos(b.angle) * b.r;
            const by = centerY + Math.sin(b.angle) * b.r;
            
            // Check sweep proximity
            let diff = Math.abs((angle % (Math.PI * 2)) - (b.angle % (Math.PI * 2)));
            if (diff < 0.2) b.pulse = 1.0;
            if (b.pulse > 0) b.pulse -= 0.015;

            ctx.beginPath();
            ctx.arc(bx, by, 4 + (b.pulse * 6), 0, Math.PI * 2);
            ctx.fillStyle = b.color;
            ctx.shadowBlur = 10 * (b.pulse + 0.3);
            ctx.shadowColor = b.color;
            ctx.fill();
            ctx.shadowBlur = 0;
          });

          requestAnimationFrame(drawRadar);
        }
        drawRadar();

        // ----------------------------------------------------
        // 2. SIMULATION & PENTEST ATTACK CONTROLS
        // ----------------------------------------------------
        let isSpiked = false;
        function toggleSimulationSpike() {
          isSpiked = !isSpiked;
          const cpu = document.getElementById('metricCpu');
          const bar = document.getElementById('barCpu');
          const score = document.getElementById('metricScore');
          const risk = document.getElementById('badgeRisk');
          const alertCpu = document.getElementById('alertCpu');
          const xaiTitle = document.getElementById('xaiTitle');
          const xaiBody = document.getElementById('xaiBody');
          const btn = document.getElementById('spikeBtn');

          if (isSpiked) {
            cpu.innerText = '94%';
            cpu.classList.add('text-rose-400');
            bar.style.width = '94%';
            bar.classList.replace('bg-sky-400', 'bg-rose-500');
            score.innerText = '0.91';
            score.classList.replace('text-amber-400', 'text-rose-400');
            risk.innerText = 'CRITICAL';
            risk.className = 'text-xs font-bold font-mono bg-rose-900 text-rose-200 border border-rose-500 px-2 py-0.5 rounded animate-pulse';
            alertCpu.innerText = 'CRITICAL HIGH';
            alertCpu.className = 'px-2 py-0.5 rounded bg-rose-900 border border-rose-500 text-rose-200 font-mono font-bold animate-pulse';
            xaiTitle.innerText = 'High Anomaly Spike: Unauthorized CPU Exhaustion';
            xaiBody.innerText = 'A foreign subprocess has initiated high-frequency floating point operations. Risk exceeds critical baseline (0.91/1.0). Immediate thread quarantine advised.';
            btn.innerText = 'Reset to Baseline';
          } else {
            cpu.innerText = '68%';
            cpu.classList.remove('text-rose-400');
            bar.style.width = '68%';
            bar.classList.replace('bg-rose-500', 'bg-sky-400');
            score.innerText = '0.74';
            score.classList.replace('text-rose-400', 'text-amber-400');
            risk.innerText = 'REVIEW';
            risk.className = 'text-xs font-bold font-mono bg-amber-900/80 text-amber-200 border border-amber-500/40 px-2 py-0.5 rounded';
            alertCpu.innerText = 'ELEVATED';
            alertCpu.className = 'px-2 py-0.5 rounded bg-rose-950 border border-rose-500/40 text-rose-300 font-mono font-bold';
            xaiTitle.innerText = 'Unusual CPU behaviour detected.';
            xaiBody.innerText = "CPU usage has increased significantly compared with the system's recent baseline. A transient worker thread is consuming disproportionate compute cycles.";
            btn.innerText = 'Inject CPU Spike';
          }
        }

        function triggerAttackSimulation() {
          toggleSimulationSpike();
          document.getElementById('demo').scrollIntoView({ behavior: 'smooth' });
        }

        // ----------------------------------------------------
        // 3. STORE LICENSE PURCHASE & VERIFY MODALS
        // ----------------------------------------------------
        let selectedTier = 'Developer Pro';
        function orderLicense(tier, price) {
          selectedTier = tier;
          document.getElementById('modalPlanName').innerText = tier + (price > 0 ? ` ($${price}/mo)` : ' (Free)');
          document.getElementById('licenseResultArea').classList.add('hidden');
          document.getElementById('checkoutBtn').classList.remove('hidden');
          document.getElementById('licenseModal').classList.remove('hidden');
        }

        async function confirmPurchase() {
          const email = document.getElementById('customerEmail').value || 'demo@sentinelai.io';
          const btn = document.getElementById('checkoutBtn');
          btn.innerText = 'Generating License...';
          btn.disabled = true;

          try {
            const resp = await fetch('/api/v1/licenses/purchase', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ tier: selectedTier, email: email })
            });
            const data = await resp.json();
            
            document.getElementById('generatedKey').innerText = data.license_key;
            document.getElementById('activationCmd').innerText = data.download_command;
            document.getElementById('licenseResultArea').classList.remove('hidden');
            btn.classList.add('hidden');
          } catch(e) {
            alert('Failed to generate license key.');
          } finally {
            btn.innerText = 'Confirm & Generate Key';
            btn.disabled = false;
          }
        }

        function openVerifyModal() {
          document.getElementById('verifyOutput').classList.add('hidden');
          document.getElementById('verifyModal').classList.remove('hidden');
        }

        async function submitVerifyKey() {
          const key = document.getElementById('verifyKeyInput').value.trim();
          const out = document.getElementById('verifyOutput');
          if (!key) return;

          try {
            const resp = await fetch('/api/v1/licenses/verify', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ license_key: key })
            });
            const data = await resp.json();
            out.className = 'text-xs font-mono p-3 rounded bg-emerald-950/80 border border-emerald-500 text-emerald-300';
            out.innerHTML = `✓ VALID LICENSE<br>Tier: ${data.tier}<br>Status: ${data.status.toUpperCase()}<br>Seats: ${data.used_seats}/${data.seats} Active`;
          } catch(e) {
            out.className = 'text-xs font-mono p-3 rounded bg-rose-950/80 border border-rose-500 text-rose-300';
            out.innerText = '✗ INVALID OR EXPIRED LICENSE KEY';
          }
          out.classList.remove('hidden');
        }

        function closeModal(id) {
          document.getElementById(id).classList.add('hidden');
        }
      </script>
    </body>
    </html>
    """
