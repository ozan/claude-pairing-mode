// Two-column option panel. The single piece of UI that's specific to the
// pair-programmer experiment.

import React, { memo } from 'react';
import { Box, Text } from 'ink';
import { Markdown } from '../core/components/Markdown.js';

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
