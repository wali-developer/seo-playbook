import type { MetadataRoute } from 'next';
import { tools } from '@/config/tools';

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: 'https://snippetforge.example', lastModified: new Date(), priority: 1 },
    { url: 'https://snippetforge.example/tools', lastModified: new Date(), priority: 0.9 },
    ...tools.map((t) => ({
      url: `https://snippetforge.example/tools/${t.slug}`,
      lastModified: new Date(),
      priority: 0.8,
    })),
  ];
}
