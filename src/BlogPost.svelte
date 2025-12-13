<script lang="ts">
  import Nav from "./lib/Nav.svelte";
  import { getPostBySlug, type Post } from "./lib/posts";
  import { link } from "svelte-spa-router";

  let { params } = $props<{ params?: { slug?: string } }>();

  let post = $derived<Post | undefined>(
    params?.slug ? getPostBySlug(params.slug) : undefined,
  );

  $effect(() => {
    if (post) {
      document.title = `${post.title} | bobby sills`;
    } else {
      document.title = "blog | bobby sills";
    }
  });

  function formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }
</script>

<main>
  <Nav />

  {#if !post}
    <h1>post not found</h1>
    <p>sorry, the post you're looking for doesn't exist.</p>
  {:else}
    <article class="blog-post">
      <header>
        <h1>{post.title}</h1>
        <time class="post-date">{formatDate(post.date)}</time>
      </header>

      <div class="post-content">
        {@html post.html}
      </div>
    </article>
  {/if}
</main>

<style>
  .blog-post header {
    margin-bottom: 2rem;
  }

  .post-date {
    display: block;
    color: var(--fg2);
    font-size: 0.9rem;
  }

  .post-content {
    line-height: 1.7;
  }

  .post-content :global(h1) {
    margin-top: 2rem;
    margin-bottom: 1rem;
  }

  .post-content :global(h2) {
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
    color: var(--aqua);
  }

  .post-content :global(h3) {
    margin-top: 1.25rem;
    margin-bottom: 0.5rem;
    color: var(--blue);
  }

  .post-content :global(p) {
    margin-bottom: 1rem;
  }

  .post-content :global(ul),
  .post-content :global(ol) {
    margin-bottom: 1rem;
    padding-left: 2rem;
  }

  .post-content :global(li) {
    margin-bottom: 0.5rem;
  }

  .post-content :global(code) {
    background: var(--bg1);
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-size: 0.9em;
    font-family: "Courier New", monospace;
  }

  .post-content :global(pre) {
    background: var(--bg1);
    padding: 1rem;
    border-radius: 5px;
    overflow-x: auto;
    margin-bottom: 1rem;
  }

  .post-content :global(pre code) {
    background: none;
    padding: 0;
  }

  .post-content :global(a) {
    color: var(--aqua);
    text-decoration: none;
  }

  .post-content :global(a:hover) {
    text-decoration: underline;
  }

  .post-content :global(blockquote) {
    border-left: 3px solid var(--aqua-dim);
    padding-left: 1rem;
    margin: 1rem 0;
    color: var(--fg2);
    font-style: italic;
  }
</style>
