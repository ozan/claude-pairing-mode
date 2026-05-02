// Entry point. We deliberately DON'T enter the alt-screen buffer — that would
// break terminal scrollback. Content flows into the terminal's regular
// buffer; <Static> writes committed entries permanently into scrollback,
// and the live region + input are re-rendered at the bottom. Mouse wheel /
// page up scroll naturally.
//
// Pre-Ink we print a small banner directly to stdout so it's committed
// permanently into scrollback (not part of the Ink render tree, so it never
// re-renders). The input lands right below the banner on launch and
// progressively moves down as committed entries accumulate above it —
// matching CC's behaviour, where the input is pushed toward the bottom of
// the viewport organically rather than pinned there from the start.

import React from 'react';
import { render } from 'ink';
import { PairApp } from './pair/PairApp.js';

const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';
const RESET = '\x1b[0m';

const banner = [
  `${BOLD}Claude Code "pairing mode" prototype${RESET}`,
  '',
  `${DIM}Try something like:${RESET}`,
  `${DIM}  • "let's write a tic tac toe implementation"${RESET}`,
  `${DIM}  • "let's solve the leetcode staircase problem"${RESET}`,
  '',
].join('\n');

process.stdout.write(banner + '\n');

render(<PairApp />, { exitOnCtrlC: true });
