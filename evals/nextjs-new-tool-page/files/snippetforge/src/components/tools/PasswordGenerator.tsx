'use client';
import { useState } from 'react';

const SETS = {
  lower: 'abcdefghijklmnopqrstuvwxyz',
  upper: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  digits: '0123456789',
  symbols: '!@#$%^&*()-_=+[]{};:,.?',
};

export function PasswordGenerator() {
  const [length, setLength] = useState(16);
  const [opts, setOpts] = useState({ lower: true, upper: true, digits: true, symbols: true });
  const [password, setPassword] = useState('');

  function generate() {
    const chars = Object.entries(opts).filter(([, on]) => on).map(([k]) => SETS[k as keyof typeof SETS]).join('');
    const values = crypto.getRandomValues(new Uint32Array(length));
    setPassword(Array.from(values, (v) => chars[v % chars.length]).join(''));
  }

  return (
    <div>
      <label>Length <input type="number" min={8} max={128} value={length} onChange={(e) => setLength(+e.target.value)} /></label>
      {Object.keys(opts).map((k) => (
        <label key={k}>
          <input type="checkbox" checked={opts[k as keyof typeof opts]} onChange={() => setOpts({ ...opts, [k]: !opts[k as keyof typeof opts] })} /> {k}
        </label>
      ))}
      <button onClick={generate}>Generate password</button>
      <output>{password}</output>
    </div>
  );
}
