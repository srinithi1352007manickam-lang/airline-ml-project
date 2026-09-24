/**
 * Srinithi - 3D Portfolio Web Audio Synthesizer
 * Procedural UI sound effects & ambient cyber-soundscape (Zero external files needed)
 */

(function () {
  'use strict';

  let audioCtx = null;
  let isSoundEnabled = false;
  let ambientOsc = null;
  let ambientGain = null;

  function getAudioContext() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        audioCtx = new AudioContext();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    return audioCtx;
  }

  function toggleSound() {
    isSoundEnabled = !isSoundEnabled;
    const btn = document.getElementById('sound-toggle-btn');
    if (btn) {
      btn.innerHTML = isSoundEnabled ? '🔊 Sound: ON' : '🔇 Sound: OFF';
      btn.style.color = isSoundEnabled ? 'var(--accent-cyan)' : 'var(--text-secondary)';
      btn.style.borderColor = isSoundEnabled ? 'var(--border-glass-bright)' : 'var(--border-glass)';
    }

    if (isSoundEnabled) {
      getAudioContext();
      playSuccess();
      startAmbientHum();
      if (window.Portfolio) window.Portfolio.showToast('Audio Feedback Enabled 🔊');
    } else {
      stopAmbientHum();
      if (window.Portfolio) window.Portfolio.showToast('Audio Feedback Muted 🔇');
    }

    return isSoundEnabled;
  }

  function playHover() {
    if (!isSoundEnabled) return;
    const ctx = getAudioContext();
    if (!ctx) return;

    try {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(420, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(840, ctx.currentTime + 0.08);

      gain.gain.setValueAtTime(0.03, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(ctx.currentTime + 0.08);
    } catch (e) {
      // Audio safety
    }
  }

  function playClick() {
    if (!isSoundEnabled) return;
    const ctx = getAudioContext();
    if (!ctx) return;

    try {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(600, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(240, ctx.currentTime + 0.1);

      gain.gain.setValueAtTime(0.08, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.1);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(ctx.currentTime + 0.1);
    } catch (e) {
      // Audio safety
    }
  }

  function playSuccess() {
    if (!isSoundEnabled) return;
    const ctx = getAudioContext();
    if (!ctx) return;

    try {
      const now = ctx.currentTime;
      const notes = [523.25, 659.25, 783.99, 1046.5]; // C5, E5, G5, C6

      notes.forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now + idx * 0.07);

        gain.gain.setValueAtTime(0.06, now + idx * 0.07);
        gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.07 + 0.2);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start(now + idx * 0.07);
        osc.stop(now + idx * 0.07 + 0.2);
      });
    } catch (e) {
      // Audio safety
    }
  }

  function startAmbientHum() {
    const ctx = getAudioContext();
    if (!ctx || ambientOsc) return;

    try {
      ambientOsc = ctx.createOscillator();
      ambientGain = ctx.createGain();

      ambientOsc.type = 'sine';
      ambientOsc.frequency.setValueAtTime(70, ctx.currentTime); // Deep soft cosmic hum

      ambientGain.gain.setValueAtTime(0.001, ctx.currentTime);
      ambientGain.gain.linearRampToValueAtTime(0.015, ctx.currentTime + 2);

      ambientOsc.connect(ambientGain);
      ambientGain.connect(ctx.destination);

      ambientOsc.start();
    } catch (e) {
      // Audio safety
    }
  }

  function stopAmbientHum() {
    if (ambientGain && audioCtx) {
      try {
        ambientGain.gain.linearRampToValueAtTime(0.0001, audioCtx.currentTime + 0.5);
        setTimeout(() => {
          if (ambientOsc) {
            ambientOsc.stop();
            ambientOsc.disconnect();
            ambientOsc = null;
          }
        }, 600);
      } catch (e) {
        ambientOsc = null;
      }
    }
  }

  window.AudioFx = {
    toggleSound,
    playHover,
    playClick,
    playSuccess,
    isEnabled: () => isSoundEnabled
  };
})();
