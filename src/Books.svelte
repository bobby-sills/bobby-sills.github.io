<script lang="ts">
  import Book from "./lib/Book.svelte";
  import Nav from "./lib/Nav.svelte";
  import ContributionGraph from "./lib/ContributionGraph.svelte";
  import koreaderBooks from "../data/koreader-books.json";
  import manualData from "../data/manual-data.json";

  $effect(() => {
    document.title = "books | bobby sills";
  });

  interface Book {
    title: string;
    authors: string;
    percentage_completed: number;
    total_pages?: number;
    date_completed?: string;
  }

  // Combine koreader books with manual books (prefer KOReader data)
  const koreaderBooksWithPages = koreaderBooks.books.map((book) => ({
    ...book,
    total_pages:
      manualData.page_counts[book.title as keyof typeof manualData.page_counts],
  }));

  // Get titles from KOReader to avoid duplicates
  const koreaderTitles = new Set(koreaderBooksWithPages.map((b) => b.title));

  // Add manual currently_reading books that aren't in KOReader data
  const manualCurrentlyReading = (
    manualData.currently_reading as Array<{
      title: string;
      authors: string;
      pages_read: number;
      total_pages: number;
    }>
  )
    .filter((book) => !koreaderTitles.has(book.title))
    .map((book) => ({
      title: book.title,
      authors: book.authors,
      percentage_completed: (book.pages_read / book.total_pages) * 100,
      total_pages: book.total_pages,
    }));

  // Add completed books from manual data
  const manualCompleted = manualData.completed
    .filter((book) => !koreaderTitles.has(book.title))
    .map((book) => ({
      title: book.title,
      authors: book.authors,
      percentage_completed: 100,
      date_completed: book.date_completed,
    }));

  // Add want to read books from manual data
  const wantToRead = manualData.want_to_read.map((book) => ({
    title: book.title,
    authors: book.authors,
  }));

  const allBooks: Book[] = [
    ...koreaderBooksWithPages,
    ...manualCurrentlyReading,
    ...manualCompleted,
  ];

  // Separate books into currently reading and completed
  const currentlyReading = allBooks.filter(
    (book) => book.percentage_completed < 100,
  );
  const completedBooks = allBooks.filter(
    (book) => book.percentage_completed >= 100,
  );
</script>

<main>
  <Nav />

  <h1>books</h1>

  <ContributionGraph />

  <h2>currently reading</h2>
  {#each currentlyReading as book (book.title)}
    <Book
      title={book.title}
      author={book.authors}
      percent={book.percentage_completed}
      totalPages={book.total_pages ?? 0}
    />
  {/each}

  <h2>completed</h2>
  {#each completedBooks as book (book.title)}
    <Book
      title={book.title}
      author={book.authors}
      percent={book.percentage_completed}
      totalPages={book.total_pages ?? 0}
      dateCompleted={book.date_completed}
    />
  {/each}

  <h2>want to read</h2>
  {#each wantToRead as book (book.title)}
    <div
      style="display: flex; flex-direction: column; gap: 5px; margin-bottom: 20px;"
    >
      <span style="color: var(--fg); font-size: larger;">{book.title}</span>
      <span style="color: var(--fg4);">by {book.authors}</span>
    </div>
  {/each}
</main>

<style>
</style>
