// DTMF (Dual-Tone Multi-Frequency) tone generator for telephone keypad
// Each key produces two simultaneous frequencies

const DTMF_FREQUENCIES: Record<string, [number, number]> = {
  '1': [697, 1209],
  '2': [697, 1336],
  '3': [697, 1477],
  '4': [770, 1209],
  '5': [770, 1336],
  '6': [770, 1477],
  '7': [852, 1209],
  '8': [852, 1336],
  '9': [852, 1477],
  '*': [941, 1209],
  '0': [941, 1336],
  '#': [941, 1477]
};

/**
 * Plays a DTMF tone for the specified key
 * @param key - The telephone key ('0'-'9', '*', '#')
 * @param duration - Duration of the tone in milliseconds (default: 200ms)
 */
export function playDialTone(key: string, duration = 200): void {
  const frequencies = DTMF_FREQUENCIES[key];
  if (!frequencies) {
    console.warn(`No DTMF frequency defined for key: ${key}`);
    return;
  }

  const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
  const [lowFreq, highFreq] = frequencies;

  // Create two oscillators for the dual-tone
  const osc1 = audioContext.createOscillator();
  const osc2 = audioContext.createOscillator();

  // Create gain node for volume control
  const gainNode = audioContext.createGain();
  gainNode.gain.value = 0.2; // Softer volume (20% of max)

  // Set frequencies
  osc1.frequency.value = lowFreq;
  osc2.frequency.value = highFreq;

  // Connect oscillators -> gain -> output
  osc1.connect(gainNode);
  osc2.connect(gainNode);
  gainNode.connect(audioContext.destination);

  // Play the tones
  osc1.start();
  osc2.start();

  // Stop after duration
  setTimeout(() => {
    osc1.stop();
    osc2.stop();
    audioContext.close();
  }, duration);
}
