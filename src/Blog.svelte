<script lang="ts">
  import Nav from "./lib/Nav.svelte";
  import { getAllPosts } from "./lib/posts";
  import { link } from "svelte-spa-router";

  const posts = getAllPosts();

  $effect(() => {
    document.title = "blog | bobby sills";
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

  <h1>blog</h1>

  {#if posts.length === 0}
    <p>No posts yet.</p>
  {:else}
    <div class="posts-list">
      {#each posts as post}
        <article class="post-preview">
          <div class="post-info">
            <h2>
              <a href="/blog/{post.slug}" use:link>{post.title}</a>
            </h2>
            <time class="post-date">{formatDate(post.date)}</time>
          </div>
        </article>
      {/each}
    </div>
  {/if}
</main>

<style>
  .posts-list {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .post-preview {
    display: flex;
  }

  .post-info {
    flex: 1;
  }

  .post-preview h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
  }

  .post-preview h2 a {
    color: var(--fg);
    text-decoration: none;
  }

  .post-preview h2 a:hover {
    color: var(--aqua);
  }

  .post-date {
    display: block;
    color: var(--fg2);
    font-size: 0.9rem;
  }
</style>
