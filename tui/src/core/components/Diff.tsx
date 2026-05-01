// Unified-diff renderer matching CC's Update/Write tool diff colors. Parses
// @@ hunk headers for line numbers; colors `+` lines green/dark-green-bg,
// `-` lines red/dark-red-bg, context lines off-white no-bg. Code content
// inside lines is syntax-highlighted via cli-highlight with a Monokai-ish
// theme tuned to match CC's palette.

import React from 'react';
import { Box, Text } from 'ink';
import chalk from 'chalk';
import { highlight, type Theme } from 'cli-highlight';

const ADD_BG = '#022800';
const ADD_FG = '#50c850';
const DEL_BG = '#3d0100';
const DEL_FG = '#dc5a5a';
const CTX_FG = '#f8f8f2';
const NUM_FG = '#696969';
const HUNK_FG = '#66d9ef';
const META_FG = '#999999';

// Monokai-ish theme — close to CC's palette (pink keywords, yellow strings,
// green types, dim olive comments). Uses chalk truecolor for richer output
// than cli-highlight's 4-bit defaults.
const SYNTAX_THEME: Theme = {
  keyword: chalk.hex('#f92672'),
  built_in: chalk.hex('#66d9ef'),
  type: chalk.hex('#a6e22e'),
  literal: chalk.hex('#ae81ff'),
  number: chalk.hex('#ae81ff'),
  string: chalk.hex('#e6db74'),
  comment: chalk.hex('#75715e'),
  doctag: chalk.hex('#75715e'),
  function: chalk.hex('#a6e22e'),
  title: chalk.hex('#a6e22e'),
  class: chalk.hex('#a6e22e'),
  params: chalk.hex('#fd971f'),
  attr: chalk.hex('#a6e22e'),
  symbol: chalk.hex('#ae81ff'),
  meta: chalk.hex('#75715e'),
  regexp: chalk.hex('#e6db74'),
};

const EXT_TO_LANG: Record<string, string> = {
  py: 'python', js: 'javascript', mjs: 'javascript', cjs: 'javascript',
  ts: 'typescript', tsx: 'typescript', jsx: 'javascript',
  go: 'go', rs: 'rust', rb: 'ruby', java: 'java', kt: 'kotlin',
  swift: 'swift', c: 'c', h: 'c', cc: 'cpp', cpp: 'cpp', hpp: 'cpp',
  cs: 'csharp', php: 'php', sh: 'bash', bash: 'bash', zsh: 'bash',
  sql: 'sql', html: 'html', xml: 'xml', css: 'css', scss: 'scss',
  json: 'json', yaml: 'yaml', yml: 'yaml', md: 'markdown', toml: 'ini',
};

export function detectLang(rawDiff: string): string | undefined {
  const m = rawDiff.match(/^(?:\+\+\+|---) (?:[ab]\/)?(\S+)/m);
  if (!m || !m[1]) return undefined;
  const ext = m[1].split('.').pop()?.toLowerCase();
  return ext ? EXT_TO_LANG[ext] : undefined;
}

function highlightCode(code: string, lang: string | undefined): string {
  if (!code || !lang) return code;
  try {
    return highlight(code, {
      language: lang,
      ignoreIllegals: true,
      theme: SYNTAX_THEME,
    });
  } catch {
    return code;
  }
}

export type Line = {
  kind: 'add' | 'del' | 'ctx' | 'hunk' | 'meta';
  num: number | null;
  text: string;
};

export function parse(raw: string): Line[] {
  const hunkRe = /^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@/;
  let oldLine: number | null = null;
  let newLine: number | null = null;
  const out: Line[] = [];

  for (const line of raw.split('\n')) {
    const hm = line.match(hunkRe);
    if (hm) {
      oldLine = parseInt(hm[1]!, 10);
      newLine = parseInt(hm[2]!, 10);
      out.push({ kind: 'hunk', num: null, text: line });
      continue;
    }
    if (line.startsWith('+++') || line.startsWith('---')) {
      out.push({ kind: 'meta', num: null, text: line });
      continue;
    }
    if (line.startsWith('+')) {
      out.push({ kind: 'add', num: newLine, text: line.slice(1) });
      if (newLine !== null) newLine += 1;
      continue;
    }
    if (line.startsWith('-')) {
      out.push({ kind: 'del', num: oldLine, text: line.slice(1) });
      if (oldLine !== null) oldLine += 1;
      continue;
    }
    const payload = line.startsWith(' ') ? line.slice(1) : line;
    out.push({ kind: 'ctx', num: newLine, text: payload });
    if (newLine !== null) newLine += 1;
    if (oldLine !== null) oldLine += 1;
  }
  return out;
}

function fmtNum(n: number | null): string {
  if (n === null) return '   ';
  return String(n).padStart(3, ' ');
}

export function Diff({
  raw,
  showFileHeader = true,
}: {
  raw: string;
  showFileHeader?: boolean;
}) {
  const lines = parse(raw);
  const lang = detectLang(raw);
  const visible = lines.filter((l) => showFileHeader || l.kind !== 'meta');
  return (
    <Box flexDirection="column">
      {visible.map((l, i) => {
        if (l.kind === 'hunk') {
          return (
            <Text key={i} color={HUNK_FG}>
              {l.text}
            </Text>
          );
        }
        if (l.kind === 'meta') {
          return (
            <Text key={i} color={META_FG}>
              {l.text}
            </Text>
          );
        }
        if (l.kind === 'add') {
          const code = highlightCode(l.text, lang);
          return (
            <Text key={i} backgroundColor={ADD_BG}>
              <Text color={NUM_FG}>{fmtNum(l.num)} </Text>
              <Text color={ADD_FG}>+ </Text>
              <Text>{code}</Text>
            </Text>
          );
        }
        if (l.kind === 'del') {
          const code = highlightCode(l.text, lang);
          return (
            <Text key={i} backgroundColor={DEL_BG}>
              <Text color={NUM_FG}>{fmtNum(l.num)} </Text>
              <Text color={DEL_FG}>- </Text>
              <Text>{code}</Text>
            </Text>
          );
        }
        const code = highlightCode(l.text, lang);
        return (
          <Text key={i}>
            <Text color={NUM_FG}>{fmtNum(l.num)} </Text>
            <Text color={CTX_FG}>  {code}</Text>
          </Text>
        );
      })}
    </Box>
  );
}


/** Synthesize and render a unified diff from old_string → new_string. */
export function EditDiff({
  filePath,
  oldString,
  newString,
}: {
  filePath: string;
  oldString: string;
  newString: string;
}) {
  const oldLines = oldString.split('\n');
  const newLines = newString.split('\n');
  const oldCount = oldLines.length;
  const newCount = newLines.length;
  const synthetic =
    `+++ ${filePath}\n` +
    `@@ -1,${oldCount} +1,${newCount} @@\n` +
    oldLines.map((l) => `-${l}`).join('\n') +
    (oldLines.length > 0 ? '\n' : '') +
    newLines.map((l) => `+${l}`).join('\n');
  return <Diff raw={synthetic} showFileHeader={false} />;
}


/** Same idea for Write — all `+` lines, no removal. */
export function WriteDiff({
  filePath,
  content,
}: {
  filePath: string;
  content: string;
}) {
  const lines = content.split('\n');
  const synthetic =
    `+++ ${filePath}\n` +
    `@@ -0,0 +1,${lines.length} @@\n` +
    lines.map((l) => `+${l}`).join('\n');
  return <Diff raw={synthetic} showFileHeader={false} />;
}
