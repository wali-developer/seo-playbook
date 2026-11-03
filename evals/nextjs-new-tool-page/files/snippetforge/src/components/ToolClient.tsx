'use client';
import { motion } from 'framer-motion';
import { getTool } from '@/config/tools';
import { JsonFormatter } from './tools/JsonFormatter';
import { Base64Tool } from './tools/Base64Tool';
import { UuidGenerator } from './tools/UuidGenerator';

export default function ToolClient({ slug }: { slug: string }) {
  const tool = getTool(slug)!;
  return (
    <div>
      <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        {tool.name}
      </motion.h1>
      <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{tool.description}</motion.p>
      {slug === 'json-formatter' && <JsonFormatter />}
      {slug === 'base64' && <Base64Tool />}
      {slug === 'uuid-generator' && <UuidGenerator />}
    </div>
  );
}
