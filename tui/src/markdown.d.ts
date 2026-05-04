// Lets us `import text from './foo.md' with { type: 'text' }`. Bun supports
// the runtime import attribute; this declaration just teaches `tsc --noEmit`
// what the module resolves to.
declare module '*.md' {
  const content: string;
  export default content;
}
