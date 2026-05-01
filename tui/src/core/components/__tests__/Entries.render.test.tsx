// Render-level tests for the entry components, using ink-testing-library.
// These exercise lastFrame() output to catch visible regressions: marker
// glyphs, summary phrasing, layout columns. They don't assert exact ANSI
// — that'd be brittle. Strip ANSI before comparing.

import React from 'react';
import { describe, expect, it } from 'bun:test';
import { render } from 'ink-testing-library';
import {
  AssistantBlock,
  ErrorLine,
  StepFooter,
  ToolPillRunning,
  ToolResult,
  UserLine,
} from '../Entries';

// Strip ANSI escape sequences for stable assertions on plain text content.
function stripAnsi(s: string | undefined): string {
  if (!s) return '';
  return s.replace(/\x1B\[[0-9;]*[A-Za-z]/g, '');
}


describe('UserLine', () => {
  it('renders `❯ <text>`', () => {
    const { lastFrame } = render(<UserLine text="hello" />);
    expect(stripAnsi(lastFrame())).toContain('❯ hello');
  });
});


describe('AssistantBlock', () => {
  it('shows the `⏺` marker and the prose', () => {
    const { lastFrame } = render(<AssistantBlock text="Hi there" />);
    const out = stripAnsi(lastFrame());
    expect(out).toContain('⏺');
    expect(out).toContain('Hi there');
  });

  it('renders inline code without the surrounding backticks', () => {
    const { lastFrame } = render(<AssistantBlock text="see `foo.py` next" />);
    const out = stripAnsi(lastFrame());
    expect(out).toContain('see ');
    expect(out).toContain('foo.py');
    expect(out).toContain(' next');
    // Backticks themselves should be consumed by the inline-code renderer.
    expect(out).not.toContain('`foo.py`');
  });
});


describe('ToolPillRunning', () => {
  it('shows `● <Name>(<args>)` with the tool name bold and args plain', () => {
    const { lastFrame } = render(
      <ToolPillRunning name="Bash" input={{ command: 'ls' }} />,
    );
    const out = stripAnsi(lastFrame());
    expect(out).toContain('● Bash');
    expect(out).toContain('(ls)');
  });

  it('renames Edit → Update', () => {
    const { lastFrame } = render(
      <ToolPillRunning name="Edit" input={{ file_path: 'foo.py' }} />,
    );
    expect(stripAnsi(lastFrame())).toContain('● Update');
  });

  it('omits parens for empty input (no `Bash({})` flicker)', () => {
    const { lastFrame } = render(<ToolPillRunning name="Bash" input={{}} />);
    const out = stripAnsi(lastFrame());
    expect(out).toContain('● Bash');
    expect(out).not.toContain('({})');
    expect(out).not.toContain('(');
  });

  it('shows the `└ $ <command>` detail line for Bash', () => {
    const { lastFrame } = render(
      <ToolPillRunning name="Bash" input={{ command: 'ls -la' }} />,
    );
    expect(stripAnsi(lastFrame())).toContain('└ $ ls -la');
  });
});


describe('ToolResult — non-Edit/Write', () => {
  it('collapses Read result to `Read N lines`', () => {
    const { lastFrame } = render(
      <ToolResult name="Read" input={{ file_path: 'a.py' }} text={'a\nb\nc'} isError={false} />,
    );
    const out = stripAnsi(lastFrame());
    expect(out).toContain('Read 3 lines');
  });

  it('collapses single-line Bash output to the line itself', () => {
    const { lastFrame } = render(
      <ToolResult name="Bash" input={{ command: 'echo hi' }} text="hi" isError={false} />,
    );
    expect(stripAnsi(lastFrame())).toContain('hi');
  });

  it('collapses empty Bash output to `(no output)`', () => {
    const { lastFrame } = render(
      <ToolResult name="Bash" input={{ command: 'true' }} text="" isError={false} />,
    );
    expect(stripAnsi(lastFrame())).toContain('(no output)');
  });

  it('on error, shows `● <Name>(<args>)` head + `└ <reason>`', () => {
    const { lastFrame } = render(
      <ToolResult
        name="Bash"
        input={{ command: 'ls /nope' }}
        text="ls: /nope: No such file"
        isError={true}
      />,
    );
    const out = stripAnsi(lastFrame());
    expect(out).toContain('● Bash');
    expect(out).toContain('(ls /nope)');
    expect(out).toContain('└ ls: /nope: No such file');
  });
});


describe('ToolResult — Update (Edit) inline diff', () => {
  it('renders `● Update(filepath)` head and a `└ Added N lines, removed M lines` summary', () => {
    const { lastFrame } = render(
      <ToolResult
        name="Edit"
        input={{ file_path: 'foo.py', old_string: 'a\nb', new_string: 'a\nb\nc' }}
        text=""
        isError={false}
      />,
    );
    const out = stripAnsi(lastFrame());
    expect(out).toContain('● Update');
    expect(out).toContain('(foo.py)');
    expect(out).toContain('Added');
    expect(out).toContain('removed');
  });
});


describe('ToolResult — Write inline diff', () => {
  it('renders `● Write(filepath)` head and a `└ Wrote N lines` summary', () => {
    const { lastFrame } = render(
      <ToolResult
        name="Write"
        input={{ file_path: 'foo.py', content: 'a\nb\nc' }}
        text=""
        isError={false}
      />,
    );
    const out = stripAnsi(lastFrame());
    expect(out).toContain('● Write');
    expect(out).toContain('(foo.py)');
    expect(out).toContain('Wrote');
  });
});


describe('StepFooter', () => {
  it('renders `✻ <verb> for Xs`', () => {
    const { lastFrame } = render(<StepFooter elapsedSec={3} />);
    const out = stripAnsi(lastFrame());
    expect(out).toContain('✻');
    expect(out).toMatch(/for 3s/);
  });

  it('rounds sub-second to 1s minimum', () => {
    const { lastFrame } = render(<StepFooter elapsedSec={0.4} />);
    expect(stripAnsi(lastFrame())).toMatch(/for 1s/);
  });
});


describe('ErrorLine', () => {
  it('renders `error: <message>`', () => {
    const { lastFrame } = render(<ErrorLine message="boom" />);
    expect(stripAnsi(lastFrame())).toContain('error: boom');
  });
});
