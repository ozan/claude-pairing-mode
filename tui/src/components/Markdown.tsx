// Minimal markdown renderer for our use case. Handles:
//   - inline `code` → light blue (color 153)
//   - **bold** / *italic*  (kept simple; nested cases skipped)
//   - fenced ```diff blocks → DiffBlock
// Other markdown features (headings, lists) are passed through as plain text.

import React from 'react';
import { Box, Text } from 'ink';
import { Diff } from './Diff.js';

const INLINE_CODE = '#afd7ff'; // 153

type Segment =
  | { kind: 'text'; value: string }
  | { kind: 'code'; value: string }
  | { kind: 'bold'; value: string }
  | { kind: 'em'; value: string };

// Split a single line (or paragraph) into inline segments.
//
// Critical invariant: every iteration must advance `i` by at least 1, even
// when we encounter an unclosed special character. (A streamed `\`code` may
// arrive with the closing backtick still in flight; if we don't advance, the
// loop hangs forever and locks up the entire UI.)
function splitInline(input: string): Segment[] {
  const out: Segment[] = [];
  let i = 0;
  while (i < input.length) {
    const c = input[i];
    if (c === '`') {
      const end = input.indexOf('`', i + 1);
      if (end > 0) {
        out.push({ kind: 'code', value: input.slice(i + 1, end) });
        i = end + 1;
        continue;
      }
      // Unclosed — emit the rest as plain text and stop.
      out.push({ kind: 'text', value: input.slice(i) });
      break;
    }
    if (c === '*' && input[i + 1] === '*') {
      const end = input.indexOf('**', i + 2);
      if (end > 0) {
        out.push({ kind: 'bold', value: input.slice(i + 2, end) });
        i = end + 2;
        continue;
      }
      out.push({ kind: 'text', value: input.slice(i) });
      break;
    }
    if (c === '*') {
      const end = input.indexOf('*', i + 1);
      if (end > 0) {
        out.push({ kind: 'em', value: input.slice(i + 1, end) });
        i = end + 1;
        continue;
      }
      out.push({ kind: 'text', value: input.slice(i) });
      break;
    }
    // Plain text run — extend until next special char.
    let j = i + 1;
    while (
      j < input.length &&
      input[j] !== '`' &&
      !(input[j] === '*' && input[j + 1] === '*') &&
      input[j] !== '*'
    ) {
      j += 1;
    }
    out.push({ kind: 'text', value: input.slice(i, j) });
    i = j;
  }
  return out;
}

function InlineLine({ line }: { line: string }) {
  const segs = splitInline(line);
  return (
    <Text>
      {segs.map((s, i) => {
        if (s.kind === 'code') return <Text key={i} color={INLINE_CODE}>{s.value}</Text>;
        if (s.kind === 'bold') return <Text key={i} bold>{s.value}</Text>;
        if (s.kind === 'em') return <Text key={i} italic>{s.value}</Text>;
        return <Text key={i}>{s.value}</Text>;
      })}
    </Text>
  );
}

// Split source into prose blocks and fenced blocks.
type Block =
  | { kind: 'prose'; text: string }
  | { kind: 'fence'; lang: string; body: string };

function splitBlocks(src: string): Block[] {
  const out: Block[] = [];
  const lines = src.split('\n');
  let i = 0;
  let buf: string[] = [];
  const flushProse = () => {
    if (buf.length) {
      out.push({ kind: 'prose', text: buf.join('\n') });
      buf = [];
    }
  };
  while (i < lines.length) {
    const line = lines[i];
    const m = line.match(/^([ \t]*)(```|~~~)(\S*)\s*$/);
    if (m) {
      flushProse();
      const fence = m[2];
      const lang = m[3] ?? '';
      const bodyLines: string[] = [];
      i += 1;
      while (i < lines.length) {
        if (new RegExp(`^[ \\t]*${fence}\\s*$`).test(lines[i])) {
          i += 1;
          break;
        }
        bodyLines.push(lines[i]);
        i += 1;
      }
      out.push({ kind: 'fence', lang, body: bodyLines.join('\n') });
      continue;
    }
    buf.push(line);
    i += 1;
  }
  flushProse();
  return out;
}

function isDiffBlock(lang: string, body: string): boolean {
  if (lang.toLowerCase() === 'diff') return true;
  if (/^@@[^\n]*@@/m.test(body)) return true;
  if (/^(?:\+\+\+|---)\s/m.test(body)) return true;
  return false;
}

export function Markdown({ src }: { src: string }) {
  const blocks = splitBlocks(src);
  return (
    <Box flexDirection="column">
      {blocks.map((b, i) => {
        if (b.kind === 'fence' && isDiffBlock(b.lang, b.body)) {
          return <Diff key={i} raw={b.body} />;
        }
        if (b.kind === 'fence') {
          // Plain fenced code block: render as-is, no syntax highlight.
          return (
            <Box key={i} flexDirection="column">
              {b.body.split('\n').map((line, j) => (
                <Text key={j} color={INLINE_CODE}>
                  {line}
                </Text>
              ))}
            </Box>
          );
        }
        return (
          <Box key={i} flexDirection="column">
            {b.text.split('\n').map((line, j) => (
              <InlineLine key={j} line={line} />
            ))}
          </Box>
        );
      })}
    </Box>
  );
}
