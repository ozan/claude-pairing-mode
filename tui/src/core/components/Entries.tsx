// One component per generic entry kind in the transcript. Experiment-specific
// entries (like the 2-column options panel) live next to their experiment.

import React, { memo, useEffect, useState } from 'react';
import { Box, Text } from 'ink';
import { Markdown } from './Markdown.js';
import { EditDiff, WriteDiff, countAddRemove, lineDiff } from './Diff.js';

const COLOR_GREY = '#949494';      // 246
const COLOR_USER = '#c0c5cc';       // soft white
const COLOR_ERROR = '#ff8787';      // 211
const COLOR_TOOL_DONE = '#50c850';  // green ● for a successfully-completed tool


export const UserLine = memo(function UserLine({ text }: { text: string }) {
  return (
    <Box marginTop={1}>
      <Text color={COLOR_USER}>❯ {text}</Text>
    </Box>
  );
});


export const AssistantBlock = memo(function AssistantBlock({ text }: { text: string }) {
  return (
    <Box flexDirection="row" marginTop={1}>
      <Box width={2}>
        <Text>⏺</Text>
      </Box>
      <Box flexDirection="column" flexGrow={1}>
        <Markdown src={text} />
      </Box>
    </Box>
  );
});


export function summarizeInput(input: unknown): string {
  if (!input || typeof input !== 'object') return '';
  const obj = input as Record<string, unknown>;
  if (Object.keys(obj).length === 0) return '';
  for (const key of ['command', 'file_path', 'path', 'pattern', 'url', 'prompt', 'query']) {
    const v = obj[key];
    if (typeof v === 'string') {
      return v.length <= 80 ? v : v.slice(0, 80) + '…';
    }
  }
  // Don't render an opaque JSON dump in the pill — empty parens are nicer
  // than `({"some_param":...})` until the tool's input is recognized.
  return '';
}


export function shortToolName(name: string): string {
  if (!name) return 'tool';
  const raw = name.replace(/^mcp__/, '').split('__').pop() ?? name;
  // CC renames Edit → Update in its TUI. Match that.
  if (raw === 'Edit') return 'Update';
  return raw;
}


// Animated dots after the tool name to signal that it's still running.
function useRunningDots(): string {
  const [n, setN] = useState(1);
  useEffect(() => {
    const t = setInterval(() => setN((v) => (v % 3) + 1), 400);
    return () => clearInterval(t);
  }, []);
  return '.'.repeat(n) + ' '.repeat(3 - n);
}


export const ToolPillRunning = memo(function ToolPillRunning({ name, input }: { name: string; input: unknown }) {
  const short = shortToolName(name);
  const args = summarizeInput(input);
  const dots = useRunningDots();
  return (
    <Box flexDirection="column" marginTop={1}>
      <Box>
        <Text color={COLOR_GREY}>● </Text>
        <Text bold>{short}</Text>
        {args ? <Text>({args})</Text> : null}
        <Text color={COLOR_GREY}> {dots}</Text>
      </Box>
      {short === 'Bash' && typeof (input as { command?: string }).command === 'string' ? (
        <Box>
          <Text color={COLOR_GREY}>  └ $ {(input as { command: string }).command.slice(0, 100)}</Text>
        </Box>
      ) : null}
    </Box>
  );
});


// Tools whose output is generally short and worth showing inline, vs. tools
// where output is potentially huge and should stay collapsed.
const TOOLS_WITH_INLINE_OUTPUT = new Set(['Bash', 'Glob', 'Grep']);
const MAX_OUTPUT_LINES = 10;
const MAX_LINE_CHARS = 200;


