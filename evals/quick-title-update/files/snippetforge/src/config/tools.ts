export interface Tool {
  slug: string;
  name: string;
  description: string;
  faqs: { q: string; a: string }[];
}

export const tools: Tool[] = [
  {
    slug: 'json-formatter',
    name: 'JSON Formatter',
    description: 'Format, validate and minify JSON online.',
    faqs: [
      { q: 'Is my JSON uploaded?', a: 'No. Formatting happens in your browser.' },
      { q: 'Can it fix invalid JSON?', a: 'It shows the line and column of the first error so you can fix it.' },
    ],
  },
  {
    slug: 'base64',
    name: 'Base64 Encoder',
    description: 'Encode and decode Base64 strings.',
    faqs: [{ q: 'Does it support Unicode?', a: 'Yes, text is encoded as UTF-8 first.' }],
  },
  {
    slug: 'uuid-generator',
    name: 'UUID Generator',
    description: 'Generate random v4 UUIDs.',
    faqs: [{ q: 'Are the UUIDs unique?', a: 'v4 UUIDs have 122 random bits, so collisions are practically impossible.' }],
  },
];

export function getTool(slug: string) {
  return tools.find((t) => t.slug === slug);
}
