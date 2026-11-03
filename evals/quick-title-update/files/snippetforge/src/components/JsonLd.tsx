export function SoftwareJsonLd({ name, description, slug }: { name: string; description: string; slug: string }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name,
    description,
    url: `https://snippetforge.example/tools/${slug}`,
    applicationCategory: 'DeveloperApplication',
    operatingSystem: 'Any',
    offers: { '@type': 'Offer', price: '0', priceCurrency: 'USD' },
    aggregateRating: { '@type': 'AggregateRating', ratingValue: '4.9', ratingCount: '1287' },
  };
  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />;
}
