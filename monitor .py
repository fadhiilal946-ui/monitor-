import requests
from IPython.display import HTML, display

html_code = """
<div style="background-color: black; padding: 20px; border-radius: 10px; text-align: center; font-family: Arial, sans-serif; width: 100%; max-width: 700px; margin: auto;">
    <h3 style="color: white; margin-bottom: 5px;">MONITOR ELEKTROMEDIK: FETAL HEART RATE</h3>
    <div style="color: #00FF00; font-size: 48px; font-weight: bold; margin-bottom: 10px;" id="bpm-display">140 <span style="font-size: 18px; color: white;">BPM</span></div>
    <canvas id="medicalCanvas" width="650" height="250" style="border: 1px solid #222; background-color: #000;"></canvas>
    <div style="margin-top: 15px;">
        <button id="btnStart" style="padding: 10px 20px; background-color: #00FF00; color: black; border: none; font-weight: bold; cursor: pointer; border-radius: 5px;">MULAI MONITOR</button>
        <button id="btnStop" style="padding: 10px 20px; background-color: red; color: white; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; margin-left: 10px;">STOP</button>
    </div>
</div>
<script>
const canvas = document.getElementById('medicalCanvas'); const ctx = canvas.getContext('2d'); const bpmDisplay = document.getElementById('bpm-display');
let animationId; let audioCtx = null; let points = new Array(canvas.width).fill(125); let running = false; let counter = 0;
function playBeep() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    let osc = audioCtx.createOscillator(); let gain = audioCtx.createGain();
    osc.type = 'sine'; osc.frequency.setValueAtTime(850, audioCtx.currentTime); gain.gain.setValueAtTime(0.06, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.00001, audioCtx.currentTime + 0.08); osc.connect(gain); gain.connect(audioCtx.destination);
    osc.start(); osc.stop(audioCtx.currentTime + 0.08);
}
function drawMonitor() {
    if (!running) return;
    ctx.fillStyle = 'black'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = '#111111'; ctx.lineWidth = 1;
    for(let i=0; i<canvas.width; i+=20) { ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke(); }
    for(let i=0; i<canvas.height; i+=20) { ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(canvas.width, i); ctx.stroke(); }
    counter++; let currentBPM = Math.round(140 + Math.sin(counter / 10) * 5 + (Math.random() - 0.5) * 3);
    let targetY = canvas.height - ((currentBPM - 90) * 3); points.shift(); points.push(targetY);
    ctx.strokeStyle = '#00FF00'; ctx.lineWidth = 2.5; ctx.shadowBlur = 8; ctx.shadowColor = '#00FF00'; ctx.beginPath();
    for(let i=0; i<points.length; i++) { if(i === 0) ctx.moveTo(i, points[i]); else ctx.lineTo(i, points[i]); }
    ctx.stroke(); ctx.shadowBlur = 0;
    if(counter % 5 === 0) { bpmDisplay.innerHTML = currentBPM + ' <span style="font-size: 18px; color: white;">BPM</span>'; }
    if(counter % 12 === 0) { playBeep(); }
    animationId = requestAnimationFrame(drawMonitor);
}
document.getElementById('btnStart').addEventListener('click', () => { if(!running) { running = true; drawMonitor(); } });
document.getElementById('btnStop').addEventListener('click', () => { running = false; cancelAnimationFrame(animationId); });
</script>
"""
display(HTML(html_code))
