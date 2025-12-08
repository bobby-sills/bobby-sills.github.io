<script lang="ts">
  import ThemeToggle from "./ThemeToggle.svelte";
  import { location } from "svelte-spa-router";

  const links = {
    home: "#/",
    blog: "#/blog",
    books: "#/books",
  };
</script>

<header>
  <nav>
    <ul>
      {#each Object.entries(links) as [text, link]}
        <li><a href={link}>{text}</a></li>
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

  a:hover {
    color: var(--aqua);
  }
</style>
