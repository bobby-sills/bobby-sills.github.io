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

  interface ManualBook {
    title: string;
    authors: string;
    status: "currently_reading" | "completed" | "want_to_read";
    total_pages?: number;
    pages_read?: number;
    date_completed?: string;
  }

  // Manual data is the source of truth for status
  // Progress percentage uses the higher value from manual or KOReader
  // KOReader completion (100%) overrides manual status
  const allBooks: Book[] = (manualData.books as ManualBook[])
    .filter((book) => book.status === "currently_reading" || book.status === "completed")
    .map((manualBook) => {
      // Try to find matching KOReader data for this book
      const koreaderBook = koreaderBooks.books.find(
        (kb) => kb.title === manualBook.title
      );

      // Calculate manual progress percentage
      const manualPercentage = manualBook.pages_read && manualBook.total_pages
        ? (manualBook.pages_read / manualBook.total_pages) * 100
        : 0;

      // Get KOReader percentage (if available)
      const koreaderPercentage = koreaderBook?.percentage_completed ?? 0;

      // Use the higher of the two percentages
      const percentage_completed = Math.max(manualPercentage, koreaderPercentage);

      // Determine if book is completed:
      // - KOReader says 100%, OR
      // - Manual status is "completed"
      const isCompleted = koreaderPercentage >= 100 || manualBook.status === "completed";

      return {
        title: manualBook.title,
        authors: manualBook.authors,
        percentage_completed: isCompleted ? 100 : percentage_completed,
        total_pages: manualBook.total_pages,
        date_completed: isCompleted
          ? (koreaderBook?.date_completed || manualBook.date_completed)
          : undefined,
      };
    });

  // Add want to read books from manual data
  const wantToRead = (manualData.books as ManualBook[])
    .filter((book) => book.status === "want_to_read")
    .map((book) => ({
      title: book.title,
      authors: book.authors,
    }));

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

  <h2>up next</h2>
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
