<script lang="ts">
  import ThemeToggle from "./ThemeToggle.svelte";
  import { location } from 'svelte-spa-router'

  const links = {
    home: "/#/",
    blog: "/#/blog",
    books: "/#/books",
  };

  // Map routes to page names for active state
  const routeToPage: Record<string, string> = {
    '/': 'home',
    '/blog': 'blog',
    '/books': 'books',
  }

  // Automatically derive current page from route
  let currentPage = $derived(routeToPage[$location] || 'home')
</script>

<header>
  <nav>
    <ul>
      {#each Object.entries(links) as [text, link]}
        <li><a href={link} class:active={text === currentPage}>{text}</a></li>
      {/each}
    </ul>
    <ThemeToggle />
  </nav>
</header>

<style>
  nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  nav ul {
    display: flex;
    gap: 20px;
    list-style: none;
    padding: 0;
    margin: 0;
  }

  header {
    padding: 24px 0px;
  }

  a.active {
    color: var(--aqua);
    font-weight: bold;
  }
</style>