export function buildResultSummary(name: string, text: string, isError: boolean) {
  if (isError) {
    const first = (text || 'Error').split('\n')[0]?.trim() ?? 'Error';
    return <Text color={COLOR_ERROR}>{first.slice(0, 200)}</Text>;
  }
  const lines = (text || '').split('\n').filter((l) => l.length > 0);
  const short = shortToolName(name);
  const NumText = ({ pre, n, suf }: { pre: string; n: number; suf: string }) => (
    <Text color={COLOR_GREY}>
      {pre}
      <Text bold color="white">{String(n)}</Text>
      {suf}
    </Text>
  );
  if (short === 'Read') {
    return <NumText pre="Read " n={lines.length} suf={` line${lines.length === 1 ? '' : 's'}`} />;
  }
  if (short === 'Write') return <Text color={COLOR_GREY}>Wrote file</Text>;
  if (short === 'Update') return <Text color={COLOR_GREY}>Applied edit</Text>;
  if (short === 'Bash' && !lines.length) {
    return <Text color={COLOR_GREY}>(no output)</Text>;
  }
  if (TOOLS_WITH_INLINE_OUTPUT.has(short) && lines.length === 1) {
    const t = lines[0]!;
    return (
      <Text color={COLOR_GREY}>
        {t.length <= MAX_LINE_CHARS ? t : t.slice(0, MAX_LINE_CHARS) + '…'}
      </Text>
    );
  }
  if (short === 'Glob' || short === 'Grep') {
    return <NumText pre="" n={lines.length} suf={` match${lines.length === 1 ? '' : 'es'}`} />;
  }
  if (short === 'Bash') {
    return <NumText pre="" n={lines.length} suf=" lines" />;
  }
  if (!lines.length) return <Text color={COLOR_GREY}>ok</Text>;
  return <NumText pre="" n={lines.length} suf=" lines" />;
}


/**
 * Renders the full multi-line output of a tool, indented with `└` on the
 * first line and 2-space continuation thereafter — matching CC. Truncates
 * to MAX_OUTPUT_LINES and adds a "… N more lines" footer if exceeded.
 * Each line itself is truncated to MAX_LINE_CHARS so a single huge line
 * (e.g. minified JSON) doesn't blow up the layout.
 */
function ToolOutputBlock({ text }: { text: string }) {
  const lines = (text || '').split('\n').filter((l) => l.length > 0);
  const visible = lines.slice(0, MAX_OUTPUT_LINES);
  const remaining = lines.length - visible.length;
  return (
    <Box flexDirection="column">
      {visible.map((line, i) => {
        const display =
          line.length <= MAX_LINE_CHARS ? line : line.slice(0, MAX_LINE_CHARS) + '…';
        return (
          <Box key={i}>
            <Text color={COLOR_GREY}>{i === 0 ? '  └ ' : '    '}</Text>
            <Text color={COLOR_GREY}>{display}</Text>
          </Box>
        );
      })}
      {remaining > 0 ? (
        <Box>
          <Text color={COLOR_GREY}>
            {'    … '}
            <Text bold color="white">{remaining}</Text>
            {` more line${remaining === 1 ? '' : 's'}`}
          </Text>
        </Box>
      ) : null}
    </Box>
  );
}


