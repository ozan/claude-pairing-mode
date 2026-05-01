// Entry point. We deliberately DON'T enter the alt-screen buffer — that would
// break terminal scrollback. Content flows into the terminal's regular
// buffer; <Static> writes committed entries permanently into scrollback,
// and the live region + input are re-rendered at the bottom. Mouse wheel /
// page up scroll naturally.

import React from 'react';
import { render } from 'ink';
import { PairApp } from './pair/PairApp.js';

render(<PairApp />, { exitOnCtrlC: true });
