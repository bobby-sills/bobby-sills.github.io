<script lang="ts">
  import ThemeToggle from "./ThemeToggle.svelte";

  const { currentPage }: { currentPage: string } = $props();

  const links = {
    home: "/",
    blog: "/blog.html",
    books: "/books.html",
  };
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
