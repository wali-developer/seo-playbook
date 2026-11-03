import type { Metadata } from 'next';
import dynamic from 'next/dynamic';
import { notFound } from 'next/navigation';
import { getTool, tools } from '@/config/tools';
import { FaqAccordion } from '@/components/FaqAccordion';
import { SoftwareJsonLd } from '@/components/JsonLd';

const ToolClient = dynamic(() => import('@/components/ToolClient'), { ssr: false });

export async function generateStaticParams() {
  return tools.map((t) => ({ slug: t.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const tool = getTool(slug);
  if (!tool) return { title: 'Tool not found' };
  return { title: tool.name, description: tool.description };
}

export default async function ToolPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const tool = await getTool(slug);
  if (!tool) notFound();

  return (
    <>
      <SoftwareJsonLd name={tool.name} description={tool.description} slug={tool.slug} />
      <ToolClient slug={tool.slug} />
      <section>
        <h3>Frequently asked questions</h3>
        <FaqAccordion faqs={tool.faqs} />
      </section>
    </>
  );
}
