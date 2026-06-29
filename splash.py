"""
splash.py — Splash screen for Evony Gear Optimizer.

Uses a small pywebview window that opens while Flask initializes.
Falls back to no splash if pywebview is unavailable.
"""

import threading
import time


SPLASH_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: #1e0404;
  font-family: Georgia, 'Times New Roman', serif;
  color: #f5e8c8;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  user-select: none;
}
.chrome {
  background: linear-gradient(180deg, #550e0e, #3d0808);
  border-bottom: 2px solid #c9a227;
  padding: 10px 18px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.app-title {
  color: #f0c040;
  font-size: 15px;
  font-weight: bold;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  text-shadow: 0 1px 4px rgba(0,0,0,0.6);
}
.app-version {
  color: #7a5c10;
  font-size: 10px;
  letter-spacing: 1px;
}
.body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 28px;
  padding: 20px 28px;
}
.icon-wrap { flex-shrink: 0; }
svg { filter: drop-shadow(0 2px 8px rgba(201,162,39,0.3)); }
.text-col { flex: 1; }
.headline {
  color: #f0c040;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 6px;
  letter-spacing: 1px;
}
.tagline {
  color: #d4b878;
  font-size: 11px;
  line-height: 1.6;
  margin-bottom: 18px;
}
.status {
  color: #8b6040;
  font-size: 10px;
  font-style: italic;
  margin-bottom: 8px;
  min-height: 14px;
  letter-spacing: 0.5px;
  transition: color 0.3s;
}
.bar-track {
  background: #2d0707;
  border: 1px solid #7a5c10;
  border-radius: 4px;
  height: 8px;
  overflow: hidden;
}
.bar-fill {
  background: linear-gradient(90deg, #7a5c10, #c9a227, #f0c040);
  height: 100%;
  width: 0%;
  border-radius: 4px;
  transition: width 0.4s ease;
}
.footer {
  background: #3d0808;
  border-top: 1px solid #7a5c10;
  padding: 7px 18px;
  font-size: 9px;
  color: #8b6040;
  letter-spacing: 0.5px;
  text-align: center;
}
</style>
</head>
<body>

<div class="chrome">
  <div>
    <div class="app-title">⚔ Evony Gear Optimizer</div>
  </div>
  <div class="app-version">v1.3.0</div>
</div>

<div class="body">
  <!-- Shield icon -->
  <div class="icon-wrap">
    <svg width="90" height="108" viewBox="-200 -250 400 520" xmlns="http://www.w3.org/2000/svg">
      <path d="M0,-230 L170,-150 L170,40 Q170,180 0,260 Q-170,180 -170,40 L-170,-150 Z"
            fill="#1a1a2e" stroke="#c9a227" stroke-width="8"/>
      <path d="M0,-200 L148,-132 L148,38 Q148,158 0,228 Q-148,158 -148,38 L-148,-132 Z"
            fill="#16213e"/>
      <path d="M0,-200 L148,-132 L148,38 Q148,158 0,228 Q-148,158 -148,38 L-148,-132 Z"
            fill="none" stroke="#7a6118" stroke-width="3"/>
      <g transform="rotate(-38)">
        <rect x="-6" y="-195" width="12" height="240" rx="2" fill="#c9a227" stroke="#7a6118" stroke-width="1.5"/>
        <rect x="-2" y="-188" width="4" height="220" rx="1" fill="#f0c040" opacity="0.5"/>
        <polygon points="-6,-195 6,-195 0,-225" fill="#f0c040"/>
        <rect x="-30" y="40" width="60" height="12" rx="4" fill="#c9a227" stroke="#7a6118" stroke-width="1.5"/>
        <rect x="-7" y="52" width="14" height="45" rx="3" fill="#3a2a0a" stroke="#7a6118" stroke-width="1.5"/>
        <ellipse cx="0" cy="104" rx="12" ry="10" fill="#c9a227" stroke="#7a6118" stroke-width="1.5"/>
      </g>
      <g transform="rotate(38)">
        <rect x="-6" y="-195" width="12" height="240" rx="2" fill="#c9a227" stroke="#7a6118" stroke-width="1.5"/>
        <rect x="-2" y="-188" width="4" height="220" rx="1" fill="#f0c040" opacity="0.5"/>
        <polygon points="-6,-195 6,-195 0,-225" fill="#f0c040"/>
        <rect x="-30" y="40" width="60" height="12" rx="4" fill="#c9a227" stroke="#7a6118" stroke-width="1.5"/>
        <rect x="-7" y="52" width="14" height="45" rx="3" fill="#3a2a0a" stroke="#7a6118" stroke-width="1.5"/>
        <ellipse cx="0" cy="104" rx="12" ry="10" fill="#c9a227" stroke="#7a6118" stroke-width="1.5"/>
      </g>
      <path d="M0,-58 L10,-28 L42,-28 L18,-10 L28,22 L0,4 L-28,22 L-18,-10 L-42,-28 L-10,-28 Z"
            fill="#f0c040" stroke="#7a6118" stroke-width="2"/>
      <path d="M-20,215 L0,240 L20,215" fill="none" stroke="#c9a227" stroke-width="4"
            stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>

  <div class="text-col">
    <div class="headline">Gear Optimizer</div>
    <div class="tagline">Find the best gear combinations<br>for your generals in Evony: The King's Return</div>
    <div class="status" id="status">Initializing...</div>
    <div class="bar-track">
      <div class="bar-fill" id="bar"></div>
    </div>
  </div>
</div>

<div class="footer">Loading — please wait</div>

<script>
  // Expose update functions so Python can call them via pywebview JS bridge
  function setStatus(msg, pct) {
    document.getElementById('status').textContent = msg;
    if (pct !== undefined) {
      document.getElementById('bar').style.width = pct + '%';
    }
  }
</script>
</body>
</html>
"""


class SplashScreen:
    """
    Opens a small pywebview window as a splash screen.
    set_status(msg, progress) can be called from any thread.
    close() destroys the window.
    """

    def __init__(self):
        import webview
        self._webview = webview
        self._window  = None
        self._ready   = threading.Event()

    def _screen_center(self, w, h):
        """Return (x, y) to center a window of size w×h on the primary screen."""
        try:
            import ctypes
            user32 = ctypes.windll.user32
            sw = user32.GetSystemMetrics(0)
            sh = user32.GetSystemMetrics(1)
            return (sw - w) // 2, (sh - h) // 2
        except Exception:
            return None, None

    def _open_window(self):
        W, H = 520, 280
        x, y = self._screen_center(W, H)
        kwargs = dict(
            title     = 'Evony Gear Optimizer',
            html      = SPLASH_HTML,
            width     = W,
            height    = H,
            resizable = False,
            on_top    = True,
            frameless = False,
            min_size  = (W, H),
        )
        if x is not None:
            kwargs['x'] = x
            kwargs['y'] = y
        self._window = self._webview.create_window(**kwargs)
        self._webview.start(self._on_shown)

    def _on_shown(self):
        self._ready.set()

    def set_status(self, message, progress=None):
        """Update the status line and progress bar (0-100)."""
        if self._window is None:
            return
        try:
            pct = progress if progress is not None else ''
            if pct != '':
                self._window.evaluate_js(
                    f"setStatus({repr(message)}, {pct})"
                )
            else:
                self._window.evaluate_js(
                    f"setStatus({repr(message)})"
                )
        except Exception:
            pass

    def close(self):
        """Close the splash window."""
        try:
            if self._window:
                self._window.destroy()
        except Exception:
            pass

    def _run_target(self, fn):
        # Wait until the webview is fully shown before sending JS calls
        self._ready.wait(timeout=5)
        time.sleep(0.2)
        fn(self)
