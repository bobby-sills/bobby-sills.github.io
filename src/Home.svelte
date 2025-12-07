<script lang="ts">
  import Nav from "./lib/Nav.svelte";
</script>

<main>
  <Nav />

  <div
    style:display="flex"
    style:margin="24px 0px"
    style:gap="24px"
    style:flex-wrap="wrap"
  >
    <img src="/profile-photo.jpg" alt="Portrait of a 9th grader" />
    <div
      style:display="flex"
      style:flex-direction="column"
      style:flex="1"
      style:min-width="300px"
    >
      <h3>bobby sills</h3>
      <span
        >9th grade developer working out of vientiane, laos. just released an
        app to learn to read lao. get it on <a
          href="https://apps.apple.com/us/app/read-lao/id6749076081">ios</a
        > and android (coming soon).
      </span>
      <span> </span>
    </div>
  </div>
</main>

<style>
  img {
    border-radius: 10px;
    max-width: 200px;
    height: auto;
  }
  h3 {
    font-weight: normal;
    font-style: italic;
    color: var(--red);
  }
</style>
