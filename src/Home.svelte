<script lang="ts">
	import Nav from "./lib/Nav.svelte";

	$effect(() => {
		document.title = "bobby sills";
	});
</script>

<main>
	<Nav />

	<div
		style:display="flex"
		style:margin="24px 0px"
		style:gap="24px"
		style:flex-wrap="wrap"
	>
		<img
			src="/profile-photo.jpg"
			alt="Portrait of a 9th grader"
			width="200"
			height="200"
		/>
		<div
			style:display="flex"
			style:flex-direction="column"
			style:flex="1"
			style:min-width="300px"
		>
			<h3>bobby sills</h3>
			<a href="mailto:bobbysills@bobbysills.dev" style="color:var(--blue);"
				>[contact]</a
			>
			<p>
				9th grade developer working out of vientiane, laos. just released
				language learning app for lao. get it on
				<a href="https://apps.apple.com/us/app/read-lao/id6749076081">ios</a>
				and
				<a
					href="https://play.google.com/store/apps/details?id=com.readlao.app&pcampaignid=web_share"
				>
					android
				</a>.
			</p>
		</div>
	</div>

	<div
		style:display="grid"
		style:grid-template-columns="repeat(auto-fit, minmax(300px, 1fr))"
		style:margin="24px 0px"
		style:gap="24px"
	>
		<div>
			<h2>currently working on</h2>
			<ul>
				<li>learning opengl and c++</li>
			</ul>
		</div>
		<div>
			<h2>projects</h2>
			<ul>
				<li><a href="#/telephone-game">telephone game</a></li>
				<li>read lao app (see above)</li>
			</ul>
		</div>
		<div>
			<h2>profiles</h2>
			<ul style="list-style-type: none; padding-left: 15px">
				<li style:display="flex" style:alignItems="center" style:gap="8px">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="24"
						height="24"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
						class="lucide lucide-github-icon lucide-github"
						><path
							d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"
						/><path d="M9 18c-4.51 2-5-2-7-2" /></svg
					>
					<a href="https://github.com/bobby-sills">github</a>
				</li>
				<li style:display="flex" style:alignItems="center" style:gap="8px">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="24"
						height="24"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
						class="lucide lucide-youtube-icon lucide-youtube"
						><path
							d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"
						/><path d="m10 15 5-3-5-3z" /></svg
					><a href="https://www.youtube.com/@itsmebobbysills">youtube</a>
				</li>
				<li style:display="flex" style:alignItems="center" style:gap="8px">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="24"
						height="24"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
						class="lucide lucide-message-square-more-icon lucide-message-square-more"
						><path
							d="M22 17a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 21.286V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2z"
						/><path d="M12 11h.01" /><path d="M16 11h.01" /><path
							d="M8 11h.01"
						/></svg
					>
					<a href="https://discord.com/users/1091870234044018809">discord</a>
				</li>
				<li style:display="flex" style:alignItems="center" style:gap="8px">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="24"
						height="24"
						viewBox="0 0 24 24"
						fill="currentColor"
						><path
							fill="currentColor"
							d="M20 14.4a.8.8 0 1 1 0 1.6a.8.8 0 0 1 0-1.6Zm-11.2 0h4.8a.8.8 0 1 1 0 1.6H8.8a.8.8 0 1 1 0-1.6ZM7.2 9.6a.8.8 0 0 1 .8.8V12a.8.8 0 1 1-1.6 0v-1.6a.8.8 0 0 1 .8-.8Zm-3.999.759A2.4 2.4 0 0 1 7.2 8.612a2.4 2.4 0 0 1 4 1.788V12a.8.8 0 1 1-1.6 0v-1.6a.8.8 0 1 0-1.6 0V12a.8.8 0 1 1-1.6 0v-1.6a.8.8 0 1 0-1.6 0V12a.8.8 0 1 1-1.6 0v-1.6l.001-.041ZM17.6 12.8v2.4a.8.8 0 1 1-1.6 0v-2.4h-2.306c-.493 0-.894-.358-.894-.8c0-.442.401-.8.894-.8h6.212c.493 0 .894.358.894.8c0 .442-.401.8-.894.8H17.6ZM16.8 8H20a.8.8 0 1 1 0 1.6h-3.2a.8.8 0 1 1 0-1.6ZM4 14.4h1.6a.8.8 0 1 1 0 1.6H4a.8.8 0 1 1 0-1.6ZM13.2 8h.4a.8.8 0 1 1 0 1.6h-.4a.8.8 0 1 1 0-1.6ZM1.6 14.4H0V8.8c0-2.208 1.792-4 4-4h16c2.208 0 4 1.792 4 4v6.4c0 2.208-1.792 4-4 4H4c-2.208 0-4-1.792-4-4v-1.6h1.6v1.6A2.4 2.4 0 0 0 4 17.6h16a2.4 2.4 0 0 0 2.4-2.4V8.8A2.4 2.4 0 0 0 20 6.4H4a2.4 2.4 0 0 0-2.4 2.4v5.6Z"
						/></svg
					>
					<a href="https://monkeytype.com/profile/WriteThatDown">monkeytype</a>
				</li>
				<li style:display="flex" style:alignItems="center" style:gap="8px">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="24"
						height="24"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
						class="lucide lucide-cat-icon lucide-cat"
						><path
							d="M12 5c.67 0 1.35.09 2 .26 1.78-2 5.03-2.84 6.42-2.26 1.4.58-.42 7-.42 7 .57 1.07 1 2.24 1 3.44C21 17.9 16.97 21 12 21s-9-3-9-7.56c0-1.25.5-2.4 1-3.44 0 0-1.89-6.42-.5-7 1.39-.58 4.72.23 6.5 2.23A9.04 9.04 0 0 1 12 5Z"
						/><path d="M8 14v.5" /><path d="M16 14v.5" /><path
							d="M11.25 16.25h1.5L12 17l-.75-.75Z"
						/></svg
					>
					<a href="https://scratch.mit.edu/users/WriteThatDown">scratch</a> (not
					as active anymore)
				</li>
			</ul>
		</div>
		<div>
			<h2>work experience</h2>
			<p>I don't really have any</p>
		</div>
	</div>
</main>

<style>
	img {
		border-radius: 10px;
		width: 200px;
		height: 200px;
		display: block;
	}
	h3 {
		font-weight: normal;
		color: var(--red);
	}
</style>
