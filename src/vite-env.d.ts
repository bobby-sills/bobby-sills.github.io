/// <reference types="svelte" />
/// <reference types="vite/client" />

declare module '*.md' {
  const attributes: {
    title?: string;
    date?: string;
    tags?: string[];
    image?: string;
  };
  const html: string;
  export { attributes, html };
}
