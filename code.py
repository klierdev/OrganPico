import wifi
import socketpool
import usb_midi
from adafruit_httpserver import Server, Request, Response
from adafruit_midi import MIDI
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

# ========== MIDI SETUP ==========
print("Available MIDI ports:", usb_midi.ports)
midi = MIDI(midi_out=usb_midi.ports[1])  # Use output port

# ========== WIFI AP SETUP ==========
AP_SSID = "OrganCtrl"
AP_PASSWORD = "organ1234"
wifi.radio.start_ap(AP_SSID, AP_PASSWORD)
ap_ip = "192.168.4.1"
print(f"\nAccess Point '{AP_SSID}'")
print(f"IP: {ap_ip}\n")

# ========== WEB SERVER ==========
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=False)

# ========== HTML/CSS ==========
HTML = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Organ Controller</title>
    <style>
        * {
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            -khtml-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            touch-action: manipulation;
        }
        body {
            background: #1a1a1a;
            color: #fff;
            font-family: Arial, sans-serif;
            padding: 20px;
            margin: 0;
            overflow: hidden;
        }
        h1 {
            color: #3498db;
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        .btn-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            padding: 0 10px;
        }
        .btn {
            padding: 20px;
            border: none;
            border-radius: 8px;
            background: #3498db;
            color: white;
            font-size: 1.1em;
            cursor: pointer;
            transition: filter 0.1s;
            min-height: 80px;
        }
        .btn:active {
            filter: brightness(80%);
            transition: filter 0s;
        }
        .pedal-btn {
            background: #e74c3c;
            grid-column: span 2;
            min-height: 100px;
        }
    </style>
</head>
<body>
    <h1>Organ Controller</h1>
    <div class="btn-grid">
        <button class="btn" data-note="60">C4 (60)</button>
        <button class="btn" data-note="62">D4 (62)</button>
        <button class="btn" data-note="64">E4 (64)</button>
        <button class="btn" data-note="65">F4 (65)</button>
        <button class="btn" data-note="67">G4 (67)</button>
        <button class="btn" data-note="69">A4 (69)</button>
        <button class="btn" data-note="71">B4 (71)</button>
        <button class="btn" data-note="72">C5 (72)</button>
        <button class="btn pedal-btn" data-note="36">Pedal C2 (36)</button>
    </div>
    <script>
        let isTouchDevice = 'ontouchstart' in window;
        let activeNotes = new Set();
        
        function handleNote(note, isOn) {
            if (isOn ? activeNotes.has(note) : !activeNotes.has(note)) return;
            
            fetch(isOn ? `/note-on/${note}` : `/note-off/${note}`)
                .catch(e => console.error('Error:', e));
            
            if (isOn) activeNotes.add(note);
            else activeNotes.delete(note);
        }
        
        function setupButton(button) {
            const note = parseInt(button.dataset.note);
            
            if (isTouchDevice) {
                button.ontouchstart = () => handleNote(note, true);
                button.ontouchend = () => handleNote(note, false);
            } else {
                button.onmousedown = () => handleNote(note, true);
                button.onmouseup = () => handleNote(note, false);
            }
        }
        
        // Setup all buttons
        document.querySelectorAll('.btn').forEach(setupButton);
        
        // Prevent context menu and touch scrolling
        document.addEventListener('contextmenu', e => e.preventDefault());
        document.body.addEventListener('touchmove', e => e.preventDefault(), { passive: false });
    </script>
</body>
</html>
"""
# ========== ROUTES ==========
@server.route("/")
def base(request: Request):
    return Response(request, body=HTML, content_type="text/html")

@server.route("/note-on/<note>")
def note_on(request: Request, note: str):
    try:
        midi.send(NoteOn(int(note), velocity=127))
        print(f"Note ON: {note}")
    except Exception as e:
        print(f"MIDI Error: {e}")
    return Response(request, body="", content_type="text/plain")

@server.route("/note-off/<note>")
def note_off(request: Request, note: str):
    try:
        midi.send(NoteOff(int(note), velocity=0))
        print(f"Note OFF: {note}")
    except Exception as e:
        print(f"MIDI Error: {e}")
    return Response(request, body="", content_type="text/plain")

# ========== CAPTIVE PORTAL ==========
CAPTIVE_PATHS = [
    "/generate_204",
    "/hotspot-detect.html",
    "/library/test/success.html",
    "/ncsi.txt",
    "/connecttest.txt"
]

for path in CAPTIVE_PATHS:
    @server.route(path)
    def redirect(request: Request):
        return Response(request, body="", status=302, headers={"Location": "http://" + ap_ip})

# ========== START SERVER ==========
server.start(port=80)
print("\nServer running!")
print("Connect to WiFi:", AP_SSID)
print("Visit http://192.168.4.1\n")

# ========== MAIN LOOP ==========
while True:
    try:
        server.poll()
    except Exception as e:
        print("Server error:", str(e))
        continue
