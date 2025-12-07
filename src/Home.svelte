<script lang="ts">
  import Nav from "./lib/Nav.svelte";
</script>

<main>
  <Nav currentPage="home" />

  <div class="container">
    <img src="public/profile-photo.jpg" alt="Portrait of a 9th grader" />
    <p>Welcome to my personal website.</p>
  </div>
</main>

<style>
  .container {
    display: flex;
  }
  img {
    width: 20%;
    height: auto;
  }
</style>
