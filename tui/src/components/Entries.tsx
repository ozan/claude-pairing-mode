// One component per entry kind in the transcript. Each renders a single
// "block" in the conversation: user line, assistant prose, tool pill +
// result, options, step footer, error.

import React, { memo, useEffect, useState } from 'react';
import { Box, Text } from 'ink';
import { Markdown } from './Markdown.js';
import { EditDiff, WriteDiff } from './Diff.js';

const COLOR_GREY = '#949494';      // 246
const COLOR_USER = '#c0c5cc';       // soft white
const COLOR_INLINE_CODE = '#afd7ff'; // 153
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
  // ⏺ marker on the first line; subsequent lines indent 2 cols (Ink's flexbox
  // layout with marginLeft on the body achieves this naturally).
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

function summarizeInput(input: unknown): string {
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

function shortToolName(name: string): string {
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

function buildResultSummary(name: string, text: string, isError: boolean) {
  if (isError) {
    const first = (text || 'Error').split('\n')[0].trim();
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
  if (short === 'Edit') return <Text color={COLOR_GREY}>Applied edit</Text>;
  if (short === 'Bash') {
    if (!lines.length) return <Text color={COLOR_GREY}>(no output)</Text>;
    if (lines.length === 1) {
      const t = lines[0];
      return (
        <Text color={COLOR_GREY}>{t.length <= 80 ? t : t.slice(0, 80) + '…'}</Text>
      );
    }
    return <NumText pre="" n={lines.length} suf=" lines" />;
  }
  if (short === 'Glob' || short === 'Grep') {
    return <NumText pre="" n={lines.length} suf={` match${lines.length === 1 ? '' : 'es'}`} />;
  }
  if (!lines.length) return <Text color={COLOR_GREY}>ok</Text>;
  return <NumText pre="" n={lines.length} suf=" lines" />;
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
  // diff inline. Header is `● Update(filepath)`, then `  └ Added N lines,
  // removed M line(s)` summary, then the diff.
  if (short === 'Update' && input && typeof input === 'object') {
    const obj = input as Record<string, unknown>;
    const filePath = typeof obj.file_path === 'string' ? obj.file_path : '';
    const oldString = typeof obj.old_string === 'string' ? obj.old_string : '';
    const newString = typeof obj.new_string === 'string' ? obj.new_string : '';
    if (filePath && (oldString || newString)) {
      const removed = oldString ? oldString.split('\n').length : 0;
      const added = newString ? newString.split('\n').length : 0;
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

  // Write: render the new file content as an all-`+` diff.
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

  return (
    <Box>
      <Text>  </Text>
      {buildResultSummary(name, text, isError)}
    </Box>
  );
});

export const OptionsBlock = memo(function OptionsBlock({
  options,
}: {
  options: { title: string; body: string }[];
}) {
  return (
    <Box flexDirection="row" marginTop={1} columnGap={2}>
      {options.map((opt, i) => {
        const letter = String.fromCharCode(65 + i);
        return (
          <Box key={i} flexDirection="column" flexBasis="50%" flexGrow={1}>
            <Text bold>{letter}.  {opt.title}</Text>
            <Box height={1} />
            <Box marginLeft={4} flexDirection="column">
              <Markdown src={opt.body} />
            </Box>
          </Box>
        );
      })}
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
