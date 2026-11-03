import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  metadataBase: new URL('https://snippetforge.example'),
  title: { default: 'SnippetForge — Free Developer Tools', template: '%s | SnippetForge' },
  description: 'Free online developer tools: JSON formatter, Base64 encoder, UUID generator and more.',
  alternates: { canonical: 'https://snippetforge.example' },
  robots: { index: true, follow: true },
  openGraph: { siteName: 'SnippetForge', images: ['/og.png'] },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header><a href="/">SnippetForge</a> <a href="/tools">Tools</a></header>
        <main>{children}</main>
      </body>
    </html>
  );
}
