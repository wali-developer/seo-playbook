'use client';
import { useState } from 'react';

export function FaqAccordion({ faqs }: { faqs: { q: string; a: string }[] }) {
  const [open, setOpen] = useState<number | null>(null);
  return (
    <div>
      {faqs.map((f, i) => (
        <div key={f.q}>
          <button onClick={() => setOpen(open === i ? null : i)}>{f.q}</button>
          {open === i && <p>{f.a}</p>}
        </div>
      ))}
    </div>
  );
}