export const ToolResult = memo(function ToolResult({
  name,
  input,
  text,
  isError,
}: {
  name: string;
  input: unknown;
  text: string;
  isError: boolean;
}) {
  // On error, CC keeps a red `●` head + `  └ <reason>` line.
  if (isError) {
    const short = shortToolName(name);
    const args = summarizeInput(input);
    const first = (text || 'Error').split('\n')[0]?.trim() ?? 'Error';
    return (
      <Box flexDirection="column" marginTop={1}>
        <Box>
          <Text color={COLOR_ERROR}>● </Text>
          <Text bold>{short}</Text>
          {args ? <Text>({args})</Text> : null}
        </Box>
        <Box>
          <Text color={COLOR_ERROR}>  └ {first.slice(0, 200)}</Text>
        </Box>
      </Box>
    );
  }

  const short = shortToolName(name);

  // Update (the SDK calls it Edit; CC renames in its TUI): render the actual
  // diff inline.
  if (short === 'Update' && input && typeof input === 'object') {
    const obj = input as Record<string, unknown>;
    const filePath = typeof obj.file_path === 'string' ? obj.file_path : '';
    const oldString = typeof obj.old_string === 'string' ? obj.old_string : '';
    const newString = typeof obj.new_string === 'string' ? obj.new_string : '';
    if (filePath && (oldString || newString)) {
      const ops = lineDiff(oldString.split('\n'), newString.split('\n'));
      const { added, removed } = countAddRemove(ops);
      return (
        <Box flexDirection="column" marginTop={1}>
          <Box>
            <Text color={COLOR_TOOL_DONE}>● </Text>
            <Text bold>Update</Text>
            <Text>({filePath})</Text>
          </Box>
          <Box>
            <Text color={COLOR_GREY}>  └ </Text>
            <Text color={COLOR_GREY}>Added </Text>
            <Text bold>{added}</Text>
            <Text color={COLOR_GREY}>{added === 1 ? ' line' : ' lines'}</Text>
            {removed > 0 ? (
              <>
                <Text color={COLOR_GREY}>, removed </Text>
                <Text bold>{removed}</Text>
                <Text color={COLOR_GREY}>{removed === 1 ? ' line' : ' lines'}</Text>
              </>
            ) : null}
          </Box>
          <Box marginLeft={2}>
            <EditDiff filePath={filePath} oldString={oldString} newString={newString} />
          </Box>
        </Box>
      );
    }
  }

  // Write: render new file content as an all-`+` diff.
  if (short === 'Write' && input && typeof input === 'object') {
    const obj = input as Record<string, unknown>;
    const filePath = typeof obj.file_path === 'string' ? obj.file_path : '';
    const content = typeof obj.content === 'string' ? obj.content : '';
    if (filePath && content) {
      const lines = content.split('\n').length;
      return (
        <Box flexDirection="column" marginTop={1}>
          <Box>
            <Text color={COLOR_TOOL_DONE}>● </Text>
            <Text bold>Write</Text>
            <Text>({filePath})</Text>
          </Box>
          <Box>
            <Text color={COLOR_GREY}>  └ Wrote </Text>
            <Text bold>{lines}</Text>
            <Text color={COLOR_GREY}>{lines === 1 ? ' line' : ' lines'}</Text>
          </Box>
          <Box marginLeft={2}>
            <WriteDiff filePath={filePath} content={content} />
          </Box>
        </Box>
      );
    }
  }

  // All other tools (Glob, Read, Bash, Grep, …): show the `● Name(args)`
  // head. For tools whose output is generally short (Bash, Glob, Grep) we
  // show the actual lines; for everything else (Read in particular, where
  // file content can be huge) we show a one-line summary.
  const args = summarizeInput(input);
  const lines = (text || '').split('\n').filter((l) => l.length > 0);
  const showOutput =
    TOOLS_WITH_INLINE_OUTPUT.has(short) && lines.length > 1;
  return (
    <Box flexDirection="column" marginTop={1}>
      <Box>
        <Text color={COLOR_TOOL_DONE}>● </Text>
        <Text bold>{short}</Text>
        {args ? <Text>({args})</Text> : null}
      </Box>
      {showOutput ? (
        <ToolOutputBlock text={text} />
      ) : (
        <Box>
          <Text color={COLOR_GREY}>  └ </Text>
          {buildResultSummary(name, text, isError)}
        </Box>
      )}
    </Box>
  );
});


const FOOTER_VERBS = [
  'Cooked', 'Cogitated', 'Pondered', 'Brewed', 'Mulled', 'Reflected',
  'Crystallized', 'Reasoned', 'Galloped', 'Simmered', 'Percolated',
  'Marinated',
];

export const StepFooter = memo(function StepFooter({ elapsedSec }: { elapsedSec: number }) {
  const verb = FOOTER_VERBS[Math.floor(Math.random() * FOOTER_VERBS.length)];
  const secs = Math.max(1, Math.round(elapsedSec));
  return (
    <Box marginTop={1}>
      <Text color={COLOR_GREY}>✻ {verb} for {secs}s</Text>
    </Box>
  );
});


export const ErrorLine = memo(function ErrorLine({ message }: { message: string }) {
  return (
    <Box marginTop={1}>
      <Text color={COLOR_ERROR}>error: {message}</Text>
    </Box>
  );
});
